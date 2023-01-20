#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pyspark.sql import SparkSession
from datetime import datetime, timedelta
from pytz import timezone
from pyspark.sql.functions import expr, col, split, explode, regexp_extract, regexp_replace, lower
from pyspark.sql.functions import posexplode_outer, row_number, isnull, count, translate, lit
from pyspark.sql import Row
from pyspark.sql.window import Window
import pandas as pd
import urllib.request # url 접근 python 3.x
import requests
import concurrent.futures # 멀티프로세싱
import time
import os
from tempfile import TemporaryFile # 임시 디렉토리
import tempfile
import re
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import glob
from io import BytesIO
import io
import numpy as np
from urllib.request import urlretrieve # url 저장경로설정
from urllib.parse import urlsplit, quote # url 바이너리 원문 split, 아스키코드 형식이 아닌 글자를 URL 인코딩시켜줌
from tqdm import tqdm, tqdm_notebook # tqdm_notebook - 세련됨
import statistics # stdev 인접한 것 구하기 위함


# In[ ]:


'''
*실행 순서*
category_df = img_url(join_category) >> 
category_rdd = down_rdd(category_df.rdd.collect()) >>
category_text = extract_text(category_rdd) >>
to_dataframe(category_text)
'''


# In[ ]:


# 생성날짜 늘림
plus_category = spark.sql(f"""
with 
managed_categories AS (
SELECT 
    * 
FROM 
    zigzag_category.managed_categories_partitioned
WHERE 
    stamp_date = '{STAMP_DATE}'),
    
product AS (
SELECT 
    category_id,
    product_id
FROM 
    zigzag_catalog.product_categories_partitioned
WHERE 
    stamp_date = '{STAMP_DATE}' AND
    CAST(created_at AS DATE) between DATE('2022-03-09') and DATE('2022-03-11'))

SELECT 
    mc2.name category_kr_1st,
    mc3.name category_kr_2nd,
    mc4.name category_kr_3rd,
    product.product_id
FROM ((((managed_categories as mc1
    LEFT JOIN managed_categories as mc2
        ON (mc1.id = mc2.parent_id))
    LEFT JOIN managed_categories as mc3
        ON (mc2.id = mc3.parent_id))
    LEFT JOIN managed_categories as mc4
        ON (mc3.id = mc4.parent_id))
    LEFT JOIN product
        ON (product.category_id = mc4.id))
where
    mc1.parent_id is NULL AND
    mc2.name <> '비치 액세서리' AND
    mc2.name <> '기타' AND
    mc2.name <> '뷰티' AND
    mc2.name <> '액세서리' AND
    mc2.name <> '패션소품'
"""
)

url = spark.sql(f""" 
select
    product_id, 
    deleted, 
    language, 
    description
from
    zigzag_catalog.product_languages_partitioned
WHERE
    stamp_date = '{STAMP_DATE}' AND
    deleted = false AND
    language = 'ko' AND 
    description is NOT NULL
"""
)

# “zigzag_catalog”.“products_partitioned”, shop_id 추가
# entry_type = 등록형
shop = spark.sql(f"""
select
    id, shop_id
from 
    zigzag_catalog.products_partitioned
where
    stamp_date = '{STAMP_DATE}' AND
    deleted = False AND
    display_status = 'VISIBLE' AND
    sales_status <> 'CLOSED' AND
    entry_type = 'DIRECT'
"""
)


# In[ ]:


# join
plus_final = (
    plus_category.join(url).where(plus_category["product_id"] == url["product_id"])
    .join(shop).where(shop["id"] == url["product_id"])
    .select(plus_category.product_id, shop.shop_id, "category_kr_1st", "category_kr_2nd", "description")
)


# In[ ]:


plus_final1 = plus_final.select("category_kr_1st").distinct().collect()
for i in plus_final1:
    print(i)


# In[ ]:


