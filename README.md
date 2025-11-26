# Nail Recommendation System

YOLO 기반 손톱 인식 + 텍스트 분석 기반 네일 쉐입·디자인 추천 모델

## 1. 프로젝트 개요

본 프로젝트는 손 사진 한 장으로 손톱을 인식하고
길이/너비 특징을 계산한 뒤
블로그 텍스트 기반 추천 룰을 적용하여 
가장 잘 어울리는 네일 쉐입 및 어울리는 네일 디자인 TOP3
을 제안하는 시스템 입니다

## 2. 폴더 구조
sbhc4
│
├── 01_data_text_rule/
│   ├── 01_naver-search.ipynb
│   ├── 02_blog-contents.ipynb
│   ├── 03_naver-search-content.ipynb
│   ├── 04_keyword-analysis.ipynb
│   ├── basic_data/
│   │   ├── 02_shape_rule_result.csv
│   │   ├── 03_design_rule_result.csv
│   │   ├── 04_group_shape_design_rule.csv
│   └── craw_download_file/
│
├── 02_nail_seg_yolo/
│   ├── YOLOv11.ipynb
│   └── best.pt
│
├── 03_nail_recommend/
│   ├── SAM_HQ_ViT_H.ipynb
│   └── 손톱길이_모양_판별.ipynb
│
└── README.md


## 3. 전체 파이프라인
[01_data_text_rule]
   │
   ├─ ① 네이버 검색결과 수집
   ├─ ② 블로그 본문 수집
   ├─ ③ 문장 기반 Shape 문맥 추출
   └─ ④ Shape → Design 룰 생성
        ↓
[Shape/Design Prob CSV]
        ↓
[02_nail_seg_yolo]
   └─ YOLO 손톱 인식 → bbox
        ↓
[03_nail_recommend]
   ├─ SAM 손톱 마스크 생성
   ├─ 길이/너비 측정 → 타입 분류
   └─ 룰 CSV 기반 Shape·Design 추천
        ↓
[최종 출력]
"길이-너비 타입", "추천 쉐입", "추천 디자인 TOP3"

## 4. 단계별 상세 설명
### 4.1 텍스트 기반 추천 룰 생성 (01_data_text_rule)
#### ● 01_naver-search.ipynb

네이버 블로그 검색결과를 크롤링하는 단계

키워드 기반으로 블로그 검색결과(제목·작성자·날짜·링크)를 수집
후반부에 **키워드 분석(등장 단어 빈도 분석)**이 포함되어 있음
네일 디자인/색상/패턴 관련 단어가 어떤 빈도로 등장하는지 확인

#### ● 02_blog-contents.ipynb

블로그 링크 목록을 바탕으로 실제 블로그 본문을 수집하는 단계

- iframe 내부 본문 파싱
- full_text 생성
- 이미지 경로 필터링

길이·너비 → 쉐입 추천 빈도를 수동으로 조사한 내용을 기반으로 규칙 생성
(02_shape_rule_result.csv)

→ 즉, **손톱 길이/너비에 따른 Shape 추천 규칙(초기 수동 버전)**을 만든 단계입니다.

#### ● 03_naver-search-content.ipynb

위 1·2번 과정을 통합:

- 네이버 검색결과
- 블로그 본문(full_text)
- 이미지 개수

를 하나의 데이터프레임으로 정리하는 단계

※ 이미지도 수집했지만, 저작권/데이터 정제 문제로 실제 모델에는 사용하지 않음.

#### ● 04_keyword-analysis.ipynb

텍스트 기반 추천 룰 생성 단계

주요 작업
 Shape & Design 키워드 사전 구축

round / square / oval / almond / squoval
glitter / french / nudes / ombre / art

변형어(“오벌/오발/oval”, “스쿠오발/squoval” 등) 정규화 처리

- Shape 문맥 기반 문장 추출

문장에서 shape 단어가 등장한 구문만 분석
노이즈 단어 제거(매장명 등)

- 디자인 키워드 카운팅

shape → design 조합이 얼마나 나타나는지 분석
조건부 확률 기반 테이블 생성

결과물:

파일명	의미
03_design_rule_result.csv	Shape → Design 확률
04_group_shape_design_rule.csv	길이·너비 및 Shape 기반 추천 룰 완성
### 4.2 손톱 인식 (02_nail_seg_yolo)
#### ● YOLOv11.ipynb

best.pt 모델을 기반으로:

손 사진에서 손톱 bbox 탐지
ROI(손톱 영역) 추출

### 4.3 길이·너비 측정 + 추천 (03_nail_recommend)
#### ● SAM_HQ_ViT_H.ipynb

YOLO의 bbox 안에 대해 SAM-HQ segmentation을 수행하여:
손톱 mask 생성
윤곽을 기반으로 길이(height), 너비(width) 측정

#### ● 손톱길이_모양_판별.ipynb

- 길이·너비 비율 기반 타입 분류
길이: short / mid / long
너비: narrow / wide

조합으로 6개 group_id(L_N, L_W, M_N …) 룰 CSV 불러오기

- Shape & Design 추천

길이-너비 타입 분류: long-narrow
추천 쉐입 & 디자인 TOP 3 : square-glitter, square-ombre, square-art  

추천 결과 생성

## 5. 사용된 데이터 요약
파일	내용
- 02_shape_rule_result.csv	길이/너비 → Shape 확률 (초기 규칙)
- 03_design_rule_result.csv	Shape → Design 확률
- 04_group_shape_design_rule.csv	길이·너비 × Shape × Design 결합 확률
## 6. 실행 순서

- 02_nail_seg_yolo/YOLOv11.ipynb 실행 → 손톱 bbox 추출
- 03_nail_recommend/SAM_HQ_ViT_H.ipynb 실행 → mask + 길이·너비 계산
- 03_nail_recommend/손톱길이_모양_판별.ipynb 실행 → 최종 추천 출력

텍스트 기반 룰을 갱신할 경우:
01_data_text_rule/04_keyword-analysis.ipynb 재실행

## 7. 팀원 역할
팀원	담당
- 허지환 : 크롤링 / 텍스트 분석 / 추천 룰 생성 (01단계)
- 양승혜	: YOLO 학습 및 손톱 인식 (02단계)
- 박소연	: 길이·너비 측정 및 추천 연결 (03단계)
## 8. 프로젝트 현황 및 한계

이미지 데이터는 수집했으나 정제 문제 등으로 미사용
텍스트 기반 분석하여 규칙 생성
손톱 이미지 자동 분류(길이·너비)는 개선 여지 있음
텍스트 분석 기반 Shape/Design 분류체계를 더 확장 가능

## 9. 향후 개선 방향

손톱 모양 외 다른 요인 추가
색상(Color) 추천 모델 추가
CNN 기반 Shape 자동 분류 학습
실 사용자 테스트 기반 모델 튜닝
API 연결 및 프론트엔드 프로토타입 제작