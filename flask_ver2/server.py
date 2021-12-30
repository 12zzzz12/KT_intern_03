import model
import cv2
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route('/upload')
def render_file():
    return render_template('upload.html')

@app.route('/fileUpload', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 이미지를 받아와서 저장
        f = request.files['file']
        f.save('C:/Users/Root/PycharmProjects/capstone/' + secure_filename(f.filename))

        # 모델 적용
        # model.py 에서 결과 이미지 받아오기
        image = model.imgreturn(f.filename)
        cv2.imshow('Object detector', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(f.filename)
    return image

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)