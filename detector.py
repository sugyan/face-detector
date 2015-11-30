import cv2
import random
from os import path

cascades_dir = path.normpath(path.join(cv2.__file__, '..', '..', '..', '..', 'share', 'OpenCV', 'haarcascades'))

def detect(img):
    cascade = cv2.CascadeClassifier(path.join(cascades_dir, 'haarcascade_frontalface_alt2.xml'))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, cols, _ = img.shape
    degrees = [x for x in range(-40, 40, 5) if x != 0]
    random.shuffle(degrees)
    degrees.insert(0, 0)
    for deg in degrees:
        M = cv2.getRotationMatrix2D((cols/2, rows/2), deg ,1)
        rotated = cv2.warpAffine(gray, M, (cols, rows))
        rects = cascade.detectMultiScale(rotated)
        if len(rects) > 0:
            print deg, rects
            rects[:,2:] += rects[:,:2]
            for rect in rects:
                x1, y1, x2, y2 = rect
                cv2.rectangle(rotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            return rotated
    return img
