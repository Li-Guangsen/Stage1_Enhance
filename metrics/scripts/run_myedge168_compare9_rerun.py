from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import cv2
import numpy as np


STAGE1_ROOT = Path(__file__).resolve().parents[2]
METRICS_ROOT = STAGE1_ROOT / "metrics"
MYEDGE_RAW_DIR = Path("D:/Desktop/MyEdgeCodex/input_test/algae")
RUN_ROOT = STAGE1_ROOT / "experiments" / "myedge168_compare9_rerun_20260527"
PYTHON_EXE = Path("D:/Desktop/DeepLearning/my_env/python.exe")
MATLAB_EXE = Path("D:/MATLAB/R2024a/bin/matlab.exe")

IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp")
STAGE_SUFFIXES = (
    "_Final",
    "_Fused",
    "_BPH",
    "_IMF1Ray",
    "_RGHS",
    "_CLAHE",
    "_HVDual",
    "_AbcFormer",
    "_GDCP",
    "_CBF",
    "_HLRP",
    "_SGUIEnet",
    "_Histoformer",
    "_WWPF",
)
NOISE_REFERENCE_METHODS = {"HLRP", "Histoformer"}


@dataclass(frozen=True)
class ManifestRow:
    index: int
    filename: str
    stem: str
    suffix: str
    size_bytes: int
    width: int
    height: int
    channels: int
    sha256: str
    source_path: Path


@dataclass(frozen=True)
class MethodRun:
    name: str
    raw_output_dir: Path
    normalized_output_dir: Path
    command: Sequence[str]
    cwd: Path
    env: Dict[str, str]
    count_dir: Path


def ps(path: Path | str) -> str:
    return str(path).replace("\\", "/")


def read_bgr(path: Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"cv2.imdecode failed: {path}")
    return img


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def list_images(root: Path) -> List[Path]:
    if not root.is_dir():
        return []
    return sorted(
        [p for p in root.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS],
        key=lambda p: p.name.lower(),
    )


def list_images_recursive(root: Path) -> List[Path]:
    if not root.is_dir():
        return []
    return sorted(
        [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS],
        key=lambda p: str(p).lower(),
    )


def normalize_stem(stem: str) -> str:
    out = stem
    changed = True
    while changed:
        changed = False
        for suffix in STAGE_SUFFIXES:
            if out.lower().endswith(suffix.lower()):
                out = out[: -len(suffix)]
                changed = True
                break
    return out


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_csv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def build_manifest() -> List[ManifestRow]:
    paths = list_images(MYEDGE_RAW_DIR)
    if len(paths) != 168:
        raise RuntimeError(f"MyEdge raw image count must be 168, got {len(paths)}: {MYEDGE_RAW_DIR}")

    rows: List[ManifestRow] = []
    seen_stems = set()
    for idx, path in enumerate(paths, start=1):
        if path.stem in seen_stems:
            raise RuntimeError(f"Duplicate raw stem in MyEdge input: {path.stem}")
        seen_stems.add(path.stem)
        img = read_bgr(path)
        h, w = img.shape[:2]
        channels = 1 if img.ndim == 2 else img.shape[2]
        rows.append(
            ManifestRow(
                index=idx,
                filename=path.name,
                stem=path.stem,
                suffix=path.suffix.lower(),
                size_bytes=path.stat().st_size,
                width=w,
                height=h,
                channels=channels,
                sha256=sha256_file(path),
                source_path=path,
            )
        )
    return rows


def write_manifest_files(rows: Sequence[ManifestRow]) -> None:
    manifest_dir = ensure_dir(RUN_ROOT / "manifests")
    csv_rows = [
        {
            "index": row.index,
            "filename": row.filename,
            "stem": row.stem,
            "suffix": row.suffix,
            "size_bytes": row.size_bytes,
            "width": row.width,
            "height": row.height,
            "channels": row.channels,
            "sha256": row.sha256,
            "source_path": str(row.source_path),
        }
        for row in rows
    ]
    write_csv(
        manifest_dir / "myedge168_input_manifest.csv",
        csv_rows,
        [
            "index",
            "filename",
            "stem",
            "suffix",
            "size_bytes",
            "width",
            "height",
            "channels",
            "sha256",
            "source_path",
        ],
    )
    (manifest_dir / "myedge168_filenames.txt").write_text(
        "\n".join(row.filename for row in rows) + "\n",
        encoding="utf-8",
    )
    (manifest_dir / "myedge168_stems.txt").write_text(
        "\n".join(row.stem for row in rows) + "\n",
        encoding="utf-8",
    )


