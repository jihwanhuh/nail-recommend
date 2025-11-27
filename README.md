[새싹 헬스케어 서비스 기획자 부트캠프 4기] Final Project  
4조 - 네일을 바꿔조  

# NailFit - Nail Recommendation System  
YOLO 기반 손톱 인식 + 텍스트 기반 네일 Shape·Design 추천 모델

---

## 1. 프로젝트 개요

본 프로젝트는 **손 사진 한 장**을 입력받아  

1) YOLOv11 기반 **손톱 위치 탐지**,  
2) SAM-HQ 기반 **고품질 손톱 마스크 생성**,  
3) OpenCV 기반 **길이·너비 측정**,  
4) 네이버 블로그 텍스트 분석 기반 **Shape·Design 추천 룰 생성**  

을 수행하여  
**가장 잘 어울리는 네일 쉐입(shape)과 디자인 TOP3**를 자동 추천하는 시스템입니다.

---

## 2. 폴더 구조  
  
sbhc4  
│  
├── 01_data_text_rule/ # 텍스트 수집·분석 → 추천 룰 생성  
│ ├── 01_naver-search.ipynb  
│ ├── 02_blog-contents.ipynb  
│ ├── 03_naver-search-content.ipynb  
│ ├── 04_keyword-analysis.ipynb  
│ ├── basic_data/  
│ │ ├── 02_shape_rule_result.csv  
│ │ ├── 03_design_rule_result.csv  
│ │ ├── 04_group_shape_design_rule.csv  
│ └── craw_download_file/  
│  
├── 02_nail_seg_yolo/ # YOLO 기반 손톱 bbox 탐지  
│ ├── YOLOv11.ipynb  
│ └── best.pt  
│  
├── 03_nail_recommend/ # 길이·너비 계산 + 추천 모델 연동  
│ ├── SAM_HQ_ViT_H.ipynb  
│ └── 손톱길이_모양_판별.ipynb  
│  
├── 04_pt_video/ # 데모 앱 (YOLO+SAM+추천)  
│ ├── app.py # run_pipeline() 통합 파이프라인  
│ ├── ui.py # Gradio 데모 인터페이스  
│ └── oval_glitter.png # 데모용 디자인 PNG (합성용)  
│  
└── README.md
  
---  

## 3. 전체 파이프라인  

[01_data_text_rule]  
├─ ① 네이버 검색결과 수집  
├─ ② 블로그 본문 크롤링  
├─ ③ 문장 기반 Shape 문맥 추출  
└─ ④ Shape → Design 규칙 생성  
↓  
(04_group_shape_design_rule.csv)  
↓  
[02_nail_seg_yolo]  
└─ YOLOv11 손톱 인식 → bbox  
↓  
[03_nail_recommend]  
├─ SAM-HQ 손톱 마스크 생성  
├─ 길이/너비 측정 → 타입 분류(6종)  
└─ 텍스트 기반 룰로 Shape/Design 추천  
↓  
[04_pt_video]  
└─ run_pipeline() 실행 → 결과 이미지/추천 TOP3 출력  

