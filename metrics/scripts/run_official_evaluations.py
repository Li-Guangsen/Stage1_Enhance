from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    python_exe = sys.executable
    registry_path = PROJECT_ROOT / "metrics" / "configs" / "official_method_registry.json"
    manifest_dir = PROJECT_ROOT / "metrics" / "manifests"
    build_manifest_script = PROJECT_ROOT / "metrics" / "scripts" / "build_official_manifests.py"
    eval_script = PROJECT_ROOT / "metrics" / "evaluate_protocol_v2.py"
    stage_output_dir = PROJECT_ROOT / "metrics" / "outputs" / "evaluate_protocol_v2" / "official_stage_progress_full502"
    compare_output_dir = PROJECT_ROOT / "metrics" / "outputs" / "evaluate_protocol_v2" / "official_compare9_complete496"

    run(
        [
            python_exe,
            str(build_manifest_script),
            "--registry",
            str(registry_path),
            "--output-dir",
            str(manifest_dir),
        ]
    )

    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    full_manifest = manifest_dir / "full502_clean_v1.txt"
    compare_manifest = manifest_dir / "compare9_complete496_v1.txt"

    for output_dir in (stage_output_dir, compare_output_dir):
        if output_dir.exists():
            shutil.rmtree(output_dir)

    stage_args = [
        python_exe,
        str(eval_script),
        "--original-dir",
        str(registry["original_dir"]),
        "--manifest",
        str(full_manifest),
        "--output-dir",
        str(stage_output_dir),
    ]
    for method in registry["stage_methods"]:
        stage_args.extend(["--method", f'{method["name"]}={method["directory"]}'])
    run(stage_args)

    compare_args = [
        python_exe,
        str(eval_script),
        "--original-dir",
        str(registry["original_dir"]),
        "--manifest",
        str(compare_manifest),
        "--output-dir",
        str(compare_output_dir),
    ]
    for method in registry["compare_methods"]:
        compare_args.extend(["--method", f'{method["name"]}={method["directory"]}'])
    run(compare_args)

    print(f"[DONE] Stage summary: {stage_output_dir}")
    print(f"[DONE] Compare summary: {compare_output_dir}")


if __name__ == "__main__":
    main()
