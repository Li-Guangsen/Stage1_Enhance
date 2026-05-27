from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


MYEDGE_ROOT = Path("D:/Desktop/MyEdgeCodex")
MYEDGE_SCRIPT_ROOT = MYEDGE_ROOT / "docs/paper_assets/scripts"
if str(MYEDGE_SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(MYEDGE_SCRIPT_ROOT))

from sync_stage1_stagewise_baseline_results import audit_root, make_visuals, rel, save_rgb


RAW_ANCHORS = {
    "msfi_50k_raw_anchor": MYEDGE_ROOT / "output_test/MSFI/algae/ema_slide_50k",
    "diffusionedge_baseline_50k_raw_anchor": (
        MYEDGE_ROOT / "output_test/baseline_diffusionedge/50k_pre_refresh_20260522"
    ),
}

LEGACY_ANCHORS = {
    "msfi_50k_legacy_stage1_final_p1": (
        MYEDGE_ROOT / "output_test/stage1_coupling/msfi_50k/stage1_final_168_p1_20260524"
    ),
    "diffusionedge_baseline_50k_legacy_stage1_final_p1": (
        MYEDGE_ROOT
        / "output_test/stage1_coupling/diffusionedge_baseline_50k/stage1_final_168_p1_20260525"
    ),
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_manifest(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def parse_ac_from_report(path: Path) -> float | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"Average Crispness \(AC\):\s*([0-9.]+)", text)
    if match:
        return float(match.group(1))
    for line in reversed([x.strip() for x in text.splitlines() if x.strip()]):
        nums: list[float] = []
        for part in re.split(r"\s+|\|", line):
            try:
                nums.append(float(part))
            except ValueError:
                continue
        if len(nums) >= 4:
            return nums[-1]
    return None


def detector_label(detector: str) -> str:
    if detector == "msfi_50k":
        return "Ours / MSFI 50k"
    if detector == "diffusionedge_baseline_50k":
        return "DiffusionEdge baseline 50k"
    return detector


def status_from_audit(root: Path, audit: dict[str, Any]) -> str:
    if not root.exists():
        return "not_started"
    if audit["core_complete"] and audit["report_assets_complete"]:
        return "complete_with_report_assets"
    if audit["core_complete"]:
        return "core_results_ready_for_report_sync"
    return "incomplete_or_failed"


def sync_assets(
    root: Path,
    input_root: Path,
    rows: list[dict[str, str]],
    threshold: float,
    overwrite: bool,
) -> dict[str, int]:
    generated = {"white": 0, "overlay": 0, "error_map": 0}
    for row in rows:
        stem = row["stem"]
        visuals = make_visuals(
            input_root / f"{stem}.png",
            Path(row["annotation_path"]),
            root / "mat" / f"{stem}.mat",
            threshold,
        )
        for key, arr in visuals.items():
            out = root / key / f"{stem}.png"
            existed = out.exists()
            save_rgb(out, arr, overwrite)
            if overwrite or not existed:
                generated[key] += 1
    return generated


def write_run_manifest(
    root: Path,
    input_root: Path,
    rows: list[dict[str, str]],
    run_id: str,
    candidate_label: str,
    threshold: float,
    asset_origin: str,
    overwrite: bool,
) -> None:
    path = root / "manifest.csv"
    if path.exists() and not overwrite:
        return
    fields = [
        "run_id",
        "variant",
        "stem",
        "staged_input",
        "gt",
        "output_mat",
        "output_png",
        "output_nms",
        "output_white",
        "output_overlay",
        "output_error_map",
        "visual_threshold",
        "asset_origin",
        "paper_table_entry",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            stem = row["stem"]
            writer.writerow(
                {
                    "run_id": run_id,
                    "variant": candidate_label,
                    "stem": stem,
                    "staged_input": rel(input_root / f"{stem}.png"),
                    "gt": row["annotation_path"],
                    "output_mat": rel(root / "mat" / f"{stem}.mat"),
                    "output_png": rel(root / "png" / f"{stem}.png"),
                    "output_nms": rel(root / "nms" / f"{stem}.png"),
                    "output_white": rel(root / "white" / f"{stem}.png"),
                    "output_overlay": rel(root / "overlay" / f"{stem}.png"),
                    "output_error_map": rel(root / "error_map" / f"{stem}.png"),
                    "visual_threshold": f"{threshold:.6f}",
                    "asset_origin": asset_origin,
                    "paper_table_entry": "diagnostic_not_main_table",
                }
            )


def write_run_report(
    root: Path,
    detector: str,
    candidate_label: str,
    asset_origin: str,
    audit: dict[str, Any],
    generated: dict[str, int],
    overwrite: bool,
) -> None:
    path = root / "run_report.md"
    if path.exists() and not overwrite:
        return
    mat = audit.get("mat_eval") or {}
    nms = audit.get("nms_eval") or {}
    lines = [
        f"# {candidate_label} to {detector} Run Report",
        "",
        f"Date: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Summary",
        "",
        f"- Variant: `{candidate_label}`",
        f"- Detector: `{detector_label(detector)}`",
        "- Scope: `168-image MyEdge ALGAE test split`",
        f"- Output root: `{rel(root)}`",
        f"- Asset origin: `{asset_origin}`",
        "- Paper table entry: `diagnostic_not_main_table`",
        "",
        "## Metric Evidence",
        "",
        "| ODS | OIS | AP | AC |",
        "|---:|---:|---:|---:|",
        f"| {mat.get('ods')} | {mat.get('ois')} | {mat.get('ap')} | {audit.get('ac')} |",
        "",
        "Supplementary NMS:",
        "",
        "| ODS | OIS | AP |",
        "|---:|---:|---:|",
        f"| {nms.get('ods')} | {nms.get('ois')} | {nms.get('ap')} |",
        "",
        "## Output Counts",
        "",
        "| Asset | Count |",
        "|---|---:|",
    ]
    for key, value in (audit.get("counts") or {}).items():
        lines.append(f"| `{key}` | {value} |")
    lines.extend(
        [
            "",
            "## Visualization Sync",
            "",
            f"- Generated/overwritten white: `{generated.get('white', 0)}`",
            f"- Generated/overwritten overlay: `{generated.get('overlay', 0)}`",
            f"- Generated/overwritten error_map: `{generated.get('error_map', 0)}`",
            "",
            "## Boundary",
            "",
            "- This run is a single Stage1 downstream-driven fixed-detector candidate.",
            "- It must be interpreted against raw-input anchors and legacy Stage1 Final P1.",
            "- It does not replace the locked Stage1 full506 formal mainline.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def summarize_candidate_run(
    run: dict[str, Any],
    rows: list[dict[str, str]],
    candidate_label: str,
    asset_origin: str,
    expected_count: int,
    write_assets: bool,
    overwrite: bool,
) -> dict[str, Any]:
    root = Path(run["output_root"])
    input_root = Path(run["staging_root"])
    initial = audit_root(root, expected_count)
    mat = initial.get("mat_eval") or {}
    threshold = mat.get("threshold")
    generated = {"white": 0, "overlay": 0, "error_map": 0}
    action = "intake_only"
    if write_assets and threshold is not None and initial.get("core_complete"):
        generated = sync_assets(root, input_root, rows, float(threshold), overwrite)
        write_run_manifest(
            root,
            input_root,
            rows,
            run["run_id"],
            candidate_label,
            float(threshold),
            asset_origin,
            overwrite,
        )
        write_run_report(
            root,
            run["detector"],
            candidate_label,
            asset_origin,
            initial,
            generated,
            overwrite,
        )
        action = "report_assets_synced"

    final = audit_root(root, expected_count)
    status = status_from_audit(root, final)
    return {
        "detector": run["detector"],
        "variant": candidate_label,
        "source_preflight_variant": run.get("variant"),
        "run_id": run["run_id"],
        "expected_count": expected_count,
        "preflight_ready": run.get("ready_for_sampling_after_confirmation"),
        "action": action,
        "generated": generated,
        "status": status,
        **final,
    }


def summarize_anchor(label: str, root: Path, expected_count: int, raw: bool) -> dict[str, Any]:
    audit = audit_root(root, expected_count)
    if raw:
        raw_complete = (
            root.exists()
            and audit["counts"]["png"] == expected_count
            and audit["counts"]["mat"] == expected_count
            and audit["counts"]["nms"] == expected_count
            and audit["required_file_exists"]["mat_eval"]
            and audit["required_file_exists"]["nms_eval"]
            and audit["report_assets_complete"]
        )
        audit["core_complete"] = raw_complete
        status = "complete_historical_anchor_no_sample_log" if raw_complete else "incomplete_or_failed"
        if audit.get("ac") is None:
            audit["ac"] = parse_ac_from_report(root / "run_report.md")
    else:
        status = status_from_audit(root, audit)
    return {"label": label, "expected_count": expected_count, "status": status, **audit}


def write_summary_csv(path: Path, report: dict[str, Any], run_key: str) -> None:
    fields = [
        "source",
        "label",
        "detector",
        "status",
        "ods",
        "ois",
        "ap",
        "ac",
        "nms_ods",
        "nms_ois",
        "nms_ap",
        "root",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for run in report[run_key]:
            mat = run.get("mat_eval") or {}
            nms = run.get("nms_eval") or {}
            writer.writerow(
                {
                    "source": "candidate_run",
                    "label": run["variant"],
                    "detector": run["detector"],
                    "status": run["status"],
                    "ods": mat.get("ods"),
                    "ois": mat.get("ois"),
                    "ap": mat.get("ap"),
                    "ac": run.get("ac"),
                    "nms_ods": nms.get("ods"),
                    "nms_ois": nms.get("ois"),
                    "nms_ap": nms.get("ap"),
                    "root": run.get("root"),
                }
            )
        for anchor in report["context_anchors"]:
            mat = anchor.get("mat_eval") or {}
            nms = anchor.get("nms_eval") or {}
            writer.writerow(
                {
                    "source": "context_anchor",
                    "label": anchor["label"],
                    "detector": "",
                    "status": anchor["status"],
                    "ods": mat.get("ods"),
                    "ois": mat.get("ois"),
                    "ap": mat.get("ap"),
                    "ac": anchor.get("ac"),
                    "nms_ods": nms.get("ods"),
                    "nms_ois": nms.get("ois"),
                    "nms_ap": nms.get("ap"),
                    "root": anchor.get("root"),
                }
            )


def write_summary_md(path: Path, report: dict[str, Any], run_key: str) -> None:
    lines = [
        f"# {report['title']}",
        "",
        f"Date: {report['date']}",
        "",
        "## Candidate Runs",
        "",
        "| Detector | Variant | Status | ODS | OIS | AP | AC |",
        "|---|---|---|---:|---:|---:|---:|",
    ]
    for run in report[run_key]:
        mat = run.get("mat_eval") or {}
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{run['detector']}`",
                    f"`{run['variant']}`",
                    f"`{run['status']}`",
                    str(mat.get("ods")),
                    str(mat.get("ois")),
                    str(mat.get("ap")),
                    str(run.get("ac")),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Context Anchors",
            "",
            "| Label | Status | ODS | OIS | AP | AC |",
            "|---|---|---:|---:|---:|---:|",
        ]
    )
    for anchor in report["context_anchors"]:
        mat = anchor.get("mat_eval") or {}
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{anchor['label']}`",
                    f"`{anchor['status']}`",
                    str(mat.get("ods")),
                    str(mat.get("ois")),
                    str(mat.get("ap")),
                    str(anchor.get("ac")),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Intake/sync only; this script does not run Stage1 enhancement, MyEdge sampling, eval.py, show.py, or training.",
            "- The result remains a fixed-detector 168 split diagnostic until structure proxy and downstream gate are generated.",
            "- Do not use this report to replace the locked Stage1 formal mainline or 502/496 enhancement protocol.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync one MyEdge fixed-detector Stage1 candidate result intake.")
    parser.add_argument("--preflight-json", type=Path, required=True)
    parser.add_argument("--out-prefix", type=Path, required=True)
    parser.add_argument("--run-key", required=True)
    parser.add_argument("--candidate-label", required=True)
    parser.add_argument("--asset-origin", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--expected-count", type=int, default=168)
    parser.add_argument("--write-assets", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    preflight = read_json(args.preflight_json)
    rows = read_manifest(Path(preflight["manifest"]))
    runs = [
        summarize_candidate_run(
            run,
            rows,
            args.candidate_label,
            args.asset_origin,
            args.expected_count,
            args.write_assets,
            args.overwrite,
        )
        for run in preflight["runs"]
    ]
    context = [
        *(summarize_anchor(label, root, args.expected_count, raw=True) for label, root in RAW_ANCHORS.items()),
        *(summarize_anchor(label, root, args.expected_count, raw=False) for label, root in LEGACY_ANCHORS.items()),
    ]
    complete = all(run["status"] == "complete_with_report_assets" for run in runs)
    report = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": args.title,
        "asset_origin": args.asset_origin,
        "run_key": args.run_key,
        "overall_status": "complete_with_report_assets" if complete else "candidate_results_incomplete_or_partial",
        "preflight_json": rel(args.preflight_json),
        "expected_count": args.expected_count,
        "manifest_rows": len(rows),
        "write_assets": bool(args.write_assets),
        "no_sampling_or_eval": True,
        args.run_key: runs,
        "context_anchors": context,
        "boundary": "Intake/sync only; downstream claims require structure proxy and downstream gate.",
    }
    args.out_prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = args.out_prefix.with_suffix(".json")
    md_path = args.out_prefix.with_suffix(".md")
    csv_path = args.out_prefix.with_suffix(".csv")
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_summary_csv(csv_path, report, args.run_key)
    write_summary_md(md_path, report, args.run_key)
    print(
        json.dumps(
            {
                "status": report["overall_status"],
                "json": rel(json_path),
                "md": rel(md_path),
                "csv": rel(csv_path),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
