import os, glob
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

## 폴더 확인
path = r'C:\Users\yhunkim\Desktop\netflix_translation7'
file_list = os.listdir(path)
os.chdir(path)
folders = [x for x in file_list if os.path.isdir(x)]

for f in folders:
    rename("netflix_translation7", f)