# 특정 카테고리 진행시
top1 = (
    plus_final.select("product_id","shop_id", "category_kr_1st", "description")
    .filter(col("category_kr_1st") == "상의")
    .orderBy("product_id")
)

skirt1 = (
    plus_final.select("product_id","shop_id", "category_kr_1st", "description")
    .filter(col("category_kr_1st") == "스커트")
    .orderBy("product_id")
)


# In[ ]:


def img_url(category):
    imgExp = r'[i|I][m|M][g|G].*?[s|S][r|R][c|C]=[\"|\'](.*?)[\"|\']'
    df = (
        category.withColumn("img_url", split(col("description"), "<"))
        .select(
            "product_id",
            "shop_id",
            "category_kr_1st",
            posexplode_outer("img_url").alias("index", "img_url") # pos, col ==> "index", "splited"(= enumerate?)
        )
        .withColumn("img_url", regexp_extract(col("img_url"), imgExp, 1))
        .filter(col("img_url") != "") # filter 이미지 정보가 없는 경우는 제외
        .withColumn(
            "img_url",
            regexp_replace(
                col("img_url"), "zigzag://", "https://cf.product-image.s.zigzag.kr/"
            ) # zigzag://로 시작하는 경우
        )
        .withColumn("img_url", regexp_replace(col("img_url"), "^//", "https://")) # //로 시작하는 경우 https://로 변경
        .filter(col("img_url").startswith("http")) # http로 시작하는 것 = (do not use a regex ^)
        .withColumn(
            "index", row_number().over(Window.partitionBy("product_id").orderBy("index"))
        ) # 상품 아이디 별로 파티션 새로생성, 상품 아이디가 달라질때마다 인덱스 새로시작
        .select("product_id", "shop_id", "category_kr_1st", "index", "img_url")
    )
    return df


# In[ ]:


# 이미지 태그의 url만 추출
plus_final_df = img_url(plus_final)
skirt_df1 = img_url(skirt1)
top_df1 = img_url(top1)


# In[ ]:


def download(url):
    import ssl
    import urllib3
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    ssl._create_default_https_context = ssl._create_unverified_context

    try:
        response = requests.get(url, verify=False) 
        img = Image.open(io.BytesIO(response.content)) 
        return validation(img)

    except: 
        try:
            temp = tempfile.NamedTemporaryFile()
            with open(temp.name, "wb") as f: 
                url_info = urlsplit(url) 
                encode = quote(url_info.path, safe=":/()%") 
                encoded_url = f"{url_info.scheme}://{url_info.netloc}{encode}"
                urlretrieve(encoded_url, temp.name)
                img = Image.open(temp.name)
            return validation(img)
        
        except:
            return None
        
# 반복되는 코드 
def validation(img):
    return None if min(img.size) < 100 else remove_alpha_channel(img)

def remove_alpha_channel(img):
#     if len(img.split()) == 4:
# OSError: cannot write mode P as JPEG
# ==> jpg파일은 투명도를 표현할수 없는 포맷인데 alpha값을 저장할려할때 생기는 오류, P?
    if img.mode != 'RGB':
        # 병합할 이미지 생성
        new_img = Image.new("RGB", img.size, (255, 255, 255))
        new_img.paste(img, mask=img.split()[3]) # new_image에 img alpha 채널 병합
        return new_img
    else:
        return img


# In[ ]:


# down img 추가
######################################### rdd - pyspark - rdd.. ??
def down_rdd(rdd):
    down_img = []
    for i in tqdm(rdd):
        temp = i.asDict()
        
        # down이미지에서 None값이 존재
        if download(i["img_url"]) is None:
            continue
        temp["down_img"] = download(i["img_url"])
        
        output = Row(**temp)
        down_img.append(output)
        
    return down_img


# In[ ]:


skirt_rdd1 = down_rdd(skirt_df1.rdd.collect())
top_rdd1 = down_rdd(top_df1.rdd.collect())


# In[ ]:


