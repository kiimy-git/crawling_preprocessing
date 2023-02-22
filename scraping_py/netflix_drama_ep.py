from selenium.webdriver.common.by import By
import time
from netflix_contents import netflix_contents_count


# index, slide_cnt, total_drama = netflix_contents_count(genre_driver, contents)
# for video in total_drama:

# ## slider 다음 버튼 클릭 row-{드라마 항목 번호}
# driver.find_element(By.XPATH, '//*[@id="row-1"]/div/div/div/span').click()
# time.sleep(1)

def drama_episodes(driver, content_index, video_num):
    """
    #### //*[@id="title-card-{content_index}-{video_num}"]/div[1]/a/div[2]/div
        Args:
            driver = driver,\n
            content_index = content 위치,\n
            video_num = 해당 위치의 작품 번호
            
            
        Retruns:
            
    """
    ## drama 이름
    drama_name = driver.find_element(By.XPATH, f'//*[@id="title-card-{content_index}-{video_num}"]/div[1]/a').text
    print(f"------------------{drama_name}------------------")
    
    ## 드라마 에피소드 목록으로 들어가기
    driver.find_element(By.XPATH, f'//*[@id="title-card-{content_index}-{video_num}"]/div[1]/a/div[2]/div').click()
    time.sleep(4)
    # //*[@id="title-card-4-1"]/div[1]/a/div[2]/div
    # //*[@id="title-card-4-23"]/div[1]/a/div[2]/div