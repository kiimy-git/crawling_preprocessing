import os
import re

def file_count(extract_folder):
    sum_cnt = 0
    key_cnt = []
    for root, dirs, files in os.walk(extract_folder):
        in_folder_name = str(root).split("\\")
        # print(root, dirs)
        try:
            if not dirs and in_folder_name[-1] == "cmp":
                sum_cnt += len(files)
                key_cnt.append(in_folder_name[-2])
                print(f"{in_folder_name[-2]} 이미지 개수 : {len(files)}")
                print("------------------------------------------------")
                
        except:
            print("Not Find")
    
    print(f"총 이미지 개수 : {sum_cnt}, 키워드 개수 : {len(key_cnt)}")
            
file_count("compare")