# 특정 카테고리의 한 가지 상품만 확인할때
def product_rdd(rdd, number):
    product_num = []
    for i in rdd:
        if i["product_id"] ==  number:
            product_num.append(i)
    return product_num


# In[ ]:


import json 
import boto3 
from google.cloud import vision
from google.oauth2.service_account import Credentials

# 구글 비전 크리덴셜
def credentials():
    ssm_client = boto3.client("ssm", region_name="ap-northeast-2")
    result = ssm_client.get_parameter(Name="gcp.vision_api_key")
    credentials_data = json.loads(result["Parameter"]["Value"], strict=False) # json 파일
    credentials = Credentials.from_service_account_info(credentials_data)
    
    return credentials


# In[ ]:


# img text 정보 추출
def img_info(img):
    client = vision.ImageAnnotatorClient(credentials=credentials())
    
    # BytesIO() - 이미지를 바이트 배열로 변환하는 방법, getvalue() - 바이트 배열 값을 가져옴
    byte_arr = io.BytesIO()
    img.save(byte_arr, format='JPEG')
    byte_arr = byte_arr.getvalue()

    image = vision.Image(content=byte_arr)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    
    # 글자 단위 추출
    final_text = []

    for page in document.pages: 

        width = page.width
        height = page.height
        
        for block in page.blocks: 

            for paragraph in block.paragraphs: 
                
                for word in paragraph.words: 
                    
                    for symbol in word.symbols: 
                            
                        symbol = json.loads(symbol.__class__.to_json(symbol))
                        
                        # 좌표
                        coordinate = symbol["boundingBox"]["vertices"]
                        
                        # dict coordinate - {"x" : 234, "y" : 235}
                        # x.extend([symbol["boundingBox"]["vertices"][i]["x"] for i in range(3)])
                        x = [symbol["boundingBox"]["vertices"][i]["x"] for i in range(3)]
                        y = [symbol["boundingBox"]["vertices"][i]["y"] for i in range(3)]
                paragraph = json.loads(paragraph.__class__.to_json(paragraph))
                for word in paragraph["words"]:    
                    text = []
                    x, y = [], []
                    for symbol in word["symbols"]:
                        x.extend([symbol["boundingBox"]["vertices"][i]["x"] for i in range(3)])
                        y.extend([symbol["boundingBox"]["vertices"][i]["y"] for i in range(3)])
                        text.extend(str(symbol["text"]).lower())

                    words = "".join(text)
                    boundingBox = [min(x), min(y), max(x), max(y)]

                    dst.append({
                        "words": words,
                        "boundingBox": boundingBox,
                    })
                        x1 = coordinate[0]["x"] # x
                        y1 = coordinate[0]["y"]
                        x2 = coordinate[1]["x"] # y
                        y2 = coordinate[1]["y"]
                        x3 = coordinate[2]["x"] # w 
                        y3 = coordinate[2]["y"]
                        x4 = coordinate[3]["x"] # h
                        y4 = coordinate[3]["y"]
                        
                        ##### 좌표 값이 음수 or 이미지 크기를 초과하는 좌표가 존재 #####
                        # 음수의 경우 = 0
                        # 이미지 크기를 초과하는 경우 = img size w or h
                        x, y, w, h = (x1,y1), (x2,y2), (x3,y3), (x4, y4)

                        # boundingbox 중앙 좌표 설정
                        center_coordinate = center_ratio(x, y, h, width, height)
                        
                        # 글자
                        word = symbol["text"]

                        final_text.append([word, [x, y, w, h], center_coordinate, [width, height]])  
    
    # center_x 인접한 경우 좌표 그룹화
    try:
        lists = near_text(final_text)
        
        # 최종 인접한 글자 그룹화
        last_group = []
        for list in lists:

            width = list[0][3][0]
            height = list[0][3][1]

            first_group = []
            bbox = [[], [], [], []]
            for cnt in range(len(list)):
                # 좌표 합치기
                coordinate = list[cnt][1]

                x = coordinate[0]
                y = coordinate[1]
                w = coordinate[2]
                h = coordinate[3]

                bbox[0].append(x)
                bbox[1].append(y)
                bbox[2].append(w)
                bbox[3].append(h)
                first_group.append(list[cnt][0])
            
            # 수정
            x = min(bbox[0])
