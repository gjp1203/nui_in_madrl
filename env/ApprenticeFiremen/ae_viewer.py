import cv2
import os.path

#file = 'outfile.jpg'
file = 'ae.jpg'

while (True):
    image = cv2.imread(file)
    try:
        height, width = image.shape[:2]
        if height > 0:
            cv2.imshow('image', image)
            k = cv2.waitKey(50)
            if k == 27:         # If escape was pressed exit
                cv2.destroyAllWindows()
                break
    except AttributeError:
        pass






