import os
import pandas as pd
import cv2

pd.options.display.max_columns = None
pd.options.display.max_rows = None

def duplicate_file(folder):

    path = folder.replace('\\', '/', 10)
    img_list = os.listdir(path)

    ## os.path.getsize('path/filename') == 파일 사이즈
    file_size = list(map(lambda x: os.path.getsize(path + "\\" + x), img_list))

    ## DataFrame
    df = pd.DataFrame({"img_name": img_list, "file_size": file_size})
    count_df = pd.DataFrame({"file_size": df["file_size"].value_counts().index, "cnt": df["file_size"].value_counts().values})
    merge_df = pd.merge(df, count_df, how="left", on ="file_size")

    ## if len(merge_df[merge_df['cnt']>1]) == 0: ==> 권장하지않음
    ## Use a.empty, a.bool(), a.item(), a.any() or a.all()
    # if not a: ==> Error
    if merge_df[merge_df['cnt']>1]["file_size"].empty:
        return print('중복 사이즈의 갯수 :', len(merge_df[merge_df['cnt']>1]))
        

    
    final = df.sort_values(['img_name'], ascending = True).drop_duplicates(['file_size'], keep = 'first')
    print(final,"\n")

    ## 이미지 확인
    for i in merge_df[merge_df['cnt']>1]["file_size"]:
        dupli_file = df[df["file_size"] == i]
        print(dupli_file, "\n")
        
        for i in range(len(dupli_file)):
            
            img = cv2.imread(path + "\\" + dupli_file["img_name"].iloc[i])
            
            if img is None:
                print(f'{dupli_file["img_name"].iloc[i]} - 삭제됨')
                continue
            
            cv2.namedWindow(f'{dupli_file.iloc[i]}')   
            cv2.imshow("img", img)
            print(dupli_file.iloc[i])
            cv2.waitKey()

duplicate_file("google_image")
