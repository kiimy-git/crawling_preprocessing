import urllib.request
from time_check import check_time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# DeprecationWarning: executable_path has been deprecated, please pass in a Service object
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from makedir import make_dir
from tqdm import tqdm
from multiprocessing import Pool
import os

def request_netflix(first_video_path):
    options = webdriver.ChromeOptions()
    # prefs = {'download.default_directory' : r'C:\Users\yhunkim\Desktop\netflix_translation6\ko-en\나홀로그대'}
    # options.add_experimental_option('prefs', prefs)
    
    ## GPU 가속 활성
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--no-sandbox')
    
    options.add_experimental_option('debuggerAddress', "127.0.0.1:9223")
    ## extentions 적용 => 안됨 why?? / => 새로 extentions 설치로 진행
    # options.add_argument("--load-extension={}".format(r'C:\Users\yhunkim\AppData\Local\Google\Chrome\User Data\Default\Extensions\hoombieeljmmljlkjmnheibnpciblicm\5.0.0_0'))
    # options.add_extension(r"hoombieeljmmljlkjmnheibnpciblicm.crx")
    driver = webdriver.Chrome(executable_path= r"C:\Users\yhunkim\Desktop\capture\chromedriver_win32 (1)\chromedriver.exe", options=options)

    # service = selenium 드라이버를 chrome버전에 맞춰 다운로드하고 경로를 찾을 필요 없어
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) 
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozila/5.0')]
    urllib.request.install_opener(opener)

    ## 드라마
    driver.get(first_video_path)
    time.sleep(10)
    
    return driver

def skip_next_btn(driver):
    ## ---------------- btn Xpath가 다를 수 있음 ---------------- ##
    ## -- skip_btn(애니 / 영화,드라마 == 그때그때 다름) -- ##
    # '//*[@id="appMountPoint"]/div/div/div[1]/div[8]/div[2]/div[3]/div[2]/button'
    # '//*[@id="appMountPoint"]/div/div/div[1]/div[8]/div[2]/div[2]/div[2]/button'

    skip_btn = '//*[@id="appMountPoint"]/div/div/div[1]/div[8]/div[2]/div[2]/div[2]/button'
    next_btn = '//*[@id="appMountPoint"]/div/div/div[1]/div[8]/div[2]/div[2]/div[2]/div/div/div[3]/div/div[3]/div[2]/button'

    ### -- next_btn -- ##
    ## 일어
    # '//*[@id="appMountPoint"]/div/div/div[1]/div[8]/div[2]/div[3]/div[2]/div/div/div[3]/div/div[3]/div[2]/button'
    ## 한국어, 영어, 중국어
    # '//*[@id="appMountPoint"]/div/div/div[1]/div[8]/div[2]/div[2]/div[2]/div/div/div[3]/div/div[3]/div[2]/button'

    try:
        ## opening skip ##
        driver.find_element(By.XPATH, skip_btn).click()
        time.sleep(2)

        ## next btn ##
        next_icon = driver.find_element(By.XPATH, next_btn)
        next_icon.click()
        time.sleep(10)
    
    ## skip btn이 없으면 다음화 클릭해서 진행
    except:
        next_icon = driver.find_element(By.XPATH, next_btn)
        next_icon.click()
        time.sleep(10)

def next_episode(driver):
    
    ## 다운로드 후 창이 한번 닫혔다가 다시 나옴(= 이 부분이 에러 요소임)
    current_url = driver.current_url
    driver.get(current_url)
    time.sleep(7)
    
    act_bar = '//*[@id="appMountPoint"]/div/div/div[1]/div[8]/div[2]/div'

    ## 무한 로딩시(=다음화 클릭시) 현재 창 다시 가져와서 클릭 버튼
    try:
        
        ## 마우스 위치 설정(= 다음 화 아이콘 있는 바 활성화(= .location))
        action = webdriver.ActionChains(driver=driver)
        position = driver.find_element(By.XPATH, act_bar)
        action.move_to_element(position).perform()
        time.sleep(2)

        ## opening skip 및 다음화 클릭 ##
        skip_next_btn(driver=driver)
        
    except:
        print("-----------------새로고침-----------------")
        ## 새로고침
        current_url = driver.current_url
        driver.get(current_url)
        time.sleep(5)
        
        ## 마우스 위치 설정(= 다음 화 아이콘 있는 바 활성화(= .location))
        action = webdriver.ActionChains(driver=driver)
        position = driver.find_element(By.XPATH, act_bar)
        action.move_to_element(position).perform()
        time.sleep(2)
        
        ## opening skip ##
        skip_next_btn(driver=driver)


