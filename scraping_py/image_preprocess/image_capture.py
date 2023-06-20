'''
1. 이미지 얼굴, 상반신, 전신으로 분류
2. capture size는 정사각형으로
'''


import os, glob
import pandas as pd
from PIL import Image
import cv2 as cv

red = (0,0,255)
## 폴더 image 파일만 

## 드래그 활성
isclick = False
x1, y1 = -1, -1

face = r'C:\Users\yhunkim\Desktop\cropped\face'
upper = r'C:\Users\yhunkim\Desktop\cropped\upper'
body = r'C:\Users\yhunkim\Desktop\cropped\body'

folders = [face, upper, body]

## 마우스 이벤트 처리 함수
def drag_img(event, x, y, flags, param):
    global x1, y1, isclick, img, folder_name, img_name
    
    # 이미지 크기
    height, width, _ = img.shape
    
    # 마우스 누른 상태
    if event == cv.EVENT_LBUTTONDOWN:
        isclick = True
        x1, y1 = x, y
        print(f"첫 좌표 = X1: {x1}, Y1: {y1}")

    # drag - 마우스 누른 상태에서
    elif event == cv.EVENT_MOUSEMOVE:
        if isclick:
            img_draw = img.copy()
            cv.rectangle(img_draw, (x1,y1), (x,y), red, 2)
            cv.imshow('img', img_draw)
    
    # image crop - crop 이미지에서 중간값을 기준으로 나누기
    elif event == cv.EVENT_LBUTTONUP:

        if isclick:
            isclick = False
            
            ## 너비 X 높이
            w = x - x1
            h = y - y1

            print (f"너비 X 높이: {w} x {h}")
            
            if w > 0 and h > 0:
                img_draw = img.copy()
                
                if w > h:
                    ## crop시 너비에 맞춰 정사각형으로 추출시, 너비(w)가 (y1좌표에서의 이미지 높이 값)보다 크면
                    ## 케릭터가 누워있을때
                    
                    if w > (height - y1):
                        y1 -= (w - (height - y1))
                        roi = img[y1:y1+w, x1:x1+w]
                        
                        
                        print(f"crop shape : {roi.shape}")
                        cv.imshow('cropped', roi)
                        cv.imwrite(f'{folder_name}\\{img_name}.png', roi)
                        print("--------------이미지 저장--------------")
                        
                        
                    else:
                        h = w
                        roi = img[y1:y1+h, x1:x1+w]
                        
                        
                        print(f"crop shape : {roi.shape}")
                        cv.imshow('cropped', roi)
                        cv.imwrite(f'{folder_name}\\{img_name}.png', roi)
                        print("--------------이미지 저장--------------")
                        
                
                ## 케릭터가 왼쪽, 오른쪽 끝에 있을 수 있음
                ## 예외- 왼쪽 끝 ,오른쪽 끝에 여유가 있을때는??
                else:
                    ## 케릭터 위치 
                    x2 = (x1+w)
                    mid_val = x1 + (w / 2)
                    
                    plus_val = (h-w) / 2
                    p_x1 = x1- plus_val
                    p_x2 = x2 + plus_val
                    mid_ratio = int((mid_val / width) * 100)
                    print(f"케릭터 중앙 위치 값 : {mid_ratio}")
                    
                    ## 케릭터가 오른쪽에 있을때,
                    if mid_ratio > 60:
                        print("---------------오른쪽---------------")
                        
                        ## 우측 여유 공간이 없을때
                        if p_x2 > width:
                            p1 = p_x2 - width
                            roi = img[y1:y1+h, int(p_x1-p1):width]
                            print(f"crop shape : {roi.shape}")
                            cv.imshow('cropped', roi)
                            cv.imwrite(f'{folder_name}\\{img_name}.png', roi)
                            print("--------------이미지 저장--------------")
                            
                        else:
                        # x1 -= (h - (width - x1))
                        # roi = img[y1:y1+h, x1:x1+h]
                            roi = img[y1:y1+h, int(p_x1):int(p_x2)]
                        
                            print(f"crop shape : {roi.shape}")
                            cv.imshow('cropped', roi)
                            cv.imwrite(f'{folder_name}\\{img_name}.png', roi)
                            print("--------------이미지 저장--------------")
                        
                        
                    ## 케릭터가 왼쪽에 있을때,
                    elif mid_ratio < 40:
                        print("---------------왼쪽---------------")

                        ## 좌측 여유 공간이 없을때
                        if p_x1 < 0:
                            p1 = abs(p_x1)
                            roi = img[y1:y1+h, 0:int(p_x2+p1)]
                            print(f"crop shape : {roi.shape}")
                            cv.imshow('cropped', roi)
                            cv.imwrite(f'{folder_name}\\{img_name}.png', roi)
                            print("--------------이미지 저장--------------")
                        # roi = img[y1:y1+h, x1:x1+h]
                        else:
                            roi = img[y1:y1+h, int(p_x1):int(p_x2)]
                            
                            print(f"crop shape : {roi.shape}")
                            cv.imshow('cropped', roi)
                            cv.imwrite(f'{folder_name}\\{img_name}.png', roi)
                            print("--------------이미지 저장--------------")
                        
                        
                    ## 일반적인 경우(가운데)
                    else:
                        print("---------------가운데---------------")
                        
                        roi = img[y1:y1+h, int(p_x1):int(p_x2)]
                        
                        print(f"crop shape : {roi.shape}")
                        cv.imshow('cropped', roi)
                        cv.imwrite(f'{folder_name}\\{img_name}.png', roi)
                        print("--------------이미지 저장--------------")





path = r"C:\Users\yhunkim\Desktop\cropped"
os.chdir(path)

# img_name = "ZEPETO_CAPTURE_-8585144551944732107"
# img = cv.imread("ZEPETO_CAPTURE_-8585144551944732107.png")
# cv.imshow('img', img)
# for folder_name in folders:
#     cv.setMouseCallback('img', drag_img)

#     cv.waitKey()

images = glob.glob("*.png")
cnt = len(images)
for i in range(len(images)):
    img_name = images[i]
    img = cv.imread(images[i])
    cv.imshow('img', img)
    
    for folder_name in folders:
        cv.setMouseCallback('img', drag_img)

        cv.waitKey()