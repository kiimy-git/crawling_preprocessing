'''
## search 아이콘 click
//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div/div/div[1]/div/button/svg

## searchbox text 입력
element = driver.find_element("input#searchboxinput")
element.send_keys(f"{drama_name}")

----------로딩 짧게----------
## Text입력 후 따로 button 누를 필요없음
----------로딩 짧게----------

## 첫번째 그림 click(= 찾는 드라마)
//*[@id="title-card-0-0"]/div[1]/a/div[1]/img

----------로딩 짧음----------
##################################################################
## <if 더보기 버튼 있으면 // 없을 수도 있음>
//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div[11]/button

## <에피소드 개수 찾기>
#appMountPoint > div > div > div:nth-child(1) > div.focus-trap-wrapper.previewModal--wrapper.detail-modal.has-smaller-buttons > div > div.previewModal--info > div > div:nth-child(2) > div > div > div.episodeSelector-container > div
##################################################################

## 영상 재생 click
//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[1]/div[4]/div

----------로딩----------
cnt = 0
while True:

    ## 여기서 class 세 가지 = for문
        ## 영상 설정 아이콘 click
        //*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div[6]/svg/path

        ## 번역 설정 title="영어 [사람 번역]"
        # title class = ["영어 [사람 번역]", "일본어 [사람 번역]", "중국어(간체) [사람 번역]"]
        //*[@id="select2-destLanguage-container"]

        ## 닫기 click
        //*[@id="lln-options-modal"]/div/div[4]/div

        ----------로딩----------

        ## 내보내기 아이콘 click
        //*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div[5]/svg

        ## Excel click
        //*[@id="lln-export-modal"]/div/div[3]/div[1]/div[1]/span[2]/div[2]

        ## 내보내기 click
        //*[@id="llnExportModalExportBtn"]

        ----------다운로드 로딩----------

    cnt += 1
    ## if 다음화 아이콘 있으면 click:
        //*[@id="appMountPoint"]/div/div/div[1]/div[8]/div[2]/div[2]/div[3]/div/div/div[3]/div/div[4]/div[2]/button/div/svg
    
    ## else:
        break
    ----------로딩----------
    

'''

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

# ## 자동 로그인
# driver.find_element(By.NAME, 'userLoginId').send_keys("smilegate_ai@smilegate.com")
# driver.find_element(By.NAME, 'password').send_keys("!SmilegateAI83#")
# driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button').click() # 로그인 클릭
# time.sleep(3)

# ## 프로필 선택
# driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[2]/div/a/div/div').click()
# time.sleep(5)

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


