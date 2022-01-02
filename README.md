# KT_intern_03 

# 흑색종 진단 서비스

## 소개
**흑색종 진단 서비스**는 [흑색종(Melanoma)](https://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=32475), 점(Venus), [검버섯(Seborrheic_keratosis)](https://www.derma.or.kr/new/general/disease.php?uid=5187&mod=document) 3가지 중 한가지로 판별하는 기능을 수행합니다.   
사용자가 안드로이드 앱을 이용해 흑색종으로 의심되는 피부를 촬영하면, 해당 이미지를 AI 모델이 있는 Flask 서버로 전송합니다. Flask에서 전송된 이미지를 AI 모델에 적용하고, 3가지 클래스중 **0.5 이상의 정확도**를 가지는 카테고리로 분류합니다. 분류된 클래스와 정확도를 앱으로 전송해 사용자에게 보여주고, 분류된 클래스가 흑색종일 경우 가까운 병원을 추천하는 과정을 거칩니다. 

**업데이트** : __Jan 01, 2021__ : AndroidImg 

**참여자** : [김륜아](https://github.com/lena-for-world), [김재근](https://github.com/12zzzz12), [김초원](https://github.com/cwaa079), [문지영](https://github.com/94MOONJI), [박인정](https://github.com/injjeong), [안시현](https://github.com/ashnnn98), [우수연](https://github.com/WSY0000), [이채흔](https://github.com/chaeheun), [장지호](https://github.com/twa04047), [천웅빈](https://github.com/woong223)


## 목차
[1. 안드로이드](#안드로이드)   
[2. AI 모델](#ai-모델)   
[3. AI 모델 실행 방법](#ai-모델-실행-방법)   
[4. 결과](#결과)   
[5. 참고자료](#Reference)   
   
---
## 1. 안드로이드   
본 서비스를 제공하기 위해서 안드로이드는 이미지 촬영, 병원 추천, AI 모델 통신 기능을 수행합니다.

### UI

사용자는 안드로이드에서 이미지를 촬영 후, 전송버튼을 눌러 AI 모델로 이미지를 전송합니다.   
<img width="50%" src="https://user-images.githubusercontent.com/53503626/147847867-fc66ee04-16d0-40ed-87ff-395da66b0a61.gif"/>   
[**이미지 선택 후 전송버튼 누르는 녹화**]     

모델에서 얻은 결과를 통해 사용자는 해당 이미지가 흑색종인지 확인할 수 있습니다.     
[**결과 및 확률이 뜨는 화면 녹화**]   

### Map 

이미지가 흑색종이라고 판단된 경우, 근처의 **병원 위치**를 지도로 표시합니다.   
[**구글 맵 뛰우는 화면 녹화 or 화면 이미지**]   



---
## 2. AI 모델   


### 개발환경
- [Python3](https://www.python.org/downloads/)
- [TensorFlow 2.x](https://www.tensorflow.org/tutorials/quickstart/beginner?hl=ko)
- [Keras](https://keras.io/ko/)
- [Flask](https://flask-docs-kr.readthedocs.io/ko/latest/)

### 데이터 수집   
* https://s3-us-west-1.amazonaws.com/udacity-dlnfd/datasets/skin-cancer
* https://www.isic-archive.com/#!/onlyHeaderTop/gallery?filter=%5B%22meta.clinical.mel_class%7Cinvasive%20melanoma%22%5D
* https://derm.cs.sfu.ca/Download.html
* http://www.cs.rug.nl/~imaging/databases/melanoma_naevi/

<table border=0 >
   <tbody>
       <tr>
			<td align="center"> 1. Melanoma (1346) </td>
			<td align="center"> 2. Venus (784) </td>
			<td align="center"> 3. Seborrheic_keratosis    (793)</td>
	</tr>
      <tr>
<td width="33%" >
<img src="https://user-images.githubusercontent.com/53503626/147816220-0e1a4294-ee2b-46c5-aa2c-9f5c5077c16b.jpg"></td>      
<td width="33%" > <img src="https://user-images.githubusercontent.com/53503626/147816828-ffc1d008-0837-4368-bbcc-ccf0f8403503.jpg"></td>
<td width="33%" > <img src="https://user-images.githubusercontent.com/53503626/147816824-e5da93ab-5c37-4b7f-aaed-c4ce267e75cd.jpg"> </td>
			

   </tbody>
 </table>
 
 
### 데이터전처리   
모델학습을 위해 이미지를 RGB형태의 값을 가진 np배열로 변환하는 작업을 진행합니다.   
```Python
for idx, category in enumerate(categories):

    #원-핫 인코딩(One-Hot Encoding)
    label = [0 for i in range(n_classes)]
    label[idx] = 1
    image_dir = data_dir + "/" + category
    
    files = glob.glob(image_dir+"/*.jpg") #jpg형태의 이미지를 리스트형태로 반환.
    print(category, "파일 개수 :", len(files))
    
    #각 이미지를 RGB값으로 변환하고 크기도 변환한 후, np배열로 저장.
    for i, f in enumerate(files):
        img = Image.open(f)
        img = img.convert("RGB")
        img = img.resize((image_w, image_h))
        data = np.asarray(img)

        X.append(data)
        y.append(label)

X = np.array(X) #입력 이미지
y = np.array(y) #label
```

### 학습
   
**모델생성 및 학습**   
본 서비스는 CNN구조를 가진 ResNet50을 사용하여 흑색종, 점, 검버섯을 판별할 수 있도록 하였습니다.
```Python   
base_model = ResNet50(include_top=False, input_shape= (224,224,3), weights = 'imagenet')

x = base_model.output

x = GlobalAveragePooling2D()(x) #extra layers
x = Dropout(0.35)(x) #overfitting 방지

predictions = Dense(3, activation= 'softmax')(x) #2개이상의 label이므로 softmax.

model = Model(inputs = base_model.input, outputs = predictions)

model.compile(loss = "categorical_crossentropy",
              optimizer = Adam(lr), 
              metrics=["accuracy"]) 
```
```Python
history = model.fit(trainx, trainy,
                    batch_size=batch_size, 
                    epochs=epoch,
                    validation_split=0.2,
                    callbacks=[checkpoint, early_stopping])
```

**파라미터**   
모델의 성능향상을 위해서 epoch, batch_size를 조정하여 높은 성능을 가지는 모델을 찾습니다.
```Python
input_shape = (224,224,3) #입력 형태 정의(행,열,채널수)
lr = 1e-5 #학습률

epoch = 10
batch_size = 16
validation_split=0.2,
```
   
### 정확도 측정   
Best모델의 정확도, 손실그래프를 통해 성능을 확인합니다.   
[**정확도, 손실 그래프 이미지**]

## Flask
AI 모델은 Flask를 이용해 안드로이드와 통신합니다.   
Flask 디렉토리에는 모델(Checkpoint.h5), 모델적용(Model.py), 안드로이드통신(Server.py)을 위한 코드가 있습니다.   
<img src="https://user-images.githubusercontent.com/53503626/147868656-d7886e02-54bb-4dc8-a832-5e3a278d6ed0.PNG" width="200" height="200">   
[Flask 디렉토리 구조]


server.py는 Android에서 전송받은 이미지를 from_and 디렉토리에 저장하고,    
model.py에서 얻은 결과값(ex. "Melanoma 80.2")을 Android로 재전송합니다.   

```Python
@app.route('/pic', methods=['POST'])
def pic():
    # 전송받은 이미지 from_and에 저장
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save('C:/Users/User/Desktop/Flask/flask_final/from_and' + filename)

        # 전송받은 이미지 AI모델에 적용 및 분류결과 전송
	# 전송하는 String 값 : "분류결과 정확도"  , EX. 'melanoma 61.2' 
	pred = model.pred_return(filename)      
        ret_pred = pred[0] + ' ' + str(pred[1]) 
        return ret_pred 	
```   

[**Flask 서버 동작 콘솔 이미지**]

---
## 3. AI 모델 실행 방법 
### 모델 설치   
      
본 프로젝트에서 사용한 모델을 실행할 수 있도록 준비된 [사이트](https://github.com/12zzzz12/KT_intern_03_prototype)에서 파일을 clone 합니다.
```
git clone https://github.com/12zzzz12/KT_intern_03_prototype.git
```   

설치한 파일을 PyCharm에서 실행시킵니다.       
<img src="https://user-images.githubusercontent.com/53503626/147846980-168754cc-4fc9-41ec-a85e-fa4f5a191068.PNG" width="200" height="200"/>    
[디렉토리 이미지]   
    
        
   
### 모델 실행
model_test.py에서 이미지 경로를 설정하고 동작하면, 테스트 이미지를 분류한 카테고리와 정확도를 출력합니다.
```Python
result, pred = pred_return("./image/melanoma.jpg") #ImgPath 설정
print(result, ':', pred , "%")
```    

코드를 실행하면 AI모델이 흑색종(Melanoma) 이미지를 분류한 것을 확인할 수 있습니다.   
<img src="https://user-images.githubusercontent.com/53503626/147847200-0132a34f-2bf0-4e8f-8ad3-0fa974abcb8b.PNG" width="700" height="200"/>
[흑색종(Melanoma) 이미지 분류결과]   

---
## 4. 결과 

### 정확도(그래프, 혼동행렬, 등등?)    



---
## 5. Reference 
* 임상헌, and 이명숙. "딥 러닝 기반의 악성흑색종 분류를 위한 컴퓨터 보조진단 알고리즘." 사) 디지털산업정보학회 논문지 14.4 (2018): 69-77.
* https://github.com/Shubham-SK/dermatologist
* https://github.com/cavitcakir/Skin-Cancer-Classification



