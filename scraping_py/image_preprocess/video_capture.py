import cv2 as cv
import sys
import os


file_path = r'C:\Users\yhunkim\Desktop\capture\image\epic_video'
file_list = os.listdir(file_path)

for i in range(len(file_list)):

    ## 파일 저장 이름
    file_name = file_list[i].split("]")[1][1:-4]
    file_name = file_name.replace("-", "_")
    
    ## 경로가 한글일때,
    # with open(file_path + '\\' + file_list[i], 'rb') as f:
    #     data = f.read()
    # data_io = BytesIO(data)

    v = cv.VideoCapture(file_path + '\\' + file_list[i])

    # # 저장할 압축된 비디오 파일 경로
    # output_file = os.getcwd() + r"\image" + r'\compressed_video.mp4'

    if not v.isOpened():
        print("Could not Open", file_path + '\\' + file_list[i])
        sys.exit(0)

    ## 비디오 파일 정보
    length = int(v.get(cv.CAP_PROP_FRAME_COUNT))
    width = int(v.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(v.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = v.get(cv.CAP_PROP_FPS)

    ## 이미지 추출 간격 설정(=3초)
    interval = int(fps * 3)

    ## 비디오 코덱 설정 == 비디오 파일 크기가 너무 클때, 압축
    codec = cv.VideoWriter_fourcc(*'XVID')
    # out = cv.VideoWriter(output_file, codec, fps, (width, height))
    
    ### save_path 
    save_path = os.getcwd() + "\\" + "img_collections" + '\\' + 'epic_images'

    try:
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    except Exception as e:
        print(e, "Create Error or Already Exists")

    frame_cnt = 1
    while v.isOpened():
        ret, frame = v.read()
        if not ret:
            break

        if int(v.get(1)) % 15 == 0: # fps

            # cv.imshow('video', frame)
            # #  cv2.waitKeyEX() 함수를 이용하면 방향키, 함수키와 같은 특수 키를 처리할 수 있습니다.
            # # ASCII 27번 == ESC
            # if cv.waitKey() == 27:
            #     break
            ## 경로에 한국어가 포함되있으면 저장안됨(= save_path, 저장할 이름(***.png) ==> 영어(Encoding))
            save_filename = f"{file_name}_{frame_cnt}.png"
            save_filepath = os.path.join(save_path.encode('utf-8'), save_filename.encode('utf-8'))

            with open(save_filepath, 'wb') as f:
                ## imencode
                ## return : retval(압축 결과 : True / False), buf(인코딩된 이미지)
                f.write(cv.imencode('.png', frame)[1]) ## retval, buf

            print(f"save image {file_name}_{frame_cnt}")

            frame_cnt += 1
        
    v.release()
