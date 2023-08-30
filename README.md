# News analysis
## Overview
RSS Feed로부터 뉴스 피드를 가져와서 카테고리, 긍정 부정, 한국어로 번역한 요약을 보여준다.

## Step
- news categorizer 훈련
  - cnn news data를 바탕으로 category를 분류하는 comprehend custom classifier
- business logic 작성
  - title, description을 합쳐서 positive negative 예측
  - title, description 번역
  - title, description 으로 카테고리 예측
- CNN RSS Feed 파싱해서 summary 추출 및 추가 훈련을 위한 데이터 셋 누적

## Dataset
- [BBC News Summary](https://www.kaggle.com/datasets/pariza/bbc-news-summary)
