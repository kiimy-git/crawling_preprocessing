from selenium.webdriver.common.by import By
import time


def genre_select(driver, genre):
    """
    ### genre = [한국 드라마, 미국 드라마, 영국 드라마,\n
                아시아 드라마, 전 세계 예능이 한곳에!, 애니,\n
                코미디, 로맨스, 드라마 장르, 액션,\n
                스릴러, SF & 판타지, 호러, 키즈, 청소년, 다큐시리즈\n
                ]
        Args:
            driver : login driver,\n
            genre (str): li[1]/a - 한드\n
                         li[2]/a - 미드\n
                         li[3]/a - 영드
        Retruns:
            genre_driver
    """
    
    ## 상단 bar에서 시리즈 선택
    driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div[1]/ul/li[3]/a').click()
    time.sleep(3)

    ## 장르 선택란 선택
    driver.find_element(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div').click()
    time.sleep(0.5)
    
    ## 장르 종류
    genre_type = driver.find_elements(By.CSS_SELECTOR, '#appMountPoint > div > div > div:nth-child(1) > div.bd.dark-background > div.pinning-header > div > div.sub-header > div > div > div > div.aro-genre-details > div.subgenres > div > div > div > div.sub-menu.theme-lakira > ul > li')
    print(len(genre_type))
        
        
    if genre == "한국드라마":
        genre = "li[1]/a"
        
    elif genre == "미국드라마":
        genre = "li[2]/a"
        
    elif genre == "영국드라마":
        genre = "li[3]/a"
    
    else:
        print("")
        
    ## 장르 선택
    driver.find_elements(By.XPATH, '//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[2]/ul[1]/li[1]/a')
    driver.find_element(By.XPATH, f'//*[@id="appMountPoint"]/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div[2]/div[1]/div/div/div/div[2]/ul[1]/{genre}').click()
    time.sleep(3)
    
    return driver