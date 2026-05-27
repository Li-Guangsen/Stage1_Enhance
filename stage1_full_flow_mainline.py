"""Full-flow downstream-aware Stage1 enhancement prototype.

This module is a planned replacement track for the near-raw downstream
diagnostic candidates. It keeps the original Stage1 innovation backbone:
gray-pixel color formation, IMF/detail, WB-safe contrast, local visibility,
multi-branch fusion, and bounded final closure.

The entry point is intentionally explicit and is not part of the locked paper
mainline unless a config sets ``final.mode=full_flow_downstream_stage1_mainline_v1``.
"""

from __future__ import annotations

import cv2
import numpy as np

from clahe_guided_visibility import clahe_3ch_wb_safe
from fusion_three import fuse_three_images_bgr
from lvbo import entropy_boost_Lab
from pybemd import imf1Ray_from_bgr
from wb_safe_contrast import wb_safe_contrast


MODE_NAME = "full_flow_downstream_stage1_mainline_v1"
MODE_NAME_V2 = "full_flow_downstream_stage1_mainline_v2"
MODE_NAME_TOPOLOGY_LOCKED = "topology_locked_visual_chroma_full_flow_v1"
MODE_NAMES = {MODE_NAME, MODE_NAME_V2, MODE_NAME_TOPOLOGY_LOCKED}


def is_full_flow_mainline_mode(mode):
    return mode in MODE_NAMES


def _to_float01(img):
    arr = np.asarray(img)
    if arr.dtype == np.uint8:
        return arr.astype(np.float32) / 255.0
    out = arr.astype(np.float32)
    if out.max(initial=0.0) > 1.5:
        out = out / 255.0
    return np.clip(out, 0.0, 1.0)


def _to_uint8(img01):
    return np.clip(np.round(np.clip(img01, 0.0, 1.0) * 255.0), 0, 255).astype(np.uint8)


def _normalize01(values, eps=1e-6):
    arr = values.astype(np.float32)
    lo = float(np.percentile(arr, 2.0))
    hi = float(np.percentile(arr, 98.0))
    if hi - lo < eps:
        return np.zeros_like(arr, dtype=np.float32)
    return np.clip((arr - lo) / (hi - lo), 0.0, 1.0).astype(np.float32)


def _odd_ksize(value, minimum=1):
    k = max(int(value), int(minimum))
    if k % 2 == 0:
        k += 1
    return k


def _luma01(img_uint8):
    lab = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    return lab[..., 0] / 255.0


def _scharr_mag(luma):
    gx = cv2.Scharr(luma.astype(np.float32), cv2.CV_32F, 1, 0)
    gy = cv2.Scharr(luma.astype(np.float32), cv2.CV_32F, 0, 1)
    return _normalize01(np.sqrt(gx * gx + gy * gy))


def _edge_confidence(luma, low_percentile=75.0, high_percentile=99.2):
    gx = cv2.Scharr(luma.astype(np.float32), cv2.CV_32F, 1, 0)
    gy = cv2.Scharr(luma.astype(np.float32), cv2.CV_32F, 0, 1)
    mag = np.sqrt(gx * gx + gy * gy).astype(np.float32)
    lo = float(np.percentile(mag, low_percentile))
    hi = float(np.percentile(mag, high_percentile))
    if hi <= lo + 1e-8:
        return np.zeros_like(luma, dtype=np.float32)
    return np.clip((mag - lo) / (hi - lo), 0.0, 1.0).astype(np.float32)


