import time
from base_camera import BaseCamera
import cv2
import yolov3Tf.yoloUtils as yoloUtils

class Camera(BaseCamera):

    @staticmethod
    def frames():
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = cam.read()
            try:
                if CameraParams.gray:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                if CameraParams.gaussian:
                    img = cv2.GaussianBlur(img, (3,3), 0)
                if CameraParams.sobel:
                    if(len(img.shape) == 3):
                        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    img = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=5)  # x
                    img = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=5)  # y 
                if CameraParams.canny:
                    img = cv2.Canny(img, 100, 200, 3, L2gradient=True)
            except Exception as e:
                print(e)
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()

class CameraParams():

    gray = False
    gaussian = False
    sobel = False
    canny = False
    yolo = False

    def __init__(self, gray, gaussian, sobel, canny, yolo):
        self.gray = gray
        self.gaussian = gaussian
        self.sobel = sobel
        self.canny = canny
        self.yolo
