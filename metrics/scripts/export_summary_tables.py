from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


METRICS = ["EME", "EMEE", "Entropy", "Contrast", "AvgGra", "MS_SSIM", "PSNR", "UCIQE", "UIQM"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export compact CSV/Markdown tables from summary.json.")
    parser.add_argument("summary_json")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    summary_path = Path(args.summary_json).resolve()
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    output_dir = summary_path.parent

    rows = []
    for method_name, payload in summary["methods"].items():
        row = {
            "Method": method_name,
            "Count": payload["complete_case_count"],
        }
        for metric in METRICS:
            row[metric] = payload["metrics"][metric]["mean"]
        rows.append(row)

    csv_path = output_dir / "mean_metrics_table.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["Method", "Count", *METRICS])
        writer.writeheader()
        for row in rows:
            out = dict(row)
            for metric in METRICS:
                out[metric] = f"{out[metric]:.4f}"
            writer.writerow(out)

    md_path = output_dir / "mean_metrics_table.md"
    header = "| Method | Count | " + " | ".join(METRICS) + " |"
    sep = "|---|---:|" + "|".join(["---:"] * len(METRICS)) + "|"
    lines = [header, sep]
    for row in rows:
        values = [row["Method"], str(row["Count"])] + [f"{row[metric]:.4f}" for metric in METRICS]
        lines.append("| " + " | ".join(values) + " |")
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[DONE] {csv_path}")
    print(f"[DONE] {md_path}")


if __name__ == "__main__":
    main()
