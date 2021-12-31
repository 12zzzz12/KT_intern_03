# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with yourIP code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import model
from flask import Flask, send_file, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home_hi():
    return 'hello!!'

@app.route('/pic', methods=['POST'])
def pic():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save('C:/Users/User/Desktop/Flask/flask_ver4/from_and' + filename)

        # 분류결과 받기
        # String ( 객체이름, 추측확률 ) , EX. ( 'melanoma', 61.2 )
        pred = model.pred_return(filename)
        ret_pred = pred[0] + ' ' + str(pred[1])
        return ret_pred


if __name__ == '__main__' :
    # 실행할 host, port 파라미터로 넣기
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