#             y = max(bbox[1])
            y = (max(bbox[1])[0], min(bbox[0])[1])
            w = (y[0], max(bbox[2])[1])
            h = (x[0], max(bbox[2])[1])

            sum_text = ''.join(first_group)
            center_xy = center_ratio(x,y,h, width, height)
            last_group.append([sum_text, [x,y,w,h], center_xy, [width, height]])
            
        return last_group
    
    # 문자가 없는 이미지의 경우
    except:
        return []


# In[ ]:


# center_x 인접한 경우 그룹화
def near_text(text):
    x_sub_values = []
    y_sub_values = []
    for x, y in zip(text[:-1], text[1:]):
        
        x_sub_values.append(y[2][0] - x[2][0])
        y_sub_values.append(y[2][1] - x[2][1])
    
    if len(x_sub_values) > 1 or len(y_sub_values) > 1:
        lists = [[text[0]]]

        x_sd = statistics.stdev(x_sub_values)
        y_sd = statistics.stdev(y_sub_values)

        for x in text[1:]:

            x_sub = x[2][0] - lists[-1][-1][2][0]
            y_sub = x[2][1] - lists[-1][-1][2][1]
            
            ##### 고정값 변경해야될 수 있음 #####
            # 가까울 수록 고정값을 작게 설정(= 특정 단어가 길면 인접 text와 가까울 수 있음)
            if abs(x_sub) / x_sd >= 0.4 :
                # 새로운 리스트 생성
                lists.append([])
            lists[-1].append(x)

        return lists
    
    ##### else: ######

def center_ratio(x, y, h, width, height):
    # 각 text 중앙 좌표값
    cx= abs(y[0]-x[0])/2
    cy= abs(h[1]-x[1])/2
    
    # 그대로 적용하면 의미가 없어(= 작은 글자는 작은 비중을 차지하는 등.. 문제가 생김)
    # == 최종 text 비율값의 오차가 생김 
    # 해당 글자의 x, y좌표값과 중앙값을 더하면 중앙 좌표값이 나옴
    cx = x[0] + cx
    cy = x[1] + cy
    
    center_y_ratio = round((cy/height)*100, 2) 
    center_x_ratio = round((cx/width)*100, 2)
    
    return [center_x_ratio, center_y_ratio]


# In[ ]:


