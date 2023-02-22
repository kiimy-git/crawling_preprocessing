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
from webdriver_manager.chrome import ChromeDriverManager
import time
from makedir import make_dir

## 디버깅
# C:\Program Files\Google\Chrome\Application
# Chrome 설치 폴더 이동 후 탐색기의 경로 부분에서 cmd 창을 열고 
# chrome.exe --remote-debugging-port=9222 --user-data-dir="C:/ChromeTEMP"
options = webdriver.ChromeOptions()
options.add_experimental_option('debuggerAddress', "127.0.0.1:9222")

## extentions 적용 => 안됨 why?? / => 새로 extentions 설치로 진행
# options.add_argument("--load-extension={}".format(r'C:\Users\yhunkim\AppData\Local\Google\Chrome\User Data\Default\Extensions\hoombieeljmmljlkjmnheibnpciblicm\5.0.0_0'))
# options.add_extension(r"hoombieeljmmljlkjmnheibnpciblicm.crx")
driver = webdriver.Chrome(r"chromedriver_win32 (1)\chromedriver.exe", options=options)
opener = urllib.request.build_opener()
opener.addheaders = [('User-Agent', 'Mozila/5.0')]
urllib.request.install_opener(opener)

## Netflex content(= genre, similars는 개수가 많음)
contents = ["popularTitles",
            "continueWatching",
            "trendingNow",
            "similars",
            "netflixOriginals", 
            "genre",
            "genre",
            "newThisWeek",
            "topTen",
            "hiddenGems"
]

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
time.sleep(4)

## 장르 선택
driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div').click()
time.sleep(4)


# 장르 종류
genre_type = driver.find_elements(By.CSS_SELECTOR, '#appMountPoint > div > div > div:nth-child(1) > div.bd.dark-background > div.pinning-header > div > div.sub-header > div > div > div > div.aro-genre-details > div.subgenres > div > div > div > div.sub-menu.theme-lakira > ul > li')
for g in genre_type:
    # print(g.text)
    pass


## 특정 장르 선택
driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[2]/ul[1]/li[2]/a').click()
time.sleep(3)

## 더보기란에 마우스 위치 이동 == webdriver.ActionChains

## 드라마 content
drama_content = driver.find_elements(By.CSS_SELECTOR, '#main-view > div > div.aro-genre > div > div')
time.sleep(2)

## drama_context ="오직 넷플리스에서" = netflixOriginals만 가져오기
for index, content in enumerate(drama_content):
    time.sleep(2)
    try:
        if "netflixOriginals" in content.get_attribute("data-list-context"):
            ## pagination-indicator ==> active되었을때
            slider_list = content.find_element(By.CLASS_NAME, "pagination-indicator")
            actives = slider_list.find_elements(By.TAG_NAME, 'li')
            
            ## 해당 목록 총 드라마 개수, 4 == 한 슬라이드에 4개 드라마
            total_drama = len(actives) * 4
            
            # ## 다음 버튼 클릭 row-{드라마 항목 번호}
            # driver.find_element(By.XPATH, '//*[@id="row-1"]/div/div/div/span').click()
            # time.sleep(1)

            ## drama 이름 및 폴더 생성(= netflix_translation5 숫자 변경)
            drama_name = driver.find_element(By.XPATH, '//*[@id="title-card-1-0"]/div[1]/a').text
            make_dir(r'C:\Users\yhunkim\Desktop\netflix_translation5\en-ko' + "\\" + drama_name)
            print(f"--------------{drama_name} 폴더 생성--------------")
            
            
            ## 드라마 에피소드 목록으로 들어가기({index+1} = 오리지널 / -0 = 작품 번호(=for문))
            driver.find_element(By.XPATH, f'//*[@id="title-card-{index+1}-0"]/div[1]/a/div[2]/div').click()
            
            time.sleep(3)
            
            ## 드라마 영상 클릭
            driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[1]/div[4]/div').click()
            # ----- 영상 로딩 -----
            time.sleep(10)
            
            ## 자막 아이콘(= 자막 설정시)
            ####--------- pass ---------####
            
            ## 모든 에피소드
            ep_cnt = 1 
            while True:
            
                ## 내보내기 아이콘 
                driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div[5]').click()
                time.sleep(3)

                ## Excel click 및 내보내기
                driver.find_element(By.XPATH, '//*[@id="lln-export-modal"]/div/div[3]/div[1]/div[1]/span[2]/div[2]').click()
                driver.find_element(By.XPATH, '//*[@id="llnExportModalExportBtn"]').click()
                
                ####------- Excel load -------####
                print("----내보내기 load----")
                time.sleep(5)
                
                ## 창이 닫혔다가 다시 뜸
                # - 영상 클릭(= 마우스 활성)
                next_icon = '//*[@id="appMountPoint"]/div/div/div[1]/div[8]/div[2]/div[2]/div[2]/div/div/div[3]/div/div[4]/div[2]/button'
                # driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[8]').click()
                # time.sleep(2)
                
                ## 마우스 위치 설정(= 다음 화 아이콘 있는 바 활성화(= .location))
                action = webdriver.ActionChains(driver=driver)
                action.move_by_offset(325, 610).perform()
                time.sleep(3)   
                
                if driver.find_element(By.XPATH, next_icon):
                    ep_cnt += 1
                    driver.find_element(By.XPATH, next_icon).click() 
                    time.sleep(10)    
                else:
                    break
                
            print(f"--------------총 에피소드 : {ep_cnt}개--------------" + "\n")
            
        else:
            continue

    except Exception as e:
        break

