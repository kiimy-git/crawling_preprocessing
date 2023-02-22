import urllib.request
from time_check import check_time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def netflix_login(chromedriver_path, debug_address):
    """
    1. 작업 폴더에 chromedriver 설치
    2. Chrome 설치 폴더 이동 후 탐색기의 경로 부분에서 cmd 창을 열고 
    3. chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"\n
    #### <참조>
    extentions 적용안됨 => 열린 Chrome 웹에서 extentions 따로 설치 진행

        Args:
            chromedriver_path : r"크롬 파일 경로"
            debug_address (str): 127.0.0.1:{9222}
        Retruns:
            driver
    """
    ## 디버깅
    # chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('debuggerAddress', f"127.0.0.1:{debug_address}")

    
    # options.add_argument("--load-extension={}".format(r'C:\Users\yhunkim\AppData\Local\Google\Chrome\User Data\Default\Extensions\hoombieeljmmljlkjmnheibnpciblicm\5.0.0_0'))
    # options.add_extension(r"hoombieeljmmljlkjmnheibnpciblicm.crx")
    driver = webdriver.Chrome(chromedriver_path, options=options)
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozila/5.0')]
    urllib.request.install_opener(opener)
    
    ## Netflix 링크
    driver.get("https://www.netflix.com/browse")

    ## 자동 로그인
    driver.find_element(By.NAME, 'userLoginId').send_keys("smilegate_ai@smilegate.com")
    driver.find_element(By.NAME, 'password').send_keys("!SmilegateAI83#")
    driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div[3]/div/div/div[1]/form/button').click() # 로그인 클릭
    time.sleep(3)
    
    ## 프로필 선택
    driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[2]/div/a/div/div').click()
    time.sleep(10)
    
    return driver

# netflix_login(r"chromedriver_win32 (1)\chromedriver.exe", 9222)