
import os, glob
import pandas as pd
from PIL import Image
import cv2 as cv

folder_name = "캐릭터"

# path = rf'C:\Users\yhunkim\Desktop\{folder_name}'
path = rf'C:\Users\yhunkim\Desktop\capture\scraping_folder\로스트아크 배경'
# file_list = os.listdir(path)
os.chdir(path)
file_list = glob.glob('*.jpg')
folders = [x for x in file_list if os.path.isdir(x)]


pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.options.display.max_rows = None
def img_resize(folders):
    for folder in folders:
        game_path = path + rf"\{folder}"

        game = os.listdir(game_path)
        for char in game:
            char_path = game_path + rf"\{char}"
            os.chdir(char_path)
            
            ## resize folder
            if not os.path.exists("resize_image"):
                os.makedirs("resize_image")

            img_files = os.listdir(char_path)
            print(f"-------------케릭터 : {char}-------------")
            img_files.sort(key=os.path.getmtime)

            # print(img_files)

            for img in img_files:
                ext = os.path.splitext(img)[1]
                if ext != '.jpg':
                    with Image.open(img) as im:
                        convert_im = im.convert('RGB')
                        ## overwrite = 덮어씌우기
                        os.chdir("resize_image")
                        convert_im.save(os.path.splitext(img)[0] + '.jpg', overwrite=True)
                        
                        ## 이미지 파일의 경로를 가져오기 = .filename
                        # os.remove(im.filename)
                
                ## 확장자 확인
                print(f"{img} = {ext}")
                
                # with Image.open(img) as im:
                #     new_img = im.resize(512, 512)
                #     new_img.show
                im = cv.imread(img)
                if im is not None and im.shape[0] > 0 and im.shape[1] > 0:
                    resized_img = cv.resize(im, dsize=(512,512), interpolation=cv.INTER_AREA)
                    
                    # Get the size of the image
                    height, width, channels = resized_img.shape

                    # Print the size of the image
                    print(f'Image size: {width} x {height}, Channels: {channels}')
                    print()
                    # Save the resized image
                    cv.imwrite(img, resized_img)
                else:
                    print('Failed to load image')
                    
            print()

def check_img(folders):
    for folder in folders:
        game_path = path + rf"\{folder}"

        game = os.listdir(game_path)
        for char in game:
            char_path = game_path + rf"\{char}"
            os.chdir(char_path)
            img_files = os.listdir(char_path)
            print(f"-------------케릭터 : {char}-------------")

            # print(img_files)

            for img in img_files:
                im = cv.imread(img)
                if im is not None and im.shape[0] > 0 and im.shape[1] > 0:
                    cv.imshow(f"{char}-{img}", im)
                    cv.waitKey(0)
                    cv.destroyAllWindows()

def img_rename(folders):
    for folder in folders:

        game_path = path + rf"\{folder}"

        game = os.listdir(game_path)
        for char in game:
            char_path = game_path + rf"\{char}"
            os.chdir(char_path)
            file_list = glob.glob('*.jpg')
            file_list.sort(key=os.path.getmtime)

            for i in range(1, len(file_list)+1):
                num = list(str(i))
                
                if len(num) == 2:
                    os.rename(char_path + rf"\{file_list[i-1]}", rf"{i}" + '.jpg')
                    
                else:
                    os.rename(char_path + rf"\{file_list[i-1]}", rf"{i}" + '.jpg')

def chage_format(file_list):
    
    for i in range(len(file_list)):
        img = cv.imread(file_list[i])
        cv.imwrite(f'{i}.png', img)
        
