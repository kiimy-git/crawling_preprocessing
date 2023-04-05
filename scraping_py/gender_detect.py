import cv2
import argparse
import os
import shutil

## Gender Detect 성능 떨어짐 = 사용 X

parser=argparse.ArgumentParser()
parser.add_argument('--image')

args=parser.parse_args()

genderProto="gender_deploy.prototxt.txt"
genderModel="gender_net.caffemodel"
'''
## 파일다운
ageProto="age_deploy.prototxt"
ageModel="age_net.caffemodel"
ageNet = ...
'''
genderNet=cv2.dnn.readNet(genderModel,genderProto)

MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
genderList=['Male','Female']

## GFPGAN으로 추출한 폴더
def gender_detect(path):
    img_list = os.listdir(path)

    ## 작업폴더 변경
    os.chdir(path)
    try:
        ## Gender 폴더 생성
        if not os.path.exists(genderList[0]) or os.path.exists(genderList[1]):
            os.makedirs(genderList[0])
            os.makedirs(genderList[1])
    except:
        print(f"{genderList[0]}, {genderList[1]} 폴더 생성됨")


    ## 한 이미지에 여러명 있을때는 못잡음
    for i in range(len(img_list)):
        
        ## 작업 폴더 변경 후 진행하면 cv2.imread 그대로 읽힘
        img = cv2.imread(img_list[i])
        try:
            blob = cv2.dnn.blobFromImage(img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds = genderNet.forward()
            gender = genderList[genderPreds[0].argmax()]
            
            # print(f"{img_list[i]}")
            print("Gender Output : {}".format(genderPreds))
            print("Gender : {}".format(gender),"\n")
            
            ## age
            # ageNet.setInput(blob)
            
            
            ## 파일 복사 후 이동
            if gender == "Male":
                shutil.copy(img_list[i], genderList[0])
                
            elif gender == "Female":
                shutil.copy(img_list[i], genderList[1])
            else:
                print("-----None-----")
        except:
            print("-----Not Image-----")
            
# gender_detect(r"path")
# gender_detect(r"compare\여자메이크업cmp\cmp")
