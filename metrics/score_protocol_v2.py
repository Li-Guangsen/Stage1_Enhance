from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Dict, List


WEIGHTS = {
    "SIFT_KP": 0.20,
    "AvgGra": 0.16,
    "Contrast": 0.12,
    "EME": 0.10,
    "EMEE": 0.08,
    "UCIQE": 0.12,
    "UIQM": 0.10,
    "Entropy": 0.06,
    "MS_SSIM": 0.04,
    "PSNR": 0.02,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Composite scoring for evaluate_protocol_v2 summary.json.")
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--reference-method", default=None)
    parser.add_argument("--output-csv", default=None)
    return parser.parse_args()


def metric_mean(method_summary: Dict[str, object], metric: str) -> float:
    metrics = method_summary["metrics"]
    value = metrics[metric]["mean"]
    if value is None:
        raise ValueError(f"Missing mean for metric {metric}")
    return float(value)


def score_methods(summary: Dict[str, object], reference_method: str | None) -> List[Dict[str, object]]:
    methods = summary["methods"]
    if not methods:
        return []
    if reference_method is None:
        reference_method = "Final" if "Final" in methods else next(iter(methods))
    if reference_method not in methods:
        raise ValueError(f"Reference method not found: {reference_method}")

    ref = methods[reference_method]
    rows = []
    for method_name, method_summary in methods.items():
        score = 0.0
        metric_parts = {}
        for metric, weight in WEIGHTS.items():
            value = metric_mean(method_summary, metric)
            ref_value = metric_mean(ref, metric)
            part = weight * math.log((value + 1e-9) / (ref_value + 1e-9))
            metric_parts[f"{metric}_log_delta"] = part
            score += part
        rows.append(
            {
                "method": method_name,
                "reference_method": reference_method,
                "composite_score": score * 100.0,
                "count": method_summary.get("complete_case_count"),
                **{metric: metric_mean(method_summary, metric) for metric in WEIGHTS},
                **metric_parts,
            }
        )
    return sorted(rows, key=lambda row: float(row["composite_score"]), reverse=True)


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    summary_path = Path(args.summary_json)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    rows = score_methods(summary, args.reference_method)
    if args.output_csv:
        write_csv(Path(args.output_csv), rows)
    print("method\tcomposite_score\tcount")
    for row in rows:
        print(f"{row['method']}\t{float(row['composite_score']):.4f}\t{row['count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
