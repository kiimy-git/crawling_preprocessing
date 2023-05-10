import os, glob
import pandas as pd
from PIL import Image


def rename(netflix_name, folder_name):


    path = rf"C:\Users\yhunkim\Desktop\{netflix_name}\{folder_name}"
    folder_list = os.listdir(path)
    for folder in folder_list:
        os.chdir(path + "\\" + folder)
        file_list = glob.glob('*.xlsx')
        file_list.sort(key=os.path.getmtime)
    
        for i in range(1, len(file_list)+1):
            num = list(str(i))
            
            if len(num) == 2:
                os.rename(path + "\\" + folder + "\\" + file_list[i-1], path + "\\" + folder + "\\" + f"{i}" + '.xlsx')
                
            else:
                os.rename(path + "\\" + folder + "\\" + file_list[i-1], path + "\\" + folder + "\\" + "0" + f"{i}" + '.xlsx')


def text_check(netflix_name, folder_name):
    
    print(netflix_name)
    print(f"-----<<<<<      {folder_name}      >>>>>-----")
    print()
    path = rf"C:\Users\yhunkim\Desktop\{netflix_name}\{folder_name}"
    
    folder_list = os.listdir(path)
    ## 파일 개수 
    
    total_cnt = 0
    for folder in folder_list:
        os.chdir(path + "\\" + folder)
        file_list = glob.glob('*.xlsx')
        file_list.sort(key=os.path.getmtime)
        
        total_cnt += len(file_list)
        
        text = []
        for cnt in range(len(file_list)):
            
            # if file_list[cnt] == "Text확인":
            #     continue
            df = pd.read_excel(file_list[cnt])
            txt_df = df.iloc[:2][["Subtitle", "Translation"]]
    
            text.append(txt_df)
                
        if not text:
            print(f"{folder} - 파일 없음")
            continue

        df1 = pd.concat(text, ignore_index=True)
        # df1.index = df1.index + 1 #인덱스 1부터 시작하기
        print(f"<<<<<<<<<<<<<<<<<{folder}, {len(file_list)}개>>>>>>>>>>>>>>>>>"+"\n")
        # print(df1)
        cnt += len(file_list)
        ## 두개row씩 묶기(= column)
        group_df = df1.groupby(df1.index // 2)
        # final_df = pd.concat([text for _, text in group_df], axis=1, keys=[## 해당 열 그룹 이름 ...])
        # print(final_df)
        
        ## print
        for eps, text in group_df:
            print(f"----------------에피소드: {eps+1}화----------------")
            print(text)
            print()
        print()
        ## df1.to_excel("Text확인.xlsx")
    print("총 추출 개수 : ", total_cnt)
## 폴더 확인
# netflix_translation22
folder_name = "netflix_translation32"

path = rf'C:\Users\yhunkim\Desktop\{folder_name}'
file_list = os.listdir(path)
os.chdir(path)
folders = [x for x in file_list if os.path.isdir(x)]


pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.options.display.max_rows = None


            

for f in folders:

    # text_check(folder_name, f)
    try:
        rename(folder_name, f)
        
    except Exception as e:
        print(e)
        
