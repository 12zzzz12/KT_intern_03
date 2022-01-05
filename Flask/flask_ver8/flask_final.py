# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with yourIP code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import detection
from flask import Flask, send_file, request, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home_hi():
    return 'hello!!'

@app.route('/upload')
def render_file():
    return render_template('upload.html')

@app.route('/pic', methods=['POST'])
def pic():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save('C:/Users/User/Desktop/flask_ver4/' + filename)

        # 분류결과 받기
        # String ( 객체이름, 추측확률 ) , EX. ( 'melanoma', 61.2 )
        pred = detection.pred_detection(filename)
        ret_pred = pred[0] + ' ' + str(pred[1])

        categories = ["melanoma", "nevus", "seborrheic_keratosis"]
        categories_kr = ['흑색종', '점', '검버섯']

        if pred[0] not in categories:
            print('다시 찍으세요.')
        else :
            cate = categories_kr[categories.index(pred[0])]
            print('분류명 :', cate, ', 정확도 :', pred[1])
        return ret_pred



if __name__ == '__main__' :
    # 실행할 host, port 파라미터로 넣기
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