## 자막 언어 고정(= 번역언어만 변경)
def trans_lang(first_video_path, total_episode):
    
    ## Netflix
    driver = request_netflix(first_video_path)

    ## 총 에피소드
    # while ep_cnt < total_episode:
    with tqdm(total = total_episode) as process:
        ep_cnt = 0
        while ep_cnt < total_episode:
            ep_cnt += 1
            
            ## 내보내기 아이콘 
            driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div[5]').click()
            time.sleep(3)

            ## Excel click 및 내보내기
            driver.find_element(By.XPATH, '//*[@id="lln-export-modal"]/div/div[3]/div[1]/div[1]/span[2]/div[2]').click()
            driver.find_element(By.XPATH, '//*[@id="llnExportModalExportBtn"]').click()
            time.sleep(8) # == 어디에 위치하느냐에 따라 error가 남
            
            ####------- Excel load -------####
            print(f"----진행 에피소드 {ep_cnt} loading----")
            process.update(1)
            
            ## 다음화 클릭
            next_episode(driver)
            
        print("----------------- 추출 종료 -----------------")


## <<자막 언어는 원어로 고정되있음>> ##
## 자막 언어 한국어로 변경(= 번역 언어만 변경)
def change_cc(first_video_path, total_episode):
    
    ## Netflix
    driver = request_netflix(first_video_path)

    ## 총 에피소드
    # while ep_cnt < total_episode:
    with tqdm(total = total_episode) as process:
        ep_cnt = 0
        while ep_cnt < total_episode:
            ep_cnt += 1
            
            ## 언어 설정 아이콘
            driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div[6]').click()
            time.sleep(2)
            
            ## 언어 설정(= 원어가 한국어인 경우, [영어,일어,중국어])
            driver.find_element(By.XPATH, '//*[@id="select2-lln-NSL-dropdown-container"]').click()
            time.sleep(2)
            
            langs = driver.find_elements(By.TAG_NAME, 'li')
            
            for lang in langs:
                ## -----------lang 변경----------- ##
                # print(lang.text)

                # "중국어(간체)", "중국어(간체) [CC]"
                # "중국어(번체)", "중국어(번체) [CC]"
                ## [CC]없는게 첫번째로 나옴
                if lang.text == "중국어(간체)":
                    lang.click()
                    time.sleep(4)
                    break
                
                ## 없으면 [CC]
                else:
                    if lang.text == "중국어(간체) [CC]":
                        lang.click()
                        time.sleep(6)
                        break

            ## 닫기 버튼
            driver.find_element(By.XPATH, '//*[@id="lln-options-modal"]/div/div[4]/div').click()
            time.sleep(4)
        
            ## 내보내기 아이콘 
            driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div[5]').click()
            time.sleep(3)

            ## Excel click 및 내보내기
            driver.find_element(By.XPATH, '//*[@id="lln-export-modal"]/div/div[3]/div[1]/div[1]/span[2]/div[2]').click()
            driver.find_element(By.XPATH, '//*[@id="llnExportModalExportBtn"]').click()
            time.sleep(8) # == 어디에 위치하느냐에 따라 error가 남
            
            ####------- Excel load -------####
            print(f"----진행 에피소드 {ep_cnt} loading----")
            process.update(1)
            
            ## 다음화 클릭
            next_episode(driver)
                    
        print("----------------- 추출 종료 -----------------")

## en-ko / ko-en / ja-ko
# trans_lang(r"https://www.netflix.com/watch/81237945?trackId=255824129",10)

# ko-ja / ko-zh / zh-ko = 자막 언어 변경 후 적용
change_cc(r"https://www.netflix.com/watch/81004129?trackId=200257858",15)


## 도중에 멈췄을때/해당 영상 스크립트 다운받아졌으면
# 1. 다음 영상 path 설정
# 2. cp_ent = load된 파일 번호
# 3. 다운로드 파일 이동(= 구현 X)
# -------- 다 추출하고 cp_ent = 0으로 초기화 --------
# -------- 영어,일어,중국어(간체)의 경우 처음에 설정 바궈서 진행 --------
# ----- 일본어 / 영어,중국어 다음 버튼 위치가 다름(= Xpath, 숫자 변경)
