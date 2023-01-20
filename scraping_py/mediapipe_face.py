import cv2
import mediapipe as mp
from PIL import Image
import urllib.request
import numpy as np
from io import BytesIO


## url path에 한글이 있을때 imread 에러남 = decode 진행
def url_to_image(url):
    
    response = urllib.request.urlopen(url) # - 이미지 저장없이 바로 사용

    ## case 1 output - array로 나옴
    image = np.asarray(bytearray(response.read()), dtype='uint8')
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    ## case 2 output - 객체로 나옴
    # res = response.read()
    # image = Image.open(BytesIO(res))
    
    return image

## 폴더에 있는 이미지 읽을때
## - 작업 폴더 변경 후 진행하면 cv2.imread 그대로 읽힘
def url_to_image2(url):
    
    with open(url, 'rb') as f:
        data = f.read()
        
    data_io = BytesIO(data)
    image = Image.open(data_io)
    return image

## 케릭터, 그림 이미지도 추출
def face_detect(url_image):

    ## 모듈은 불러와지는데...
    mp_face_detections = mp.solutions.face_detection

    ## landmark drawing
    mp_drawing = mp.solutions.drawing_utils

    with mp_face_detections.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:

        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        # process - 인자값으로 array형태가 들어가야함 
        res = face_detection.process(cv2.cvtColor(url_image, cv2.COLOR_BGR2RGB))

        ## 탐지 못하면 무시하고 진행
        return res.detections