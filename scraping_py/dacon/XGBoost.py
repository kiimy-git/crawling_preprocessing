import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, make_scorer
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
import gensim.downloader as api
from gensim.models import KeyedVectors
from sklearn.svm import LinearSVC
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download('averaged_perceptron_tagger')
import zipfile


# 전처리 함수 정의
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def pos_tagging(text):
    words = word_tokenize(text)
    pos = nltk.pos_tag(words)
    return " ".join([lemmatizer.lemmatize(word, pos=get_wordnet_pos(pos_tag)) for word, pos_tag in pos])

def preprocess(text):
    # 숫자 제거
    text = re.sub(r'\d+', '', text)
    # 구두점 제거
    text = re.sub(r'[^\w\s]', '', text)
    # 특수문자 제거
    text = re.sub(r'[^a-zA-Z0-9ㄱ-ㅣ가-힣]', '', text)
    # 소문자 변환
    text = text.lower()
    # 불용어 제거
    stop_words = set(stopwords.words('english'))
    stop_words.update(['amp', 'rt', 'https', 'co'])  # 특정 단어 추가
    words = word_tokenize(text)
    pos = nltk.pos_tag(words)
    
    return " ".join([lemmatizer.lemmatize(word, pos=get_wordnet_pos(pos_tag)) for word, pos_tag in pos])

# GloVe 벡터화 적용
glove_model = api.load('glove-twitter-25')

def get_vector(text):
    vectors = []
    for word in text.split():
        try:
            vectors.append(glove_model[word])
        except KeyError:
            pass
    if len(vectors) > 0:
        return list(np.mean(vectors, axis=0))
    else:
        return list(np.zeros(25)) # if no vector is found, return a vector of 25 zeros
    
with zipfile.ZipFile("open.zip", "r") as zip_f:
    print(zip_f.namelist())
    file_list = zip_f.namelist()
    df_list = []
    for f in file_list:
        
        with zip_f.open(f) as file:
            df = pd.read_csv(file)
            df_list.append(df)

    submission_df = df_list[0]
    train_df = df_list[2]
    test_df = df_list[1]

    # train 데이터와 test 데이터에 전처리 함수 적용
    # train_df['text'] = train_df['text'].apply(remove_stopwords)
    # train_df['text'] = train_df['text'].apply(pos_tagging)
    train_df['text'] = train_df['text'].apply(preprocess)
    train_df['text'] = train_df['text'].apply(get_vector)

    # test_df['text'] = test_df['text'].apply(remove_stopwords)
    # test_df['text'] = test_df['text'].apply(pos_tagging)
    test_df['text'] = test_df['text'].apply(preprocess)
    test_df['text'] = test_df['text'].apply(get_vector)
    
    X = np.array(train_df['text'].tolist())
    y = np.array(train_df['label'])
    
    # train 데이터와 test 데이터 분리
    train_X, valid_X, train_y, valid_y = train_test_split(X, y, test_size=0.2, random_state=42)
    evals = [(valid_X, valid_y)]
    
    # # # DMatrix 생성
    # # train_dmatrix = xgb.DMatrix(train_X, label=train_y)
    # # valid_dmatrix = xgb.DMatrix(valid_X, label=valid_y)

    # 하이퍼파라미터 튜닝을 위한 그리드 서치
    params = {
    'max_depth': [3, 4, 5],
    'n_estimators': [100, 200, 300],
    'learning_rate': [0.01, 0.05, 0.1],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'subsample': [0.6, 0.8, 1.0]
    }

    xgb_model = xgb.XGBClassifier(
        objective='multi:softmax',
        num_class = 8,
        n_jobs= -1,
        tree_method='gpu_hist', gpu_id=0, eval_metric='mlogloss'
    )
    xgb_model.set_params(early_stopping_rounds=100)
    scorer = make_scorer(f1_score, average='macro')
    clf = GridSearchCV(xgb_model, params, scoring=scorer, cv=5, n_jobs=-1, verbose=2)
    clf.fit(train_X, train_y, eval_set=evals, verbose=True)
    
    # 검증용 데이터로 모델 평가
    y_pred = clf.predict(valid_X)
    macro_f1 = f1_score(valid_y, y_pred, average='macro')
    accuracy = accuracy_score(valid_y, y_pred)
    print("검증용 데이터에서의 정확도: {:.3f}".format(accuracy))
    print('Macro F1 Score:', macro_f1)
    
    # # 검증 데이터로 모델 성능 평가
    # valid_pred = best_clf.predict(valid_X)
    # f1_macro = f1_score(valid_y, valid_pred, average='macro')
    # print('Validation Macro F1 Score: {:.4f}'.format(f1_macro))
    
    # test 데이터를 사용한 예측 결과 생성
    # GridSearchCV의 refit으로 이미 학습된 estimator반환
    estimator = clf.best_estimator_
    test_y_pred = estimator.predict(np.array(test_df['text'].tolist()))
    submission_df['label'] = test_y_pred
    submission_df.to_csv('submission.csv', index=False)