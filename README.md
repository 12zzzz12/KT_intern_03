# KT_intern_03 

# 흑색종 진단 서비스

## 소개
**흑색종 진단 서비스**는 [흑색종(Melanoma)](https://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=32475), 점(Nevus), [검버섯(Seborrheic_keratosis)](https://www.derma.or.kr/new/general/disease.php?uid=5187&mod=document) 3가지 중 한가지로 판별하는 기능을 수행합니다.   
사용자가 안드로이드 앱을 이용해 흑색종으로 의심되는 피부를 촬영하면, 해당 이미지를 AI 모델이 있는 Flask 서버로 전송합니다. Flask에서 전송된 이미지를 AI 모델에 적용하고, 3가지 클래스중 **0.5 이상의 정확도**를 가지는 카테고리로 분류합니다. 분류된 클래스와 정확도를 앱으로 전송해 사용자에게 보여주고, 분류된 클래스가 흑색종일 경우 가까운 병원을 추천하는 과정을 거칩니다. 

**업데이트** : __Jan 05, 2021__  

**참여자** : [김륜아](https://github.com/lena-for-world), [김재근](https://github.com/12zzzz12), [김초원](https://github.com/cwaa079), [문지영](https://github.com/94MOONJI), [박인정](https://github.com/injjeong), [안시현](https://github.com/ashnnn98), [우수연](https://github.com/WSY0000), [이채흔](https://github.com/chaeheun), [장지호](https://github.com/twa04047), [천웅빈](https://github.com/woong223)!



## 목차
[1. 안드로이드](#안드로이드)   
[2. AI 모델](#ai-모델)   
[3. AI 모델 실행 방법](#ai-모델-실행-방법)  
[4. 결과](#결과)   
[5. 참고자료](#Reference)   
   
---
## 1. 안드로이드   
본 서비스를 제공하기 위해서 안드로이드는 이미지 촬영, 병원 추천, AI 모델 통신 기능을 수행합니다.

### 이미지 전송

사용자는 안드로이드에서 이미지를 촬영 후, 전송버튼을 눌러 AI 모델로 이미지를 전송합니다.   
```Java
@Override
public void onClick(View v) {
	// flask [post] /pic api로 사진 전송 (Volley MultipartRequest 이용)
	ByteArrayMultiPartRequest byteArrayMultiPartRequest = new ByteArrayMultiPartRequest(Request.Method.POST, AiServerUrl, new Response.Listener<byte[]>() {
        	@Override
		public void onResponse(byte[] response) {
                        Log.d("server", "ai 서버 성공" + response);
                        String st = new String(response);
                        if(st.equals("다시 찍으세요. 0")) {
                            Toast.makeText(getApplicationContext(), "이미지가 정확하지 않아요! 사진을 다시 찍어주세요", Toast.LENGTH_LONG).show();
                        } else {
			    // 결과값 파싱
                            parseResult(st);
                        }
                        submitToServerButton.setVisibility(View.INVISIBLE);
                    }
                }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        Log.d("AIserver", error.toString());
                }
	});

	String imageFileName = saveBitmapToCache(doubleRotated);
        String imageFilePath = getFilePathFromCache(imageFileName);

        // "file"이라는 이름으로, imageFilePath에 해당하는 사진 upload
        // volley를 사용하여 통신
        byteArrayMultiPartRequest.addFile("file", imageFilePath);

        // volley의 requestQueue에 추가
        VolleySingletonRQ.getInstance(getApplicationContext()).addToRequestQueue(byteArrayMultiPartRequest);
}
```
<img width="300" height = "500" src="https://user-images.githubusercontent.com/53503626/148164518-78342356-d806-48c0-a6da-9e15410c40a5.gif"/>   
[이미지 선택 후 전송버튼 누르는 과정]   

### 결과 확인   
모델에서 얻은 결과를 통해 사용자는 해당 이미지가 흑색종인지 확인할 수 있습니다.     
만약 흑색종을 판별된 경우는 질병에 대한 정보, 주변 병원 위치를 사용자에게 알려줍니다.
```Java
// 질병명 따라 분기 처리
// 흑색종 판별 or 설문조사 결과가 흑색종인 경우
if (diseaseName.equals("melanoma") || diseaseName.equals("returnedMelanoma")) {
	diseaseText.setText("흑색종 의심!");
	nearIntent = new Intent(this, melanomaPageActivity.class);
        infoIntent.setData(Uri.parse("https://www.amc.seoul.kr/asan/healthinfo/disease/diseaseDetail.do?contentId=32475"));
} else if (diseaseName.equals("returnedSK")) { // 설문조사 결과가 검버섯인 경우
	diseaseText.setText("검버섯");
	nearIntent = new Intent(this, skPageActivity.class);
        infoIntent.setData(Uri.parse("https://www.derma.or.kr/new/general/disease.php?uid=5187&mod=document"));
} else {// 점 또는 검버섯인 경우 설문조사 페이지로 이동
	intent = new Intent(this, skResearchPageActivity.class);
        intent.putExtra("diseaseName", diseaseName);
        startActivity(intent);
}
```
<img width="300" height = "500" src="https://user-images.githubusercontent.com/53503626/148165867-9180e493-0289-4a41-a514-b626445dcfa3.gif"/> 
[결과확인 및 병원 위치표시]   

### Map 
Android는 2가지 경우에 사용자에게 Map을 보여줍니다.   
* 흑색종으로 의심될 경우    
근처의 **대학병원**을 지도에 표시합니다.   
```Java
new NRPlaces.Builder()
	.listener(melanomaPageActivity.this) // listener로 PlacesListener interface 구현한 activity 넣음
        .key("AIzaSyBCuGuTxO2Yj7mQcj8Xp_37Hd_3JYF4CWw")
        .latlng(location.latitude, location.longitude)
        .radius(5000)
        .keyword("대학병원")
        .type(null)
        .build()
        .execute();
```
[대학병원 위치]   
<img src="https://user-images.githubusercontent.com/53503626/148166372-41f30120-a138-48c7-b5e4-04989f487d50.PNG" width="300" height="500">  
        
* 검버섯으로 의심될 경우   
 근처의 **피부과**를 지도에 표시합니다.   
```Java
new NRPlaces.Builder()
        .listener(skPageActivity.this) // listener로 PlacesListener interface 구현한 activity 넣음
        .key("AIzaSyBCuGuTxO2Yj7mQcj8Xp_37Hd_3JYF4CWw")
        .latlng(location.latitude, location.longitude)
        .radius(5000)
        .keyword("피부과")
        .type(null)
        .build()
        .execute();
```
[피부과 위치]   
<img src="https://user-images.githubusercontent.com/53503626/148180622-5d18db2b-d12a-469a-a433-7574d27d8539.jpg" width="300" height="500">  


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
			<td align="center"> 2. Nevus (784) </td>
			<td align="center"> 3. Seborrheic_keratosis(793)</td>
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
   
### Object_detection   

본 서비스의 AI모델은 분류 모델을 메인으로 합니다.      
하지만 분류 모델은 흑색종, 점, 검버섯에 대한 이미지로 학습을 진행하였기 때문에, 그 외 분류되지 않는 사진(EX. 사람, 노트북, 커피)에 대한 부분을 보완하기 위해 객체검출 모델을 이용하였습니다. 400여장의 이미지를 학습시킨 객체 검출(Object detection)모델에서 서비스가 원하는 이미지가 맞는지 먼저 판단하고 분류모델 적용을 결정하는 과정을 지닙니다.   
해당 모델은 오픈API를 이용하여 구축했기 때문에, 자세한 설명은 아래 링크를 첨부합니다.   
<img src="https://user-images.githubusercontent.com/53503626/148170855-e714c0e0-8afd-4cb2-b8e1-7694a5ef888b.jpg" width="250" height="250">      
[분류할 객체가 있는지 확인]   
오픈API : https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10


## Flask
AI 모델은 Flask를 이용해 안드로이드와 통신합니다.   
Flask 디렉토리에는 분류모델(classificatin_model.h5), 객체모델(detection_model.pb), 분류(pred_classificatin.py), 객체검출(pred_detection.py), 통신(flask.py)을 위한 파일이 있습니다.   
<img src="https://user-images.githubusercontent.com/53503626/148169968-4318c3da-f86d-4faf-812c-639a8ee6809d.PNG" width="250" height="250">   
[Flask 디렉토리 구조]


flask.py는 Android에서 전송받은 이미지를 Flask 디렉토리에 저장하고,    
Detection(검출)-Classification(분류) 과정을 거쳐서 얻은 결과값(ex. "Melanoma 80.2")을 Android로 재전송합니다.   

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
<img src="https://user-images.githubusercontent.com/53503626/148171356-1b471de1-0046-480a-98b3-09fcc65944b5.jpg" width="250" height="250">
[Flask 서버 콘솔 이미지]

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

코드를 실행하면 AI모델이 세 가지 카테고리로 이미지를 분류한 것을 확인할 수 있습니다.   

<img src="https://user-images.githubusercontent.com/53503626/148182756-19bba4c3-2401-4a40-9316-891e54d79c17.PNG" width="200" height="200"/> <img src="https://user-images.githubusercontent.com/53503626/148182538-7533beae-0bb4-4741-8170-0bb4375a4fef.PNG" width="200" height="200"/> <img src="https://user-images.githubusercontent.com/53503626/148182540-ce96b506-413a-4362-b735-7f77a7c17fc5.PNG" width="200" height="200"/>     
[이미지 분류결과]   

---
## 4. 결과 

#### 파라미터 조정 
최적의 모델을 생성하기 위해 Epoch/Batch를 조정하여 학습한 결과, Epoch = 15, Batch = 16 인 모델이 Validation data에 대해 93%의 정확도를 가지는 것을 확인하였습니다.
| Epoch/Batch | 16 | 10 |
| :---: | :---: | :---: |
| 10 | 92% | 90% |
| 15 | **93%** | 92% |
| 20 | 90% | 91% |

#### 정확도, Loss 그래프
짧은 시간안에 고성능의 모델을 생성하기 위해서 Dropout과 Batch Nomalization 중, 비교적 정확도가 높은 Batch를 사용하였습니다.
| Dropout |  Batch Nomalization |
| :---: |  :---: |
| <img src="https://user-images.githubusercontent.com/53503626/148176049-53ebec64-a670-4f9d-ab7c-f8e8b78750d7.PNG"> | <img src="https://user-images.githubusercontent.com/53503626/148176048-ff31d87f-0c5b-4713-9e2e-aaf0c8762380.PNG"> |


---
## 5. Reference 
* 임상헌, and 이명숙. "딥 러닝 기반의 악성흑색종 분류를 위한 컴퓨터 보조진단 알고리즘." 사) 디지털산업정보학회 논문지 14.4 (2018): 69-77.
* https://github.com/Shubham-SK/dermatologist
* https://github.com/cavitcakir/Skin-Cancer-Classification



