import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import colors
from openpyxl.styles import Font, Color
import os

## 모든 열, 행
pd.options.display.max_columns = None
pd.options.display.max_rows = None

## 파일 압축
def to_zip(file_list):
    import shutil
    for i in file_list:
        if "matching" in i:
            shutil.make_archive(i, "zip", i)


## 다른 문자 확인
def Unmatching_text(text1, text2):
    import re
        
    t1 = text1.split(" ")
    t2 = text2.split(" ")
    
    
    ## 순서만 바뀐 경우도 있음
    ## 아이, != 아이 처럼 문장부호가 붙어 있는 경우 추출못하고 있음
    remove_str1 = []
    remove_str2 = []
    
    ## set
    for i in t1:
        p = rf"{i}"

        for v in t2:
            m1 = re.match(p, v)
            m2 = re.match(v, p)
            
            ##### v도 같이 내보내면?? #####
            ## v 순서가 이상
            if m1 and m2:
                remove_str1.append(p)
                remove_str2.append(v)
                        
    diff_text1 = list(set(t1) - set(remove_str1))
    diff_text2 = list(set(t2) - set(remove_str2))

    return [diff_text1, diff_text2]
        
## 스크립트 매칭
def emotions(e):
    
    try:
        if not os.path.exists(f"matching"):
            os.makedirs("matching")
        
        ## matching 폴더 이동
        os.chdir("matching")
        
        if not os.path.exists(f"{e}_matching"):
            os.makedirs(f"{e}_matching")

    except OSError:
        print("Error: 생성 실패")
    
    emotions = os.listdir(e)
    
    for i in range(len(emotions)-1):
        file_name = emotions[i].split("_")[0]
        
        for v in range(i+1, len(emotions)):
            file_name1 = emotions[v].split("_")[0]
            
            df = pd.read_excel(e + "\\" + emotions[i])
            df1 = pd.read_excel(e + "\\" + emotions[v])

            ## 결측치 제거(axis=0, row)
            df.dropna(axis=0, inplace=True)
            df1.dropna(axis=0, inplace=True)
            
            text = []
            for index, val in enumerate(df["전사 문장"]):
                ## non-breaking space로 Latin1, chr(160)인코딩형태로 나옴
                # ==> ex) 이런 다짐을 어떻게 (\x0)해석해야만        
                try:
                    val = val.replace(u'\xa0', u' ')
                    val2 = list(df1["전사 문장"])[index].replace(u'\xa0', u' ')
                    
                    if val not in val2:
                            ## text 요소별 비교
                            words = Unmatching_text(val, val2)
                            text.append([index+1, words, val, val2])

                except Exception as ex:
                    print(f"------------({e}_{file_name}\\{file_name1}) - {ex}------------")
                    continue

            ## to dataframe
            col_list = ["문장 번호", "틀린 단어", f"{file_name}전사 문장", f"{file_name1}전사 문장"]
            df = pd.DataFrame(text, columns=col_list)
            
            ## to excel
            writer = pd.ExcelWriter(f"{e}_matching\\{file_name}_{file_name1}_{len(text)}.xlsx", engine='xlsxwriter')
            df.to_excel(writer, sheet_name= 'Matching', index=False)
            
            ## value 값에 column 길이 맞추기
            wb = writer.book
            ws = writer.sheets["Matching"]
            ws.set_column('C:D', 85)
            
            ## 틀린 문자 Font 설정
            # format 설정
            # ft = Font(color=colors.Color(rgb="FF0000"), bold=True)
            f1 = wb.add_format({'bold':True, 'font_color': 'red'})
            ws.set_column("B:B", 25, f1)
            
            
            ## Column길이에 cell 길이 맞추기
            # for col in df:
            #     col_width = df[col].astype(str).map(len).max()
            #     col_idx = df.columns.get_loc(col)

            #     writer.sheets["Matching"].set_column(col_idx, col_idx, col_width)

            writer.close()
                
            print(f"{e}_{file_name}_{file_name1}", len(text))

print(os.listdir())

# for i in os.listdir()[:-1]:
#     emotions(i)
        
    
# print(remove_str)
    # t2 = re.sub(rf"{i}", "", t2)
    # print(t2)
    

## 배열의 길이가 다를때, 다른 건 None으로 출력
from itertools import zip_longest
# for a, b in zip_longest(t1,t2):
#     pass

## df.iloc[모든 행, 지정 열]
# print(df.iloc[:, 2:4])

    
    