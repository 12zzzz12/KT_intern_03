# KT_intern_03 

# 흑색종 진단 서비스

## 소개
**흑색종 진단 서비스**는 흑색종(Melanoma)[**흑색종사이트링크**], 점(Nevus), 검버섯(Seborrheic_keratosis)[**검버섯사이트링크**] 3가지 중 한가지로 판별해준다. 안드로이드 앱에서 흑색종으로 의심되는 피부를 촬영 후, AI 모델을 서빙하는 Flask 서버로 전송한다. Flask에서 전송된 이미지를 AI 모델에 적용하고, 3가지 클래스중 0.5 이상의 정확도를 가지는 카테고리로 분류한다. 분류된 클래스와 정확도를 앱으로 전송해 사용자에게 보여주고, 분류된 클래스가 흑색종일 경우 가까운 병원을 추천하는 과정을 지닌다. 

**개발기간**: __Jan 01, 2022__ : 흑색종 진단 서비스 

**참여자**: [김륜아](https://github.com/lena-for-world), [김재근](https://github.com/12zzzz12), [김초원](https://github.com/cwaa079), [문지영](https://github.com/94MOONJI), [박인정](https://github.com/injjeong), [안시현](https://github.com/ashnnn98), [우수연](https://github.com/WSY0000), [이채흔](https://github.com/chaeheun), [장지호](https://github.com/twa04047), [천웅빈](https://github.com/woong223)
 

## 목차
1. [안드로이드](#안드로이드)
2. [AI 모델 및 데이터](#AI-모델-및-데이터)
3. [AI 모델 실행 방법](#AI-모델-실행-방법)
4. [결과](#결과)
5. [참고자료](#참고자료)

## 1. 안드로이드 
   
## 2. AI 모델 및 데이터 

## 3. AI 모델 실행 방법 
#### 모델 설치   
      
본 프로젝트에서 사용한 모델을 실행할 수 있도록 준비된 [사이트](https://github.com/12zzzz12/KT_intern_03_prototype)에서 파일을 clone 합니다.
```
git clone https://github.com/12zzzz12/KT_intern_03_prototype.git
```
설치한 파일을 PyCharm에서 실행시킵니다.   
[***파이참 설치된 파일구조 사진***]   

PyCharm에 세팅한 파일구조
   
#### 모델 실행
[***모델 동작 사진 및 결과 사진***]   
model.py를 실행시키면 테스트 이미지를 분류한 카테고리와 정확도를 출력합니다.


## 4. 결과 

## 5. 참고자료 



















"참고사이트"

ink : https://github.com/cavitcakir/Skin-Cancer-Classification



