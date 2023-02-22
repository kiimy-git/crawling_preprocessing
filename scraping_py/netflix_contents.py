from selenium.webdriver.common.by import By
import time


def netflix_contents_count(genre_driver, contents):
    """
        Args:
            genre_driver == driver,\n
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
        Retruns:
            해당 content 위치, content 더보기 개수, 드라마 개수
    """
    ## 드라마 content
    drama_content = genre_driver.find_elements(By.CSS_SELECTOR, '#main-view > div > div.aro-genre > div > div')
    time.sleep(2)
    for index, c in enumerate(drama_content):
        try:
            if contents in c.get_attribute("data-list-context"):
                ## pagination-indicator ==> active되었을때
                slider_list = c.find_element(By.CLASS_NAME, "pagination-indicator")
                slides = slider_list.find_elements(By.TAG_NAME, 'li')
                
                ## 해당 목록 총 드라마 개수, 4 == 한 슬라이드에 4개 드라마
                total_drama = len(slides) * 4
                
                return index+1, len(slides), total_drama
            
            else:
                continue
        except Exception as e:
            print(e)