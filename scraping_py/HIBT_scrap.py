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
import re
import time
from makedir import make_dir
from mediapipe_face import url_to_image
import ssl
from multiprocessing import Pool

'''
LAION-5B
이미지와 텍스트 쌍을 작성함에 있어서, LAION은 인터넷 상의 데이터를 제공하는 비영리단체 ‘Common Crawl(커먼 크롤)’의 파일을 해석하고, 
텍스트와 이미지 쌍을 선택하고 CLIP를 이용해 유사성이 높은 이미지와 텍스트 쌍을 추출했다. 더 짧은 텍스트, 해상도가 너무 큰 이미지, 중복 데이터, 
불법 콘텐츠 등을 가능한 한 삭제해 최종적으로 58억5000만 개의 이미지와 텍스트 쌍으로 구성된 샘플이 남았다고 한다.

출처 : 테크튜브(http://www.techtube.co.kr)
'''

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ssl._create_default_https_context = ssl._create_unverified_context

## 페이지 스크롤
def scrolling(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        new_height = driver.execute_script("return document.body.scrollHeight") 
        
        if new_height == last_height:
            break
            
        last_height = new_height

## 종료
def exit_code():
    import sys
    sys.exit()

## 이미지 업로드이기 때문에 input = 파일 경로
def HIBT_scrap(img_path):

    name = img_path.split("\\")[-1].split(".")[0]
    
    ## scraping폴더 생성 및 작업 폴더 변경
    make_dir("HIBT_scraping")
    os.chdir("HIBT_scraping")
    
    ## 작업경로에 폴더 생성
    make_dir(name)
    
    ## handshake failed error 로그 노출 X => add_experimental_option
    ## Passthrough is not supported, GL is disabled, ANGLE is => --headless and --disable-gpu
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome("C:\\Users\\yhunkim\\Desktop\\capture\\chromedriver", options=options)

    ## 이미지 검색 링크
    driver.get("https://haveibeentrained.com/")

    ## 찾을 이미지 첨부 = input[type=file]
    element = driver.find_element(By.CSS_SELECTOR, "input[type=file]")
    element.send_keys(img_path)

    ## 데이터 불러오는 로딩이 길 수 있음
    time.sleep(10) # == 무조건 10초 기다림


    ## Crawling
    img_cnt = 0
    index = 0
    try:
        
        while True:
            ## 페이지 계속 업데이트
            # condition = elements_length_changes(locator=locator, length=img_cnt)
            # WebDriverWait(driver, 20).until(condition)
            locator = (By.XPATH, "//*[@id='root']/div/main/div/div[3]/div/img")
            images = driver.find_elements(*locator) # *args는 파라미터를 몇개를 받을지 모르는 경우 사용하고 튜플 형태로 전달

            ## 업데이트가 빠를 수 있음 = 중간에 텀 부여
            time.sleep(0.5)
            img_cnt = len(images)
            
            print(img_cnt, index)
            
            ## 업데이트 개수와 index가 같으면 종료
            if img_cnt == index:
                break

            try:
                while index < img_cnt:
                    images[index].click()
                    img_url = driver.find_element(By.XPATH, 
                                            "//*[@id='root']/div/div[1]/div/div/img").get_attribute('src')
                    ## HTTP Error 403: Forbidden
                    # = 크롬 부라우저에서 요청한 것으로 인식하게 만들어 크롤링한다는 사실을 숨김
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-Agent', 'Mozila/5.0')]
                    urllib.request.install_opener(opener)
                    
                    ## 이미지 저장
                    urllib.request.urlretrieve(img_url, f"{name}/" + str(index+1) + ".jpg")
                    print(f"{name}--save image {index+1}")
                    index += 1
  
                ## 스크롤 함수 = HIBT 페이지는 자동으로 업데이트
                # scrolling(driver=driver)
                
                ## 페이지 업데이트 될때마다 바로 실행
                driver.implicitly_wait(30)


            ## element click intercepted: Element => driver.execute_script("arguments[0].click();", images[index]) / 이유 알 수 없음
            except Exception as e:
                print(e)
                try:
                    while index < img_cnt:
                        ## Message: stale element reference: element is not attached to the page document
                        # =  웹페이지가 너무 빨리 넘어가면 error 발생
                        
                        ## 이미지를 클릭할 수 없을때
                        img_url = driver.find_element(By.XPATH, 
                                                "//*[@id='root']/div/div[1]/div/div/img").get_attribute('src')
                        driver.execute_script("arguments[0].click();", images[index])

                        ## HTTP Error 403: Forbidden
                        # = 크롬 부라우저에서 요청한 것으로 인식하게 만들어 크롤링한다는 사실을 숨김
                        opener = urllib.request.build_opener()
                        opener.addheaders = [('User-Agent', 'Mozila/5.0')]
                        urllib.request.install_opener(opener)
                        
                        ## 이미지 저장
                        urllib.request.urlretrieve(img_url, f"{name}/" + str(index+1) + ".jpg")
                        print(f"{name}--save image {index+1}")
                        index += 1
                        
                    driver.implicitly_wait(30)
                
                ## 사이트 자체에서 클릭을 막았을 때는 제외
                except Exception as e:
                    print(e)
                    index+=1
                    driver.implicitly_wait(30)
    finally:
        driver.quit()
    
        # ## 마지막 이미지까지 다 보고 난 후 결과 더 보기 
        # ## search for more click
        # if c == len(images):
        #     button = driver.find_element(By.CSS_SELECTOR, "button")
        #     button.click()



if __name__ == "__main__":
    
    ## 작업 폴더
    file_list = os.listdir("작업 폴더")

    ## abspath = 현재 작업 디렉토리에 상대적인 절대 경로
    '''
    f = os.listdir("작업 폴더")
    print([os.path.abspath(i) for i in f]) = C:\\Users\\yhunkim\\Desktop\\capture\\detail.jpeg
    os.chdir("작업 폴더")
    print([os.path.abspath(i) for i in f]) = C:\\Users\\yhunkim\\Desktop\\capture\\hibt_img\\detail.jpeg
    '''
    os.chdir("작업 폴더")
    abs_file = [os.path.abspath(f) for f in file_list] # \ => \\

    ## 상위 폴더 이동
    os.chdir("..")
    
    s_time = time.time()
    cpu_cnt = os.cpu_count() ## 최대 12개
    pool = Pool(processes=cpu_cnt) 
    pool.map(HIBT_scrap, abs_file)
    print("--- %s seconds ---" % (time.time() - s_time))

'''
1. hibt에 적용할 폴더 생성 및 관련 이미지 첨부
2. run
'''
