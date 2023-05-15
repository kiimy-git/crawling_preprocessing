import os
import cv2
from skimage.metrics import structural_similarity as ssim

def compare_image(path):
    
    img_file = os.listdir(path)

    ## 경로가 한글이면 안 읽힘
    # image = np.asarray(bytearray(file_path), dtype='uint8')
    # image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    img1 = cv2.imread(path + "\\" + img_file[0])
    img2 = cv2.imread(path + "\\" + img_file[1])

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    print(gray1.shape, gray2.shape)

    ## same shape dimensions
    (score, diff) = ssim(gray1, gray2, full=True)
    diff = (diff * 255).astype("uint8")
    print(score, diff)

    cv2.imshow("img1", gray1)
    cv2.imshow("img2", gray2)
    cv2.waitKey()

# compare_image(r'path')
