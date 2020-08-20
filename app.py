from flask import Flask, render_template, Response, stream_with_context, request, redirect, url_for
from werkzeug import secure_filename
import cv2
from camera import Camera, CameraParams
import os, time, json, base64

from yolov3Tf.yoloUtils import YoloUtils

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/cameraParams', methods=['GET', 'POST'])
def cameraParams():
    if request.method == 'GET':
        data = {
            'gray': CameraParams.gray,
            'gaussian': CameraParams.gaussian,
            'sobel': CameraParams.sobel,
            'canny': CameraParams.canny
        }
        return app.response_class(response=json.dumps(data),
                                    status=200,
                                    mimetype='application/json')
    elif request.method == 'POST':
        try:
            data = request.form.to_dict()
            print(data)
            CameraParams.gray = str_to_bool(data['gray'])
            CameraParams.gaussian = str_to_bool(data['gaussian'])
            CameraParams.sobel = str_to_bool(data['sobel'])
            CameraParams.canny = str_to_bool(data['canny'])
            message = {'message': 'Success'}
            response = app.response_class(response=json.dumps(message),
                                    status=200,
                                    mimetype='application/json')
            return response
        except Exception as e:
            print(e)
            response = app.response_class(response=json.dumps(e),
                                    status=400,
                                    mimetype='application/json')
            return response
    else:
        data = { "error": "Method not allowed. Please GET or POST request!" }
        return app.response_class(response=json.dumps(data),
                                    status=400,
                                    mimetype='application/json')
    
@app.route('/realtime')
def realtime():
    return render_template('real-time.html')

@app.route('/detectYolo', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            data = { "message": "Por favor, selecione uma imagem!" }
            return app.response_class(response=json.dumps(data),
                                    status=400,
                                    mimetype='application/json')
        if f and allowed_file(f.filename):
            timestamp = time.time()
            filename = 'uploads/' + str(int(timestamp)) + '-' + f.filename
            f.save(filename)
            imagePath, result = YoloUtils.detectImage(filename)
            image = cv2.imread(imagePath)
            _, img_encoded = cv2.imencode('.jpg', image)
            jpg_as_text = base64.b64encode(img_encoded).decode('utf-8')
            data = { "success": "file uploaded successfully", "imagePath": imagePath, "base64": jpg_as_text, "detections": result }
            return app.response_class(response=json.dumps(data),
                                    status=200,
                                    mimetype='application/json')
        else:
            data = { "error": "File format not allowed." }
            return app.response_class(response=json.dumps(data),
                                    status=400,
                                    mimetype='application/json')
    else:
        data = { "error": "Method not allowed. Please POST request!" }
        return app.response_class(response=json.dumps(data),
                                    status=400,
                                    mimetype='application/json')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(genWeb(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.errorhandler(404)
def page_not_found(error):
    return 'Ops, page not found!', 404

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def genWeb(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def str_to_bool(s):
    if s == "true":
        return True
    elif s == "false":
        return False
    else:
        raise ValueError

# def genYolo():
#     try:
#         yoloUtils = YoloUtils()
#         while True:
#             for frame in yoloUtils.tinyYolo():
#                 yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
#                 yield frame
#                 yield b'\r\n\r\n'
#     except GeneratorExit:
#         YoloUtils.closeTF()
#         print('closed')

# @app.route('/yolo_stream')
# def yolo_stream():
#     return Response(stream_with_context(genYolo()),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(host="0.0.0.0", port=5000, debug=True)