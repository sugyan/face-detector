# face-detector

face detection by OpenCV.

![](https://cloud.githubusercontent.com/assets/80381/11557325/77d7da88-99ef-11e5-8551-d3e0f1f5124c.png)

## Requirements ##

- Python 2.7
- OpenCV 3.0
- Node 5.1

## How to use ##

    $ git@github.com:sugyan/face-detector.git
    $ cd face-detector
    $ pip install -r requirements.txt
    $ npm install
    $ gunicorn main:app --log-file=-

## Deploy to heroku ##

    $ git@github.com:sugyan/face-detector.git
    $ cd face-detector
    $ npm install
    $ heroku docker:release
