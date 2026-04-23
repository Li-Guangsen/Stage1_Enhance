from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")
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


@dataclass(frozen=True)
class MethodSpec:
    name: str
    directory: Path


@dataclass
class ImageIndex:
    by_key: Dict[str, Path]
    collisions: List[Tuple[str, str, str]]


def resolve_project_path(path_like: str | Path) -> Path:
    path = Path(path_like)
    if path.is_absolute():
        return path
    return (PROJECT_ROOT / path).resolve()


def is_image_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in IMAGE_EXTS


def normalize_result_stem(stem: str) -> str:
    normalized = stem
    changed = True
    while changed:
        changed = False
        for suffix in STAGE_SUFFIXES:
            if normalized.lower().endswith(suffix.lower()):
                normalized = normalized[: -len(suffix)]
                changed = True
                break
    return normalized


def manifest_entry_to_stem(line: str) -> Optional[str]:
    item = line.strip().lstrip("\ufeff")
    if not item or item.startswith("#"):
        return None
    token = item.split("#", 1)[0].strip()
    if not token:
        return None
    token = re.split(r"[\s,]+", token, maxsplit=1)[0]
    token_path = Path(token)
    stem = token_path.stem if token_path.suffix.lower() in IMAGE_EXTS else token_path.name
    return normalize_result_stem(stem)


def read_manifest(manifest_path: str | Path) -> List[str]:
    path = resolve_project_path(manifest_path)
    stems: List[str] = []
    seen = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        stem = manifest_entry_to_stem(line)
        if stem and stem not in seen:
            stems.append(stem)
            seen.add(stem)
    return stems


def list_image_files(directory: str | Path) -> List[Path]:
    root = resolve_project_path(directory)
    if not root.is_dir():
        return []
    return sorted((p for p in root.iterdir() if is_image_file(p)), key=lambda p: p.name.lower())


def build_image_index(directory: str | Path, include_normalized_keys: bool) -> ImageIndex:
    by_key: Dict[str, Path] = {}
    collisions: List[Tuple[str, str, str]] = []

    for path in list_image_files(directory):
        keys = [path.stem]
        normalized = normalize_result_stem(path.stem)
        if include_normalized_keys and normalized != path.stem:
            keys.append(normalized)

        for key in keys:
            existing = by_key.get(key)
            if existing is None:
                by_key[key] = path
            elif existing.resolve() != path.resolve():
                collisions.append((key, str(existing), str(path)))

    return ImageIndex(by_key=by_key, collisions=collisions)


def parse_method_specs(method_args: Optional[Sequence[str]], result_dir: str | Path, method_name: Optional[str]) -> List[MethodSpec]:
    specs: List[MethodSpec] = []
    if method_args:
        for item in method_args:
            if "=" in item:
                name, path_text = item.split("=", 1)
                name = name.strip()
                path_text = path_text.strip()
            else:
                path_text = item.strip()
                name = Path(path_text).name
            if not name:
                raise ValueError(f"Invalid method name in --method: {item}")
            specs.append(MethodSpec(name=name, directory=resolve_project_path(path_text)))
    else:
        resolved = resolve_project_path(result_dir)
        specs.append(MethodSpec(name=method_name or resolved.name, directory=resolved))

    seen = set()
    for spec in specs:
        if spec.name in seen:
            raise ValueError(f"Duplicate method name: {spec.name}")
        seen.add(spec.name)
    return specs


def select_common_stems(
    original_index: ImageIndex,
    method_indexes: Dict[str, ImageIndex],
    manifest_stems: Optional[Sequence[str]],
    limit: Optional[int],
) -> Tuple[List[str], List[Dict[str, str]]]:
    failures: List[Dict[str, str]] = []

    if manifest_stems is None:
        candidate = set(original_index.by_key)
        for index in method_indexes.values():
            candidate &= set(index.by_key)
        stems = sorted(candidate, key=str.lower)
    else:
        stems = []
        for stem in manifest_stems:
            missing = []
            if stem not in original_index.by_key:
                missing.append("original")
            for method_name, index in method_indexes.items():
                if stem not in index.by_key:
                    missing.append(method_name)
            if missing:
                failures.append(
                    {
                        "phase": "matching",
                        "stem": stem,
                        "method": ",".join(missing),
                        "error": "missing image for manifest entry",
                    }
                )
            else:
                stems.append(stem)

    if limit is not None and limit > 0:
        stems = stems[:limit]
    return stems, failures


def read_bgr(path: str | Path) -> np.ndarray:
    import cv2
    import numpy as np

    path = Path(path)
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError(f"cv2.imdecode failed: {path}")
    return img


def write_image(path: str | Path, img: np.ndarray) -> None:
    import cv2

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    ok, encoded = cv2.imencode(path.suffix, img)
    if not ok:
        raise RuntimeError(f"cv2.imencode failed: {path}")
    encoded.tofile(str(path))


def resize_bgr(img_bgr: np.ndarray, resize_to: Optional[Tuple[int, int]]) -> np.ndarray:
    import cv2

    if resize_to is None:
        return img_bgr
    width, height = resize_to
    h, w = img_bgr.shape[:2]
    if (w, h) == (width, height):
        return img_bgr
    return cv2.resize(img_bgr, (width, height), interpolation=cv2.INTER_CUBIC)


def safe_output_stem(stem: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", stem)


def write_lines(path: str | Path, lines: Iterable[str]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
