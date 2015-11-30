import cv2
import math
import numpy as np
from os import path

cascades_dir = path.normpath(path.join(cv2.__file__, '..', '..', '..', '..', 'share', 'OpenCV', 'haarcascades'))

def detect(img):
    cascade_f = cv2.CascadeClassifier(path.join(cascades_dir, 'haarcascade_frontalface_alt2.xml'))
    cascade_e = cv2.CascadeClassifier(path.join(cascades_dir, 'haarcascade_eye.xml'))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rows, cols, _ = img.shape
    print rows, cols
    hypot = int(math.ceil(math.hypot(rows, cols)))
    frame = np.zeros((hypot, hypot), np.uint8)
    frame[(hypot - rows) / 2:(hypot + rows) / 2, (hypot - cols) / 2:(hypot + cols) / 2] = gray
    results = {}
    for deg in range(-42, 43, 6):
        M = cv2.getRotationMatrix2D((hypot / 2, hypot / 2), deg, 1.0)
        rotated = cv2.warpAffine(frame, M, (hypot, hypot))
        faces = cascade_f.detectMultiScale(rotated)
        print '%s: %s face' % (deg, len(faces))
        for face in faces:
            x, y, w, h = face
            roi = rotated[y : y + h, x : x + w]
            eyes = map(lambda e: e.tolist(), cascade_e.detectMultiScale(roi))
            eyes = filter(lambda e: (e[0] > w / 2 or e[0] + e[2] < w / 2) and e[1] + e[3] < h / 2, eyes)
            if len(eyes) == 2:
                print '2 eyes detected'
                if results.get(deg) is None:
                    results[deg] = []
                results[deg].append({
                    'face': face.tolist(),
                    'eyes': eyes,
                })
    import pprint
    pprint.pprint(results)
    frame = np.zeros((hypot, hypot, 3), np.uint8)
    frame[(hypot - rows) / 2:(hypot + rows) / 2, (hypot - cols) / 2:(hypot + cols) / 2] = img
    for deg in results.keys():
        M = cv2.getRotationMatrix2D((hypot / 2, hypot / 2), deg, 1.0)
        frame = cv2.warpAffine(frame, M, (hypot, hypot))
        for result in results[deg]:
            x, y, w, h = result['face']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
        M = cv2.getRotationMatrix2D((hypot / 2, hypot / 2), -deg, 1.0)
        frame = cv2.warpAffine(frame, M, (hypot, hypot))
    return frame[(hypot - rows) / 2:(hypot + rows) / 2, (hypot - cols) / 2:(hypot + cols) / 2]