def _local_std(luma, ksize):
    k = _odd_ksize(ksize, minimum=3)
    mean = cv2.boxFilter(luma, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    mean2 = cv2.boxFilter(luma * luma, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    return np.sqrt(np.maximum(mean2 - mean * mean, 0.0)).astype(np.float32)


def _blur_map(mask, ksize):
    k = _odd_ksize(ksize, minimum=1)
    if k <= 1:
        return np.clip(mask.astype(np.float32), 0.0, 1.0)
    return np.clip(cv2.GaussianBlur(mask.astype(np.float32), (k, k), 0), 0.0, 1.0)


def _dilate_map(mask, ksize):
    k = _odd_ksize(ksize, minimum=1)
    if k <= 1:
        return np.clip(mask.astype(np.float32), 0.0, 1.0)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    return np.clip(cv2.dilate(mask.astype(np.float32), kernel), 0.0, 1.0)


def _diagnose_degradation(original_uint8, params):
    l_raw = _luma01(original_uint8)
    edge_conf = _edge_confidence(
        l_raw,
        params.get("edge_low_percentile", 75.0),
        params.get("edge_high_percentile", 99.2),
    )
    local_contrast = _normalize01(_local_std(l_raw, params.get("local_std_ksize", 15)))

    structure_support = np.clip(
        0.70 * edge_conf + 0.30 * local_contrast,
        0.0,
        1.0,
    )
    structure_support = np.power(
        structure_support,
        float(params.get("support_power", 0.85)),
    )
    structure_support = _blur_map(structure_support, params.get("support_blur_ksize", 5))

    weak_boundary_need = (1.0 - local_contrast) * np.power(edge_conf, 0.75)
    weak_boundary_need = _blur_map(weak_boundary_need, params.get("mask_blur_ksize", 5))

    texture_risk = _normalize01(_local_std(l_raw, params.get("texture_std_ksize", 7)))
    background_risk = (1.0 - edge_conf) * np.power(texture_risk, 0.85)
    background_risk = _blur_map(background_risk, params.get("mask_blur_ksize", 5))

    saturation = np.max(original_uint8.astype(np.float32), axis=2) / 255.0
    saturation_risk = _blur_map(np.clip((saturation - 0.92) / 0.08, 0.0, 1.0), 5)

    return {
        "l_raw": l_raw,
        "edge_conf": np.clip(edge_conf, 0.0, 1.0),
        "local_contrast": np.clip(local_contrast, 0.0, 1.0),
        "structure_support": np.clip(structure_support, 0.0, 1.0),
        "weak_boundary_need": np.clip(weak_boundary_need, 0.0, 1.0),
        "texture_risk": np.clip(texture_risk, 0.0, 1.0),
        "background_risk": np.clip(background_risk, 0.0, 1.0),
        "saturation_risk": np.clip(saturation_risk, 0.0, 1.0),
    }


def _blend_luma(base_uint8, candidate_uint8, alpha_map, max_luma_delta):
    base_lab = cv2.cvtColor(base_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    cand_lab = cv2.cvtColor(candidate_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    alpha = np.clip(alpha_map.astype(np.float32), 0.0, 1.0)
    delta = cand_lab[..., 0] - base_lab[..., 0]
    if max_luma_delta is not None and max_luma_delta > 0:
        delta = np.clip(delta, -float(max_luma_delta), float(max_luma_delta))
    out_lab = base_lab.copy()
    out_lab[..., 0] = np.clip(base_lab[..., 0] + alpha * delta, 0.0, 255.0)
    return cv2.cvtColor(out_lab.astype(np.uint8), cv2.COLOR_LAB2BGR)


def _cap_chroma_delta(raw_uint8, candidate_uint8, max_chroma_delta):
    if max_chroma_delta is None or max_chroma_delta <= 0:
        return candidate_uint8
    raw_lab = cv2.cvtColor(raw_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    cand_lab = cv2.cvtColor(candidate_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    out_lab = cand_lab.copy()
    for channel in (1, 2):
        delta = cand_lab[..., channel] - raw_lab[..., channel]
        out_lab[..., channel] = raw_lab[..., channel] + np.clip(
            delta,
            -float(max_chroma_delta),
            float(max_chroma_delta),
        )
    return cv2.cvtColor(np.clip(out_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _support_mix(diagnosis, floor, weak_gain=0.0):
    support = diagnosis["structure_support"] + float(weak_gain) * diagnosis["weak_boundary_need"]
    support = np.clip(support, 0.0, 1.0)
    floor = float(np.clip(floor, 0.0, 1.0))
    return np.clip(floor + (1.0 - floor) * support, 0.0, 1.0)


def _support_guided_pullback(anchor_uint8, candidate_uint8, diagnosis, flow_params, prefix):
    alpha = float(flow_params.get(f"{prefix}_flat_pullback_alpha", 0.0))
    if alpha <= 0.0:
        return candidate_uint8

    power = max(float(flow_params.get(f"{prefix}_flat_pullback_power", 1.35)), 1e-6)
    flat = (1.0 - diagnosis["structure_support"]) * (1.0 - 0.50 * diagnosis["weak_boundary_need"])
    flat = np.power(np.clip(flat, 0.0, 1.0), power)
    pullback = np.clip(alpha * flat, 0.0, 1.0)

    anchor_lab = cv2.cvtColor(anchor_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    cand_lab = cv2.cvtColor(candidate_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    out_lab = cand_lab.copy()
    for channel in (0, 1, 2):
        out_lab[..., channel] = cand_lab[..., channel] * (1.0 - pullback) + anchor_lab[..., channel] * pullback
    return cv2.cvtColor(np.clip(out_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _build_detail_branch(original_uint8, bph_uint8, bph_float, diagnosis, imf_params, flow_params):
    raw_l = diagnosis["l_raw"]
    imf_float = imf1Ray_from_bgr(bph_float, **dict(imf_params or {}))
    imf_uint8 = _to_uint8(imf_float)

    alpha = float(flow_params.get("detail_alpha", 0.80))
    texture_penalty = float(flow_params.get("detail_texture_penalty", 0.70))
    weak_gain = float(flow_params.get("detail_weak_boundary_gain", 0.45))
    max_luma_delta = float(flow_params.get("detail_max_luma_delta", 18.0))

    support = diagnosis["edge_conf"] + weak_gain * diagnosis["weak_boundary_need"]
    risk = texture_penalty * diagnosis["background_risk"] + 0.35 * diagnosis["saturation_risk"]
    alpha_map = np.clip(alpha * support * (1.0 - risk), 0.0, 1.0)
    branch = _blend_luma(bph_uint8, imf_uint8, alpha_map, max_luma_delta)

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    branch_lab = cv2.cvtColor(branch, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_detail = raw_l - cv2.GaussianBlur(raw_l, (0, 0), 1.2)
    branch_lab[..., 0] = np.clip(
        branch_lab[..., 0] + 255.0 * float(flow_params.get("raw_detail_rescue_alpha", 0.05)) * raw_detail,
        0.0,
        255.0,
    )
    return cv2.cvtColor(branch_lab.astype(np.uint8), cv2.COLOR_LAB2BGR)


def _build_safe_contrast_branch(original_uint8, bph_uint8, bph_float, diagnosis, rghs_params, flow_params):
    rghs_float = wb_safe_contrast(bph_float, **dict(rghs_params or {}))
    rghs_uint8 = _to_uint8(rghs_float)

    contrast_alpha = float(flow_params.get("contrast_alpha", 0.85))
    max_luma_delta = float(flow_params.get("contrast_max_luma_delta", 22.0))
    risk = 0.55 * diagnosis["background_risk"] + 0.35 * diagnosis["saturation_risk"]
    support = _support_mix(
        diagnosis,
        flow_params.get("contrast_support_floor", 0.22),
        flow_params.get("contrast_weak_boundary_gain", 0.20),
    )
    alpha_map = np.clip(contrast_alpha * support * (1.0 - risk), 0.0, 1.0)
    branch = _blend_luma(bph_uint8, rghs_uint8, alpha_map, max_luma_delta)
    branch = _support_guided_pullback(bph_uint8, branch, diagnosis, flow_params, "contrast")
    return _cap_chroma_delta(original_uint8, branch, float(flow_params.get("contrast_max_chroma_delta", 10.0)))


def _build_local_visibility_branch(original_uint8, bph_uint8, bph_float, diagnosis, clahe_params, flow_params):
    clahe_float = clahe_3ch_wb_safe(bph_float, **dict(clahe_params or {}))
    clahe_uint8 = _to_uint8(clahe_float)

    visibility_alpha = float(flow_params.get("visibility_alpha", 0.75))
    weak_gain = float(flow_params.get("visibility_weak_boundary_gain", 0.65))
    max_luma_delta = float(flow_params.get("visibility_max_luma_delta", 18.0))
    risk = 0.70 * diagnosis["background_risk"] + 0.25 * diagnosis["saturation_risk"]
    support = _support_mix(
        diagnosis,
        flow_params.get("visibility_support_floor", 0.20),
        weak_gain,
    )
    alpha_map = np.clip(visibility_alpha * support * (1.0 - risk), 0.0, 1.0)
    branch = _blend_luma(bph_uint8, clahe_uint8, alpha_map, max_luma_delta)
    branch = _support_guided_pullback(bph_uint8, branch, diagnosis, flow_params, "visibility")
    return _cap_chroma_delta(original_uint8, branch, float(flow_params.get("visibility_max_chroma_delta", 8.0)))


def _direct_weighted_base_fusion(bph_uint8, detail_uint8, contrast_uint8, visibility_uint8, diagnosis, flow_params):
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    detail_lab = cv2.cvtColor(detail_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    contrast_lab = cv2.cvtColor(contrast_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    visibility_lab = cv2.cvtColor(visibility_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)

    support = diagnosis["structure_support"]
    weak = diagnosis["weak_boundary_need"]
    local = diagnosis["local_contrast"]
    background = np.clip(1.0 - support, 0.0, 1.0)
    risk = np.clip(0.65 * diagnosis["background_risk"] + 0.35 * background, 0.0, 1.0)

    w_detail = float(flow_params.get("direct_detail_weight", 1.10)) * (0.15 + 0.85 * support)
    w_detail *= 1.0 - 0.65 * risk
    w_contrast = float(flow_params.get("direct_contrast_weight", 0.95)) * (0.20 + 0.50 * support + 0.30 * local)
    w_contrast *= 1.0 - 0.75 * risk
    w_visibility = float(flow_params.get("direct_visibility_weight", 0.80)) * (0.15 + weak + 0.35 * support * (1.0 - local))
    w_visibility *= 1.0 - 0.70 * risk
    w_bph = float(flow_params.get("direct_bph_weight", 0.65)) + float(
        flow_params.get("direct_bph_background_weight", 1.35)
    ) * background

    denom = w_detail + w_contrast + w_visibility + w_bph + 1e-6
    out_lab = bph_lab.copy()
    out_lab[..., 0] = (
        detail_lab[..., 0] * w_detail
        + contrast_lab[..., 0] * w_contrast
        + visibility_lab[..., 0] * w_visibility
        + bph_lab[..., 0] * w_bph
    ) / denom

    chroma_alpha = float(np.clip(flow_params.get("direct_chroma_alpha", 0.18), 0.0, 1.0))
    chroma_support = chroma_alpha * support
    branch_chroma_a = (contrast_lab[..., 1] + visibility_lab[..., 1] + detail_lab[..., 1]) / 3.0
    branch_chroma_b = (contrast_lab[..., 2] + visibility_lab[..., 2] + detail_lab[..., 2]) / 3.0
    out_lab[..., 1] = bph_lab[..., 1] * (1.0 - chroma_support) + branch_chroma_a * chroma_support
    out_lab[..., 2] = bph_lab[..., 2] * (1.0 - chroma_support) + branch_chroma_b * chroma_support
    return cv2.cvtColor(np.clip(out_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _downstream_aware_fusion(original_uint8, bph_uint8, detail_uint8, contrast_uint8, visibility_uint8, diagnosis, fusion_params, flow_params):
    backend = str(flow_params.get("fusion_backend", "direct_weighted")).lower()
    if backend == "direct_weighted":
        base_fused = _direct_weighted_base_fusion(
            bph_uint8,
            detail_uint8,
            contrast_uint8,
            visibility_uint8,
            diagnosis,
            flow_params,
        )
    elif backend == "laplacian":
        base_fused = _to_uint8(
            fuse_three_images_bgr(
                _to_float01(detail_uint8),
                _to_float01(contrast_uint8),
                _to_float01(visibility_uint8),
                **dict(fusion_params or {}),
            )
        )
    else:
        raise ValueError(f"Unsupported fusion_backend: {backend}")

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    fused_lab = cv2.cvtColor(base_fused, cv2.COLOR_BGR2LAB).astype(np.float32)

    pullback = (
        float(flow_params.get("fusion_texture_pullback", 0.45)) * diagnosis["background_risk"]
        + float(flow_params.get("fusion_saturation_pullback", 0.35)) * diagnosis["saturation_risk"]
    )
    support = diagnosis["edge_conf"] + float(flow_params.get("fusion_weak_boundary_gain", 0.50)) * diagnosis["weak_boundary_need"]
    floor = float(np.clip(flow_params.get("fusion_support_floor", 0.28), 0.0, 1.0))
    keep = np.clip(float(flow_params.get("fusion_enhancement_alpha", 0.90)) * (floor + (1.0 - floor) * support), 0.0, 1.0)
    keep = np.clip(keep * (1.0 - np.clip(pullback, 0.0, 1.0)), 0.0, 1.0)

    target_l = raw_lab[..., 0] * (1.0 - keep) + fused_lab[..., 0] * keep
    bph_anchor = float(flow_params.get("fusion_bph_lowfreq_anchor", 0.12))
    low_raw = cv2.GaussianBlur(raw_lab[..., 0], (0, 0), float(flow_params.get("fusion_low_sigma", 15.0)))
    low_bph = cv2.GaussianBlur(bph_lab[..., 0], (0, 0), float(flow_params.get("fusion_low_sigma", 15.0)))
    target_l += bph_anchor * (low_bph - low_raw) * (1.0 - diagnosis["saturation_risk"])

    max_luma_delta = float(flow_params.get("fusion_max_luma_delta", 28.0))
    target_l = raw_lab[..., 0] + np.clip(target_l - raw_lab[..., 0], -max_luma_delta, max_luma_delta)

    out_lab = fused_lab.copy()
    out_lab[..., 0] = np.clip(target_l, 0.0, 255.0)

    chroma_alpha = float(flow_params.get("fusion_chroma_alpha", 0.70))
    max_chroma_delta = float(flow_params.get("fusion_max_chroma_delta", 12.0))
    for channel in (1, 2):
        chroma_target = raw_lab[..., channel] * (1.0 - chroma_alpha) + fused_lab[..., channel] * chroma_alpha
        delta = np.clip(chroma_target - raw_lab[..., channel], -max_chroma_delta, max_chroma_delta)
        out_lab[..., channel] = raw_lab[..., channel] + delta

    fused = cv2.cvtColor(np.clip(out_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    return _support_guided_pullback(bph_uint8, fused, diagnosis, flow_params, "fusion")


def _detector_compatible_fusion(original_uint8, bph_uint8, detail_uint8, contrast_uint8, visibility_uint8, diagnosis, flow_params):
    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    detail_lab = cv2.cvtColor(detail_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    contrast_lab = cv2.cvtColor(contrast_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    visibility_lab = cv2.cvtColor(visibility_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)

    weak_gain = float(flow_params.get("dc_weak_boundary_gain", 0.55))
    local_gain = float(flow_params.get("dc_local_contrast_gain", 0.25))
    support = (
        diagnosis["edge_conf"]
        + weak_gain * diagnosis["weak_boundary_need"]
        + local_gain * diagnosis["local_contrast"]
    )
    support = np.clip(support, 0.0, 1.0)
    support = np.power(support, float(flow_params.get("dc_support_power", 0.80)))
    support = _dilate_map(support, flow_params.get("dc_support_dilate_ksize", 3))
    support = _blur_map(support, flow_params.get("dc_support_blur_ksize", 5))

    background_risk = np.clip(
        float(flow_params.get("dc_background_risk_weight", 0.75)) * diagnosis["background_risk"]
        + float(flow_params.get("dc_flat_weight", 0.25)) * (1.0 - support),
        0.0,
        1.0,
    )
    background_risk = np.power(
        background_risk,
        float(flow_params.get("dc_background_power", 1.15)),
    )

    low_sigma = float(flow_params.get("dc_low_sigma", 13.0))
    color_alpha = float(np.clip(flow_params.get("dc_color_chroma_alpha", 0.78), 0.0, 1.0))
    color_branch_mix = float(np.clip(flow_params.get("dc_color_branch_mix", 0.20), 0.0, 1.0))
    max_chroma_delta = float(flow_params.get("dc_max_chroma_delta", 18.0))

    out_lab = raw_lab.copy()
    for channel in (1, 2):
        low_raw = cv2.GaussianBlur(raw_lab[..., channel], (0, 0), low_sigma)
        low_bph = cv2.GaussianBlur(bph_lab[..., channel], (0, 0), low_sigma)
        low_branch = cv2.GaussianBlur(
            (detail_lab[..., channel] + contrast_lab[..., channel] + visibility_lab[..., channel]) / 3.0,
            (0, 0),
            low_sigma,
        )
        low_target = low_bph * (1.0 - color_branch_mix) + low_branch * color_branch_mix
        alpha = color_alpha * (1.0 - 0.25 * background_risk)
        delta = np.clip(alpha * (low_target - low_raw), -max_chroma_delta, max_chroma_delta)
        out_lab[..., channel] = np.clip(raw_lab[..., channel] + delta, 0.0, 255.0)

    low_luma_alpha = float(np.clip(flow_params.get("dc_low_luma_alpha", 0.22), 0.0, 1.0))
    low_luma_max_delta = float(flow_params.get("dc_low_luma_max_delta", 8.0))
    low_raw_l = cv2.GaussianBlur(raw_lab[..., 0], (0, 0), low_sigma)
    low_bph_l = cv2.GaussianBlur(bph_lab[..., 0], (0, 0), low_sigma)
    low_luma_delta = np.clip(
        low_luma_alpha * (low_bph_l - low_raw_l) * (0.35 + 0.65 * support),
        -low_luma_max_delta,
        low_luma_max_delta,
    )

    def high_residual(candidate_l):
        delta = candidate_l - bph_lab[..., 0]
        return delta - cv2.GaussianBlur(delta, (0, 0), float(flow_params.get("dc_residual_low_sigma", 5.0)))

    detail_res = high_residual(detail_lab[..., 0])
    contrast_res = high_residual(contrast_lab[..., 0])
    visibility_res = high_residual(visibility_lab[..., 0])
    residual = (
        float(flow_params.get("dc_detail_residual_alpha", 0.38)) * detail_res
        + float(flow_params.get("dc_contrast_residual_alpha", 0.24)) * contrast_res
        + float(flow_params.get("dc_visibility_residual_alpha", 0.26)) * visibility_res
    )
    residual_gate = support * (1.0 - float(flow_params.get("dc_background_luma_suppression", 0.85)) * background_risk)
    residual_gate = np.clip(residual_gate, 0.0, 1.0)
    residual = np.clip(
        residual * residual_gate,
        -float(flow_params.get("dc_max_structure_residual", 8.0)),
        float(flow_params.get("dc_max_structure_residual", 8.0)),
    )

    target_l = raw_lab[..., 0] + low_luma_delta + residual
    max_total_delta = float(flow_params.get("dc_max_total_luma_delta", 14.0))
    target_l = raw_lab[..., 0] + np.clip(target_l - raw_lab[..., 0], -max_total_delta, max_total_delta)

    if bool(flow_params.get("dc_enable_background_smoothing", True)):
        smooth_l = cv2.GaussianBlur(raw_lab[..., 0] + low_luma_delta, (0, 0), float(flow_params.get("dc_background_smooth_sigma", 1.4)))
        bg_alpha = np.clip(float(flow_params.get("dc_background_smooth_alpha", 0.65)) * background_risk, 0.0, 1.0)
        target_l = target_l * (1.0 - bg_alpha) + smooth_l * bg_alpha

    out_lab[..., 0] = np.clip(target_l, 0.0, 255.0)
    out = cv2.cvtColor(np.clip(out_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)

    if bool(flow_params.get("dc_enable_bilateral_closure", True)):
        closed = cv2.bilateralFilter(
            out,
            int(flow_params.get("dc_bilateral_d", 5)),
            float(flow_params.get("dc_bilateral_sigma_color", 18.0)),
            float(flow_params.get("dc_bilateral_sigma_space", 5.0)),
        )
        close_alpha = np.clip(float(flow_params.get("dc_bilateral_alpha", 0.35)) * background_risk[..., None], 0.0, 1.0)
        out = np.clip(out.astype(np.float32) * (1.0 - close_alpha) + closed.astype(np.float32) * close_alpha, 0, 255).astype(np.uint8)

    return out


def _project_to_raw_cv_gray_plane(original_uint8, candidate_uint8, chroma_alpha=1.0):
    """Keep candidate chroma on the raw OpenCV-grayscale plane.

    The 168 proxy uses cv2 BGR2GRAY before Sobel/Otsu. Lab-L locking can still
    drift under that projection, so this projection discards candidate gray and
    keeps only its BGR chroma vector around the raw gray anchor.
    """

    raw_gray = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2GRAY).astype(np.float32)
    cand = candidate_uint8.astype(np.float32)
    weights = np.array([0.114, 0.587, 0.299], dtype=np.float32)
    cand_gray = np.sum(cand * weights[None, None, :], axis=2)
    chroma = cand - cand_gray[..., None]

    alpha = float(np.clip(chroma_alpha, 0.0, 1.0))
    beta = np.full(raw_gray.shape, alpha, dtype=np.float32)
    for channel in range(3):
        ch = chroma[..., channel]
        positive = ch > 1e-6
        negative = ch < -1e-6
        beta[positive] = np.minimum(beta[positive], (255.0 - raw_gray[positive]) / ch[positive])
        beta[negative] = np.minimum(beta[negative], (0.0 - raw_gray[negative]) / ch[negative])

    beta = np.clip(beta, 0.0, alpha)
    projected = raw_gray[..., None] + beta[..., None] * chroma
    return np.clip(np.round(projected), 0, 255).astype(np.uint8)


def _topology_locked_visual_chroma_fusion(
    original_uint8,
    bph_uint8,
    detail_uint8,
    contrast_uint8,
    visibility_uint8,
    diagnosis,
    flow_params,
):
    """Build a visually nontrivial output while keeping raw luma topology.

    FA01 showed that fixed raw-trained detectors are much more sensitive to
    luma/detail topology drift than to the mere existence of Stage1 branch
    evidence. This fusion path therefore uses the full Stage1 branch stack to
    form color/visibility evidence, but constrains the final Lab-L channel to a
    raw-topology anchor plus bounded low-frequency illumination and weak-boundary
    residuals.
    """

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    detail_lab = cv2.cvtColor(detail_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    contrast_lab = cv2.cvtColor(contrast_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    visibility_lab = cv2.cvtColor(visibility_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)

    low_sigma = float(flow_params.get("tl_low_sigma", 15.0))
    low_alpha = float(flow_params.get("tl_low_luma_alpha", 0.18))
    low_max_delta = float(flow_params.get("tl_low_luma_max_delta", 5.0))
    residual_alpha = float(flow_params.get("tl_weak_residual_alpha", 0.18))
    residual_max_delta = float(flow_params.get("tl_weak_residual_max_delta", 3.5))
    background_suppression = float(flow_params.get("tl_background_luma_suppression", 0.90))

    raw_l = raw_lab[..., 0]
    bph_l = bph_lab[..., 0]
    low_delta = cv2.GaussianBlur(bph_l - raw_l, (0, 0), low_sigma)
    low_delta = np.clip(low_delta, -low_max_delta, low_max_delta)

    branch_l = (
        float(flow_params.get("tl_detail_luma_weight", 0.38)) * detail_lab[..., 0]
        + float(flow_params.get("tl_contrast_luma_weight", 0.28)) * contrast_lab[..., 0]
        + float(flow_params.get("tl_visibility_luma_weight", 0.34)) * visibility_lab[..., 0]
    )
    branch_l /= max(
        float(flow_params.get("tl_detail_luma_weight", 0.38))
        + float(flow_params.get("tl_contrast_luma_weight", 0.28))
        + float(flow_params.get("tl_visibility_luma_weight", 0.34)),
        1e-6,
    )
    residual = branch_l - cv2.GaussianBlur(branch_l, (0, 0), float(flow_params.get("tl_residual_low_sigma", 5.0)))
    residual = np.clip(residual, -residual_max_delta, residual_max_delta)
    weak_support = np.clip(
        diagnosis["weak_boundary_need"] + float(flow_params.get("tl_edge_support_gain", 0.28)) * diagnosis["edge_conf"],
        0.0,
        1.0,
    )
    luma_support = weak_support * (1.0 - background_suppression * diagnosis["background_risk"])

    out_lab = raw_lab.copy()
    out_lab[..., 0] = np.clip(raw_l + low_alpha * low_delta + residual_alpha * luma_support * residual, 0, 255)

    bph_chroma_delta = bph_lab[..., 1:3] - raw_lab[..., 1:3]
    branch_chroma = (
        float(flow_params.get("tl_detail_chroma_weight", 0.10)) * (detail_lab[..., 1:3] - raw_lab[..., 1:3])
        + float(flow_params.get("tl_contrast_chroma_weight", 0.28)) * (contrast_lab[..., 1:3] - raw_lab[..., 1:3])
        + float(flow_params.get("tl_visibility_chroma_weight", 0.22)) * (visibility_lab[..., 1:3] - raw_lab[..., 1:3])
    )
    color_delta = (
        float(flow_params.get("tl_bph_chroma_weight", 0.72)) * bph_chroma_delta
        + branch_chroma
    )
    color_support = np.clip(
        float(flow_params.get("tl_color_support_floor", 0.72))
        + float(flow_params.get("tl_color_weak_gain", 0.18)) * diagnosis["weak_boundary_need"]
        - float(flow_params.get("tl_color_saturation_penalty", 0.22)) * diagnosis["saturation_risk"],
        0.0,
        1.0,
    )
    max_chroma_delta = float(flow_params.get("tl_max_chroma_delta", 24.0))
    out_lab[..., 1:3] = raw_lab[..., 1:3] + color_support[..., None] * np.clip(
        color_delta,
        -max_chroma_delta,
        max_chroma_delta,
    )

    out_bgr = cv2.cvtColor(np.clip(out_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)

    if bool(flow_params.get("tl_enable_bilateral_finish", True)):
        bilateral = cv2.bilateralFilter(
            out_bgr,
            int(flow_params.get("tl_bilateral_d", 5)),
            float(flow_params.get("tl_bilateral_sigma_color", 16.0)),
            float(flow_params.get("tl_bilateral_sigma_space", 5.0)),
        )
        bilab = cv2.cvtColor(bilateral, cv2.COLOR_BGR2LAB).astype(np.float32)
        alpha = float(flow_params.get("tl_bilateral_alpha", 0.18))
        out_lab[..., 1:3] = (1.0 - alpha) * out_lab[..., 1:3] + alpha * bilab[..., 1:3]
        out_bgr = cv2.cvtColor(np.clip(out_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)

    if bool(flow_params.get("tl_enable_raw_gray_plane_projection", False)):
        out_bgr = _project_to_raw_cv_gray_plane(
            original_uint8,
            out_bgr,
            chroma_alpha=float(flow_params.get("tl_gray_plane_chroma_alpha", 0.90)),
        )
    elif bool(flow_params.get("tl_enable_cv_gray_lock", True)):
        raw_gray = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2GRAY).astype(np.float32)
        out_gray = cv2.cvtColor(out_bgr, cv2.COLOR_BGR2GRAY).astype(np.float32)
        delta = raw_gray - out_gray
        max_shift = float(flow_params.get("tl_cv_gray_lock_max_shift", 10.0))
        delta = np.clip(delta, -max_shift, max_shift)
        alpha = float(flow_params.get("tl_cv_gray_lock_alpha", 0.90))
        out_bgr_f = out_bgr.astype(np.float32) + alpha * delta[..., None]
        out_bgr = np.clip(np.round(out_bgr_f), 0, 255).astype(np.uint8)

    return out_bgr


def _final_closure(original_uint8, fused_uint8, diagnosis, flow_params):
    mode = str(flow_params.get("closure_mode", "entropy")).lower()
    if not bool(flow_params.get("enable_final_closure", True)):
        return fused_uint8

    if mode == "none":
        closed = fused_uint8
    elif mode == "entropy":
        closed = entropy_boost_Lab(
            fused_uint8,
            p_low=float(flow_params.get("closure_p_low", 1.0)),
            p_high=float(flow_params.get("closure_p_high", 99.0)),
            clahe_clip=float(flow_params.get("closure_clahe_clip", 1.15)),
            clahe_tile=tuple(flow_params.get("closure_clahe_tile", [8, 8])),
            mix_global=float(flow_params.get("closure_mix_global", 0.45)),
            mix_local=float(flow_params.get("closure_mix_local", 0.20)),
            chroma_gain=float(flow_params.get("closure_chroma_gain", 1.015)),
        )
    else:
        raise ValueError(f"Unsupported closure_mode: {mode}")

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    fused_lab = cv2.cvtColor(fused_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    closed_lab = cv2.cvtColor(closed, cv2.COLOR_BGR2LAB).astype(np.float32)

    risk = (
        float(flow_params.get("closure_texture_pullback", 0.35)) * diagnosis["background_risk"]
        + float(flow_params.get("closure_saturation_pullback", 0.30)) * diagnosis["saturation_risk"]
    )
    keep = np.clip(float(flow_params.get("closure_alpha", 0.70)) * (1.0 - risk), 0.0, 1.0)
    max_luma_delta = float(flow_params.get("closure_max_luma_delta", 10.0))

    target_l = fused_lab[..., 0] + keep * (closed_lab[..., 0] - fused_lab[..., 0])
    target_l = raw_lab[..., 0] + np.clip(target_l - raw_lab[..., 0], -max_luma_delta, max_luma_delta)

    out_lab = closed_lab.copy()
    out_lab[..., 0] = np.clip(target_l, 0.0, 255.0)

    max_chroma_delta = float(flow_params.get("closure_max_chroma_delta", 12.0))
    for channel in (1, 2):
        delta = np.clip(out_lab[..., channel] - raw_lab[..., channel], -max_chroma_delta, max_chroma_delta)
        out_lab[..., channel] = raw_lab[..., channel] + delta

    return cv2.cvtColor(np.clip(out_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _global_luma_stats(original_uint8, candidate_uint8):
    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    cand_lab = cv2.cvtColor(candidate_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0] / 255.0
    cand_l = cand_lab[..., 0] / 255.0
    raw_grad = _scharr_mag(raw_l)
    cand_grad = _scharr_mag(cand_l)
    return {
        "grad_ratio": float(np.mean(cand_grad) / (np.mean(raw_grad) + 1e-9)),
        "luma_std_ratio": float(np.std(cand_lab[..., 0]) / (np.std(raw_lab[..., 0]) + 1e-9)),
        "mean_abs_luma_delta": float(np.mean(np.abs(cand_lab[..., 0] - raw_lab[..., 0]))),
    }


def _blend_bgr(anchor_uint8, candidate_uint8, scale):
    scale = float(np.clip(scale, 0.0, 1.0))
    out = anchor_uint8.astype(np.float32) * (1.0 - scale) + candidate_uint8.astype(np.float32) * scale
    return np.clip(np.round(out), 0, 255).astype(np.uint8)


def _bounded_output_selection(original_uint8, bph_uint8, candidate_uint8, flow_params):
    if not bool(flow_params.get("enable_bounded_output_selection", True)):
        return candidate_uint8

    scales = flow_params.get("bounded_output_scales", [1.0, 0.75, 0.55, 0.40])
    max_grad_ratio = float(flow_params.get("bounded_max_grad_ratio", 1.85))
    max_luma_std_ratio = float(flow_params.get("bounded_max_luma_std_ratio", 1.75))
    max_mean_abs_luma_delta = float(flow_params.get("bounded_max_mean_abs_luma_delta", 18.0))
    anchor_name = str(flow_params.get("bounded_output_anchor", "bph")).lower()
    anchor_uint8 = original_uint8 if anchor_name == "original" else bph_uint8

    best = candidate_uint8
    for scale in scales:
        trial = _blend_bgr(anchor_uint8, candidate_uint8, float(scale))
        stats = _global_luma_stats(original_uint8, trial)
        best = trial
        if (
            stats["grad_ratio"] <= max_grad_ratio
            and stats["luma_std_ratio"] <= max_luma_std_ratio
            and stats["mean_abs_luma_delta"] <= max_mean_abs_luma_delta
        ):
            return trial
    return best


def run_full_flow_downstream_stage1_mainline(
    original_uint8,
    *,
    bph_uint8,
    imf1ray_params=None,
    rghs_params=None,
    clahe_params=None,
    fusion_params=None,
    full_flow_params=None,
):
    """Run the full-flow Stage1 prototype and return named uint8 stages."""
    if bph_uint8 is None:
        raise ValueError("full_flow_downstream_stage1_mainline_v1 requires bph_uint8")

    params = dict(full_flow_params or {})
    supported = {
        "local_std_ksize",
        "texture_std_ksize",
        "mask_blur_ksize",
        "support_power",
        "support_blur_ksize",
        "edge_low_percentile",
        "edge_high_percentile",
        "detail_alpha",
        "detail_texture_penalty",
        "detail_weak_boundary_gain",
        "detail_max_luma_delta",
        "raw_detail_rescue_alpha",
        "contrast_alpha",
        "contrast_support_floor",
        "contrast_weak_boundary_gain",
        "contrast_flat_pullback_alpha",
        "contrast_flat_pullback_power",
        "contrast_max_luma_delta",
        "contrast_max_chroma_delta",
        "visibility_alpha",
        "visibility_support_floor",
        "visibility_weak_boundary_gain",
        "visibility_flat_pullback_alpha",
        "visibility_flat_pullback_power",
        "visibility_max_luma_delta",
        "visibility_max_chroma_delta",
        "fusion_texture_pullback",
        "fusion_saturation_pullback",
        "fusion_weak_boundary_gain",
        "fusion_backend",
        "fusion_support_floor",
        "fusion_enhancement_alpha",
        "fusion_bph_lowfreq_anchor",
        "fusion_low_sigma",
        "fusion_flat_pullback_alpha",
        "fusion_flat_pullback_power",
        "fusion_max_luma_delta",
        "fusion_chroma_alpha",
        "fusion_max_chroma_delta",
        "direct_detail_weight",
        "direct_contrast_weight",
        "direct_visibility_weight",
        "direct_bph_weight",
        "direct_bph_background_weight",
        "direct_chroma_alpha",
        "enable_final_closure",
        "closure_mode",
        "closure_p_low",
        "closure_p_high",
        "closure_clahe_clip",
        "closure_clahe_tile",
        "closure_mix_global",
        "closure_mix_local",
        "closure_chroma_gain",
        "closure_texture_pullback",
        "closure_saturation_pullback",
        "closure_alpha",
        "closure_max_luma_delta",
        "closure_max_chroma_delta",
        "final_flat_pullback_alpha",
        "final_flat_pullback_power",
        "enable_bounded_fusion_selection",
        "enable_bounded_output_selection",
        "bounded_output_scales",
        "bounded_max_grad_ratio",
        "bounded_max_luma_std_ratio",
        "bounded_max_mean_abs_luma_delta",
        "bounded_output_anchor",
        "_mode",
        "flow_version",
        "enable_detector_sensitive_diagnosis",
        "enable_gray_pixel_color_lane",
        "enable_frequency_detail_evidence",
        "enable_contrast_evidence",
        "enable_visibility_evidence",
        "enable_color_structure_decoupling",
        "enable_topology_compatible_fusion",
        "enable_background_luma_suppression",
        "enable_bounded_filtering_closure",
        "dc_weak_boundary_gain",
        "dc_local_contrast_gain",
        "dc_support_power",
        "dc_support_dilate_ksize",
        "dc_support_blur_ksize",
        "dc_background_risk_weight",
        "dc_flat_weight",
        "dc_background_power",
        "dc_low_sigma",
        "dc_color_chroma_alpha",
        "dc_color_branch_mix",
        "dc_max_chroma_delta",
        "dc_low_luma_alpha",
        "dc_low_luma_max_delta",
        "dc_residual_low_sigma",
        "dc_detail_residual_alpha",
        "dc_contrast_residual_alpha",
        "dc_visibility_residual_alpha",
        "dc_background_luma_suppression",
        "dc_max_structure_residual",
        "dc_max_total_luma_delta",
        "dc_enable_background_smoothing",
        "dc_background_smooth_sigma",
        "dc_background_smooth_alpha",
        "dc_enable_bilateral_closure",
        "dc_bilateral_d",
        "dc_bilateral_sigma_color",
        "dc_bilateral_sigma_space",
        "dc_bilateral_alpha",
        "tl_low_sigma",
        "tl_low_luma_alpha",
        "tl_low_luma_max_delta",
        "tl_weak_residual_alpha",
        "tl_weak_residual_max_delta",
        "tl_background_luma_suppression",
        "tl_detail_luma_weight",
        "tl_contrast_luma_weight",
        "tl_visibility_luma_weight",
        "tl_residual_low_sigma",
        "tl_edge_support_gain",
        "tl_detail_chroma_weight",
        "tl_contrast_chroma_weight",
        "tl_visibility_chroma_weight",
        "tl_bph_chroma_weight",
        "tl_color_support_floor",
        "tl_color_weak_gain",
        "tl_color_saturation_penalty",
        "tl_max_chroma_delta",
        "tl_enable_bilateral_finish",
        "tl_bilateral_d",
        "tl_bilateral_sigma_color",
        "tl_bilateral_sigma_space",
        "tl_bilateral_alpha",
        "tl_enable_raw_gray_plane_projection",
        "tl_gray_plane_chroma_alpha",
        "tl_enable_cv_gray_lock",
        "tl_cv_gray_lock_alpha",
        "tl_cv_gray_lock_max_shift",
    }
    unknown = sorted(set(params) - supported)
    if unknown:
        raise ValueError(f"Unsupported full-flow params: {unknown}")

    original_uint8 = np.asarray(original_uint8, dtype=np.uint8)
    bph_uint8 = np.asarray(bph_uint8, dtype=np.uint8)
    bph_float = _to_float01(bph_uint8)

    mode = params.get("_mode", MODE_NAME)
    flow_version = str(params.get("flow_version", "v1")).lower()

    diagnosis = _diagnose_degradation(original_uint8, params)
    if bool(params.get("enable_frequency_detail_evidence", True)):
        detail = _build_detail_branch(original_uint8, bph_uint8, bph_float, diagnosis, imf1ray_params, params)
    else:
        detail = bph_uint8
    if bool(params.get("enable_contrast_evidence", True)):
        contrast = _build_safe_contrast_branch(original_uint8, bph_uint8, bph_float, diagnosis, rghs_params, params)
    else:
        contrast = bph_uint8
    if bool(params.get("enable_visibility_evidence", True)):
        visibility = _build_local_visibility_branch(original_uint8, bph_uint8, bph_float, diagnosis, clahe_params, params)
    else:
        visibility = bph_uint8

    if mode == MODE_NAME_TOPOLOGY_LOCKED or flow_version == "topology_locked_visual_chroma_v1":
        fused = _topology_locked_visual_chroma_fusion(
            original_uint8,
            bph_uint8,
            detail,
            contrast,
            visibility,
            diagnosis,
            params,
        )
    elif mode == MODE_NAME_V2 or flow_version == "detector_compatible_v2":
        if bool(params.get("enable_topology_compatible_fusion", True)):
            fused = _detector_compatible_fusion(original_uint8, bph_uint8, detail, contrast, visibility, diagnosis, params)
        else:
            fused = _downstream_aware_fusion(original_uint8, bph_uint8, detail, contrast, visibility, diagnosis, fusion_params, params)
    else:
        fused = _downstream_aware_fusion(original_uint8, bph_uint8, detail, contrast, visibility, diagnosis, fusion_params, params)
    if bool(params.get("enable_bounded_fusion_selection", True)):
        fused = _bounded_output_selection(original_uint8, bph_uint8, fused, params)
    final = _final_closure(original_uint8, fused, diagnosis, params)
    final = _support_guided_pullback(bph_uint8, final, diagnosis, params, "final")
    final = _bounded_output_selection(original_uint8, bph_uint8, final, params)
    if (
        mode == MODE_NAME_TOPOLOGY_LOCKED
        and bool(params.get("tl_enable_raw_gray_plane_projection", False))
    ):
        final = _project_to_raw_cv_gray_plane(
            original_uint8,
            final,
            chroma_alpha=float(params.get("tl_gray_plane_chroma_alpha", 0.90)),
        )

    return {
        "IMF1Ray": detail,
        "RGHS": contrast,
        "CLAHE": visibility,
        "Fused": fused,
        "Final": final,
    }
