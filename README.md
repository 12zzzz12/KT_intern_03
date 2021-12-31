# KT_intern_03 

# 흑색종 진단 서비스

**흑색종 진단 서비스**는 흑색종(Melanoma), 점(Nevus), 검버섯(Seborrheic_keratosis) 3가지 중 한가지로 판별해준다. 안드로이드 앱에서 흑색종으로 의심되는 피부를 촬영 후, AI 모델을 서빙하는 Flask 서버로 전송한다. Flask에서 전송된 이미지를 AI 모델에 적용하고, 3가지 클래스중 0.5 이상의 정확도를 가지는 카테고리로 분류한다. 분류된 클래스와 정확도를 앱으로 전송해 사용자에게 보여주고, 분류된 클래스가 흑색종일 경우 가까운 병원을 추천하는 과정을 지닌다. 

**기간**: __Jan 01, 2022__: 흑색종 진단 서비스 is extended and applied to fast autonomous exploration. Check this [repo](https://github.com/HKUST-Aerial-Robotics/FUEL) for more details.


## 목차
1.	소개 (요약)
2.	학습 데이터 링크 
3.	모델 학습 
4.	학습된 모델 추출
5.	학습된 분류 모델 사용 
6.	Flask에 분류 모델 적용
7.	참고사이트 

## 소개

















"참고사이트"

ink : https://github.com/cavitcakir/Skin-Cancer-Classification



