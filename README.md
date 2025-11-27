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
  

---

## 4. 단계별 상세 설명

### 4.1 텍스트 기반 추천 룰 생성 (01_data_text_rule)

#### ● 01_naver-search.ipynb  
네이버 검색 자동화(Selenium)로  
블로그 제목·링크·날짜 데이터를 수집.  

키워드 등장 빈도 분석 포함 → 네일 색상·쉐입·패턴 단어 군집 확인 가능.

---

#### ● 02_blog-contents.ipynb  
블로그 링크를 실제로 열어 본문을 수집하는 단계.

- iframe 내부 본문 추출
- HTML 제거 → `full_text` 생성
- postfiles 이미지 필터링

추가로,  
**길이·너비 → Shape 수동 조사표**를 기반으로  
초기 shape 분포(02_shape_rule_result.csv) 계산.

---

#### ● 03_naver-search-content.ipynb  
검색결과 + 본문 텍스트를 통합.

- 제목
- 작성자
- 날짜
- full_text  
- 이미지 개수

※ 이미지 데이터는 품질·저작권 문제로 모델에 사용하지 않음.

---

#### ● 04_keyword-analysis.ipynb  
텍스트 기반 Shape/Design 추천 모델 핵심 단계.

작업 내용:
- Shape/Design 키워드 사전 구축  
- 변형어(예: 오벌/오발/oval) 정규화  
- 문장 단위 shape 문맥 추출  
- noise 제거  
- 조건부 확률  
P(design | shape)

yaml
코드 복사
계산

**결과물**

| 파일명 | 내용 |
|--------|------|
| 03_design_rule_result.csv | Shape → Design 추천 확률 |
| 04_group_shape_design_rule.csv | 길이·너비 × Shape × Design 결합 모델 |

---

### 4.2 손톱 인식 (02_nail_seg_yolo)

#### ● YOLOv11.ipynb  
best.pt 모델을 이용해:

- 손톱 bbox 탐지  
- ROI(손톱 영역) 추출

---

### 4.3 길이·너비 측정 및 추천 (03_nail_recommend)

#### ● SAM_HQ_ViT_H.ipynb  
YOLO bbox를 입력 받아 SAM-HQ로:

- 고품질 손톱 마스크 생성  
- 마스크 윤곽 기반 길이/너비 측정  

---

#### ● 손톱길이_모양_판별.ipynb  
OpenCV 측정값을 기반으로 **6개 타입으로 분류**

L_N, L_W, M_N, M_W, S_N, S_W

yaml
코드 복사

이후 추천 룰 CSV를 불러와:

- `P(shape | length,width)`
- `P(design | shape)`

결합하여 **Shape/Design TOP3 추천** 생성.

---

## 5. 사용된 데이터 요약

| 파일명 | 내용 |
|--------|------|
| 02_shape_rule_result.csv | 길이·너비 → Shape 확률(초기 규칙) |
| 03_design_rule_result.csv | Shape → Design 확률 |
| 04_group_shape_design_rule.csv | 최종 결합 규칙(150개 조합) |

---

## 6. 실행 순서

1. **02_nail_seg_yolo/YOLOv11.ipynb** → 손톱 bbox 추출  
2. **03_nail_recommend/SAM_HQ_ViT_H.ipynb** → 마스크 + 길이/너비 계산  
3. **03_nail_recommend/손톱길이_모양_판별.ipynb** → 추천 TOP3 출력  

텍스트 분석 룰 갱신 필요 시:  
→ `01_data_text_rule/04_keyword-analysis.ipynb` 재실행

04_pt_video(app.py, ui.py)은  
**데모용 통합 파이프라인**으로 구성됨.

---

## 7. 팀원 역할

| 팀원 | 담당                            |
|------|-------------------------------|
| 허지환 | 텍스트 수집·정제·추천 룰 생성             |
| 양승혜 | YOLOv11 학습 및 손톱 인식, 시연용 버전 제작 |
| 박소연 | SAM 기반 길이·너비 측정 및 추천 연결       |

---

## 8. 프로젝트 현황 및 한계

- 이미지 크롤링 데이터는 정제 한계로 미사용  
- Shape/Design 추천이 텍스트 기반 규칙 모델에 한정됨  
- 길이·너비 분류 품질이 SAM 마스크에 크게 의존  
- 색상, 피부톤 등 고급 요인은 모델에 미포함  
- 디자인 PNG 합성은 데모 기능 수준으로 구현됨  

---

## 9. 향후 개선 방향

- CNN 기반 Shape 자동 분류 모델 개발  
- 손가락 길이·피부톤 반영한 종합 추천 모델  
- 네일 색상 추천(컬러 팔레트 기반) 확장  
- 사용자 평가 기반 추천 규칙 보정  
- API 및 UI 프로토타입 기반 서비스화  