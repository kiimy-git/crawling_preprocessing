import os
import pandas as pd
import xlsxwriter
import json
import glob
from tqdm import tqdm

a = os.listdir(r"C:\Users\yhunkim\Desktop\namu_wiki\beyond_the_jeju\data\jsonl")
## to list
def to_list(work_folder_path):
    file_list = os.listdir(work_folder_path)
    os.chdir(r"C:\Users\yhunkim\Desktop\namu_wiki")
    res = []
    for i in file_list:
        
        json_data = []
        with open(rf'beyond_the_jeju\data\jsonl\{i}', 'rt', encoding='UTF-8') as file:
            for line in file:
                if "sentence" in line:
                    line = line.replace("sentence", "text")
                    
                ## eval ==> dict
                json_data.append(eval(line))
                

        res.append(json_data)

    return res

## make excel file
def create_xlsx_file(file_path: str, headers: dict, items: list):
    
    with xlsxwriter.Workbook(file_path) as workbook:
        worksheet = workbook.add_worksheet()
        
        worksheet.write_row(row=0, col=0, data=headers.values())
        
        worksheet.set_column(0, 0, 30)
        worksheet.set_column(1, 1, 150)
        
        header_keys = list(headers.keys())
        for index, item in enumerate(items):
            row = map(lambda field_id: item.get(field_id, ''), header_keys)
            worksheet.write_row(row=index + 1, col=0, data=row)

## to excel
def to_excel(work_folder_path):
    res = to_list(work_folder_path)
    
    header = {"title": "title", 
              "text": "text"}
    
    for i in range(len(res)):
        name = a[i].split(".")[0]
        ## make excel file
        create_xlsx_file(f"{name}.xlsx", header, res[i])


## remove text
def remove_text(df):
    remove_index = df[df["del"] == "o"].index
    df.drop(remove_index, inplace=True)
    df.drop(["del"], axis=1, inplace=True)
    
    return df

## to jsonl and remove_text => glob
def to_json(excel_file_path):
    # 게임스토리
    import re
    os.chdir(excel_file_path)
    
    files = glob.glob('*.xlsx')
    for file in files:
        if file == "포맷.xlsx":
            continue
        name = file.split(".")
        df = pd.read_excel(file)

        ## 파일명 변경
        with open(f'{name[0]}.jsonl', 'w', encoding='utf-8') as outfile:
            
            ## to_json = 한글 깨짐 ==> force_ascii=False // 최종적으로 저장할때만 사용하면됨
            for entry in tqdm(df.T.to_dict().values(),
                              desc = f"{name}",
                              ncols = 90,
                              leave = True):
                ## dict key 이름 변경
                # dic[new_key] = dic.pop(old_key)
                try:
                    entry["Subtitle"] = entry["Subtitle"].replace("\"", "")

                    ## json.dumps = 한글 깨짐 ==> ensure_ascii=False
                    json.dump(entry, outfile, ensure_ascii= False) # => indent를 여기서 설정하면 이상하게 나옴
                    outfile.write('\n')
                except:
                    continue

to_json('게임스토리')
# excel = files[3]
# # print(files[3])
# df = pd.read_excel(excel)
# for entry in df.T.to_dict().values():
#     entry["Subtitle"] = entry["Subtitle"].replace("\"", "")
#     print(entry)



# def cell_width(df, save_file_name):
#     writer = pd.ExcelWriter(f"{save_file_name}.xlsx")

#     df.to_excel(writer, sheet_name=save_file_name, index=False)

#     for column in df:
#         column_length = max(df[column].astype(str).map(len).max(), len(column))
#         col_idx = df.columns.get_loc(column)
#         writer.sheets['sheet1'].set_column(col_idx, col_idx, column_length)

#     writer
