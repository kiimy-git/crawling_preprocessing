import requests
import os
from bs4 import BeautifulSoup as BS
import urllib3
import urllib.request
from PIL import Image
from io import BytesIO
from time_check import check_time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
from makedir import make_dir
from multiprocessing import Pool
from mediapipe_face import face_detect, url_to_image

urllib3.disable_warnings()

## ID 다음에 html 소스가 없으면 동적 == selenium 이용
## 정적인 페이지 == BeautifulSoup

## 정적
# page - 사이트 여러개(외부에서 for문)
@check_time
def bs_wep_scrap(url, tag, folder, page):

    #### -------------- 페이지 범위 설정 -------------- ####
    # = 외부에서 for 반복문(url{page})
    
    ## verify???
    page = requests.get(url, verify=False)

    soup = BS(page.content, 'html.parser')

    ## css 선택자로 검색한다. 그냥 태그를 쓰면 태그 검색. 항상 리스트로 리턴함
    images = soup.select(tag)
    
    i = 1
    for img in images:
        ## 웹 주소 요청
        res = requests.get(img["src"], verify=False)
    
        ## Image.open()함수에는 보통 이미지 파일 경로를 매개변수로 넘겨주지만, 때에 따라선 io.BytesIO()객체를 넘겨줄 수도 있다.
        ## 객체를 넘겨주면 객체 내에 저장된 bytes 정보를 불러와 이미지로 읽어줌
        
        get_img = Image.open(BytesIO(res.content))

        get_img.save(f'{folder}/{page}-test{i}.jpg')
        i += 1
    
        if i == len(images):
            return print(f"스크랩 이미지 개수 : {len(images)}")



## 동적
# page - 사이트 여러개(외부에서 for문)
@check_time
def sel_web_scrap(url, tag, folder, page):

    ## 이미지 번호
    p = re.compile('(?<=[/])[0-9]+')

    ## Selenium
    driver = webdriver.Chrome("C:\\Users\\yhunkim\\Desktop\\capture\\chromedriver")

    driver.get(url=url)
    ## Error- driver.find_element_by_css_selector(tag)
    # => from selenium.webdriver.common.by import By 해줌
    elements = driver.find_elements(By.CSS_SELECTOR, tag)

    for i in elements:
        res = i.get_attribute("src")
        
        ## get_image = Image.open(BytesIO(res))
        # = TypeError: a bytes-like object is required, not 'str' // res가 str이기 때문에 decode
        '''
        str => 디코딩 => bytes
        bytes => 인코딩 => str
        # res_decode = res.e ('utf-8')
        # get_image = Image.open(BytesIO(res_encode))
        '''
        text_num = p.findall(res)[0]
        
        # 이미지 요청 및 다운로드
        urllib.request.urlretrieve(res, f'{folder}/{page}-{text_num}.jpg')

@check_time
def google_crawling(search):
    driver = webdriver.Chrome("C:\\Users\\yhunkim\\Desktop\\capture\\chromedriver")

    ## 이미지 검색 링크
    driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")

    ## 검색어
    # search = "한국 여성 영화"
    element = driver.find_element(By.NAME, "q")
    element.send_keys(search)
    element.send_keys(Keys.RETURN)
    
    ## 구글 이미지 검색이 스크롤을 내리면 계속 새로운 스크롤이 갱신됨
    scroll_time = 1

    ## execute_script("스크립트", 요소) - 해당 페이지에 스크립트를 만들때 사용
    # 요소는 필수 파라미터는 아니고 요소가 있으면 요소에 스크립트가 실행되고 없으면 전체 페이지에 스크립트가 움직입니다.
    # 오버플로로 인해 화면에 표시되지 않는 콘텐츠를 포함하여 요소 콘텐츠의 높이를 측정한 것(= DHTML scrollHeight)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        
        ## window.scrollTo(x-좌표, y-좌표) - 문서의 지정된 위치로 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_time)
        new_height = driver.execute_script("return document.body.scrollHeight") 
        
        if new_height == last_height:
            try:
                driver.find_element(By.CSS_SELECTOR, ".mye4qd").click()

            except:
                break
            
        last_height = new_height
    
    ## scraping폴더 생성 및 작업 폴더 변경
    make_dir("scraping_folder")
    os.chdir("scraping_folder")
    
    ## 작업경로에 폴더 생성
    make_dir(search)

    ## 이미지 찾기 및 저장(=원본 이미지)
    images = driver.find_elements(By.CSS_SELECTOR, ".rg_i.Q4LuWd")
    cnt = 1

    for img in images:
        try:
            ## 해당 이미지 클릭 == 원본 이미지
            img.click()
            time.sleep(2)

            img_url = driver.find_element(By.XPATH, 
                                        "//*[@id='Sva75c']/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img").get_attribute('src')

            ## 이미지 얼굴 인식
            convert_img = url_to_image(img_url)
            
            ## 얼굴이 아니면 무시
            if not face_detect(convert_img):
                print(f"--------------{search} No Face--------------")
                continue
            
            else:
                ## 이미지 저장
                urllib.request.urlretrieve(img_url, f"{search}/" + str(cnt) + ".jpg")
                print(f"{search}--save image {cnt}")
                cnt += 1
                
                if cnt > 500:
                    break
        except Exception as e:
            print(e)
    
    driver.close()

'''
[한국 여성 영화, 
한국 여자, 
한국 여성, 
한국 여성 유튜버, 
한국 여성 인플루언서, 
한국 여성 틱톡커, 
한국 여자 메이크업,
한국 여성 인스타,
"한국 여성 쇼핑몰 모델",
"필라테스",
"레깅스",
"여자 머리",
"여고 단체사진"
]
'''
## "여성 의류" == ???
key_word = ["여성 의류", "여성 원피스"]

## print(multiprocessing.cpu_count())
## with Pool(processes=cpu_cnt) as pool:
##     pool.map(func, iterable)

def mp_pool(f, cpu_cnt, key_word):
    pool = Pool(processes=cpu_cnt)
    pool.map(f, key_word)

    
if __name__ == "__main__":
    s_time = time.time()
    pool = Pool(processes=8)
    pool.map(google_crawling, key_word)
    print("--- %s seconds ---" % (time.time() - s_time))


'''
## multiprocess
* map() - iterable에 대해 동일한 함수를 멀티프로세싱을 이용하여 처리하고자 할 때 사용한다. 단, 사용하고자 하는 함수는 단일 인자를 받아야 한다.
= map의 결과물은 list

* apply() - Pool에게 작업 하나를 시킨다. 그리고 작업이 끝날 때까지 기다렸다가 결과를 받는다.
= pool.apply(func, func인자값)

* starmap() - 인자를 두 개 이상 받을 수 있다
= pool.starmap(func, zip(func인자값, func인자값)= 둘다 iterable )

* imap() - 결과물의 길이가 길어서 list로 나타내었을 때 메모리에 부담이 가는 경우 imap을 사용해주면 좋다
= imap의 결과물은 iterator

----- iterator / iterable ----
iterator - for 문이 이터러블을 받으면 이터러블의 __iter__()를 호출
iterable - 반복가능한 객체(list, dict, tuple...)

iterable은 순회를 당할 수 있는 객체
iterator은 iterable의 순회를 주관


* 대용량 데이터 불러올때 사용 - chunksize 
'''