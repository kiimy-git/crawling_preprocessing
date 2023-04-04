import os, glob
import pandas as pd
from PIL import Image
import cv2 as cv

def img_crop(file_list):
    global img
    img = cv.imread(file_list)

    # 이미지 크기
    height, width, _ = img.shape
    
    ## 원본 이미지 1:1 비율로 줄이기

    # 설정할 부분의 크기 (512x512)
    crop_size = 512

    # 마우스 이벤트 처리 함수
    def crop_img(event, x, y, flags, param):
        global img, crop_rect
        
        # 클릭한 위치를 중심으로 512x512 크기의 박스 생성
        crop_rect = (max(0, x - crop_size // 2), max(0, y - crop_size // 2), min(width, x + crop_size // 2), min(height, y + crop_size // 2))

        # 박스 내부 이미지 추출
        crop = img[crop_rect[1]:crop_rect[3], crop_rect[0]:crop_rect[2]]
        
        if event == cv.EVENT_LBUTTONDOWN:
            print(crop.shape)
            # 추출된 이미지 확인
            cv.imshow("crop", crop)

        # 왼쪽 버튼을 누르고 떼어지면 활성화
        elif event == cv.EVENT_LBUTTONUP:
            pass
                
        # 왼쪽 마우스 버튼을 누른 상태에서 마우스 이동
        elif event == cv.EVENT_MOUSEMOVE:  
            if flags & cv.EVENT_FLAG_LBUTTON:
                # 이미지에 박스 그리기
                # cv.rectangle(img, (crop_rect[0], crop_rect[1]), (crop_rect[2], crop_rect[3]), (0, 0, 255), 2)
                cv.imshow("crop", crop)
                
    cv.namedWindow('image', cv.WINDOW_NORMAL)
    cv.setMouseCallback('image', crop_img)

    while True:
        cv.imshow('image', img)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cv.destroyAllWindows()