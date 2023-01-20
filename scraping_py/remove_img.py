import os
import re


## GFPGAN으로 생성된 이미지 파일로부터 
## ------------지우지말고 복사(?)------------

remove_list = "1_00 100_00 102_00 104_00 108_00 113_00 117_00 117_01 120_00 129_00 129_01 \
13_00 130_01 133_00 136_00 143_00 144_00 145_00 149_00 152_00 16_00 160_00 162_00 162_01 \
169_00 177_00 177_01 179_00 18_00 182_00 183_00 188_00 192_00 192_01 202_00 203_00 205_00 \
206_00 208_02 209_00 209_01 209_02 21_00 217_00 218_00 219_00 220_00 223_00 235_00 237_00 \
25_00 252_00 259_00 260_00 265_00 266_00 267_00 269_00 27_01 27_02 27_03 271_00 272_00 272_01 \
275_00 278_00 279_00 279_01 279_02 282_00 284_00 34_00 35_00 38_00 43_00 46_00 46_01 50_00 \
53_03 60_00 61_00 65_00 66_00 7_00 73_00 75_00 80_00 81_00 93_00 95_00 96_00 97_00 99_00"  
 
def to_list(remove_list):
    new_list = remove_list.split(" ")
            
    return new_list
        
def remove_img_func(remove_list, cmp_path, restored_path):
    remove_img = to_list(remove_list)
    
    c_path = os.listdir(cmp_path)
    r_path = os.listdir(restored_path)
    
    for c, r in zip(c_path, r_path):
        c_img = c.split(".png")[0]
        r_img = r.split(".png")[0]

        if c_img in remove_img and r_img in remove_img:
            print(c_img, r_img)
            os.remove(f'{cmp_path}\\{c}')
            os.remove(f'{restored_path}\\{r}')

remove_img_func(remove_list, 
                r"compare\한국여성쇼핑몰모델cmp\cmp",
                r"compare\한국여성쇼핑몰모델restored\restored_faces")
# print(to_list(remove_list))

# os.rename('filename.txt', 'new_filename.txt')