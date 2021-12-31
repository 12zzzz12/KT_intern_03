# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
from flask import Flask, render_template, send_file, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home_hi():
    print('hello')
    return 'hello!!'

@app.route('/pic', methods=['GET', 'POST'])
def pic():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save('C:/Users/User/Desktop/image/' + filename)
        #return render_template('img.html', image_file="C:/Users/User/Desktop/image/"+filename)
        return send_file('C:/Users/User/Desktop/image/pic.jpg', mimetype='image/jpg') # 테스트
    if request.method == 'GET':
        return 'pic post method'

if __name__ == '__main__' :
    # 실행할 host, port 파라미터로 넣기
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