# ## 오리지널 part 더보기 개수
# elements = driver.find_elements(By.XPATH, '//*[@id="row-5"]/div/div/div/ul')
# print("더보기 개수: ", len(elements))
# time.sleep(1)


# ## 드라마 에피소드 개수(+ 더보기 버튼 클릭)
# if driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div[11]/button').is_displayed():
#     driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div[11]/button').click()
#     time.sleep(0.5)
#     episode = driver.find_elements(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div')
    
# ## 없으면 그냥 진행
# episode = driver.find_elements(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div')
# time.sleep(1)

# ## 첫 영상 클릭
# driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[1]/div[4]/div').click()

# # ---- 영상 및 자막 로딩 ----
# time.sleep(6)

# ## 에피소드
# episode_cnt = 0
# while episode_cnt <= len(episode):
    
#     ## 번역 언어 설정 
#     # ------------------------- pass -------------------------
#     # driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div[6]/svg').click()

#     # ## 번역 언어 클릭 및 언어 설정 Enter(기본 설정 영어??)
#     # languages = ["영어 [사람 번역]", "일본어 [사람 번역]", "중국어(간체)[사람 번역]"]
#     # //*[@id="lln-options-modal"]/div/div[3]/div/div[2]/div[9]/label/span[2]/span[1]
    
#     ## 스크립트
#     driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div[5]').click()
#     ## Excel선택 및 내보내기
#     driver.find_element(By.XPATH, '//*[@id="lln-export-modal"]/div/div[3]/div[1]/div[1]/span[2]/div[2]').click()
#     driver.find_element(By.XPATH, '//*[@id="llnExportModalExportBtn"]').click()

#     # ---- 다운 로딩 ----
#     time.sleep(10)
    
#     ## 다음화 클릭 / 없다면 종료
#     next_episode = driver.find_element(By.XPATH, '/div/div[2]/div/div/div[3]/div/div[4]/div[2]/button')
#     if next_episode.is_displayed():
#         ## 더보기 클릭
#         driver.find_element(By.XPATH, '//*[@id="row-7"]/div/div/div/span[2]').click()
#         time.sleep(10)
#         episode_cnt += 1
    
#     else:
#         break
    

'''
## 해당 항목에 있는 드라마 6 - 10 range(6, 11)
drama_cnt = 0
while drama_cnt <= len(elements):
    for i in range(6, 11):
        ## 영상 클릭
        driver.find_element(By.XPATH, f'//*[@id="row-7"]/div/div/div/div/div/div[{i}]').click()
        time.sleep(1)
        
        ## 드라마 에피소드 개수(+ 더보기 버튼 클릭)
        if driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div[11]/button').is_displayed():
            driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div[11]/button').click()
            time.sleep(0.5)
            episode = driver.find_elements(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div')
            
        episode = driver.find_elements(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/div')
        time.sleep(1)

        ## 첫 영상 클릭
        driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[2]/div/div[1]/div[4]/div').click()
        
        # ---- 영상 및 자막 로딩 ----
        time.sleep(6)
        
        ## 에피소드
        episode_cnt = 0
        while episode_cnt <= len(episode):
            
            ## 번역 언어 설정 
            # ------------------------- pass -------------------------
            # driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div[6]/svg').click()

            # ## 번역 언어 클릭 및 언어 설정 Enter(기본 설정 영어??)
            # languages = ["영어 [사람 번역]", "일본어 [사람 번역]", "중국어(간체)[사람 번역]"]
            # //*[@id="lln-options-modal"]/div/div[3]/div/div[2]/div[9]/label/span[2]/span[1]
            
            ## 스크립트
            driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div[5]').click()
            ## Excel선택 및 내보내기
            driver.find_element(By.XPATH, '//*[@id="lln-export-modal"]/div/div[3]/div[1]/div[1]/span[2]/div[2]').click()
            driver.find_element(By.XPATH, '//*[@id="llnExportModalExportBtn"]').click()

            # ---- 다운 로딩 ----
            time.sleep(10)
            
            ## 다음화 클릭 / 없다면 종료
            next_episode = driver.find_element(By.XPATH, '/div/div[2]/div/div/div[3]/div/div[4]/div[2]/button')
            if next_episode.is_displayed():
                ## 더보기 클릭
                driver.find_element(By.XPATH, '//*[@id="row-7"]/div/div/div/span[2]').click()
                time.sleep(10)
                episode_cnt += 1
            
            else:
                break
                
        ## 다시 원래 페이지로 돌아와야함 // 우선 하나만
        ----------------------------------------------------------------------------
        
        ## 다음 드라마 리스트
        driver.find_element(By.XPATH, '//*[@id="row-5"]/div/div/div/span')
        drama_cnt += 1
'''
