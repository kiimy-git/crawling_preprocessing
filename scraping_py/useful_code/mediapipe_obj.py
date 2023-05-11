import mediapipe as mp
import cv2
from io import BytesIO
from PIL import Image

# mp.solutions.mediapipe.python.solutions.drawing_utils == 자동완성됨

mp_draw = mp.solutions.drawing_utils
mp_obj = mp.solutions.objectron

# print(mp_obj)


with mp_obj.Objectron(static_image_mode=True,
                      max_num_objects =5,
                      min_detection_confidence=.5,
                      model_name='Shoe') as obj:
    img = cv2.imread("dd.jpg")
    
    res = obj.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    print(res)

    src = img.copy()

    for detected_object in res.detected_objects:
        mp_draw.draw_landmarks(src,
                               detected_object.landmarks_2d,
                               mp_obj.BOX_CONNECTIONS)

        mp_draw.draw_axis(src,
                          detected_object.rotation,
                          detected_object.translation)

        cv2.imshow("img", src)
        cv2.waitKey()
