import os
import urllib3
import urllib.request
from time_check import check_time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


## 디버깅

options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('debuggerAddress', "127.0.0.1:9222")
# options.add_argument("--disable-gpu")
driver = webdriver.Chrome("C:\\Users\\yhunkim\\Desktop\\capture\\chromedriver", options=options)

opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozila/5.0')]
urllib.request.install_opener(opener)

def drama_script(drama_name):
    """
    # 주석
    drama_script 함수
        Args:
            get_path (str): a value
            drama (str): c value
        Retruns:
            None
    """

## Netflix 링크
driver.get("https://www.netflix.com/browse")

## 자동 로그인
driver.find_element(By.NAME, 'userLoginId').send_keys("smilegate_ai@smilegate.com")
driver.find_element(By.NAME, 'password').send_keys("!SmilegateAI83#")
driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button').click() # 로그인 클릭
time.sleep(3)

## 프로필 선택
driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[2]/div/a/div/div').click()
time.sleep(5)

## 시리즈 선택
driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div[1]/ul/li[3]/a').click()
time.sleep(3)

## 장르 선택(한국드라마, 미국 or 영국드라마)
# li[1]/a - 한드
# li[2]/a - 미드
# li[3]/a - 영드
driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div').click()
driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[2]/ul[1]/li[1]/a').click()
time.sleep(3)

## 더보기란에 마우스 위치 이동 == webdriver.ActionChains

## 오리지널 part 더보기 개수
elements = driver.find_elements(By.XPATH, '//*[@id="row-7"]/div/div/div/ul')

## 6 - 10 range(6, 11)
cnt = 0
while cnt < len(elements):
    for i in range(6, 11):
        ## 영상 클릭
        driver.find_element(By.XPATH, f'//*[@id="row-7"]/div/div/div/div/div/div[{i}]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[1]/div[4]/div').click()
        ## 스크립트 내보내기
        # ...
        break
        
    ## 더보기 클릭
    driver.find_element(By.XPATH, '//*[@id="row-7"]/div/div/div/span[2]').click()
    cnt += 1
    
    

## 돋보기 아이콘 클릭
# element = driver.find_element(By.CLASS_NAME, "searchBox")
# element.send_keys("비밀의 숲")
# time.sleep(1)

## 검색
# element = driver.find_element(By.CLASS_NAME, 'searchInput')
# element.send_keys(Keys.RETURN)
# element.send_keys(Keys.RETURN)

# ## 첫번째 나오는 영상 클릭
# driver.find_element(By.XPATH, '//*[@id="title-card-0-0"]/div[1]/a/div[1]/img').click()


