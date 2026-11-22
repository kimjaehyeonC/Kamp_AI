# 6. 코드 및 재현성

## 실행 방법

```bash
export KAMP_DATA_DIR=/path/to/press_anomaly_dataset   # 기본값 있음, 생략 가능
conda activate my_base                                  # pandas 2.2.3 / scikit-learn 1.6.1
python scripts/run_pipeline.py
```

한 줄로 **전처리 → 피처 생성 → 모델 학습(베이스라인 + Mahalanobis/Isolation Forest/
One-Class SVM + 길이별 폴백 모델) → 평가(단일 분할 + 6-fold 교차검증) → 추론 데모**까지
수작업 없이 끝까지 실행된다. 결과는 터미널 끝부분("최종 결과 요약")에 표로 출력된다.
같은 내용을 노트북으로 직접 열어보려면 `notebooks/00_submission_pipeline.ipynb`를
Run All 한다 — `scripts/run_pipeline.py`는 이 노트북의 코드 셀을 그대로 순서대로
실행하는 래퍼다(nbconvert 등 추가 패키지 설치가 필요 없도록 직접 구현).

## 결정론성

`IsolationForest(random_state=0)`만 시드가 필요하고, 나머지(`LedoitWolf`, 분위수
임계, `OneClassSVM`)는 전부 결정적이다. 동일 환경·동일 데이터로 재실행하면 모든
수치가 그대로 재현된다.

## 참고 — 탐색 과정 노트북

`00_submission_pipeline.ipynb`는 이미 확정된 피처·모델만 담았다. "왜 이 피처·모델을
골랐는지"의 탐색 과정은 아래에 남겨뒀다(실행은 선택 사항).

| 노트북 | 내용 |
|---|---|
| `01_eda.ipynb` ~ `03_feature.ipynb` | 세그먼트 복원, EDA, 규칙 기반 1차 평가 |
| `04_rule_base.ipynb` | 베이스라인 규칙 + 최종 피처 재검증 |
| `05_oneclass.ipynb`, `05_oneclass_fp_analysis.ipynb` | 모델 비교, 피처 선택(VIF), 오탐·미탐 분석, n<10 대응 |
| `06_window_latency.ipynb` | 조기 탐지 지연시간 검증 |
| `07_report_figures.ipynb` | 본 보고서 삽입 그림 생성 |

근거 문서: `docs/01_eda_findings.md`, `docs/02_feature_candidates.md`,
`docs/03_modeling_strategy.md`, `docs/04_methodology.md`.
