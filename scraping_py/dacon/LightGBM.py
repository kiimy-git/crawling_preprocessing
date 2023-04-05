import pandas as pd
import numpy as np
import time
from scipy import sparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.tree import DecisionTreeClassifier
import re
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import zipfile
from transformers import BertTokenizer, BertModel
from sklearn.neural_network import MLPClassifier
import lightgbm as lgb
from lightgbm import early_stopping
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import GridSearchCV

## 토큰을 다시 텍스트로 변환
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()

# 전처리 함수 정의
def clean_text(text):
    # 소문자 변환
    text = text.lower()
    # 특수문자 제거
    text = re.sub('[^a-zA-Z]', ' ', text)
    # 불용어 제거
    words = text.split()
    words = [word for word in words if not word in stop_words]
    # 텍스트 정규화
    words = [lemmatizer.lemmatize(word) for word in words]
    text = ' '.join(words)
    return text

def train_model(X, y, params):

    
    # Train/Validation set을 나누어 모델을 학습시킵니다.
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    dtrain = lgb.Dataset(X_train, label=y_train)
    dval = lgb.Dataset(X_val, label=y_val)
    
    model = lgb.train(params, 
                      dtrain, valid_sets=[dtrain, dval], 
                      verbose_eval=100, 
                      num_boost_round=500, 
                      early_stopping_rounds=100)

    return model

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

    # 벡터화 모델 설정
    vectorizer = TfidfVectorizer(max_features=20000)
    
    train_df['text'] = train_df['text'].apply(clean_text)
    test_df['text'] = test_df['text'].apply(clean_text)
    
    # train 데이터셋을 배치별로 벡터화합니다.
    batch_size = 1000
    X = None
    for i in range(0, len(train_df), batch_size):
        batch_text = train_df['text'][i:i+batch_size]
        batch_X = vectorizer.fit_transform(batch_text).astype('float32')
        if X is None:
            X = batch_X
        else:
            # 열의 개수를 맞추기 위해 합칩니다.
            if X.shape[1] != batch_X.shape[1]:
                n_features = max(X.shape[1], batch_X.shape[1])
                vectorizer.max_features = n_features
                X = vectorizer.fit_transform(train_df['text'].values.astype('U'))
            else:
                X = sparse.vstack([X, batch_X])
    
    # test 데이터셋을 배치별로 벡터화합니다.
    X_test = None
    for i in range(0, len(test_df), batch_size):
        batch_text = test_df['text'][i:i+batch_size]
        batch_X = vectorizer.transform(batch_text).astype('float32')
        if X_test is None:
            X_test = batch_X
        else:
            # 열의 개수를 맞추기 위해 합칩니다.
            if X_test.shape[1] != batch_X.shape[1]:
                n_features = max(X_test.shape[1], batch_X.shape[1])
                vectorizer.max_features = n_features
                X_test = vectorizer.transform(test_df['text'].values.astype('U'))
            else:
                X_test = sparse.vstack([X_test, batch_X])
            
    # LightGBM 모델 하이퍼파라미터 설정
    params = {
        'objective': 'multiclass',
        'num_class': 8,
        'num_leaves': 63,
        'max_depth': 5,
        'learning_rate': 0.01,
        'min_child_samples': 20,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
    }
    # param_grid = {
    #     'num_leaves': [31, 63, 127],
    #     'learning_rate': [0.01, 0.05],
    #     'max_depth': [3, 5]
    # }
    y = train_df['label']
    # X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    # LightGBM 모델 학습
    start_time = time.time()
    model = train_model(X, y, params)

    # grid_search = GridSearchCV(estimator=lgb.LGBMClassifier(),
    #                         param_grid=param_grid,
    #                         n_jobs=-1,
    #                         verbose=2,
    #                         scoring='f1_macro',
    #                         cv=3)
    # grid_search.fit(X_train, y_train)
    print('Fit time : ', time.time()-start_time)
    
    # test 데이터에 대한 예측 값을 생성합니다.
    # best_model = grid_search.best_estimator_
    y_test_pred = model.predict(X_test)
    '''
    Neural Networks나 LightGBM과 같은 몇몇 모델의 경우, 
    predict 메서드는 예측된 클래스 레이블이 아니라 각 클래스에 대한 출력 확률(probability)을 반환
    '''
    ## (n_samples, n_classes) 모양의 NumPy 배열이라면
    y_test_pred = np.argmax(y_test_pred, axis=1)
    
    # 제출 파일 생성
    submission_df = pd.read_csv('submission.csv')
    submission_df['label'] = y_test_pred
    submission_df.to_csv('my_submission.csv', index=False)