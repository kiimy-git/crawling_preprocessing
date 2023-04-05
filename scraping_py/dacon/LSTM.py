import pandas as pd
from sklearn.preprocessing import LabelEncoder
from gensim.models import Word2Vec
import pandas as pd
import numpy as np
import tensorflow as tf #  패키지 설치 경로가 길어져서 윈도우의 폴더 이름 길이인 256을 넘어서 문제가 발생
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.callbacks import EarlyStopping
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Embedding, Bidirectional, Flatten, GlobalAveragePooling1D
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
import lightgbm as lgb
import gensim.downloader as api
from gensim.models import KeyedVectors
from sklearn.svm import LinearSVC
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import zipfile
from tensorflow.python.ops.numpy_ops import np_config
import lightgbm as lgb
from lightgbm.callback import early_stopping
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from tensorflow.python.client import device_lib

# # GPU 인식 확인
# print(device_lib.list_local_devices())

# # GPU 사용 가능한지 확인
# print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
# print(tf.test.is_gpu_available())

# # 모든 GPU 메모리 사용 허용
# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         tf.config.experimental.set_virtual_device_configuration(
#             gpus[0],
#             [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024 * 4)]
#         )
#     except RuntimeError as e:
#         print(e)
        
nltk.download("stopwords")

# Load Word2Vec model
model_w2v = api.load("word2vec-google-news-300")

# 전처리 함수 정의
def preprocess_text(text):
    # 소문자로 변환
    text = text.lower()
    # 특수문자 제거
    text = re.sub(r"[^a-zA-Z]", " ", text)
    # 불용어 제거
    words = text.split()
    stop_words = set(stopwords.words("english"))
    words = [word for word in words if word not in stop_words]
    # 어간(Stemming), 표제어(Lemmatization) 추출
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    # 텍스트로 다시 변환
    text = " ".join(words)
    return text

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
    
    train_df['text'] = train_df['text'].apply(preprocess_text)
    test_df['text'] = test_df['text'].apply(preprocess_text)
    

    # Tokenize text and convert to sequences
    tokenizer = Tokenizer(num_words=5000)
    tokenizer.fit_on_texts(train_df['text'])
    sequences_train = tokenizer.texts_to_sequences(train_df['text'])
    sequences_test = tokenizer.texts_to_sequences(test_df['text'])
    X_train = pad_sequences(sequences_train, maxlen=500)
    X_test = pad_sequences(sequences_test, maxlen=500)
    y_train = train_df['label']

    # Convert word sequences to vectors using Word2Vec model
    
    # vectorizer = TfidfVectorizer()
    # tokenizer = Tokenizer(num_words=5000)
    # tokenizer.fit_on_texts(train_df['text'])
    # sequences_train = tokenizer.texts_to_sequences(train_df['text'])
    # X = pad_sequences(sequences_train, maxlen=500)
    
    # tokenizer.fit_on_texts(test_df['text'])
    # sequences_train = tokenizer.texts_to_sequences(test_df['text'])
    # X_test = pad_sequences(sequences_train, maxlen=500)
    
    # y = train_df['label']

    # 학습 및 검증 데이터셋 분할
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
    
    # 모델 구축
    model = Sequential()
    model.add(Embedding(input_dim=len(tokenizer.word_index)+1, output_dim=100, input_length=500))
    model.add(Bidirectional(LSTM(128, dropout=0.5, recurrent_dropout=0.5)))
    model.add(GlobalAveragePooling1D())
    model.add(Dense(8, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, batch_size=64, 
              validation_data=(X_val, y_val), callbacks=[EarlyStopping(patience=3)])


    # 모델 학습
    # clf = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train, epochs=15, batch_size=64)
    
    model_name = "Word2vec"
    model.save(f"{model_name}.h5")
    '''
    # 모델 불러오기
    loaded_model = tf.keras.models.load_model("my_model.h5")

    # 모델 사용
    result = loaded_model.predict(test_data)
    '''
    y_test_pred = model.predict(X_test)
    # y_test_pred = encoder.inverse_transform(y_test_pred.argmax(axis=1))
    
    # 제출 파일 생성
    submission_df = pd.read_csv('submission.csv')
    submission_df['label'] = y_test_pred.argmax(axis=1)
    submission_df.to_csv(f'{model_name}.csv', index=False)