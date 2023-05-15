'''
** file load
- json.load시 ","로 끝나는 경우(= 올바르지 않은 형식) load X

** regex
- re {....} 묶인 것만 가져오기
  - key값은 다 있지만 "}"으로 안 끝나는 경우(= 마지막 key_value 값이 완성되지 않은 문장 or 완성된(?) 문장도 있음)
** value 값 - "..."..." 형식 str

1. fille merge
2. 제거할 data(
    1. 요소(key)가 4개가 아닌것, 
    2. instruction, input의 value 값이 쌍으로 같은 것)
3. instruction, input, output 순으로 오름차순 정렬 및 jsonl로 저장
4. task key 제거(= task_{task 데이터 개수}.txt로 저장)
'''

import json
import re
import glob
import os
import pandas as pd

pd.set_option('display.max_rows', None)

## .txt file merge
def merge_file(folder_path):

    fn = "merge_file.txt"
    if os.path.exists(fn):
        os.remove(fn)
    else:
        print("파일 생성")

    ## .txt file 생성 될때마다 늘어남 -----------------------------------------
    read_files = glob.glob("*.txt")

    print(len(read_files))

    ## (rb, r) - 읽기, wb - 쓰기
    '''
    'wb' 모드는 이진(binary) 모드로 파일을 열기 위한 모드
    이 모드로 파일을 열면, 파일 내용이 바이너리 형태로 저장.
    따라서, 이진(binary) 모드로 열린 파일에는 텍스트를 쓸 수 없고,
    바이너리 모드로 파일을 열 때는 인코딩 지정을 생략
    
    ** wb <-> w
    이진모드(wb)는 모든파일을 읽고쓰고할수있자만
    텍스트모드(w)는 바이너리파일을 읽고쓰지는 못 함
    텍스트가 아니기 때문에 글자가 깨어져나온다
    '''
    with open(fn, 'w', encoding="utf-8") as f:
        for r in read_files:
            with open(r, "r", encoding="utf-8") as rf:
                f.write(rf.read())

    with open(fn, "r", encoding="utf-8") as mf:
        data = mf.read()
        
    return data

## preprocessing
def make_found_file(pattern, data, match_data):

    ## found
    with open('found.txt', 'w', encoding='utf-8') as ff:
        
        for s in match_data:
            ff.write(s + '\n')
        ff.close()
        
    ## not Found
    with open('not_found.txt', 'w', encoding='utf-8') as nf:

        not_found = re.sub(pattern, '', data)
        not_found = not_found.replace(",", "")
        # not_found = not_found.replace("\n", "")
        nf.write(not_found)
        ## 구분자 포함 re.split(r"({)", rnf)
        not_found = not_found.split("{")
        print(f"------------추출되지 않은 데이터 개수: {len(not_found)}------------")
        print()
        # nf.write("\n".join(not_found))

def extract_data(folder):
    os.chdir(folder)
    
    ## data merge
    if os.path.exists("found.txt") and os.path.exists("not_found.txt"):
        os.remove("found.txt")
        os.remove("not_found.txt")
    else:
        print("파일 재생성")
        
    ## data merge
    data = merge_file(folder_path=folder)
    
    ## pattern
    p = r'\{[^{}]+\}'
    match_data = re.findall(p, data)

    ## found, not_found file 생성
    make_found_file(pattern=p, data=data, match_data=match_data)

    file_list = []

    '''
    dump 계열은 파이썬의 객체(dict 등)를 다른 형태로 변환
    load 계열은 대상을 파싱해서 파이썬의 객체(dict 등)로 변환
    '''
    for line in match_data:
        ## json.loads() 함수로  dictionary로 객체로 변환시(parsing) Error(= \n)
        ## 1. json.loads(str, strict=False)
        ## 2. \n을 \\n으로 치환
        try:
            line = line.replace("\n", "")
            line = json.loads(line)
            file_list.append(line)
            
        except Exception as e:
            ## 따옴표 "..." ..." 이런 경우가 있음 
            # print(e)
            # print(line + '\n')

            ## 끝에서 두번째 따옴표 제거
            ## - 정상적인 따옴표 개수 = 16
            q = [i.start() for i in re.finditer('"', line)]
            new_line = line[:q[-2]] + line[q[-2]+1:]
            new_line = json.loads(new_line)
            file_list.append(new_line)
            

    df = pd.DataFrame(file_list, columns=["task", "instruction", "input", "output"])
    print(f"------------추출 데이터 개수: {len(df)}------------")

    if os.path.exists(f"extract_data_{len(df)}.xlsx"):
        os.remove(f"extract_data_{len(df)}.xlsx")
    else:
        print(f"extract_data 파일 생성")
        
    df.to_excel(f"extract_data_{len(df)}.xlsx")
    
    ## 카테고리
    print(f"task_category - {df.task.unique()}")
    category = df.task.unique()

    for cat in category:
        print(f"-------------카테고리: {cat}-------------")
        
        cat_df = df[df["task"] == cat]
        cat_df = cat_df.drop_duplicates(subset=["instruction", "input"], keep='first')
        cat_df = cat_df.iloc[:, 1:]
        
        cat_df.to_json(cat + "_" + str(len(cat_df)) + ".jsonl", 
                       orient='records', lines=True, force_ascii=False)


folder = r"C:\Users\yhunkim\Downloads\finance_dataset\\"
extract_data(folder=folder)