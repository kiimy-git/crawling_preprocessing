import os

## 폴더 생성
def make_dir(dir_name):
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

    except OSError:
        print("Error: 생성 실패")
    '''
    우선 mkdir은 한 폴더만 생성이 가능합니다. 아래처럼 ./a/b/c 와 같이 폴더 내의 폴더는 생성할 수 없습니다.

    단, 기존에 new_folder라는 폴더가 있으면 os.mkdir('./new_folder/a') 를 통해 a라는 폴더 하나를 생성할 수 있습니다.

    다만 이와 같은 경우에 new_folder 폴더가 없으면 exception 에러가 뜨게 됩니다.

    

    makedirs는 './a/b/c' 처럼 원하는 만큼 디렉토리를 생성할 수 있습니다.

    exist_ok라는 파라미터를 True로 하면 해당 디렉토리가 기존에 존재하면 에러발생 없이 넘어가고, 없을 경우에만 생성합니다.

    반대로, exist_ok를 True로 설정하지 않았을 때 이미 해당 디렉토리가 존재하는 경우에는 exception에러가 뜨게 됩니다
    '''
    