def extract_text(img):
    
    # 1.상품 img그림에 숫자가 기입되있을 수도 있음
    # \b[xsXS|sS|mM|lL|xlXL|free|FREE|Free\d.-]+\b
    # 숫자만 \d+
    p_num = re.compile(r'[xsXS|sS|mM|lL|xlXL]|free|Free|FREE| *([-./0-9])*\d')
    p_word = re.compile(
        r'사이즈|size|SIZE|Size|허리|힙|허벅지|엉덩이|밑단|총장|총기장|장|길이|기장|어깨|가슴|암홀|소매|팔|소매길이|밑위|캡|컵|패드|하의|굽|발볼|폭|길이|높이'
                       )
    
    # 최종 추출
    final = []
    
    for s in tqdm(range(len(img))):
        
        # 추출 정보
        extract_word = []
        extract_num = []

        # 추출한 이미지
        temp_rdd = []
        
        # rdd_dict
        temp = img[s].asDict()
        text = img_info(img[s]["down_img"])
        
        # 인접한 단어들의 좌표를 구하기 위함
        coord = []
        
        # 제거할 필드
        # shop_id, category_1st 추가 삭제 
        keys_to_remove = ["index", "img_url", "down_img"]
        for key in keys_to_remove:
            del temp[key]
        
        # 키워드, 치수 정보 추출
        for i in text:
            if p_num.match(i[0]):
                extract_num.append(i)
                
            # 키워드 정보에 숫자나 알파벳도 같이 있는 경우가 있음
            # match가 아닌 search 함수 적용 
            if p_word.search(i[0]):
                extract_word.append(i)
                coord.append(i[2])

        # 빈 값 제외
        if not extract_word or not extract_num:
            continue

        # 치수 정보에 있는 size 제거
        ######################################## == upper or lower
        for v in extract_num:
            if "size" in v[0] or "Size" in v[0] or "SIZE" in v[0]:
                extract_num.remove(v)

        # 키워드가 가로 or 세로
        y_cnt, y_near_list = near_y_word(coord)
        x_cnt, x_near_list = near_x_word(coord)
        
        # 최종 추출 키워드, 치수정보
        final_word = []
        
        # 빈도수가 가장 많은 비율 값 비교
        # 키워드 정보가 가로
        if y_cnt > x_cnt:
            
            # y 값이 인접한 치수 정보 그룹화
            num = near_y_num(extract_num)
            
            # 가장 많이 인접한 치수 정보를 가져옴
            # 만약 세트라면 리스트가 두개 == sum(near_num_group, [])
            near_num_group = vertical_num_group(num)
            
            # word 왼쪽에서 오른쪽으로 읽기= x 정렬
            key_word = []
            extract_word= sorted(extract_word, key=lambda z: z[2][0])

            for word in extract_word:
                # 세트의 경우 list는 두개 
                # list 합치기
                y_sum_list = sum(y_near_list, [])

                if word[2] in y_sum_list:

                    key_word.append(word)

            # matching
            try:
                for w in key_word:

                    for n in near_num_group:

                        w_y = w[2][1]
                        n_y = n[0][2][1]

                        w_x = w[2][0]
                        n_x = n[0][2][0]

                        # 그룹화 시킨 치수 정보와 키워드 차이 값
                        # x가 인접한 경우
                        if abs(w_x - n_x) < 0.5 and 0 < abs(w_y - n_y) < 10:
                            
                            # 치수 정보 세로로 읽기
                            number = []
                            for cnt in range(len(n)):
                                number.append(n[cnt][0])
                            
                            final_word.append([w[0], number])
                            
            except Exception as e:
                print(e, "/ matching error")
                
            
        # 키워드 정보가 세로
        if y_cnt < x_cnt:
            # x 값이 인접한 치수 정보 그룹화
            num = near_x_num(extract_num)

            # word 위에서 아래로 읽기= y 정렬
            # x 인접 num 그룹화 및 정렬
            
            key_word = []
            extract_word= sorted(extract_word, key=lambda z: z[2][1])
            for word in extract_word:
                # list 합치기
#                 print(word)
                x_sum_list = sum(x_near_list, [])

                if word[2] in x_sum_list:
                    key_word.append(word)

            # matching
            try:
                for w in key_word:

                    for n in num:

                        w_y = w[2][1]
                        n_y = n[0][2][1]

                        w_x = w[2][0]
                        n_x = n[0][2][0]

                        # 그룹화 시킨 치수 정보와 키워드 차이 값
                        # y값이 인접한 경우
                        # 키워드와 치수 정보의 거리가 꽤 큼(우선 0보다 큰 값을 찾아내는 걸로)
                        if abs(w_y - n_y) < 0.5 and abs(w_x - n_x) > 0:
                            # 가로로 읽기
                            number = []
                            for cnt in range(len(n)):
                                number.append(n[cnt][0])
                            
                            final_word.append([w[0], number])

            except Exception as e:
                print(e, "/ matching error")
                
        # dict
        data_dict = {}

        for x in final_word:
            num = x[1]
            if x[0] not in data_dict:
                data_dict.setdefault(x[0],[]).append(num)
            
            # 세트의 경우 동의어가 존재하는데 우선은 other 추가해서 사용
            else:
                data_dict["other"+ x[0]] = [num]
        
        # 나온 값이 없을 경우
        if not data_dict:
            continue
        
        # 치수 정보 2차원 --> 1차원
        data_dict = {k : sum(v, []) for k, v in data_dict.items()}
        
        # 상품 정보와 병합
        merge_dict = dict(temp, **data_dict)
        final.append(merge_dict)
        
    return final


