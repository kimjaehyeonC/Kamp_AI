# Kamp_AI — 파인블랭킹 프레스 유압펌프 이상탐지

유압펌프 모터의 상·하부 진동(AI0/AI1)과 전류(AI2) 시계열로 설비 이상을 조기 탐지하는 모델을 만든다.
탐지율만이 아니라 **정상적인 운전변화를 이상으로 오판하는 오경보(FP)** 를 줄이고,
미탐지·오경보가 발생하는 조건을 설명하는 것이 목표.

## 데이터
원본: `/mnt/d/data/kamp_ai/press_anomaly_dataset/` (리포에 커밋하지 않음)

| 파일 | 행 | 기간 | Equipment_state |
|---|---|---|---|
| `press_data_normal.csv` | 20,000 | 2022-07-12 00:00 ~ 01:17 | 전부 0 |
| `outlier_data.csv` | 600 | 2022-07-17 10:51 ~ 10:54 | 전부 1 |

컬럼: `TimeStamp, AI0_Vibration, AI1_Vibration, AI2_Current, Equipment_state`

경로는 환경변수로 덮어쓸 수 있다: `export KAMP_DATA_DIR=/path/to/press_anomaly_dataset`

## 진행
- [x] `notebooks/01_eda.ipynb` — 구조 점검, 취득 사이클 복원, normal/outlier 시간관계 검증, 신호 비교
- [ ] `02_feature.ipynb` — 사이클 단위 피처 설계
- [ ] `03_model.ipynb` — 정상 기준 이상탐지 모델
- [ ] `04_error_analysis.ipynb` — 미탐지·오경보 조건 분석

## 환경
conda `my_base` (pandas 2.2.3 / scikit-learn 1.6.1)
