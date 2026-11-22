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
- [x] `notebooks/02_eda_segment_patterns.ipynb` — 세그먼트 단위 유형 파악(normal 국면 존재 여부, outlier 내 이상 단계 분류, 시간순 악화 궤적 검증)
- [x] `notebooks/02_eda_segment_features.ipynb` — 전체 세그먼트 지표 EDA(지표 시계열, 길이별 분포·결측, 대표 원시 파형 비교)
- [x] `notebooks/03_feature.ipynb` — 사이클 지표의 규칙 기반 평가(정상 내부 오경보율, 결합 점수, 길이별 오경보·미탐률)
- [x] `notebooks/04_rule_base.ipynb` — 완전중복 제거, 정상 60/20/20 분할, 6개 피처의 99.9% 정적 규칙 및 OR 조합 평가. **최종 재평가(## 6)로 종료**: 05와 동일한 3개 피처로 fold 기준 재평가해 OR이 Mahalanobis보다 FP 3~8배 높음을 확인(피처가 아니라 OR 결합 자체의 한계) — 이후 모든 피처 개선은 05 계열에서만 진행
- [x] `notebooks/05_oneclass.ipynb` — Mahalanobis/Isolation Forest/One-Class SVM 비교(n≥10), 설명력 분석(기여도 분해·permutation importance·SHAP). **## 8에 n<10 대응 추가**: `cur_ai0_resid`·`cur_ai1_resid` 2개 전용 피처로 n=2~9 오탐률 32.2%→3.3%(탐지율 100% 유지) — 2-track 설계(n≥10: 3개 피처, n=2~9: 2개 피처, n=1: 판정 보류)로 수렴
- [x] `notebooks/05_oneclass_fp_analysis.ipynb` — 오탐·미탐 발생조건 분석: 전구간 FP census, 연속성 검증, V-dip 전환구간 진단, fold 기준 재검증(IsolationForest 구조적 미탐은 seg3 1건뿐), 피처 평면 시각화, **n<10 전체 포함 재검증(핵심 한계 발견: Mahalanobis도 n=2~9에서 오탐률 32.2%)**
- [x] `notebooks/06_window_latency.ipynb` — 사이클 완료 전 더 짧은 윈도우(K샘플)로도 판단 가능한지 검증(n≥10 한정) — 1.0초(10샘플)면 전체 사이클과 동일한 성능
- [ ] `07_deep_window.ipynb` — LSTM/CNN으로 1.0초보다 더 짧은 윈도우에서 판단 가능한지 확인 (06의 통계적 절단 결과를 기준선으로 비교)
- [ ] N중M 지속성 규칙: 05-1에서 이 데이터엔 연속 오탐/미탐 패턴이 없어 검증·정당화 불가로 확인됨 — 채택하지 않음
- [x] n<10 세그먼트(정상 11.5%·outlier 19%) 처리: 05-1에서 심각한 오탐 문제로 확인됨(04 rule-base도 동일 — 모델이 아니라 피처 자체의 근본 한계) → 05 ## 8에서 2-track(n=2~9 전용 2피처 Mahalanobis)으로 대응, 오탐률 32.2%→3.3%. n=1은 계산 불가로 판정 보류 유지(미해결)

정리 문서: `docs/01_eda_findings.md` (01~03 결과 종합·근거, 다음 단계 상세),
`docs/02_feature_candidates.md` (피처 후보 현재 상태 — 자주 갱신됨),
`docs/03_modeling_strategy.md` (모델 학습·평가 전략),
`docs/04_methodology.md` (05에 쓰인 방법론 개념 설명 — VIF/PCA, Mahalanobis·Ledoit-Wolf,
Isolation Forest, One-Class SVM, 블록 k-fold, permutation importance, SHAP)

## 환경
- `my_base` (pandas 2.2.3 / scikit-learn 1.6.1 / shap 0.52.0) — 01~05 노트북 전체
- `my_base2` (torch 2.6.0+cu126 / shap 0.51.0) — 향후 딥러닝 비교 실험용(아직 미사용)