# In[ ]:


def near_y_word(center):
    y_sub_values = []
    
    for x, y in zip(center[:-1], center[1:]):

        y_sub_values.append(abs(y[1] - x[1]))

    if len(y_sub_values) > 1:
        y_sd = statistics.stdev(y_sub_values)
        
        y_lists = [[center[0]]]
        for x in center[1:]:
            
            y_sub = x[1] - y_lists[-1][-1][1]
            
            # sd가 0일 수 있음 == 일직선의 경우
            # 1 / 0 = zero division error
            if y_sd == 0:
                if abs(y_sub) > 1:
                    y_lists.append([])
                y_lists[-1].append(x)
            
            ##### 고정값 변경될 수 있음 #####

            else:
                if abs(y_sub) / y_sd > 0.3:
                    y_lists.append([])
                y_lists[-1].append(x)

        count = []

        extract_list = []

        for list in y_lists:
            count.append(len(list))
            # 세트 상품의 경우 키워드가 다수 존재
            if len(list) >= 4:
                extract_list.append(list)

        return max(count), extract_list

    else:
        return [], []
    
def near_x_word(center):
    x_sub_values = []
    
    for x, y in zip(center[:-1], center[1:]):
        x_sub_values.append(abs(y[0] - x[0]))

    if len(x_sub_values) > 1:
        x_sd = statistics.stdev(x_sub_values)
        
        x_lists = [[center[0]]]
        for x in center[1:]:
            
            x_sub = x[0] - x_lists[-1][-1][0]
            
            # sd가 0일 수 있음 == 일직선의 경우
            if x_sd == 0:
                if abs(x_sub) > 1:
                    x_lists.append([])
                x_lists[-1].append(x)
            
            ##### 고정값 변경될 수 있음 #####
            else:
                if abs(x_sub) / x_sd > 0.3:
                    x_lists.append([])
                x_lists[-1].append(x)


        count = []

        extract_list = []

        for list in x_lists:
            count.append(len(list))
            # 세트 상품의 경우 키워드가 다수 존재
            if len(list) >= 4:
                extract_list.append(list)

        return max(count), extract_list

    else:
        return [], []


# In[ ]:


# y 인접한 부분 추출
def near_y_num(text):
        
    lists = [[text[0]]]

    for x in text[1:]:
        y_sub = x[2][1] - lists[-1][-1][2][1]

        if abs(y_sub) >= 0.4:
            # 새로운 리스트 생성
            lists.append([])
        lists[-1].append(x)

    return lists

    
# 가장 많이 인접한 치수 정보만 불러오기
def vertical_num_group(num):
    try:
        group = []

        num_cnt = [len(i) for i in num]
        # 그룹화시킨 치수정보 개수
        # == 가장 많은 것
        for v in range(max(num_cnt)):
            first_group = []
            ##### 세트의 경우 두개 존재 #####
            # 1. 세트의 경우 키워드 개수가 같지 않은 경우가 있음
            # 2. 키워드는 있지만 치수가 없는 경우가 있음
            for i in range(len(num)):
                if len(num[i]) < max(num_cnt):
                    continue
                first_group.append(num[i][v])
            group.append(first_group)
        return group
    
    except Exception as e:
        print(e, "/ num group error")


# In[ ]:


# extract_text
def to_dataframe(info):
    df_list = []
    for i in info:
        df = pd.DataFrame(i)
        ##### 1인치 = 2.54cm #####
        df.replace('cm|inch', r'', regex=True, inplace=True)
        df_list.append(df)
        
    return df_list