def copy_inputs(rows: Sequence[ManifestRow]) -> Path:
    input_dir = ensure_dir(RUN_ROOT / "inputs" / "raw")
    for row in rows:
        target = input_dir / row.filename
        if not target.exists():
            shutil.copy2(row.source_path, target)
        elif sha256_file(target) != row.sha256:
            raise RuntimeError(f"Existing copied input differs from source: {target}")
    return input_dir


def matlab_quote(path: Path | str) -> str:
    return str(path).replace("\\", "\\\\").replace("'", "''")


def write_matlab_wrappers(input_dir: Path) -> Dict[str, Path]:
    wrapper_dir = ensure_dir(RUN_ROOT / "matlab_wrappers")

    gdcp_repo = Path("D:/Desktop/2018_Generalization-of-the-Dark-Channel-Prior")
    gdcp_out = RUN_ROOT / "outputs_raw" / "GDCP"
    gdcp = wrapper_dir / "run_gdcp_myedge168.m"
    gdcp.write_text(
        "\n".join(
            [
                "clear; clc; close all;",
                f"setenv('GDCP_INPUT_DIR','{matlab_quote(input_dir)}');",
                f"setenv('GDCP_OUTPUT_DIR','{matlab_quote(gdcp_out)}');",
                f"cd('{matlab_quote(gdcp_repo)}');",
                "IR_GDCP;",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    wwpf_repo = Path("D:/Desktop/2024_WWPF_code/2023-WWPE")
    wwpf_out = RUN_ROOT / "outputs_raw" / "WWPF"
    wwpf = wrapper_dir / "run_wwpf_myedge168.m"
    wwpf.write_text(
        "\n".join(
            [
                "clear; clc; close all;",
                f"setenv('WWPF_INPUT_DIR','{matlab_quote(input_dir)}');",
                f"setenv('WWPF_OUTPUT_DIR','{matlab_quote(wwpf_out)}');",
                f"cd('{matlab_quote(wwpf_repo)}');",
                "WWPE;",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    cbf_repo = Path("D:/Desktop/2018_Color-Balance-and-fusion-for-underwater-image-enhancement")
    cbf_out = RUN_ROOT / "outputs_raw" / "CBF"
    cbf = wrapper_dir / "run_cbf_myedge168.m"
    cbf.write_text(
        f"""clear; clc; close all;
repo = '{matlab_quote(cbf_repo)}';
input_dir = '{matlab_quote(input_dir)}';
output_dir = '{matlab_quote(cbf_out)}';
addpath(repo);
if ~exist(output_dir, 'dir'), mkdir(output_dir); end
exts = {{'*.jpg','*.jpeg','*.png','*.bmp','*.tif','*.tiff'}};
files = [];
for e = 1:numel(exts)
    files = [files; dir(fullfile(input_dir, exts{{e}}))]; %#ok<AGROW>
end
fprintf('Found %d images in %s\\n', numel(files), input_dir);
for i = 1:numel(files)
    fn = files(i).name;
    try
        fprintf('[%d/%d] %s\\n', i, numel(files), fn);
        rgbImage = im2double(imread(fullfile(input_dir, fn)));
        if ndims(rgbImage) == 2, rgbImage = repmat(rgbImage, [1 1 3]); end
        Ir = rgbImage(:,:,1); Ig = rgbImage(:,:,2); Ib = rgbImage(:,:,3);
        Ir_mean = mean(Ir(:)); Ig_mean = mean(Ig(:)); Ib_mean = mean(Ib(:));
        alpha = 0.1;
        Irc = Ir + alpha * (Ig_mean - Ir_mean);
        alpha = 0;
        Ibc = Ib + alpha * (Ig_mean - Ib_mean);
        I = cat(3, Irc, Ig, Ibc);
        I = min(max(I, 0), 1);
        I_lin = rgb2lin(I);
        percentiles = 5;
        illuminant = illumgray(I_lin, percentiles);
        I_lin = chromadapt(I_lin, illuminant, 'ColorSpace', 'linear-rgb');
        Iwb = lin2rgb(I_lin);
        Iwb = min(max(Iwb, 0), 1);
        Igamma = imadjust(Iwb, [], [], 2);
        sigma = 20;
        Igauss = Iwb;
        N = 30;
        for iter = 1:N
            Igauss = imgaussfilt(Igauss, sigma);
            Igauss = min(Iwb, Igauss);
        end
        gain = 1;
        Norm = Iwb - gain * Igauss;
        for n = 1:3
            Norm(:,:,n) = histeq(Norm(:,:,n));
        end
        Isharp = (Iwb + Norm) / 2;
        Isharp = min(max(Isharp, 0), 1);
        Igamma = min(max(Igamma, 0), 1);
        Isharp_lab = rgb2lab(Isharp);
        Igamma_lab = rgb2lab(Igamma);
        R1 = double(Isharp_lab(:,:,1)) / 255;
        WC1 = sqrt(((Isharp(:,:,1)-R1).^2 + (Isharp(:,:,2)-R1).^2 + (Isharp(:,:,3)-R1).^2) / 3);
        WS1 = saliency_detection(Isharp); WS1 = WS1 / max(WS1, [], 'all');
        WSAT1 = sqrt(1/3 * ((Isharp(:,:,1)-R1).^2 + (Isharp(:,:,2)-R1).^2 + (Isharp(:,:,3)-R1).^2));
        R2 = double(Igamma_lab(:,:,1)) / 255;
        WC2 = sqrt(((Igamma(:,:,1)-R2).^2 + (Igamma(:,:,2)-R2).^2 + (Igamma(:,:,3)-R2).^2) / 3);
        WS2 = saliency_detection(Igamma); WS2 = WS2 / max(WS2, [], 'all');
        WSAT2 = sqrt(1/3 * ((Igamma(:,:,1)-R1).^2 + (Igamma(:,:,2)-R1).^2 + (Igamma(:,:,3)-R1).^2));
        W1 = (WC1 + WS1 + WSAT1 + 0.1) ./ (WC1 + WS1 + WSAT1 + WC2 + WS2 + WSAT2 + 0.2);
        W2 = (WC2 + WS2 + WSAT2 + 0.1) ./ (WC1 + WS1 + WSAT1 + WC2 + WS2 + WSAT2 + 0.2);
        level = 10;
        Weight1 = gaussian_pyramid(W1, level);
        Weight2 = gaussian_pyramid(W2, level);
        R1p = laplacian_pyramid(Isharp(:,:,1), level);
        G1p = laplacian_pyramid(Isharp(:,:,2), level);
        B1p = laplacian_pyramid(Isharp(:,:,3), level);
        R2p = laplacian_pyramid(Igamma(:,:,1), level);
        G2p = laplacian_pyramid(Igamma(:,:,2), level);
        B2p = laplacian_pyramid(Igamma(:,:,3), level);
        for k = 1:level
            Rr{{k}} = Weight1{{k}} .* R1p{{k}} + Weight2{{k}} .* R2p{{k}}; %#ok<SAGROW>
            Rg{{k}} = Weight1{{k}} .* G1p{{k}} + Weight2{{k}} .* G2p{{k}}; %#ok<SAGROW>
            Rb{{k}} = Weight1{{k}} .* B1p{{k}} + Weight2{{k}} .* B2p{{k}}; %#ok<SAGROW>
        end
        fusion = cat(3, pyramid_reconstruct(Rr), pyramid_reconstruct(Rg), pyramid_reconstruct(Rb));
        fusion = min(max(fusion, 0), 1);
        [~, stem, ~] = fileparts(fn);
        imwrite(fusion, fullfile(output_dir, [stem '_CBF.jpg']));
    catch ME
        fprintf('ERROR on %s: %s\\n', fn, ME.message);
        rethrow(ME);
    end
end
fprintf('Done. Results saved to: %s\\n', output_dir);
""",
        encoding="utf-8",
    )

    hlrp_repo = Path("D:/Desktop/2022_HLRP-main/HLRP_Code")
    hlrp_out = RUN_ROOT / "outputs_raw" / "HLRP"
    hlrp = wrapper_dir / "run_hlrp_myedge168.m"
    hlrp.write_text(
        f"""clear; clc; close all;
repo = '{matlab_quote(hlrp_repo)}';
input_dir = '{matlab_quote(input_dir)}';
output_dir = '{matlab_quote(hlrp_out)}';
addpath(repo);
if ~exist(output_dir, 'dir'), mkdir(output_dir); end
exts = {{'*.jpg','*.jpeg','*.png','*.bmp','*.tif','*.tiff'}};
files = [];
for e = 1:numel(exts)
    files = [files; dir(fullfile(input_dir, exts{{e}}))]; %#ok<AGROW>
end
fprintf('Found %d images in %s\\n', numel(files), input_dir);
ecoff = 2.0;
for i = 1:numel(files)
    fn = files(i).name;
    try
        fprintf('[%d/%d] %s\\n', i, numel(files), fn);
        img1 = double(imread(fullfile(input_dir, fn)));
        if ndims(img1) == 2, img1 = repmat(img1, [1 1 3]); end
        enhanced = HLRP(img1, ecoff);
        enhanced = min(max(enhanced, 0), 255);
        [~, stem, ~] = fileparts(fn);
        imwrite(uint8(enhanced), fullfile(output_dir, [stem '_HLRP.jpg']));
    catch ME
        fprintf('ERROR on %s: %s\\n', fn, ME.message);
        rethrow(ME);
    end
end
fprintf('Done. Results saved to: %s\\n', output_dir);
""",
        encoding="utf-8",
    )

    return {"GDCP": gdcp, "CBF": cbf, "HLRP": hlrp, "WWPF": wwpf}


def preflight(rows: Sequence[ManifestRow]) -> None:
    required_paths = [
        PYTHON_EXE,
        MATLAB_EXE,
        STAGE1_ROOT / "main.py",
        STAGE1_ROOT / "experiments" / "optimization_v1" / "configs" / "locked_full506_final_mainline.json",
        Path("D:/Desktop/2025AAAI_HVDual_former/test_d8.py"),
        Path("D:/Desktop/2025AAAI_HVDual_former/checkpoints/cubed8/Histoformer_3_epoch_207.pth"),
        Path("D:/Desktop/2025AAAI_HVDual_former/checkpoints/cubed8/CAformer_3_epoch_207.pth"),
        Path("D:/Desktop/2025CVPR_ABC-Former/ABC-Former/test.py"),
        Path("D:/Desktop/2025CVPR_ABC-Former/Mixed-illuminant/Hist_d16.pth"),
        Path("D:/Desktop/2025CVPR_ABC-Former/Mixed-illuminant/Lab_d16.pth"),
        Path("D:/Desktop/2025CVPR_ABC-Former/Mixed-illuminant/sRGB_d16.pth"),
        Path("D:/Desktop/2018_Generalization-of-the-Dark-Channel-Prior/IR_GDCP.m"),
        Path("D:/Desktop/2018_Color-Balance-and-fusion-for-underwater-image-enhancement/main.m"),
        Path("D:/Desktop/2022_HLRP-main/HLRP_Code/HLRP.p"),
        Path("D:/Desktop/2022_SGUIE_Net_Simple/test.py"),
        Path("D:/Desktop/2022_SGUIE_Net_Simple/checkpoints/test_name/latest_net_G.pth"),
        Path("D:/Desktop/2024_Histoformer-main/test.py"),
        Path("D:/Desktop/2024_Histoformer-main/checkpoints/Histoformer-PQR_288_modifyloss.pth"),
        Path("D:/Desktop/2024_Histoformer-main/checkpoints/Histoformer-PQR_netG_288_modifyloss.pth"),
        Path("D:/Desktop/2024_WWPF_code/2023-WWPE/WWPE.m"),
    ]
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        raise RuntimeError("Preflight missing required paths:\n" + "\n".join(missing))
    if len(rows) != 168:
        raise RuntimeError(f"Expected 168 manifest rows, got {len(rows)}")


def method_runs(input_dir: Path, wrappers: Dict[str, Path]) -> List[MethodRun]:
    logs_dir = ensure_dir(RUN_ROOT / "logs")
    raw_root = RUN_ROOT / "outputs_raw"
    norm_root = RUN_ROOT / "outputs_normalized"
    manifest_txt = RUN_ROOT / "manifests" / "myedge168_filenames.txt"
    base_env = os.environ.copy()

    runs: List[MethodRun] = []

    ours_out = raw_root / "Ours"
    runs.append(
        MethodRun(
            name="Ours",
            raw_output_dir=ours_out,
            normalized_output_dir=norm_root / "Ours",
            command=[
                str(PYTHON_EXE),
                "main.py",
                "--input-dir",
                str(input_dir),
                "--output-dir",
                str(ours_out),
                "--manifest",
                str(manifest_txt),
                "--params-json",
                str(STAGE1_ROOT / "experiments" / "optimization_v1" / "configs" / "locked_full506_final_mainline.json"),
                "--skip-existing",
            ],
            cwd=STAGE1_ROOT,
            env=base_env,
            count_dir=ours_out / "png" / "Final",
        )
    )

    hv_out = raw_root / "HVDualformer"
    env = dict(base_env)
    env["HV_TEST_DIR"] = str(input_dir)
    runs.append(
        MethodRun(
            name="HVDualformer",
            raw_output_dir=hv_out,
            normalized_output_dir=norm_root / "HVDualformer",
            command=[str(PYTHON_EXE), "test_d8.py", "--save_image_dir", str(hv_out), "--outdir", str(logs_dir / "HVDualformer_txt")],
            cwd=Path("D:/Desktop/2025AAAI_HVDual_former"),
            env=env,
            count_dir=hv_out,
        )
    )

    abc_out = raw_root / "ABC-Former"
    env = dict(base_env)
    env["ABC_TEST_DIR"] = str(input_dir)
    runs.append(
        MethodRun(
            name="ABC-Former",
            raw_output_dir=abc_out,
            normalized_output_dir=norm_root / "ABC-Former",
            command=[
                str(PYTHON_EXE),
                "test.py",
                "--save_image_dir",
                str(abc_out),
                "--outdir",
                str(logs_dir / "ABC-Former_txt"),
            ],
            cwd=Path("D:/Desktop/2025CVPR_ABC-Former/ABC-Former"),
            env=env,
            count_dir=abc_out,
        )
    )

    for name in ["GDCP", "CBF", "HLRP", "WWPF"]:
        raw_out = raw_root / name
        runs.append(
            MethodRun(
                name=name,
                raw_output_dir=raw_out,
                normalized_output_dir=norm_root / name,
                command=[str(MATLAB_EXE), "-batch", f"run('{ps(wrappers[name])}')"],
                cwd=wrappers[name].parent,
                env=base_env,
                count_dir=raw_out,
            )
        )

    sguie_parent = raw_root / "SGUIE-Net_parent"
    sguie_count = sguie_parent / "test_name"
    runs.append(
        MethodRun(
            name="SGUIE-Net",
            raw_output_dir=sguie_count,
            normalized_output_dir=norm_root / "SGUIE-Net",
            command=[
                str(PYTHON_EXE),
                "test.py",
                "--dataroot",
                str(input_dir),
                "--name",
                "test_name",
                "--model",
                "test_SGUIE",
                "--results_dir",
                str(sguie_parent),
                "--num_test",
                "168",
                "--gpu_ids",
                "0",
            ],
            cwd=Path("D:/Desktop/2022_SGUIE_Net_Simple"),
            env=base_env,
            count_dir=sguie_count,
        )
    )

    histo_out = raw_root / "Histoformer"
    env = dict(base_env)
    env["HISTOFORMER_TEST_DIR"] = str(input_dir)
    runs.append(
        MethodRun(
            name="Histoformer",
            raw_output_dir=histo_out,
            normalized_output_dir=norm_root / "Histoformer",
            command=[str(PYTHON_EXE), "test.py", "--save_image_dir", str(histo_out)],
            cwd=Path("D:/Desktop/2024_Histoformer-main"),
            env=env,
            count_dir=histo_out,
        )
    )

    return runs


def output_count(path: Path) -> int:
    return len(list_images_recursive(path))


def run_subprocess(method: MethodRun) -> int:
    ensure_dir(method.raw_output_dir)
    ensure_dir(method.count_dir)
    log_path = ensure_dir(RUN_ROOT / "logs") / f"{method.name}.log"
    command_txt = " ".join(f'"{part}"' if " " in part else part for part in method.command)
    print(f"[RUN] {method.name}")
    print(f"[CMD] {command_txt}")
    print(f"[LOG] {log_path}")

    start = time.time()
    next_report = start + 60.0
    with log_path.open("w", encoding="utf-8", errors="replace") as log:
        log.write(f"# {method.name}\n")
        log.write(f"cwd: {method.cwd}\n")
        log.write(f"command: {command_txt}\n")
        log.write(f"started_at: {datetime.now().isoformat(timespec='seconds')}\n\n")
        log.flush()
        proc = subprocess.Popen(
            list(method.command),
            cwd=str(method.cwd),
            env=method.env,
            stdout=log,
            stderr=subprocess.STDOUT,
            text=True,
        )
        while proc.poll() is None:
            now = time.time()
            if now >= next_report:
                elapsed = int(now - start)
                count = output_count(method.count_dir)
                print(f"[PROGRESS] {method.name}: elapsed={elapsed}s, outputs={count}/168, log={log_path}")
                next_report = now + 60.0
            time.sleep(5)
        code = proc.returncode
        elapsed = int(time.time() - start)
        count = output_count(method.count_dir)
        log.write(f"\nfinished_at: {datetime.now().isoformat(timespec='seconds')}\n")
        log.write(f"exit_code: {code}\n")
        log.write(f"elapsed_sec: {elapsed}\n")
        log.write(f"output_count_observed: {count}\n")
    print(f"[DONE] {method.name}: exit={code}, elapsed={elapsed}s, outputs={count}/168")
    return int(code)


def run_ours_parallel(method: MethodRun, rows: Sequence[ManifestRow], workers: int) -> int:
    workers = max(1, int(workers))
    chunk_dir = ensure_dir(RUN_ROOT / "manifests" / "ours_chunks")
    logs_dir = ensure_dir(RUN_ROOT / "logs")
    ensure_dir(method.count_dir)
    chunks: List[List[ManifestRow]] = [[] for _ in range(workers)]
    for i, row in enumerate(rows):
        chunks[i % workers].append(row)

    procs: List[Tuple[int, subprocess.Popen[bytes], Path]] = []
    start = time.time()
    for idx, chunk in enumerate(chunks, start=1):
        if not chunk:
            continue
        manifest = chunk_dir / f"chunk_{idx:02d}.txt"
        manifest.write_text("\n".join(row.filename for row in chunk) + "\n", encoding="utf-8")
        log_path = logs_dir / f"Ours_chunk_{idx:02d}.log"
        cmd = [
            str(PYTHON_EXE),
            "main.py",
            "--input-dir",
            str(RUN_ROOT / "inputs" / "raw"),
            "--output-dir",
            str(method.raw_output_dir),
            "--manifest",
            str(manifest),
            "--params-json",
            str(STAGE1_ROOT / "experiments" / "optimization_v1" / "configs" / "locked_full506_final_mainline.json"),
            "--skip-existing",
        ]
        command_txt = " ".join(f'"{part}"' if " " in part else part for part in cmd)
        log = log_path.open("w", encoding="utf-8", errors="replace")
        log.write(f"# Ours chunk {idx}\n")
        log.write(f"cwd: {STAGE1_ROOT}\n")
        log.write(f"manifest: {manifest}\n")
        log.write(f"chunk_size: {len(chunk)}\n")
        log.write(f"command: {command_txt}\n")
        log.write(f"started_at: {datetime.now().isoformat(timespec='seconds')}\n\n")
        log.flush()
        proc = subprocess.Popen(
            cmd,
            cwd=str(STAGE1_ROOT),
            env=method.env,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        procs.append((idx, proc, log_path))
    print(f"[RUN] Ours parallel chunks={len(procs)}, workers={workers}")

    next_report = time.time() + 60.0
    while True:
        active = [(idx, proc, log_path) for idx, proc, log_path in procs if proc.poll() is None]
        now = time.time()
        if now >= next_report or not active:
            elapsed = int(now - start)
            count = output_count(method.count_dir)
            active_ids = [idx for idx, _, _ in active]
            print(f"[PROGRESS] Ours parallel: elapsed={elapsed}s, final_png={count}/168, active_chunks={active_ids}")
            next_report = now + 60.0
        if not active:
            break
        time.sleep(5)

    failed = []
    for idx, proc, log_path in procs:
        code = int(proc.returncode)
        with log_path.open("a", encoding="utf-8", errors="replace") as log:
            log.write(f"\nfinished_at: {datetime.now().isoformat(timespec='seconds')}\n")
            log.write(f"exit_code: {code}\n")
        if code != 0:
            failed.append((idx, code, log_path))
    if failed:
        for idx, code, log_path in failed:
            print(f"[FAIL] Ours chunk {idx} exit={code}, log={log_path}")
        return 1
    print(f"[DONE] Ours parallel: final_png={output_count(method.count_dir)}/168")
    return 0


def normalize_method_outputs(method: MethodRun, rows: Sequence[ManifestRow]) -> List[Dict[str, object]]:
    ensure_dir(method.normalized_output_dir)
    images = list_images_recursive(method.count_dir)
    by_stem: Dict[str, Path] = {}
    collisions: List[Tuple[str, Path, Path]] = []
    for path in images:
        stem = normalize_stem(path.stem)
        existing = by_stem.get(stem)
        if existing is not None and existing.resolve() != path.resolve():
            collisions.append((stem, existing, path))
        else:
            by_stem[stem] = path
    if collisions:
        sample = "\n".join(f"{stem}: {first} | {second}" for stem, first, second in collisions[:5])
        raise RuntimeError(f"{method.name} output stem collisions:\n{sample}")

    index_rows: List[Dict[str, object]] = []
    missing: List[str] = []
    for row in rows:
        src = by_stem.get(row.stem)
        if src is None:
            missing.append(row.stem)
            continue
        dst = method.normalized_output_dir / f"{row.stem}{src.suffix.lower()}"
        shutil.copy2(src, dst)
        index_rows.append(
            {
                "method": method.name,
                "stem": row.stem,
                "raw_filename": row.filename,
                "raw_sha256": row.sha256,
                "source_output": str(src),
                "normalized_output": str(dst),
                "output_sha256": sha256_file(dst),
            }
        )
    if missing:
        raise RuntimeError(f"{method.name} missing {len(missing)} normalized outputs, first 10: {missing[:10]}")
    if len(index_rows) != 168:
        raise RuntimeError(f"{method.name} normalized rows expected 168, got {len(index_rows)}")

    write_csv(
        RUN_ROOT / "manifests" / f"{method.name}_normalized_index.csv",
        index_rows,
        ["method", "stem", "raw_filename", "raw_sha256", "source_output", "normalized_output", "output_sha256"],
    )
    return index_rows


def run_metrics() -> Path:
    metrics_output = RUN_ROOT / "metrics" / "enhancement_metrics"
    cmd = [
        str(PYTHON_EXE),
        str(METRICS_ROOT / "evaluate_protocol_v2.py"),
        "--original-dir",
        str(RUN_ROOT / "inputs" / "raw"),
        "--methods-root",
        str(RUN_ROOT / "outputs_normalized"),
        "--manifest",
        str(RUN_ROOT / "manifests" / "myedge168_stems.txt"),
        "--output-dir",
        str(metrics_output),
    ]
    method = MethodRun(
        name="enhancement_metrics",
        raw_output_dir=metrics_output,
        normalized_output_dir=metrics_output,
        command=cmd,
        cwd=STAGE1_ROOT,
        env=os.environ.copy(),
        count_dir=metrics_output,
    )
    code = run_subprocess(method)
    if code != 0:
        raise RuntimeError(f"enhancement metric evaluation failed with exit code {code}")

    export_cmd = [str(PYTHON_EXE), str(METRICS_ROOT / "scripts" / "export_summary_tables.py"), str(metrics_output / "summary.json")]
    export_method = MethodRun(
        name="export_summary_tables",
        raw_output_dir=metrics_output,
        normalized_output_dir=metrics_output,
        command=export_cmd,
        cwd=STAGE1_ROOT,
        env=os.environ.copy(),
        count_dir=metrics_output,
    )
    code = run_subprocess(export_method)
    if code != 0:
        raise RuntimeError(f"summary table export failed with exit code {code}")
    write_primary_tables(metrics_output)
    return metrics_output


def write_primary_tables(metrics_output: Path) -> None:
    source = metrics_output / "mean_metrics_table.csv"
    with source.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    for row in rows:
        row["analysis_role"] = "high_noise_diagnostic_reference" if row["Method"] in NOISE_REFERENCE_METHODS else "primary_reference"

    all_roles = metrics_output / "method_roles.csv"
    write_csv(all_roles, rows, list(rows[0].keys()) if rows else ["Method", "analysis_role"])

    primary_rows = [row for row in rows if row.get("analysis_role") == "primary_reference"]
    primary_csv = metrics_output / "mean_metrics_table_primary_reference.csv"
    fieldnames = [field for field in rows[0].keys() if field != "analysis_role"] if rows else []
    write_csv(primary_csv, primary_rows, fieldnames)

    if fieldnames:
        lines = []
        lines.append("| " + " | ".join(fieldnames) + " |")
        lines.append("|" + "|".join(["---"] + ["---:"] * (len(fieldnames) - 1)) + "|")
        for row in primary_rows:
            lines.append("| " + " | ".join(row[field] for field in fieldnames) + " |")
        (metrics_output / "mean_metrics_table_primary_reference.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_run_report(rows: Sequence[ManifestRow], method_rows: Sequence[Dict[str, object]], metrics_output: Optional[Path]) -> None:
    report = RUN_ROOT / "run_report.md"
    lines = [
        "# MyEdge 168 Compare9 Rerun Report",
        "",
        f"Created at: {datetime.now().isoformat(timespec='seconds')}",
        f"Run root: `{RUN_ROOT}`",
        "",
        "## Scope",
        "",
        "- Data source: `D:/Desktop/MyEdgeCodex/input_test/algae`.",
        "- This run regenerates enhancement outputs for the exact 168 MyEdge edge-detection test images.",
        "- Old Stage1 502/496 outputs are not used as result sources because same-name files are not guaranteed to be byte-identical.",
        "- No DiffusionEdge/MSFI sampling, `eval.py`, `show.py`, 502/496 complete-case, or 2770 full-pool run was executed.",
        "",
        "## Inputs",
        "",
        f"- MyEdge raw images: {len(rows)}",
        "- Input manifest: `manifests/myedge168_input_manifest.csv`",
        "- Copied raw input dir: `inputs/raw`",
        "",
        "## Methods",
        "",
        "| Method | Normalized outputs | Role |",
        "|---|---:|---|",
    ]
    counts: Dict[str, int] = {}
    normalized_root = RUN_ROOT / "outputs_normalized"
    if normalized_root.is_dir():
        for child in normalized_root.iterdir():
            if child.is_dir():
                counts[child.name] = len(list_images(child))
    for row in method_rows:
        counts[str(row["method"])] = max(counts.get(str(row["method"]), 0), 1)
    for method in [
        "Ours",
        "HVDualformer",
        "ABC-Former",
        "GDCP",
        "CBF",
        "HLRP",
        "SGUIE-Net",
        "Histoformer",
        "WWPF",
    ]:
        role = "high-noise diagnostic reference" if method in NOISE_REFERENCE_METHODS else "primary/full record"
        lines.append(f"| {method} | {counts.get(method, 0)} | {role} |")
    lines.extend(
        [
            "",
            "## Metrics",
            "",
            f"- Metrics output: `{metrics_output}`" if metrics_output else "- Metrics output: not generated.",
            "- Metrics: EME, EMEE, Entropy, Contrast, AvgGra, MS_SSIM, PSNR, UCIQE, UIQM.",
            "- MS_SSIM and PSNR are interpreted only as raw-reference structural consistency.",
            "",
            "## Logs",
            "",
            "- Per-method logs: `logs/{method}.log`.",
            "- MATLAB wrappers generated under `matlab_wrappers/`.",
        ]
    )
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Rerun 9 enhancement methods on MyEdge 168 raw test images.")
    parser.add_argument("--skip-run", action="store_true", help="Only normalize existing outputs and run metrics.")
    parser.add_argument("--ours-workers", type=int, default=6, help="Parallel workers for the slow Stage1 Ours run.")
    parser.add_argument("--only-method", action="append", default=None, help="Run only selected method(s), then compute metrics from all normalized outputs.")
    args = parser.parse_args()

    ensure_dir(RUN_ROOT)
    rows = build_manifest()
    preflight(rows)
    write_manifest_files(rows)
    input_dir = copy_inputs(rows)
    wrappers = write_matlab_wrappers(input_dir)

    runs = method_runs(input_dir, wrappers)
    if args.only_method:
        wanted = set(args.only_method)
        runs = [run for run in runs if run.name in wanted]
        missing = sorted(wanted - {run.name for run in runs})
        if missing:
            raise RuntimeError(f"Unknown --only-method value(s): {missing}")
    method_index_rows: List[Dict[str, object]] = []
    if not args.skip_run:
        for method in runs:
            if method.name == "Ours":
                code = run_ours_parallel(method, rows, args.ours_workers)
            else:
                code = run_subprocess(method)
            if code != 0:
                write_run_report(rows, method_index_rows, None)
                raise RuntimeError(f"{method.name} failed with exit code {code}. See logs/{method.name}.log")
            method_index_rows.extend(normalize_method_outputs(method, rows))
    else:
        for method in runs:
            method_index_rows.extend(normalize_method_outputs(method, rows))

    metrics_output = run_metrics()
    write_run_report(rows, method_index_rows, metrics_output)
    print(f"[DONE] MyEdge 168 compare9 rerun complete: {RUN_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
