import shutil
import os
from makedir import make_dir

print(os.getcwd())

os.chdir("scraping_folder")

def to_zip(folder_name):
    make_dir("원본 이미지 압축")
    shutil.make_archive(folder_name, 'zip', folder_name)
    shutil.move(folder_name + ".zip", "원본 이미지 압축")
to_zip("한국 여성 쇼핑몰 모델")

