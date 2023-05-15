import cv2 as cv

def aspect_ratio(image):
    img = cv.imread(image)

    ## 이미지의 종힁비가 일치하지않아, 늘어나 보임
    # min_dim = min(img.shape[0], img.shape[1])
    # dim = (min_dim, min_dim)

    # resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)

    # 이미지 크기
    height, width, _ = img.shape

    ## 가로 or 세로 값중 하나를 특정 값으로 고정
    max_width = 500
    width = img.shape[1]
    height = img.shape[0]
    
    ## 고정 값과 현재 이미지 사이즈와 비교
    if width > max_width:
        scale = max_width / width
        width = int(width * scale)
        height = int(height * scale)

    resized = cv.resize(img, (width, height), interpolation=cv.INTER_AREA)
    print(resized.shape)
    cv.imshow("resized", resized)
    cv.waitKey()
    
