from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.phase3.prompt_evaluator import run_prompt_evaluation


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Phase 3 prompt comparison.")
    parser.add_argument(
        "--model",
        default="gpt-4o-mini",
        help="OpenAI model name for LangChain ChatOpenAI",
    )
    args = parser.parse_args()

    rows = run_prompt_evaluation(
        test_set_path=Path("data/phase3/prompt_eval_test_set.json"),
        output_json_path=Path("outputs/phase3/prompt_comparison_results.json"),
        output_md_path=Path("reports/phase3_prompt_comparison.md"),
        model_name=args.model,
    )

    print(f"Completed prompt comparison. Total rows: {len(rows)}")
    print("Results: outputs/phase3/prompt_comparison_results.json")
    print("Table: reports/phase3_prompt_comparison.md")


if __name__ == "__main__":
    main()
