import pandas as pd
import os
from glob import glob
        
## TTS = not None
def tts_ch(work_path, folder):

    ## 작업 폴더 변경
    os.chdir(rf"{work_path}")
    try:    
        if not os.path.exists(f"Check"):
            os.makedirs("Check")
            
        
        if not os.path.exists(f"Check\\tts_check"):
            os.makedirs("Check\\tts_check")
            
        if not os.path.exists(f"Check\\emo_check"):
            os.makedirs("Check\\emo_check")
            
            
    except OSError:
        print("Error: 생성 실패")

    ## 해당 폴더의 폴더 리스트
    os.chdir(folder)
    folder_list = os.listdir(folder)
    
    for folder in folder_list:
        if folder == "Check":
            continue
        
        os.chdir(folder)
        file_list = glob("*.xlsx")
    

        tts_df = []
        for i in file_list:
            file_name = i.split("_")[0]
            df = pd.read_excel(i)

        
            not_tts = (df["검수"].notnull()) & (df["검수"] != "o")
            if df[not_tts].empty:
                continue
            else:
                try:
                    
                    tts_df.append(df[not_tts][["문장 번호", "파일명", "검수", "틀린부분", "전사 문장"]])
                                
                except:

                    tts_df.append(df[not_tts][["문장 번호", "파일명", "검수", "틀린부분", "정제 문장"]])
            
            
        print(f"-----------------------tts_ch,{folder}-----------------------")
        os.chdir(rf"{work_path}")
        try:
            if tts_df:
                df = pd.concat(tts_df)
                writer = pd.ExcelWriter(f"Check\\tts_check\\{folder}_{len(df)}.xlsx", engine='xlsxwriter')
                df.to_excel(writer, sheet_name= 'TTS_Check', index=False)
                
                ws = writer.sheets["TTS_Check"]
                ws.set_column('B:B', 24)
                ws.set_column('C:C', 29)
                ws.set_column('D:D', 60)
                ws.set_column('E:E', 60)
                

                
                writer.close()
            else:
                print(f"{folder} -- 잘못된 스크립트 없음")
        except Exception as e:
            print(e)
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

        not_collect = (df["검수"].notnull()) & (df["검수"] != "o")
        if df[not_collect].empty:
            continue
        else:
            try:
                emo_df.append(df[not_collect][["문장 번호", "파일명", "틀린부분", "검수", "전사 문장"]])
                    
            except:
                emo_df.append(df[not_collect][["문장 번호", "파일명", "틀린부분", "검수", "정제 문장"]])
        
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