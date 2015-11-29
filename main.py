from flask import Flask, request, jsonify

import cv2
import numpy as np
import urllib

app = Flask(__name__)
app.debug = True

@app.route('/api')
def api():
    url = request.args['url']
    buf = np.fromstring(urllib.urlopen(url).read(), dtype=np.uint8)
    img = cv2.imdecode(buf, cv2.CV_LOAD_IMAGE_COLOR)
    if img is None:
        return jsonify(error='read image failed.')
    return jsonify(shape=img.shape)

@app.route('/')
def main():
    return 'OK'
