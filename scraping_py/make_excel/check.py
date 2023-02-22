import pandas as pd
import os

## 작업 폴더 변경
os.chdir("C:\\Users\\yhunkim\\Desktop\\검수")
try:    
    if not os.path.exists(f"Check"):
        os.makedirs("Check")
        
    
    if not os.path.exists(f"Check\\tts_check"):
        os.makedirs("Check\\tts_check")
        
    if not os.path.exists(f"Check\\emo_check"):
        os.makedirs("Check\\emo_check")
        
except OSError:
    print("Error: 생성 실패")
    
folder_list = os.listdir()[1:]
print(folder_list)

def extract_case(df, folder, conditions):
    # 밖에서 try구문 진행
    ## except empty
    if conditions == "not_tts":
        return df[conditions][["문장 번호", "파일명", "TTS", "전사 문장"]]
    
    else:
        return df[conditions][["문장 번호", "파일명", "TTS", "검수", "전사 문장"]]
    
    
## TTS = not None
def tts_ch(folder):
    
    file_list = os.listdir(folder)


    tts_df = []
    for i in file_list:
        ## 파일 이름에 ~$ 존재
        i = i.replace("~$", "")
        file_name = i.split("_")[0]
        df = pd.read_excel(f"{folder}\\{i}")

    
        not_tts = df["TTS"].notnull()
        if df[not_tts].empty:
            continue
        else:
            try:
                
                tts_df.append(df[not_tts][["문장 번호", "파일명", "TTS", "전사 문장"]])
                            
            except:

                tts_df.append(df[not_tts][["문장 번호", "파일명", "TTS", "정제 문장"]])
        
        
    print(f"-----------------------tts_ch,{folder}-----------------------")
    try:
            
        df = pd.concat(tts_df)
        writer = pd.ExcelWriter(f"Check\\tts_check\\{folder}_{len(df)}.xlsx", engine='xlsxwriter')
        df.to_excel(writer, sheet_name= 'TTS_Check', index=False)
        
        ws = writer.sheets["TTS_Check"]
        ws.set_column('B:B', 24)
        ws.set_column('C:C', 29)
        ws.set_column('D:D', 60)
        
        
        print(pd.concat(tts_df))
        
        writer.close()
    except:
        print("다르게 말한 스크립트 없음")
    print()

## 검수 = not "O" 
## 중복 코드 변경
def emo_ch(folder):
    file_list = os.listdir(folder)

    emo_df = []
    for i in file_list:
        i = i.replace("~$", "")
        file_name = i.split("_")[0]
        df = pd.read_excel(f"{folder}\\{i}")

        not_collect = (df["검수"].notnull()) & (df["검수"] != "O")
        if df[not_collect].empty:
            continue
        else:
            try:
                emo_df.append(df[not_collect][["문장 번호", "파일명", "TTS", "검수", "전사 문장"]])
                    
            except:
                emo_df.append(df[not_collect][["문장 번호", "파일명", "TTS", "검수", "정제 문장"]])
        
    # print(emo_df)
    print(f"-----------------------emo_ch, {folder}-----------------------")
    try:
        df = pd.concat(emo_df)
        writer = pd.ExcelWriter(f"Check\\emo_check\\{folder}_{len(df)}.xlsx", engine='xlsxwriter')
        df.to_excel(writer, sheet_name= 'EMO_Check', index=False)
        
        ws = writer.sheets["EMO_Check"]
        ws.set_column('B:B', 24)
        ws.set_column('C:C', 29)
        ws.set_column('D:D', 11)
        ws.set_column('E:E', 60)
        print(pd.concat(emo_df))
        
        writer.close()
        
    except:
        print("다르게 표현한 스크립트 없음")
    print()   

import shutil
for folder in folder_list[1:5]:

    tts_ch(folder)
    emo_ch(folder)

    shutil.make_archive("check", "zip", "check")
        

## TTS = not None
## 검수 = not "O"


# file_list = os.listdir(folder_list[2])
# emo_df = []

# for i in file_list:
#     df = pd.read_excel(f"{folder_list[2]}\\{i}")

#     # if df[df["TTS"].notnull()][["파일명", "TTS", "검수", "전사 문장"]]
#     # print(i, len(df[ (df["검수"].notnull()) & (df["검수"] != "O") ]))
#     # print(len(df[ (df["검수"].notnull()) & (df["검수"] != "O") ]))
#     emo_df.append(df[ (df["검수"].notnull()) & (df["검수"] != "O") ][["문장 번호", "파일명", "TTS", "검수", "전사 문장"]])
# print(pd.concat(emo_df))

