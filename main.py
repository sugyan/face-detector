from flask import Flask, request, jsonify, render_template

import cv2
import numpy as np
import urllib
import detector

app = Flask(__name__)
app.debug = True

@app.route('/api')
def api():
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

    faces = detector.detect(img)
    return jsonify(faces=faces)

@app.route('/')
def main():
    return render_template('index.html')
