import os
import sys
import cv2
import time

## 눈을 감고 있거나 정면이 아닌 이미지에선 얼굴 인식 X
## 옆모습도 인식 X

### 얼굴 검출되는 이미지 추출???

path = "./"

file_list = os.listdir(path + "scraping_image2")

## 이미지 개수
print(f"이미지 개수 : {len(file_list)}\n")


img = cv2.imread(path + "scraping_image2/" + "16-71.jpg")

if img is None:
    print('Image load failed!')
    sys.exit()

## 이미지 크기
print(f"이미지 크기 : {img.shape}\n")



## face detection
classifier = cv2.CascadeClassifier(path + "haar/haarcascade_frontalface_alt2.xml")

if classifier.empty():
    print("Xml load failed")
    sys.exit()

s_time = time.time()

faces = classifier.detectMultiScale(img)
# if faces is not None:
e_time = time.time()

## Detect 속도
print(f"{e_time - s_time}\n")

## 여러명의 face 검출시
crop_list = []
for (x,y,w,h) in faces:
    
    ## face detect 이미지 중앙값
    center_x, center_y = abs(int(w / 2)), abs(int(h / 2))

    ## crop 시작점
    x1 = x-center_x
    y1 = y-center_y


    ## 중앙값을 추가했을때 
    if x1 <= 0:
        x1 = 0

    if y1 <= 0:
        y1 = 0
        
    ##1 crop 세로, 가로
    crop_img = img[y1:y+h+center_y, x1:x+w+center_x].copy()
    crop_list.append(crop_img)
    
    print(f"crop 이미지 사이즈 : {crop_img.shape}")
    
    cv2.rectangle(img, (x,y,w,h), (0,0,255), 1, cv2.LINE_AA)

    # # 얼굴에서 윗 부분만 ROI
    # faceROI = src[y1:y1 + h1 //2, x1:x1 + w1]
    # # eyes = eye_classifier.detectMultiScale(faceROI)

    # # for (x2,y2,w2,h2) in eyes:
    # #     center = (x2 + w2 // 2, y2 + h2 // 2)
    # #     cv2.circle(faceROI, center, w2 // 2, (255,255,0), 2, cv2.LINE_AA)

'''
이미지를 자르거나 복사할 때, dst = src의 형태로 사용할 경우, 얕은 복사(shallow copy)가 되어 원본도 영향
그러므로, *.copy()를 이용해 깊은 복사(deep copy)를 진행
'''


cv2.imshow('src', img)
# cv2.imshow("#1 crop", crop_img)
for i in crop_list:
    cv2.imshow("img", i)
    cv2.waitKey()
    
cv2.waitKey()

