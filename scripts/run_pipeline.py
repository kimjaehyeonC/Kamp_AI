"""전처리~학습~추론~결과생성을 자동 실행한다.

사용법:
    conda activate my_base
    export KAMP_DATA_DIR=/path/to/press_anomaly_dataset   # 생략 시 기본값 사용
    python scripts/run_pipeline.py

notebooks/00_submission_pipeline.ipynb의 코드 셀을 순서대로 그대로 실행한다
(nbconvert/ipykernel 설치 없이 동작하도록, 셀 소스를 읽어 단일 프로세스에서
순차 실행하는 방식 — 노트북과 동일한 결과를 낸다).
"""
import json
import sys
from pathlib import Path

NOTEBOOK = Path(__file__).resolve().parent.parent / "notebooks" / "00_submission_pipeline.ipynb"


def main():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    g = {"__name__": "__main__"}
    for i, cell in enumerate(nb["cells"]):
        if cell["cell_type"] != "code":
            continue
        src = "".join(cell["source"])
        try:
            exec(compile(src, f"<{NOTEBOOK.name} cell {i}>", "exec"), g)
        except Exception:
            print(f"\n--- 실패: 셀 {i} ---\n{src[:500]}", file=sys.stderr)
            raise
    print("\n파이프라인 실행 완료.")


if __name__ == "__main__":
    main()
