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
'''