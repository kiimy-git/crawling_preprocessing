# Crawling

### GFPGAN - 얼굴 인식 및 SR 사용
1. 주름, 눈동자에 비친 빛, 점 없앰
2. 잘안보이는 경우 이미지 생성시 외국인처럼 나옴(= 학습 데이터가 주로 외국인??)
3. 코가 커짐, 손이 통통해짐(손은 제대로 생성 못함)
4. 눈을 감고 있는 이미지에서 눈을 억지로 생성할려고함
5. 치아 배열, 크기 자연스럽지 않음
6. 한 이미지에 여러명 있을 수 있음(남자, 여자 얼굴 다 인식)
  - 개개인의 얼굴 이미지 가져옴


### Google Crawling
1. 특정 키워드(= 키워드를 명확하게 전달)를 통해 이미지를 가져올 수 있음(가수 ???, 배우 ???)
2. 중복 이미지 확인 불가
3. Mediapipe API(Face Detection)를 사용, 그림 이미지도 가져올 수 있음


### HIBT Crawling
1. Text or Image와 유사한 이미지들 검색(= 중복 제외, 간혹 있음)
2. 개수가 많지 않음
3. NSFW(=Not safe for work, 후방주의?) filter를 사용했다지만 불법 컨텐츠 이미지도 가져올 수 있음(= 일반인 이미지 적용 X)
4. 이미지로 찾을 경우 비슷한 느낌의 이미지도 추가로 가져옴(= 다른 사람의 이미지도 가져옴)

### gender_detect
1. 한국인의 얼굴 데이터셋으로 학습하지 않음
2. 결과적으로 제대로 구분하지 못 함

### Iruda Chat
1. [Iruda_Chat](https://nutty.chat/login)
2. [ChatGPT_Iruda_Chat_Code](scraping_py/iruda_chat.py)

[Web_Crawling 코드](scraping_py/netflix)

[사용한 라이브러리 및 API](scraping_py/useful_code)


# Data Preprocessing / Automation
[이미지_전처리](scraping_py/image_preprocess)

[텍스트_전처리](scraping_py/data_preprocess)

[엑셀화](scraping_py/make_excel)
