import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
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
from sklearn.feature_extraction.text import TfidfVectorizer
import xgboost as xgb
import lightgbm as lgb
import gensim.downloader as api
from gensim.models import KeyedVectors
from sklearn.svm import LinearSVC
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import torch
import zipfile
from datasets import Dataset

# 데이터 전처리
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

    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)

    # 미리 학습된 모델과 토크나이저를 불러옵니다.
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # 토큰화 함수 정의
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    # 데이터셋 토큰화
    tokenized_train_dataset = train_dataset.map(tokenize_function, batched=True)
    tokenized_test_dataset = test_dataset.map(tokenize_function, batched=True)

    # 모델 초기화
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=8)

    # 학습 인자 설정
    training_args = TrainingArguments(
        output_dir="results",
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        evaluation_strategy="epoch",
        logging_dir="logs",
    )

    # 트레이너 초기화
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train_dataset,
        eval_dataset=tokenized_test_dataset,
    )

    # 모델 학습
    trainer.train()


    # 테스트 데이터셋에 대한 예측 수행
    predictions = trainer.predict(tokenized_test_dataset)

    # 예측 결과를 클래스 인덱스로 변환
    predicted_class_indices = np.argmax(predictions.predictions, axis=1)

    # 인덱스를 레이블로 변환 (필요한 경우)
    # predicted_labels = [index_to_label_map[index] for index in predicted_class_indices]
    
    # 예측 결과
    submission_df['label'] = predicted_class_indices
    submission_df.to_csv('submission.csv', index=False)