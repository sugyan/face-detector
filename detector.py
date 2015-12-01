import cv2
import math
import numpy as np
from os import path

cascades_dir = path.normpath(path.join(cv2.__file__, '..', '..', '..', '..', 'share', 'OpenCV', 'haarcascades'))

def detect(img):
    cascade_f = cv2.CascadeClassifier(path.join(cascades_dir, 'haarcascade_frontalface_alt2.xml'))
    cascade_e = cv2.CascadeClassifier(path.join(cascades_dir, 'haarcascade_eye.xml'))
    # resize if learch image
    rows, cols, _ = img.shape
    if max(rows, cols) > 512:
        l = max(rows, cols)
        img = cv2.resize(img, (cols * 512 / l, rows * 512 / l))
    rows, cols, _ = img.shape
    # create gray image for rotate
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hypot = int(math.ceil(math.hypot(rows, cols)))
    frame = np.zeros((hypot, hypot), np.uint8)
    frame[(hypot - rows) / 2.0:(hypot + rows) / 2.0, (hypot - cols) / 2.0:(hypot + cols) / 2.0] = gray

    def translate(coord, deg):
        x, y = coord
        rad = math.radians(deg)
        return {
            'x': (  math.cos(rad) * x + math.sin(rad) * y - hypot / 2.0 * math.cos(rad) - hypot / 2.0 * math.sin(rad) + hypot / 2.0 - (hypot - cols) / 2.0) / float(cols) * 100.0,
            'y': (- math.sin(rad) * x + math.cos(rad) * y + hypot / 2.0 * math.sin(rad) - hypot / 2.0 * math.cos(rad) + hypot / 2.0 - (hypot - rows) / 2.0) / float(rows) * 100.0,
        }
    # rotate and detect faces
    results = []
    for deg in range(-50, 51, 5):
        M = cv2.getRotationMatrix2D((hypot / 2.0, hypot / 2.0), deg, 1.0)
        rotated = cv2.warpAffine(frame, M, (hypot, hypot))
        faces = cascade_f.detectMultiScale(rotated)
        for face in faces:
            x, y, w, h = face
            # eyes in face?
            roi = rotated[y : y + h, x : x + w]
            eyes = cascade_e.detectMultiScale(roi, 1.1, 3)
            eyes = filter(lambda e: (e[0] > w / 2 or e[0] + e[2] < w / 2) and e[1] + e[3] < h / 2, eyes)
            if len(eyes) == 2 and abs(eyes[0][0] - eyes[1][0]) > w / 4:
                score = abs(math.atan2(eyes[1][1] - eyes[0][1], eyes[1][0] - eyes[0][0]))
                if eyes[0][1] == eyes[1][1]:
                    score = 0.0
                results.append({
                    'center': translate([face[0] + face[2] / 2.0, face[1] + face[3] / 2.0], -deg),
                    'w': float(face[2]) / float(cols) * 100.0,
                    'h': float(face[3]) / float(rows) * 100.0,
                    'eyes': [translate([face[0] + e[0] + e[2] / 2.0, face[1] + e[1] + e[3] / 2.0], -deg) for e in eyes],
                    'score': score,
                })
    # unify duplicate faces
    faces = []
    for result in results:
        x, y = result['center']['x'], result['center']['y']
        exists = False
        for i in range(len(faces)):
            face = faces[i]
            if (face['center']['x'] - face['w'] / 2.0 < x < face['center']['x'] + face['w'] / 2.0 and
                face['center']['y'] - face['h'] / 2.0 < y < face['center']['y'] + face['h'] / 2.0):
                exists = True
                if result['score'] < face['score']:
                    faces[i] = result
        if not exists:
            faces.append(result)
    for face in faces:
        del face['score']
    return faces
