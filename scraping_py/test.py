import os       
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from PIL import Image as Img
import multiprocessing


'''
내 구글 드라이브에 저장해놓은 데이터를 Colab 환경에 불러오는 시간이 만만치 않아 대기시간이 길어지는 경우가 종종있었다.
TFrecord 파일 사용, 압축

1. 압축
- shutil.make_archive("폴더명", 확장자, 폴더)

## colab
# !unzip -qq "zip 파일 경로(.zip)" -d "압축 푼 파일 저장할 경로"


from numba import jit

## Numba는 수치 계산에 초점을 맞춘 파이썬을 위한 오픈 소스 JIT
@git
def ----:
    빠르다

## np.array <> np.asarray
- array => copy = True
- asarray => cop = False
array를 다른 변수에 할당하고 원본을 변경할 경우 array의 copy본은 변경되지 않는다.
그러나 asarray의 경우에는 원본이 변경될 경우 asarray의 복사본까지 변경된다.

## multiprocess
* map() - iterable에 대해 동일한 함수를 멀티프로세싱을 이용하여 처리하고자 할 때 사용한다. 단, 사용하고자 하는 함수는 단일 인자를 받아야 한다.
= map의 결과물은 list

* apply() - Pool에게 작업 하나를 시킨다. 그리고 작업이 끝날 때까지 기다렸다가 결과를 받는다.
= pool.apply(func, func인자값)

* starmap() - 인자를 두 개 이상 받을 수 있다
= pool.starmap(func, zip(func인자값, func인자값)= 둘다 iterable )

* imap() - 결과물의 길이가 길어서 list로 나타내었을 때 메모리에 부담이 가는 경우 imap을 사용해주면 좋다
= imap의 결과물은 iterator

----- iterator / iterable ----
iterator - for 문이 이터러블을 받으면 이터러블의 __iter__()를 호출
iterable - 반복가능한 객체(list, dict, tuple...)

iterable은 순회를 당할 수 있는 객체
iterator은 iterable의 순회를 주관


* 대용량 데이터 불러올때 사용 - chunksize 
'''
t = "010216"
import pandas as pd

# df = pd.read_csv("KP2021.csv", encoding='cp949')
# df1 = pd.read_csv("KP2020.csv", encoding='cp949')

acc = [401, 402, 403, 404, 405, 406]
    
    
# print(len(df.columns), len(df1.columns))
# print(len(df[(df["SME_EVT_YN"].notnull()) & (df["SME_EVT_YN"] == "N")]))
# df = df[(df["HPPN_PNU_ADDR"].notna()) & (df["HPPN_X"].notna()) & (df["HPPN_Y"].notna())]
# df1 = df1[(df1["HPPN_PNU_ADDR"].notna()) & (df1["HPPN_X"].notna()) & (df1["HPPN_Y"].notna())]

import numpy as np
from pprint import pprint

## print threshold / max = 1000
np.set_printoptions(threshold=1000)

## string to factorizations
# classes = np.array(list(set(df1[df1["RECV_DEPT_NM"].str.contains("대전")]["HPPN_PNU_ADDR"])))
# name, indices = np.unique(classes, return_inverse=True)

# print(pprint(classes))

f = os.listdir("hibt_img")
s = []
s1 = []
for i in f:
    
    s.append(rf"{os.path.abspath(i)}") 
    s1.append(os.path.abspath(i))
print(s)
print(s1)
print([os.path.abspath(i) for i in f])