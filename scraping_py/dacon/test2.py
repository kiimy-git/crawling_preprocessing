import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import tensorflow as tf #  패키지 설치 경로가 길어져서 윈도우의 폴더 이름 길이인 256을 넘어서 문제가 발생
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, make_scorer
from sklearn.model_selection import GridSearchCV
import xgboost as xgb
import lightgbm as lgb
import gensim.downloader as api
from gensim.models import KeyedVectors
from sklearn.svm import LinearSVC
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import torch
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download('averaged_perceptron_tagger')
import zipfile
from tensorflow.python.ops.numpy_ops import np_config
import lightgbm as lgb
from transformers import AutoTokenizer, AutoModel
import requests
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 위에서 다운로드한 BERT 모델과 tokenizer를 불러옵니다.
model_name = "bert-base-multilingual-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
bert_model = AutoModel.from_pretrained(model_name)

# 문자열을 숫자로 변환하는 함수 정의
def tokenize_text(df):
    tokenized_text = df['text'].apply((lambda x: tokenizer.encode(x, add_special_tokens=True)))
    return tokenized_text

# BERT 모델을 사용하여 텍스트 데이터를 벡터화합니다.
def get_bert_embeddings(inputs):
    embeddings = []
    for input_ids in inputs:
        with torch.no_grad():
            outputs = bert_model(torch.tensor(input_ids).unsqueeze(0))
            last_hidden_states = outputs[0]
            embedding = np.mean(last_hidden_states.numpy(), axis=1)
            embeddings.append(embedding)
    return embeddings

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
    
    train_inputs = tokenize_text(train_df['text'])
    train_labels = train_df['label'].values

    # 학습용/검증용 데이터 분리
    X_train, X_val, y_train, y_val = train_test_split(train_inputs, train_labels, test_size=0.2, random_state=42)

    train_embeddings = get_bert_embeddings(X_train)
    val_embeddings = get_bert_embeddings(X_val)
    
    # lightGBM 모델을 학습시킵니다.
    params = {
        'boosting_type': 'gbdt',
        'objective': 'multiclass',
        'num_class': 8,
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
    }

    train_dataset = lgb.Dataset(train_embeddings, label=y_train)
    val_dataset = lgb.Dataset(val_embeddings, label=y_val)

    model = lgb.train(params, train_dataset, valid_sets=[train_dataset, val_dataset], num_boost_round=1000, early_stopping_rounds=10)

    # 검증용 데이터 정확도 측정
    val_preds = model.predict(X_val)
    val_preds = np.argmax(val_preds, axis=1)
    val_accuracy = accuracy_score(y_val, val_preds)
    print(f"검증용 데이터 정확도: {val_accuracy:.4f}")

    # 테스트 데이터 숫자로 변환
    test_inputs = test_df['text'].values
    test_inputs = tokenize_text(test_inputs)

    # 모델 예측 수행
    test_preds = model.predict(test_inputs)
    test_preds = np.argmax(test_preds, axis=1)
    
    # 예측 결과
    submission_df['label'] = test_preds
    submission_df.to_csv('submission.csv', index=False)
