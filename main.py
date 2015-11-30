from flask import Flask, request, jsonify, make_response

import cv2
import numpy as np
import urllib
import detector

app = Flask(__name__)
app.debug = True

@app.route('/image')
def image():
    url = request.args.get('url')
    if url is None:
        return jsonify(error='"url" is required.')
    try:
        data = urllib.urlopen(url).read()
    except Exception:
        return jsonify(error='urlopen failed.')
    buf = np.fromstring(data, dtype=np.uint8)
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
    if img is None:
        return jsonify(error='read image failed.')

    img = detector.detect(img)
    _, data = cv2.imencode('.jpg', img)
    resp = make_response(data.tobytes())
    resp.headers['Content-Type'] = 'image/jpeg'
    return resp

@app.route('/')
def main():
    return 'OK'
