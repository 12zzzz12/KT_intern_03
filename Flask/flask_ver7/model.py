from keras.models import load_model
from PIL import Image
import os, glob, numpy as np

def pred_return(img) :

    categories = ["melanoma", "nevus", "seborrheic_keratosis"]

    # 이미지크기
    image_w = 224
    image_h = 224

    X = []

    # 이미지 load
    # Flask에서 저장하는 디렉토리경로로 수정해놨습니다.
    image = Image.open('C:/Users/User/Desktop/Flask/flask_ver4/from_and'+img)
    image = image.convert("RGB")
    image = image.resize((image_w, image_h))
    data = np.asarray(image)

    X.append(data)
    X = np.array(X)

    #### 이미지 모델에 적용 ####
    # 모델 load
    model = load_model('checkpoint.h5')

    # 이미지 적용 및 예측값 추출
    predictions = model.predict(X)
    #np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

    # [0.3, 0.3, 0.3] 확률 리스트 생성
    prediction = list(predictions[0])

    # max(prediction) = 모델이 예측한 분류확률의 최댓값
    # (ex, [0.1, 0.2, 0.7] -> 0.7
    # 최대확률이 0.5 이상이면 해당 객체로 분류
    if max(prediction) > 0.5 :
        result_return = categories[prediction.index(max(prediction))]
        pred_return  = float('{:.3f}'.format(max(prediction))) * 100
    # 최대확률이 0.5 이하이면 안내문구 (3가지 카테고리 중 어느곳에도 속하지 않는 경우)
    else :
        result_return = '다시 찍으세요.'
        pred_return = 0

    # 분류된 모델 이름, 분류 확률 리턴
    return [result_return, pred_return]
