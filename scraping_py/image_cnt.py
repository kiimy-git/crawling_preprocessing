import os
import re

def file_count(extract_folder):
    sum_cnt = 0
    for root, dirs, files in os.walk(extract_folder):
        in_folder_name = str(root).split("\\")
        # print(root, dirs)
        if not dirs and in_folder_name[-1] == "cmp":
            sum_cnt += len(files)
            print(f"{in_folder_name[-2]} 이미지 개수 : {len(files)}")
            print("------------------------------------------------")
    
    return print(f"총 이미지 개수 : {sum_cnt}")
file_count("compare")