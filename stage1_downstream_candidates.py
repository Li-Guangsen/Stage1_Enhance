"""Experimental downstream-driven final-stage candidates for Stage1Codex.

These modes are archived diagnostic candidates. They are not the locked Stage1
mainline and only run when a config explicitly sets the corresponding
``final.mode``. Keeping them out of ``main.py`` prevents candidate accumulation
from obscuring the production seven-stage pipeline.
"""

import cv2
import numpy as np


def _pick_final_source(name, fused_uint8, original_uint8=None, bph_uint8=None):
    if name == "fused":
        return fused_uint8
    if name == "original":
        if original_uint8 is None:
            raise ValueError("final source `original` requires original_uint8")
        return original_uint8
    if name == "bph":
        if bph_uint8 is None:
            raise ValueError("final source `bph` requires bph_uint8")
        return bph_uint8
    raise ValueError(f"未知 final source: {name}")


def _final_source_requirements(final_params):
    params = dict(final_params or {})
    enabled = bool(params.pop("enabled", True))
    if not enabled:
        return {"bph": True, "fused": True}
    mode = params.pop("mode", "homomorphic")
    if mode in {"homomorphic", "entropy", "homomorphic_entropy", "none"}:
        return {"bph": True, "fused": True}
    if mode in {"original", "generic_luma_clahe", "generic_luma_gamma"}:
        return {"bph": False, "fused": False}
    if mode in {
        "edge_safe_gamma_bph",
        "boundary_aware_luma_bph",
        "microstructure_csp_bph",
        "topology_guarded_microfusion_bph",
        "topology_pruned_microfusion_bph",
        "endpoint_stabilized_weak_boundary_bph",
        "ac_guarded_weak_boundary_bph",
        "dual_anchor_false_edge_floor_bph",
        "raw_detail_lowfreq_chroma_bph",
        "downstream_d01_structure_flow_bph",
        "degradation_aware_pyramid_frequency_bph",
        "weak_boundary_pyramid_fusion_bph",
    }:
        return {"bph": True, "fused": False}
    if mode == "bph":
        return {"bph": True, "fused": False}
    if mode == "edge_preserve_blend":
        sources = {params.get("base", "original"), params.get("color_source", "bph")}
        return {"bph": "bph" in sources, "fused": "fused" in sources}
    return {"bph": True, "fused": True}


def _edge_preserve_blend(fused_uint8, original_uint8=None, bph_uint8=None, **params):
    """Mild Lab-domain blend for downstream edge-detector safety.

    The mode keeps luminance close to the selected base image and only transfers
    a limited amount of color/illumination from a Stage1 source. It is intended
    for downstream diagnostics, not as a replacement for the locked paper
    mainline.
    """
    base_name = params.pop("base", "original")
    source_name = params.pop("color_source", "bph")
    luma_alpha = float(params.pop("luma_alpha", 0.05))
    chroma_alpha = float(params.pop("chroma_alpha", 0.20))
    post_blend_alpha = float(params.pop("post_blend_alpha", 1.0))
    luma_alpha = float(np.clip(luma_alpha, 0.0, 1.0))
    chroma_alpha = float(np.clip(chroma_alpha, 0.0, 1.0))
    post_blend_alpha = float(np.clip(post_blend_alpha, 0.0, 1.0))
    if params:
        raise ValueError(f"edge_preserve_blend 不支持的参数: {sorted(params.keys())}")

    base = _pick_final_source(base_name, fused_uint8, original_uint8, bph_uint8)
    source = _pick_final_source(source_name, fused_uint8, original_uint8, bph_uint8)
    base_lab = cv2.cvtColor(base, cv2.COLOR_BGR2LAB).astype(np.float32)
    source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype(np.float32)
    mixed_lab = base_lab.copy()
    mixed_lab[..., 0] = (1.0 - luma_alpha) * base_lab[..., 0] + luma_alpha * source_lab[..., 0]
    mixed_lab[..., 1] = (1.0 - chroma_alpha) * base_lab[..., 1] + chroma_alpha * source_lab[..., 1]
    mixed_lab[..., 2] = (1.0 - chroma_alpha) * base_lab[..., 2] + chroma_alpha * source_lab[..., 2]
    mixed = cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    if post_blend_alpha < 1.0:
        mixed = cv2.addWeighted(base, 1.0 - post_blend_alpha, mixed, post_blend_alpha, 0)
    return mixed


def _generic_luma_clahe(original_uint8, **params):
    """Apply a generic luminance-only CLAHE control on the raw image.

    This is a downstream-control mode: it perturbs raw luminance while preserving
    raw Lab chroma, so it can test whether P4 signals are Stage1/BPH-specific or
    merely caused by a generic contrast adjustment.
    """
    clip_limit = float(params.pop("clip_limit", 1.2))
    tile_size = params.pop("tile_size", [8, 8])
    luma_alpha = float(params.pop("luma_alpha", 0.25))
    if params:
        raise ValueError(f"generic_luma_clahe 不支持的参数: {sorted(params.keys())}")
    if isinstance(tile_size, int):
        tile_grid_size = (int(tile_size), int(tile_size))
    else:
        if len(tile_size) != 2:
            raise ValueError("generic_luma_clahe.tile_size 必须是整数或长度为 2 的列表")
        tile_grid_size = (int(tile_size[0]), int(tile_size[1]))
    tile_grid_size = (max(1, tile_grid_size[0]), max(1, tile_grid_size[1]))
    luma_alpha = float(np.clip(luma_alpha, 0.0, 1.0))

    lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    l_orig = lab[..., 0].astype(np.uint8)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    l_eq = clahe.apply(l_orig).astype(np.float32)
    lab[..., 0] = (1.0 - luma_alpha) * lab[..., 0] + luma_alpha * l_eq
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _generic_luma_gamma(original_uint8, **params):
    """Apply a generic luminance-only gamma/contrast control on the raw image."""
    gamma = float(params.pop("gamma", 0.95))
    contrast_alpha = float(params.pop("contrast_alpha", 1.03))
    beta = float(params.pop("beta", 0.0))
    luma_alpha = float(params.pop("luma_alpha", 0.35))
    if params:
        raise ValueError(f"generic_luma_gamma 不支持的参数: {sorted(params.keys())}")
    gamma = max(gamma, 1e-6)
    luma_alpha = float(np.clip(luma_alpha, 0.0, 1.0))

    lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    l_orig = lab[..., 0] / 255.0
    adjusted = np.power(np.clip(l_orig, 0.0, 1.0), gamma)
    mean_l = float(np.mean(l_orig))
    adjusted = mean_l + contrast_alpha * (adjusted - mean_l) + beta / 255.0
    adjusted = np.clip(adjusted, 0.0, 1.0) * 255.0
    lab[..., 0] = (1.0 - luma_alpha) * lab[..., 0] + luma_alpha * adjusted
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _edge_safe_gamma_bph(original_uint8, bph_uint8=None, **params):
    """Luminance-safe gamma control with mild BPH chroma transfer.

    This diagnostic mode combines the two least damaging signals observed so
    far: raw-domain luminance perturbation and very small BPH color transfer.
    It intentionally skips IMF1Ray/RGHS/CLAHE/Fusion/legacy Final so that the
    detector sees a near-raw spatial structure.
    """
    if bph_uint8 is None:
        raise ValueError("edge_safe_gamma_bph requires bph_uint8")
    gamma = float(params.pop("gamma", 0.95))
    contrast_alpha = float(params.pop("contrast_alpha", 1.02))
    beta = float(params.pop("beta", 0.0))
    luma_alpha = float(params.pop("luma_alpha", 0.25))
    chroma_alpha = float(params.pop("chroma_alpha", 0.10))
    if params:
        raise ValueError(f"edge_safe_gamma_bph 不支持的参数: {sorted(params.keys())}")
    gamma = max(gamma, 1e-6)
    luma_alpha = float(np.clip(luma_alpha, 0.0, 1.0))
    chroma_alpha = float(np.clip(chroma_alpha, 0.0, 1.0))

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)

    l_orig = raw_lab[..., 0] / 255.0
    adjusted = np.power(np.clip(l_orig, 0.0, 1.0), gamma)
    mean_l = float(np.mean(l_orig))
    adjusted = mean_l + contrast_alpha * (adjusted - mean_l) + beta / 255.0
    adjusted = np.clip(adjusted, 0.0, 1.0) * 255.0

    mixed_lab = raw_lab.copy()
    mixed_lab[..., 0] = (1.0 - luma_alpha) * raw_lab[..., 0] + luma_alpha * adjusted
    mixed_lab[..., 1] = (1.0 - chroma_alpha) * raw_lab[..., 1] + chroma_alpha * bph_lab[..., 1]
    mixed_lab[..., 2] = (1.0 - chroma_alpha) * raw_lab[..., 2] + chroma_alpha * bph_lab[..., 2]
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _boundary_aware_luma_bph(original_uint8, bph_uint8=None, **params):
    """Boundary-aware luminance adjustment with mild BPH chroma transfer.

    This downstream-driven diagnostic mode keeps the detector input close to
    raw while using a gradient mask to separate likely boundary pixels from
    low-gradient background. Background areas receive light smoothing to reduce
    pseudo edges; likely boundaries receive clipped unsharp support to improve
    continuity without the legacy high-frequency/fusion stages.
    """
    if bph_uint8 is None:
        raise ValueError("boundary_aware_luma_bph requires bph_uint8")
    gamma = float(params.pop("gamma", 0.97))
    contrast_alpha = float(params.pop("contrast_alpha", 1.015))
    beta = float(params.pop("beta", 0.0))
    luma_alpha = float(params.pop("luma_alpha", 0.18))
    chroma_alpha = float(params.pop("chroma_alpha", 0.08))
    denoise_alpha = float(params.pop("denoise_alpha", 0.10))
    sharpen_alpha = float(params.pop("sharpen_alpha", 0.08))
    max_luma_delta = float(params.pop("max_luma_delta", 6.0))
    grad_low_percentile = float(params.pop("grad_low_percentile", 45.0))
    grad_high_percentile = float(params.pop("grad_high_percentile", 82.0))
    mask_blur_ksize = int(params.pop("mask_blur_ksize", 5))
    bilateral_d = int(params.pop("bilateral_d", 5))
    bilateral_sigma_color = float(params.pop("bilateral_sigma_color", 18.0))
    bilateral_sigma_space = float(params.pop("bilateral_sigma_space", 5.0))
    unsharp_sigma = float(params.pop("unsharp_sigma", 1.0))
    if params:
        raise ValueError(f"boundary_aware_luma_bph 不支持的参数: {sorted(params.keys())}")

    gamma = max(gamma, 1e-6)
    luma_alpha = float(np.clip(luma_alpha, 0.0, 1.0))
    chroma_alpha = float(np.clip(chroma_alpha, 0.0, 1.0))
    denoise_alpha = float(np.clip(denoise_alpha, 0.0, 1.0))
    sharpen_alpha = float(np.clip(sharpen_alpha, 0.0, 1.0))
    max_luma_delta = max(0.0, max_luma_delta)
    grad_low_percentile = float(np.clip(grad_low_percentile, 0.0, 100.0))
    grad_high_percentile = float(np.clip(grad_high_percentile, 0.0, 100.0))
    if grad_high_percentile <= grad_low_percentile:
        grad_high_percentile = min(100.0, grad_low_percentile + 1.0)
    if mask_blur_ksize < 1:
        mask_blur_ksize = 1
    if mask_blur_ksize % 2 == 0:
        mask_blur_ksize += 1
    bilateral_d = max(1, bilateral_d)

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]

    sobel_x = cv2.Sobel(raw_l, cv2.CV_32F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(raw_l, cv2.CV_32F, 0, 1, ksize=3)
    grad = cv2.magnitude(sobel_x, sobel_y)
    low = float(np.percentile(grad, grad_low_percentile))
    high = float(np.percentile(grad, grad_high_percentile))
    scale = max(high - low, 1e-6)
    edge_mask = np.clip((grad - low) / scale, 0.0, 1.0)
    background_mask = 1.0 - edge_mask
    if mask_blur_ksize > 1:
        edge_mask = cv2.GaussianBlur(edge_mask, (mask_blur_ksize, mask_blur_ksize), 0)
        background_mask = cv2.GaussianBlur(background_mask, (mask_blur_ksize, mask_blur_ksize), 0)
    edge_mask = np.clip(edge_mask, 0.0, 1.0)
    background_mask = np.clip(background_mask, 0.0, 1.0)

    raw_l_norm = raw_l / 255.0
    gamma_l = np.power(np.clip(raw_l_norm, 0.0, 1.0), gamma)
    mean_l = float(np.mean(raw_l_norm))
    gamma_l = mean_l + contrast_alpha * (gamma_l - mean_l) + beta / 255.0
    gamma_l = np.clip(gamma_l, 0.0, 1.0) * 255.0

    smooth_l = cv2.bilateralFilter(
        raw_l.astype(np.uint8),
        bilateral_d,
        bilateral_sigma_color,
        bilateral_sigma_space,
    ).astype(np.float32)
    blur_l = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=max(unsharp_sigma, 1e-6))
    unsharp_l = np.clip(raw_l + (raw_l - blur_l), 0.0, 255.0)

    target_l = raw_l.copy()
    target_l += luma_alpha * (gamma_l - raw_l)
    target_l += denoise_alpha * background_mask * (smooth_l - raw_l)
    target_l += sharpen_alpha * edge_mask * (unsharp_l - raw_l)
    if max_luma_delta > 0:
        target_l = np.clip(target_l, raw_l - max_luma_delta, raw_l + max_luma_delta)
    target_l = np.clip(target_l, 0.0, 255.0)

    mixed_lab = raw_lab.copy()
    mixed_lab[..., 0] = target_l
    mixed_lab[..., 1] = (1.0 - chroma_alpha) * raw_lab[..., 1] + chroma_alpha * bph_lab[..., 1]
    mixed_lab[..., 2] = (1.0 - chroma_alpha) * raw_lab[..., 2] + chroma_alpha * bph_lab[..., 2]
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _as_float_list(value, default):
    if value is None:
        return [float(x) for x in default]
    if isinstance(value, (int, float)):
        return [float(value)]
    return [float(x) for x in value]


def _odd_ksize(value, minimum=1):
    ksize = max(int(value), int(minimum))
    if ksize % 2 == 0:
        ksize += 1
    return ksize


def _candidate_luma_score(raw_l, candidate_l, edge_mask, background_mask, background_weight, delta_weight, saturation_weight):
    raw_x = cv2.Sobel(raw_l, cv2.CV_32F, 1, 0, ksize=3)
    raw_y = cv2.Sobel(raw_l, cv2.CV_32F, 0, 1, ksize=3)
    cand_x = cv2.Sobel(candidate_l, cv2.CV_32F, 1, 0, ksize=3)
    cand_y = cv2.Sobel(candidate_l, cv2.CV_32F, 0, 1, ksize=3)
    raw_grad = cv2.magnitude(raw_x, raw_y)
    cand_grad = cv2.magnitude(cand_x, cand_y)
    eps = 1e-6
    edge_gain = float(np.sum(cand_grad * edge_mask) / (np.sum(raw_grad * edge_mask) + eps))
    bg_gain = float(np.sum(cand_grad * background_mask) / (np.sum(raw_grad * background_mask) + eps))
    structure_delta = float(np.mean(np.abs(candidate_l - raw_l)) / 255.0)
    saturation = float(np.mean((candidate_l <= 2.0) | (candidate_l >= 253.0)))
    contrast_gain = float((np.std(candidate_l) + eps) / (np.std(raw_l) + eps))
    return (
        edge_gain
        + 0.12 * contrast_gain
        - background_weight * max(0.0, bg_gain - 1.0)
        - delta_weight * structure_delta
        - saturation_weight * saturation
    )


def _normalize_by_percentiles(values, low_percentile=10.0, high_percentile=90.0):
    low = float(np.percentile(values, np.clip(low_percentile, 0.0, 100.0)))
    high = float(np.percentile(values, np.clip(high_percentile, 0.0, 100.0)))
    return np.clip((values - low) / max(high - low, 1e-6), 0.0, 1.0)


def _microstructure_csp_bph(original_uint8, bph_uint8=None, **params):
    """Conservative microscopy structure-preserving candidate for C01.

    This non-mainline mode is designed from the downstream_driven_v1 method
    synthesis. It keeps raw luminance dominant, adds clipped gray-world color
    compensation, extracts local bright/dark and weak-structure residuals, and
    uses texture-risk guards plus fallback to avoid background false edges.
    """
    if bph_uint8 is None:
        raise ValueError("microstructure_csp_bph requires bph_uint8")

    wb_gain_cap = params.pop("wb_gain_cap", [0.90, 1.10])
    channel_imbalance_skip = float(params.pop("channel_imbalance_skip", 0.03))
    wb_luma_alpha = float(params.pop("wb_luma_alpha", 0.06))
    wb_chroma_alpha = float(params.pop("wb_chroma_alpha", 0.12))
    bph_chroma_alpha = float(params.pop("bph_chroma_alpha", 0.04))
    window_size = _odd_ksize(params.pop("window_size", 31), minimum=3)
    contrast_alpha = float(params.pop("contrast_alpha", 0.06))
    structure_alpha = float(params.pop("structure_alpha", 0.08))
    denoise_alpha = float(params.pop("denoise_alpha", 0.06))
    max_luma_delta = float(params.pop("max_luma_delta", 5.0))
    guard_ratio = float(params.pop("guard_ratio", 1.10))
    guard_local_var_ratio = float(params.pop("guard_local_var_ratio", guard_ratio))
    grad_low_percentile = float(params.pop("grad_low_percentile", 45.0))
    grad_high_percentile = float(params.pop("grad_high_percentile", 88.0))
    texture_low_percentile = float(params.pop("texture_low_percentile", 55.0))
    texture_high_percentile = float(params.pop("texture_high_percentile", 92.0))
    mask_blur_ksize = _odd_ksize(params.pop("mask_blur_ksize", 5), minimum=1)
    bilateral_d = int(params.pop("bilateral_d", 5))
    bilateral_sigma_color = float(params.pop("bilateral_sigma_color", 16.0))
    bilateral_sigma_space = float(params.pop("bilateral_sigma_space", 5.0))
    detail_sigmas = _as_float_list(params.pop("detail_sigmas", None), [1.0, 2.0])
    structure_power = float(params.pop("structure_power", 1.25))
    texture_risk_power = float(params.pop("texture_risk_power", 1.20))
    if params:
        raise ValueError(f"microstructure_csp_bph 不支持的参数: {sorted(params.keys())}")

    if isinstance(wb_gain_cap, (int, float)):
        gain_low, gain_high = 1.0 / float(wb_gain_cap), float(wb_gain_cap)
    else:
        if len(wb_gain_cap) != 2:
            raise ValueError("wb_gain_cap must be a number or length-2 list")
        gain_low, gain_high = float(wb_gain_cap[0]), float(wb_gain_cap[1])
    gain_low, gain_high = min(gain_low, gain_high), max(gain_low, gain_high)
    wb_luma_alpha = float(np.clip(wb_luma_alpha, 0.0, 1.0))
    wb_chroma_alpha = float(np.clip(wb_chroma_alpha, 0.0, 1.0))
    bph_chroma_alpha = float(np.clip(bph_chroma_alpha, 0.0, 1.0))
    contrast_alpha = float(np.clip(contrast_alpha, 0.0, 1.0))
    structure_alpha = float(np.clip(structure_alpha, 0.0, 1.0))
    denoise_alpha = float(np.clip(denoise_alpha, 0.0, 1.0))
    max_luma_delta = max(0.0, max_luma_delta)
    guard_ratio = max(1.0, guard_ratio)
    guard_local_var_ratio = max(1.0, guard_local_var_ratio)
    bilateral_d = max(1, bilateral_d)
    structure_power = max(structure_power, 1e-6)
    texture_risk_power = max(texture_risk_power, 1e-6)

    raw_f = original_uint8.astype(np.float32)
    channel_means = np.mean(raw_f.reshape(-1, 3), axis=0)
    mean_all = float(np.mean(channel_means))
    imbalance = float(np.std(channel_means) / max(mean_all, 1e-6))
    gains = np.ones(3, dtype=np.float32)
    if imbalance >= channel_imbalance_skip:
        gains = np.clip(mean_all / np.maximum(channel_means, 1e-6), gain_low, gain_high).astype(np.float32)
    wb_uint8 = np.clip(raw_f * gains.reshape(1, 1, 3), 0, 255).astype(np.uint8)

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    wb_lab = cv2.cvtColor(wb_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    wb_l = wb_lab[..., 0]

    grad_x = cv2.Sobel(raw_l, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(raw_l, cv2.CV_32F, 0, 1, ksize=3)
    raw_grad = cv2.magnitude(grad_x, grad_y)
    edge_conf = _normalize_by_percentiles(raw_grad, grad_low_percentile, grad_high_percentile)

    stable_detail = np.zeros_like(raw_l, dtype=np.float32)
    stable_grad = np.zeros_like(raw_l, dtype=np.float32)
    for sigma in detail_sigmas:
        sigma = max(float(sigma), 1e-6)
        smooth = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=sigma)
        stable_detail += raw_l - smooth
        sx = cv2.Sobel(smooth, cv2.CV_32F, 1, 0, ksize=3)
        sy = cv2.Sobel(smooth, cv2.CV_32F, 0, 1, ksize=3)
        stable_grad += cv2.magnitude(sx, sy)
    stable_detail /= max(len(detail_sigmas), 1)
    stable_grad /= max(len(detail_sigmas), 1)
    stable_edge = _normalize_by_percentiles(stable_grad, grad_low_percentile, grad_high_percentile)
    structure_conf = np.power(np.clip(np.sqrt(edge_conf * stable_edge), 0.0, 1.0), structure_power)

    local_mean = cv2.blur(raw_l, (window_size, window_size))
    bright_residual = np.maximum(raw_l - local_mean, 0.0)
    dark_residual = np.maximum(local_mean - raw_l, 0.0)
    contrast_residual = bright_residual - dark_residual
    contrast_scale = float(np.percentile(np.abs(contrast_residual), 95.0))
    if contrast_scale > 1e-6:
        contrast_residual = np.clip(contrast_residual, -contrast_scale, contrast_scale)

    local_mean_g = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=1.5)
    local_mean_sq = cv2.GaussianBlur(raw_l * raw_l, (0, 0), sigmaX=1.5)
    local_std = np.sqrt(np.maximum(local_mean_sq - local_mean_g * local_mean_g, 0.0))
    texture_risk = _normalize_by_percentiles(local_std, texture_low_percentile, texture_high_percentile)
    high_freq = _normalize_by_percentiles(np.abs(stable_detail), 60.0, 95.0)
    texture_risk = np.power(np.clip(0.65 * texture_risk + 0.35 * high_freq * (1.0 - structure_conf), 0.0, 1.0), texture_risk_power)
    safe_weight = np.clip((1.0 - texture_risk) * (0.25 + 0.75 * structure_conf), 0.0, 1.0)
    if mask_blur_ksize > 1:
        safe_weight = cv2.GaussianBlur(safe_weight, (mask_blur_ksize, mask_blur_ksize), 0)
    safe_weight = np.clip(safe_weight, 0.0, 1.0)
    background_weight = 1.0 - safe_weight

    smooth_l = cv2.bilateralFilter(
        np.clip(raw_l, 0, 255).astype(np.uint8),
        bilateral_d,
        bilateral_sigma_color,
        bilateral_sigma_space,
    ).astype(np.float32)

    def build_luma(alpha_c, alpha_s, alpha_d):
        target = raw_l.copy()
        target += wb_luma_alpha * (wb_l - raw_l)
        target += alpha_c * safe_weight * contrast_residual
        target += alpha_s * safe_weight * stable_detail
        target += alpha_d * background_weight * (smooth_l - target)
        if max_luma_delta > 0:
            target = np.clip(target, raw_l - max_luma_delta, raw_l + max_luma_delta)
        return np.clip(target, 0.0, 255.0)

    def guard_pass(candidate_l):
        cand_x = cv2.Sobel(candidate_l, cv2.CV_32F, 1, 0, ksize=3)
        cand_y = cv2.Sobel(candidate_l, cv2.CV_32F, 0, 1, ksize=3)
        cand_grad = cv2.magnitude(cand_x, cand_y)
        raw_grad_mean = float(np.mean(raw_grad)) + 1e-6
        cand_grad_mean = float(np.mean(cand_grad))
        raw_grad_p95 = float(np.percentile(raw_grad, 95.0)) + 1e-6
        cand_grad_p95 = float(np.percentile(cand_grad, 95.0))
        cand_mean = cv2.GaussianBlur(candidate_l, (0, 0), sigmaX=1.5)
        cand_mean_sq = cv2.GaussianBlur(candidate_l * candidate_l, (0, 0), sigmaX=1.5)
        cand_std = np.sqrt(np.maximum(cand_mean_sq - cand_mean * cand_mean, 0.0))
        raw_std_mean = float(np.mean(local_std)) + 1e-6
        cand_std_mean = float(np.mean(cand_std))
        return (
            cand_grad_mean <= raw_grad_mean * guard_ratio
            and cand_grad_p95 <= raw_grad_p95 * guard_ratio
            and cand_std_mean <= raw_std_mean * guard_local_var_ratio
        )

    fallback_steps = [
        (contrast_alpha, structure_alpha, denoise_alpha),
        (contrast_alpha, 0.0, denoise_alpha),
        (0.0, 0.0, min(denoise_alpha, 0.03)),
        (0.0, 0.0, 0.0),
    ]
    target_l = raw_l.copy()
    for alpha_c, alpha_s, alpha_d in fallback_steps:
        candidate_l = build_luma(alpha_c, alpha_s, alpha_d)
        target_l = candidate_l
        if guard_pass(candidate_l):
            break

    mixed_lab = raw_lab.copy()
    mixed_lab[..., 0] = target_l
    chroma_budget = min(wb_chroma_alpha + bph_chroma_alpha, 1.0)
    raw_chroma_weight = max(0.0, 1.0 - chroma_budget)
    mixed_lab[..., 1] = (
        raw_chroma_weight * raw_lab[..., 1]
        + wb_chroma_alpha * wb_lab[..., 1]
        + bph_chroma_alpha * bph_lab[..., 1]
    )
    mixed_lab[..., 2] = (
        raw_chroma_weight * raw_lab[..., 2]
        + wb_chroma_alpha * wb_lab[..., 2]
        + bph_chroma_alpha * bph_lab[..., 2]
    )
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _degradation_aware_pyramid_frequency_bph(original_uint8, bph_uint8=None, **params):
    """Degradation-aware multi-branch enhancement for downstream edge tasks.

    This non-mainline mode performs per-image lightweight parameter selection
    and combines color-channel compensation, gamma/CLAHE/Retinex luminance
    candidates, multi-scale detail support, background pseudo-edge suppression,
    and capped structure-preserving fusion. It is designed for P12 diagnostics:
    stronger than the earlier mild gamma controls, but still guarded against
    the legacy Final failure mode.
    """
    if bph_uint8 is None:
        raise ValueError("degradation_aware_pyramid_frequency_bph requires bph_uint8")

    gamma_candidates = _as_float_list(params.pop("gamma_candidates", None), [0.90, 0.95, 1.00])
    contrast_candidates = _as_float_list(params.pop("contrast_candidates", None), [1.00, 1.04, 1.08])
    clahe_clip_candidates = _as_float_list(params.pop("clahe_clip_candidates", None), [1.20, 1.60])
    luma_alpha = float(params.pop("luma_alpha", 0.42))
    clahe_alpha = float(params.pop("clahe_alpha", 0.20))
    retinex_alpha = float(params.pop("retinex_alpha", 0.10))
    detail_alpha = float(params.pop("detail_alpha", 0.12))
    bph_detail_alpha = float(params.pop("bph_detail_alpha", 0.04))
    denoise_alpha = float(params.pop("denoise_alpha", 0.18))
    pseudoedge_suppress_alpha = float(params.pop("pseudoedge_suppress_alpha", 0.18))
    chroma_alpha = float(params.pop("chroma_alpha", 0.14))
    max_luma_delta = float(params.pop("max_luma_delta", 12.0))
    grad_low_percentile = float(params.pop("grad_low_percentile", 45.0))
    grad_high_percentile = float(params.pop("grad_high_percentile", 86.0))
    mask_blur_ksize = _odd_ksize(params.pop("mask_blur_ksize", 7), minimum=1)
    clahe_tile_size = params.pop("clahe_tile_size", [8, 8])
    bilateral_d = int(params.pop("bilateral_d", 5))
    bilateral_sigma_color = float(params.pop("bilateral_sigma_color", 18.0))
    bilateral_sigma_space = float(params.pop("bilateral_sigma_space", 6.0))
    detail_sigmas = _as_float_list(params.pop("detail_sigmas", None), [0.8, 1.6])
    retinex_sigma = float(params.pop("retinex_sigma", 18.0))
    background_weight = float(params.pop("background_weight", 0.45))
    delta_weight = float(params.pop("delta_weight", 1.10))
    saturation_weight = float(params.pop("saturation_weight", 1.40))
    raw_edge_rescue_alpha = float(params.pop("raw_edge_rescue_alpha", 0.0))
    raw_edge_rescue_power = float(params.pop("raw_edge_rescue_power", 1.0))
    raw_global_blend_alpha = float(params.pop("raw_global_blend_alpha", 0.0))
    if params:
        raise ValueError(f"degradation_aware_pyramid_frequency_bph 不支持的参数: {sorted(params.keys())}")

    luma_alpha = float(np.clip(luma_alpha, 0.0, 1.0))
    clahe_alpha = float(np.clip(clahe_alpha, 0.0, 1.0))
    retinex_alpha = float(np.clip(retinex_alpha, 0.0, 1.0))
    detail_alpha = float(np.clip(detail_alpha, 0.0, 1.0))
    bph_detail_alpha = float(np.clip(bph_detail_alpha, 0.0, 1.0))
    denoise_alpha = float(np.clip(denoise_alpha, 0.0, 1.0))
    pseudoedge_suppress_alpha = float(np.clip(pseudoedge_suppress_alpha, 0.0, 1.0))
    chroma_alpha = float(np.clip(chroma_alpha, 0.0, 1.0))
    raw_edge_rescue_alpha = float(np.clip(raw_edge_rescue_alpha, 0.0, 1.0))
    raw_edge_rescue_power = max(float(raw_edge_rescue_power), 1e-6)
    raw_global_blend_alpha = float(np.clip(raw_global_blend_alpha, 0.0, 1.0))
    max_luma_delta = max(0.0, max_luma_delta)
    bilateral_d = max(1, bilateral_d)
    if isinstance(clahe_tile_size, int):
        tile_grid_size = (int(clahe_tile_size), int(clahe_tile_size))
    else:
        if len(clahe_tile_size) != 2:
            raise ValueError("clahe_tile_size must be an int or a length-2 list")
        tile_grid_size = (int(clahe_tile_size[0]), int(clahe_tile_size[1]))
    tile_grid_size = (max(1, tile_grid_size[0]), max(1, tile_grid_size[1]))

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    bph_l = bph_lab[..., 0]

    grad_x = cv2.Sobel(raw_l, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(raw_l, cv2.CV_32F, 0, 1, ksize=3)
    grad = cv2.magnitude(grad_x, grad_y)
    low = float(np.percentile(grad, np.clip(grad_low_percentile, 0.0, 100.0)))
    high = float(np.percentile(grad, np.clip(grad_high_percentile, 0.0, 100.0)))
    if high <= low:
        high = low + 1e-6
    edge_mask = np.clip((grad - low) / (high - low), 0.0, 1.0)
    if mask_blur_ksize > 1:
        edge_mask = cv2.GaussianBlur(edge_mask, (mask_blur_ksize, mask_blur_ksize), 0)
    edge_mask = np.clip(edge_mask, 0.0, 1.0)
    background_mask = 1.0 - edge_mask

    clahe_maps = []
    raw_l_uint8 = np.clip(raw_l, 0, 255).astype(np.uint8)
    for clip_limit in clahe_clip_candidates:
        clahe = cv2.createCLAHE(clipLimit=max(float(clip_limit), 0.01), tileGridSize=tile_grid_size)
        clahe_maps.append(clahe.apply(raw_l_uint8).astype(np.float32))

    blur_for_retinex = cv2.GaussianBlur(raw_l + 1.0, (0, 0), sigmaX=max(retinex_sigma, 1e-6))
    retinex = np.log(raw_l + 1.0) - np.log(np.maximum(blur_for_retinex, 1.0))
    retinex = (retinex - float(np.mean(retinex))) / (float(np.std(retinex)) + 1e-6)
    retinex_l = np.clip(raw_l + retinex * 7.5, 0.0, 255.0)

    raw_l_norm = raw_l / 255.0
    mean_l = float(np.mean(raw_l_norm))
    best_l = raw_l.copy()
    best_score = -1e18
    for gamma in gamma_candidates:
        gamma = max(float(gamma), 1e-6)
        gamma_l = np.power(np.clip(raw_l_norm, 0.0, 1.0), gamma)
        for contrast_alpha in contrast_candidates:
            contrast_alpha = float(contrast_alpha)
            contrast_l = mean_l + contrast_alpha * (gamma_l - mean_l)
            contrast_l = np.clip(contrast_l, 0.0, 1.0) * 255.0
            for clahe_l in clahe_maps:
                candidate = raw_l.copy()
                candidate += luma_alpha * (contrast_l - raw_l)
                candidate += clahe_alpha * edge_mask * (clahe_l - raw_l)
                candidate += retinex_alpha * (0.35 + 0.65 * edge_mask) * (retinex_l - raw_l)
                if max_luma_delta > 0:
                    candidate = np.clip(candidate, raw_l - max_luma_delta, raw_l + max_luma_delta)
                candidate = np.clip(candidate, 0.0, 255.0)
                score = _candidate_luma_score(
                    raw_l,
                    candidate,
                    edge_mask,
                    background_mask,
                    background_weight,
                    delta_weight,
                    saturation_weight,
                )
                if score > best_score:
                    best_score = score
                    best_l = candidate

    detail = np.zeros_like(raw_l, dtype=np.float32)
    for sigma in detail_sigmas:
        sigma = max(float(sigma), 1e-6)
        detail += raw_l - cv2.GaussianBlur(raw_l, (0, 0), sigmaX=sigma)
    detail /= max(len(detail_sigmas), 1)
    bph_detail = bph_l - cv2.GaussianBlur(bph_l, (0, 0), sigmaX=1.2)

    smooth_l = cv2.bilateralFilter(
        np.clip(raw_l, 0, 255).astype(np.uint8),
        bilateral_d,
        bilateral_sigma_color,
        bilateral_sigma_space,
    ).astype(np.float32)
    target_l = best_l.copy()
    target_l += detail_alpha * edge_mask * detail
    target_l += bph_detail_alpha * edge_mask * bph_detail
    target_l += denoise_alpha * background_mask * (smooth_l - target_l)

    target_x = cv2.Sobel(target_l, cv2.CV_32F, 1, 0, ksize=3)
    target_y = cv2.Sobel(target_l, cv2.CV_32F, 0, 1, ksize=3)
    target_grad = cv2.magnitude(target_x, target_y)
    pseudo_delta = np.maximum(target_grad - grad, 0.0)
    pseudo_high = float(np.percentile(pseudo_delta, 85.0))
    pseudo_mask = background_mask * np.clip(pseudo_delta / max(pseudo_high, 1e-6), 0.0, 1.0)
    target_l = (1.0 - pseudoedge_suppress_alpha * pseudo_mask) * target_l + (
        pseudoedge_suppress_alpha * pseudo_mask
    ) * smooth_l
    if raw_edge_rescue_alpha > 0:
        rescue_mask = np.power(np.clip(edge_mask, 0.0, 1.0), raw_edge_rescue_power)
        target_l = (1.0 - raw_edge_rescue_alpha * rescue_mask) * target_l + (
            raw_edge_rescue_alpha * rescue_mask
        ) * raw_l
    if raw_global_blend_alpha > 0:
        target_l = (1.0 - raw_global_blend_alpha) * target_l + raw_global_blend_alpha * raw_l

    if max_luma_delta > 0:
        target_l = np.clip(target_l, raw_l - max_luma_delta, raw_l + max_luma_delta)
    target_l = np.clip(target_l, 0.0, 255.0)

    chroma_gain = chroma_alpha * (0.65 + 0.35 * background_mask)
    mixed_lab = raw_lab.copy()
    mixed_lab[..., 0] = target_l
    mixed_lab[..., 1] = (1.0 - chroma_gain) * raw_lab[..., 1] + chroma_gain * bph_lab[..., 1]
    mixed_lab[..., 2] = (1.0 - chroma_gain) * raw_lab[..., 2] + chroma_gain * bph_lab[..., 2]
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _weak_boundary_pyramid_fusion_bph(original_uint8, bph_uint8=None, **params):
    """Fuse a skeleton-safe base with a stronger multi-branch enhancement.

    P14 is a downstream-driven diagnostic mode. It first builds a conservative
    skeleton-safe base and a degradation-aware enhanced candidate, then transfers
    the enhanced candidate only in low-contrast weak-boundary regions. Background
    and strong raw edges are pulled back toward the base/raw image to suppress
    pseudo edges and preserve detector-domain crispness.
    """
    if bph_uint8 is None:
        raise ValueError("weak_boundary_pyramid_fusion_bph requires bph_uint8")

    base_params = dict(params.pop("base_params", {}))
    enhancement_params = dict(params.pop("enhancement_params", {}))
    fusion_alpha = float(params.pop("fusion_alpha", 0.62))
    structure_sharpen_alpha = float(params.pop("structure_sharpen_alpha", 0.05))
    bph_structure_alpha = float(params.pop("bph_structure_alpha", 0.02))
    background_denoise_alpha = float(params.pop("background_denoise_alpha", 0.10))
    pseudoedge_suppress_alpha = float(params.pop("pseudoedge_suppress_alpha", 0.22))
    raw_strong_edge_rescue_alpha = float(params.pop("raw_strong_edge_rescue_alpha", 0.20))
    raw_global_blend_alpha = float(params.pop("raw_global_blend_alpha", 0.04))
    chroma_fusion_alpha = float(params.pop("chroma_fusion_alpha", 0.18))
    max_luma_delta = float(params.pop("max_luma_delta", 9.0))
    local_std_sigma = float(params.pop("local_std_sigma", 3.0))
    std_low_percentile = float(params.pop("std_low_percentile", 20.0))
    std_high_percentile = float(params.pop("std_high_percentile", 82.0))
    grad_low_percentile = float(params.pop("grad_low_percentile", 45.0))
    grad_high_percentile = float(params.pop("grad_high_percentile", 88.0))
    mask_blur_ksize = _odd_ksize(params.pop("mask_blur_ksize", 7), minimum=1)
    detail_sigmas = _as_float_list(params.pop("detail_sigmas", None), [0.8, 1.6])
    bilateral_d = int(params.pop("bilateral_d", 5))
    bilateral_sigma_color = float(params.pop("bilateral_sigma_color", 18.0))
    bilateral_sigma_space = float(params.pop("bilateral_sigma_space", 6.0))
    if params:
        raise ValueError(f"weak_boundary_pyramid_fusion_bph 不支持的参数: {sorted(params.keys())}")

    fusion_alpha = float(np.clip(fusion_alpha, 0.0, 1.0))
    structure_sharpen_alpha = float(np.clip(structure_sharpen_alpha, 0.0, 1.0))
    bph_structure_alpha = float(np.clip(bph_structure_alpha, 0.0, 1.0))
    background_denoise_alpha = float(np.clip(background_denoise_alpha, 0.0, 1.0))
    pseudoedge_suppress_alpha = float(np.clip(pseudoedge_suppress_alpha, 0.0, 1.0))
    raw_strong_edge_rescue_alpha = float(np.clip(raw_strong_edge_rescue_alpha, 0.0, 1.0))
    raw_global_blend_alpha = float(np.clip(raw_global_blend_alpha, 0.0, 1.0))
    chroma_fusion_alpha = float(np.clip(chroma_fusion_alpha, 0.0, 1.0))
    max_luma_delta = max(0.0, max_luma_delta)
    local_std_sigma = max(local_std_sigma, 1e-6)
    bilateral_d = max(1, bilateral_d)

    base_uint8 = _boundary_aware_luma_bph(original_uint8, bph_uint8=bph_uint8, **base_params)
    enhanced_uint8 = _degradation_aware_pyramid_frequency_bph(
        original_uint8,
        bph_uint8=bph_uint8,
        **enhancement_params,
    )

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    base_lab = cv2.cvtColor(base_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    enhanced_lab = cv2.cvtColor(enhanced_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    bph_l = bph_lab[..., 0]
    base_l = base_lab[..., 0]
    enhanced_l = enhanced_lab[..., 0]

    raw_x = cv2.Sobel(raw_l, cv2.CV_32F, 1, 0, ksize=3)
    raw_y = cv2.Sobel(raw_l, cv2.CV_32F, 0, 1, ksize=3)
    bph_x = cv2.Sobel(bph_l, cv2.CV_32F, 1, 0, ksize=3)
    bph_y = cv2.Sobel(bph_l, cv2.CV_32F, 0, 1, ksize=3)
    raw_grad = cv2.magnitude(raw_x, raw_y)
    bph_grad = cv2.magnitude(bph_x, bph_y)

    grad_low = float(np.percentile(raw_grad, np.clip(grad_low_percentile, 0.0, 100.0)))
    grad_high = float(np.percentile(raw_grad, np.clip(grad_high_percentile, 0.0, 100.0)))
    raw_edge = np.clip((raw_grad - grad_low) / max(grad_high - grad_low, 1e-6), 0.0, 1.0)
    bph_edge = np.clip((bph_grad - grad_low) / max(grad_high - grad_low, 1e-6), 0.0, 1.0)
    reveal_delta = np.maximum(bph_grad - raw_grad, 0.0)
    reveal_high = float(np.percentile(reveal_delta, 90.0))
    reveal_mask = np.clip(reveal_delta / max(reveal_high, 1e-6), 0.0, 1.0)

    local_mean = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=local_std_sigma)
    local_mean_sq = cv2.GaussianBlur(raw_l * raw_l, (0, 0), sigmaX=local_std_sigma)
    local_std = np.sqrt(np.maximum(local_mean_sq - local_mean * local_mean, 0.0))
    std_low = float(np.percentile(local_std, np.clip(std_low_percentile, 0.0, 100.0)))
    std_high = float(np.percentile(local_std, np.clip(std_high_percentile, 0.0, 100.0)))
    low_contrast = np.clip((std_high - local_std) / max(std_high - std_low, 1e-6), 0.0, 1.0)

    weak_boundary_mask = (0.65 * raw_edge + 0.35 * bph_edge) * (0.45 + 0.55 * low_contrast)
    weak_boundary_mask += 0.25 * reveal_mask * low_contrast
    weak_boundary_mask = np.clip(weak_boundary_mask, 0.0, 1.0)
    if mask_blur_ksize > 1:
        weak_boundary_mask = cv2.GaussianBlur(
            weak_boundary_mask,
            (mask_blur_ksize, mask_blur_ksize),
            0,
        )
    weak_boundary_mask = np.clip(weak_boundary_mask, 0.0, 1.0)
    background_mask = np.clip(1.0 - weak_boundary_mask, 0.0, 1.0)

    target_l = base_l + fusion_alpha * weak_boundary_mask * (enhanced_l - base_l)
    raw_detail = np.zeros_like(raw_l, dtype=np.float32)
    bph_detail = np.zeros_like(raw_l, dtype=np.float32)
    for sigma in detail_sigmas:
        sigma = max(float(sigma), 1e-6)
        raw_detail += raw_l - cv2.GaussianBlur(raw_l, (0, 0), sigmaX=sigma)
        bph_detail += bph_l - cv2.GaussianBlur(bph_l, (0, 0), sigmaX=sigma)
    raw_detail /= max(len(detail_sigmas), 1)
    bph_detail /= max(len(detail_sigmas), 1)
    target_l += structure_sharpen_alpha * weak_boundary_mask * raw_detail
    target_l += bph_structure_alpha * weak_boundary_mask * bph_detail

    smooth_l = cv2.bilateralFilter(
        np.clip(base_l, 0, 255).astype(np.uint8),
        bilateral_d,
        bilateral_sigma_color,
        bilateral_sigma_space,
    ).astype(np.float32)
    target_l += background_denoise_alpha * background_mask * (smooth_l - target_l)

    target_x = cv2.Sobel(target_l, cv2.CV_32F, 1, 0, ksize=3)
    target_y = cv2.Sobel(target_l, cv2.CV_32F, 0, 1, ksize=3)
    target_grad = cv2.magnitude(target_x, target_y)
    pseudo_delta = np.maximum(target_grad - raw_grad, 0.0)
    pseudo_high = float(np.percentile(pseudo_delta, 88.0))
    pseudo_mask = background_mask * np.clip(pseudo_delta / max(pseudo_high, 1e-6), 0.0, 1.0)
    target_l = (1.0 - pseudoedge_suppress_alpha * pseudo_mask) * target_l + (
        pseudoedge_suppress_alpha * pseudo_mask
    ) * smooth_l

    strong_edge = np.power(np.clip(raw_edge, 0.0, 1.0), 1.5)
    target_l = (1.0 - raw_strong_edge_rescue_alpha * strong_edge) * target_l + (
        raw_strong_edge_rescue_alpha * strong_edge
    ) * raw_l
    if raw_global_blend_alpha > 0:
        target_l = (1.0 - raw_global_blend_alpha) * target_l + raw_global_blend_alpha * raw_l
    if max_luma_delta > 0:
        target_l = np.clip(target_l, raw_l - max_luma_delta, raw_l + max_luma_delta)
    target_l = np.clip(target_l, 0.0, 255.0)

    chroma_mask = chroma_fusion_alpha * np.clip(0.35 + 0.65 * weak_boundary_mask, 0.0, 1.0)
    mixed_lab = base_lab.copy()
    mixed_lab[..., 0] = target_l
    mixed_lab[..., 1] = (1.0 - chroma_mask) * base_lab[..., 1] + chroma_mask * enhanced_lab[..., 1]
    mixed_lab[..., 2] = (1.0 - chroma_mask) * base_lab[..., 2] + chroma_mask * enhanced_lab[..., 2]
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _topology_guarded_microfusion_bph(original_uint8, bph_uint8=None, **params):
    """Topology-guarded fusion of conservative and weak-boundary candidates.

    P17 keeps the P16 microstructure-preserving candidate as the spatial base
    and injects a guarded P15-style weak-boundary candidate only in stable,
    low-risk boundary regions. Background pseudo edges, isolated high-frequency
    spur responses and strong raw edges are pulled back toward raw/base before
    a per-image gradient guard accepts the result.
    """
    if bph_uint8 is None:
        raise ValueError("topology_guarded_microfusion_bph requires bph_uint8")

    base_params = dict(params.pop("base_params", {}))
    weak_params = dict(params.pop("weak_params", {}))
    fusion_alpha = float(params.pop("fusion_alpha", 0.36))
    structure_sharpen_alpha = float(params.pop("structure_sharpen_alpha", 0.018))
    bph_structure_alpha = float(params.pop("bph_structure_alpha", 0.006))
    background_denoise_alpha = float(params.pop("background_denoise_alpha", 0.18))
    pseudoedge_suppress_alpha = float(params.pop("pseudoedge_suppress_alpha", 0.46))
    spur_suppress_alpha = float(params.pop("spur_suppress_alpha", 0.38))
    raw_strong_edge_rescue_alpha = float(params.pop("raw_strong_edge_rescue_alpha", 0.42))
    raw_strong_edge_power = float(params.pop("raw_strong_edge_power", 1.55))
    raw_global_blend_alpha = float(params.pop("raw_global_blend_alpha", 0.10))
    chroma_fusion_alpha = float(params.pop("chroma_fusion_alpha", 0.08))
    max_luma_delta = float(params.pop("max_luma_delta", 5.5))
    local_std_sigma = float(params.pop("local_std_sigma", 3.0))
    grad_low_percentile = float(params.pop("grad_low_percentile", 48.0))
    grad_high_percentile = float(params.pop("grad_high_percentile", 90.0))
    std_low_percentile = float(params.pop("std_low_percentile", 20.0))
    std_high_percentile = float(params.pop("std_high_percentile", 82.0))
    texture_low_percentile = float(params.pop("texture_low_percentile", 55.0))
    texture_high_percentile = float(params.pop("texture_high_percentile", 92.0))
    mask_blur_ksize = _odd_ksize(params.pop("mask_blur_ksize", 7), minimum=1)
    detail_sigmas = _as_float_list(params.pop("detail_sigmas", None), [0.8, 1.6, 2.4])
    bilateral_d = int(params.pop("bilateral_d", 5))
    bilateral_sigma_color = float(params.pop("bilateral_sigma_color", 16.0))
    bilateral_sigma_space = float(params.pop("bilateral_sigma_space", 5.0))
    pseudoedge_margin = float(params.pop("pseudoedge_margin", 0.04))
    spur_margin = float(params.pop("spur_margin", 0.04))
    guard_background_grad_ratio = float(params.pop("guard_background_grad_ratio", 1.005))
    guard_global_grad_ratio = float(params.pop("guard_global_grad_ratio", 1.035))
    guard_local_var_ratio = float(params.pop("guard_local_var_ratio", 1.035))
    guard_mean_abs_delta = float(params.pop("guard_mean_abs_delta", 2.2))
    fallback_scales = _as_float_list(params.pop("fallback_scales", None), [1.0, 0.7, 0.4, 0.0])
    if params:
        raise ValueError(f"topology_guarded_microfusion_bph 不支持的参数: {sorted(params.keys())}")

    fusion_alpha = float(np.clip(fusion_alpha, 0.0, 1.0))
    structure_sharpen_alpha = float(np.clip(structure_sharpen_alpha, 0.0, 1.0))
    bph_structure_alpha = float(np.clip(bph_structure_alpha, 0.0, 1.0))
    background_denoise_alpha = float(np.clip(background_denoise_alpha, 0.0, 1.0))
    pseudoedge_suppress_alpha = float(np.clip(pseudoedge_suppress_alpha, 0.0, 1.0))
    spur_suppress_alpha = float(np.clip(spur_suppress_alpha, 0.0, 1.0))
    raw_strong_edge_rescue_alpha = float(np.clip(raw_strong_edge_rescue_alpha, 0.0, 1.0))
    raw_global_blend_alpha = float(np.clip(raw_global_blend_alpha, 0.0, 1.0))
    chroma_fusion_alpha = float(np.clip(chroma_fusion_alpha, 0.0, 1.0))
    raw_strong_edge_power = max(raw_strong_edge_power, 1e-6)
    max_luma_delta = max(0.0, max_luma_delta)
    local_std_sigma = max(local_std_sigma, 1e-6)
    bilateral_d = max(1, bilateral_d)
    guard_background_grad_ratio = max(1e-6, guard_background_grad_ratio)
    guard_global_grad_ratio = max(1e-6, guard_global_grad_ratio)
    guard_local_var_ratio = max(1e-6, guard_local_var_ratio)
    guard_mean_abs_delta = max(0.0, guard_mean_abs_delta)

    base_uint8 = _microstructure_csp_bph(original_uint8, bph_uint8=bph_uint8, **base_params)
    weak_uint8 = _weak_boundary_pyramid_fusion_bph(original_uint8, bph_uint8=bph_uint8, **weak_params)

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    base_lab = cv2.cvtColor(base_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    weak_lab = cv2.cvtColor(weak_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    bph_l = bph_lab[..., 0]
    base_l = base_lab[..., 0]
    weak_l = weak_lab[..., 0]

    raw_x = cv2.Sobel(raw_l, cv2.CV_32F, 1, 0, ksize=3)
    raw_y = cv2.Sobel(raw_l, cv2.CV_32F, 0, 1, ksize=3)
    bph_x = cv2.Sobel(bph_l, cv2.CV_32F, 1, 0, ksize=3)
    bph_y = cv2.Sobel(bph_l, cv2.CV_32F, 0, 1, ksize=3)
    raw_grad = cv2.magnitude(raw_x, raw_y)
    bph_grad = cv2.magnitude(bph_x, bph_y)
    raw_edge = _normalize_by_percentiles(raw_grad, grad_low_percentile, grad_high_percentile)
    bph_edge = _normalize_by_percentiles(bph_grad, grad_low_percentile, grad_high_percentile)

    stable_detail = np.zeros_like(raw_l, dtype=np.float32)
    stable_grad = np.zeros_like(raw_l, dtype=np.float32)
    bph_detail = np.zeros_like(raw_l, dtype=np.float32)
    for sigma in detail_sigmas:
        sigma = max(float(sigma), 1e-6)
        raw_smooth = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=sigma)
        bph_smooth = cv2.GaussianBlur(bph_l, (0, 0), sigmaX=sigma)
        stable_detail += raw_l - raw_smooth
        bph_detail += bph_l - bph_smooth
        sx = cv2.Sobel(raw_smooth, cv2.CV_32F, 1, 0, ksize=3)
        sy = cv2.Sobel(raw_smooth, cv2.CV_32F, 0, 1, ksize=3)
        stable_grad += cv2.magnitude(sx, sy)
    stable_detail /= max(len(detail_sigmas), 1)
    bph_detail /= max(len(detail_sigmas), 1)
    stable_grad /= max(len(detail_sigmas), 1)
    stable_edge = _normalize_by_percentiles(stable_grad, grad_low_percentile, grad_high_percentile)

    local_mean = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=local_std_sigma)
    local_mean_sq = cv2.GaussianBlur(raw_l * raw_l, (0, 0), sigmaX=local_std_sigma)
    local_std = np.sqrt(np.maximum(local_mean_sq - local_mean * local_mean, 0.0))
    low_contrast = 1.0 - _normalize_by_percentiles(local_std, std_low_percentile, std_high_percentile)
    texture_risk = _normalize_by_percentiles(local_std, texture_low_percentile, texture_high_percentile)
    high_freq_risk = _normalize_by_percentiles(np.abs(stable_detail), 65.0, 96.0) * (1.0 - stable_edge)
    texture_risk = np.clip(0.70 * texture_risk + 0.30 * high_freq_risk, 0.0, 1.0)

    reveal_delta = np.maximum(bph_grad - raw_grad, 0.0)
    reveal_mask = _normalize_by_percentiles(reveal_delta, 70.0, 96.0) * low_contrast
    boundary_mask = (0.55 * raw_edge + 0.25 * stable_edge + 0.20 * bph_edge)
    boundary_mask *= 0.40 + 0.60 * low_contrast
    boundary_mask += 0.18 * reveal_mask
    boundary_mask *= 1.0 - texture_risk
    boundary_mask = np.clip(boundary_mask, 0.0, 1.0)
    if mask_blur_ksize > 1:
        boundary_mask = cv2.GaussianBlur(boundary_mask, (mask_blur_ksize, mask_blur_ksize), 0)
    boundary_mask = np.clip(boundary_mask, 0.0, 1.0)
    background_mask = np.clip(1.0 - boundary_mask, 0.0, 1.0)

    smooth_l = cv2.bilateralFilter(
        np.clip(raw_l, 0, 255).astype(np.uint8),
        bilateral_d,
        bilateral_sigma_color,
        bilateral_sigma_space,
    ).astype(np.float32)

    raw_lap = np.abs(cv2.Laplacian(raw_l, cv2.CV_32F, ksize=3))
    raw_bg_grad = float(np.sum(raw_grad * background_mask)) + 1e-6
    raw_grad_mean = float(np.mean(raw_grad)) + 1e-6
    raw_grad_p95 = float(np.percentile(raw_grad, 95.0)) + 1e-6
    raw_std_mean = float(np.mean(local_std)) + 1e-6

    def build_luma(scale):
        scale = float(np.clip(scale, 0.0, 1.0))
        target = base_l + scale * fusion_alpha * boundary_mask * (weak_l - base_l)
        target += scale * structure_sharpen_alpha * boundary_mask * stable_detail
        target += scale * bph_structure_alpha * boundary_mask * bph_detail
        target += background_denoise_alpha * background_mask * (smooth_l - target)

        target_x = cv2.Sobel(target, cv2.CV_32F, 1, 0, ksize=3)
        target_y = cv2.Sobel(target, cv2.CV_32F, 0, 1, ksize=3)
        target_grad = cv2.magnitude(target_x, target_y)
        pseudo_delta = np.maximum(target_grad - raw_grad * (1.0 + pseudoedge_margin), 0.0)
        pseudo_mask = background_mask * _normalize_by_percentiles(pseudo_delta, 65.0, 96.0)
        target = (1.0 - pseudoedge_suppress_alpha * pseudo_mask) * target + (
            pseudoedge_suppress_alpha * pseudo_mask
        ) * raw_l

        target_lap = np.abs(cv2.Laplacian(target, cv2.CV_32F, ksize=3))
        spur_delta = np.maximum(target_lap - raw_lap * (1.0 + spur_margin), 0.0)
        spur_mask = background_mask * (1.0 - boundary_mask) * _normalize_by_percentiles(spur_delta, 70.0, 97.0)
        target = (1.0 - spur_suppress_alpha * spur_mask) * target + (
            spur_suppress_alpha * spur_mask
        ) * raw_l

        strong_edge = np.power(np.clip(raw_edge, 0.0, 1.0), raw_strong_edge_power)
        target = (1.0 - raw_strong_edge_rescue_alpha * strong_edge) * target + (
            raw_strong_edge_rescue_alpha * strong_edge
        ) * raw_l
        if raw_global_blend_alpha > 0:
            target = (1.0 - raw_global_blend_alpha) * target + raw_global_blend_alpha * raw_l
        if max_luma_delta > 0:
            target = np.clip(target, raw_l - max_luma_delta, raw_l + max_luma_delta)
        return np.clip(target, 0.0, 255.0)

    def guard_pass(candidate_l):
        cand_x = cv2.Sobel(candidate_l, cv2.CV_32F, 1, 0, ksize=3)
        cand_y = cv2.Sobel(candidate_l, cv2.CV_32F, 0, 1, ksize=3)
        cand_grad = cv2.magnitude(cand_x, cand_y)
        cand_bg_grad = float(np.sum(cand_grad * background_mask))
        cand_grad_mean = float(np.mean(cand_grad))
        cand_grad_p95 = float(np.percentile(cand_grad, 95.0))
        cand_mean = cv2.GaussianBlur(candidate_l, (0, 0), sigmaX=local_std_sigma)
        cand_mean_sq = cv2.GaussianBlur(candidate_l * candidate_l, (0, 0), sigmaX=local_std_sigma)
        cand_std = np.sqrt(np.maximum(cand_mean_sq - cand_mean * cand_mean, 0.0))
        mean_abs_delta = float(np.mean(np.abs(candidate_l - raw_l)))
        return (
            cand_bg_grad <= raw_bg_grad * guard_background_grad_ratio
            and cand_grad_mean <= raw_grad_mean * guard_global_grad_ratio
            and cand_grad_p95 <= raw_grad_p95 * guard_global_grad_ratio
            and float(np.mean(cand_std)) <= raw_std_mean * guard_local_var_ratio
            and mean_abs_delta <= guard_mean_abs_delta
        )

    target_l = raw_l.copy()
    for scale in fallback_scales:
        candidate_l = build_luma(scale)
        target_l = candidate_l
        if guard_pass(candidate_l):
            break

    chroma_mask = chroma_fusion_alpha * boundary_mask
    mixed_lab = raw_lab.copy()
    mixed_lab[..., 0] = target_l
    mixed_lab[..., 1] = (
        (1.0 - chroma_fusion_alpha) * raw_lab[..., 1]
        + chroma_fusion_alpha * base_lab[..., 1]
    )
    mixed_lab[..., 2] = (
        (1.0 - chroma_fusion_alpha) * raw_lab[..., 2]
        + chroma_fusion_alpha * base_lab[..., 2]
    )
    mixed_lab[..., 1] = (1.0 - chroma_mask) * mixed_lab[..., 1] + chroma_mask * weak_lab[..., 1]
    mixed_lab[..., 2] = (1.0 - chroma_mask) * mixed_lab[..., 2] + chroma_mask * weak_lab[..., 2]
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _edge_mask_from_luma(luma_float):
    grad_x = cv2.Sobel(luma_float, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(luma_float, cv2.CV_32F, 0, 1, ksize=3)
    grad = cv2.magnitude(grad_x, grad_y)
    max_grad = float(np.max(grad))
    if max_grad <= 1e-12:
        return grad, np.zeros_like(luma_float, dtype=np.uint8)
    grad_u8 = np.clip(grad / max_grad * 255.0, 0, 255).astype(np.uint8)
    _, mask = cv2.threshold(grad_u8, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return grad, (mask > 0).astype(np.uint8)


def _small_component_mask(mask_uint8, max_area):
    if max_area <= 0 or not np.any(mask_uint8):
        return np.zeros_like(mask_uint8, dtype=np.float32)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask_uint8.astype(np.uint8), connectivity=8)
    out = np.zeros_like(mask_uint8, dtype=np.float32)
    for label in range(1, num_labels):
        area = int(stats[label, cv2.CC_STAT_AREA])
        if 0 < area <= max_area:
            out[labels == label] = 1.0
    return out


def _component_shape_risk_mask(mask_uint8, max_area, max_minor_axis, min_aspect_ratio):
    """Return a soft mask for isolated or line-like added edge components."""
    if not np.any(mask_uint8):
        return np.zeros_like(mask_uint8, dtype=np.float32)
    max_area = max(0, int(max_area))
    max_minor_axis = max(0, int(max_minor_axis))
    min_aspect_ratio = max(float(min_aspect_ratio), 1.0)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(mask_uint8.astype(np.uint8), connectivity=8)
    out = np.zeros_like(mask_uint8, dtype=np.float32)
    for label in range(1, num_labels):
        area = int(stats[label, cv2.CC_STAT_AREA])
        width = int(stats[label, cv2.CC_STAT_WIDTH])
        height = int(stats[label, cv2.CC_STAT_HEIGHT])
        minor = max(1, min(width, height))
        major = max(width, height)
        aspect = float(major) / float(minor)
        small = max_area > 0 and area <= max_area
        thin = max_minor_axis > 0 and minor <= max_minor_axis and aspect >= min_aspect_ratio
        if small or thin:
            out[labels == label] = 1.0
    return out


def _downstream_d01_structure_flow_bph(original_uint8, bph_uint8=None, **params):
    """D01 modular downstream-driven enhancement flow.

    This downstream_driven_v2 mode is not another P12-P28 guard tweak. It keeps
    the main modules switchable for later ablation: capped color consistency,
    low-frequency illumination/chroma correction, structure-preserving
    luma/detail formation, edge/background guided fusion, false-edge
    suppression, light sharpening and bounded parameter selection.
    """
    if bph_uint8 is None:
        raise ValueError("downstream_d01_structure_flow_bph requires bph_uint8")

    enable_color_consistency = bool(params.pop("enable_color_consistency", True))
    enable_lowfreq_correction = bool(params.pop("enable_lowfreq_correction", True))
    enable_local_contrast = bool(params.pop("enable_local_contrast", True))
    enable_structure_branch = bool(params.pop("enable_structure_branch", True))
    enable_edge_guided_fusion = bool(params.pop("enable_edge_guided_fusion", True))
    enable_false_edge_suppression = bool(params.pop("enable_false_edge_suppression", True))
    enable_structure_sharpen = bool(params.pop("enable_structure_sharpen", True))
    enable_bounded_selection = bool(params.pop("enable_bounded_selection", True))

    wb_gain_cap = params.pop("wb_gain_cap", [0.93, 1.07])
    channel_imbalance_skip = float(params.pop("channel_imbalance_skip", 0.025))
    wb_luma_alpha = float(params.pop("wb_luma_alpha", 0.04))
    wb_chroma_alpha = float(params.pop("wb_chroma_alpha", 0.05))
    bph_chroma_alpha = float(params.pop("bph_chroma_alpha", 0.06))
    max_chroma_delta = float(params.pop("max_chroma_delta", 3.0))
    chroma_sigma = float(params.pop("chroma_sigma", 13.0))

    low_sigma = float(params.pop("low_sigma", 17.0))
    illum_alpha = float(params.pop("illum_alpha", 0.06))
    bph_low_luma_alpha = float(params.pop("bph_low_luma_alpha", 0.03))
    nonuniformity_reference = float(params.pop("nonuniformity_reference", 0.32))

    gamma_candidates = _as_float_list(params.pop("gamma_candidates", None), [0.98, 1.0, 1.02])
    contrast_candidates = _as_float_list(params.pop("contrast_candidates", None), [0.995, 1.0, 1.01])
    clahe_clip_limit = float(params.pop("clahe_clip_limit", 0.8))
    clahe_tile_size = params.pop("clahe_tile_size", [8, 8])
    local_contrast_alpha = float(params.pop("local_contrast_alpha", 0.05))

    structure_sigmas = _as_float_list(params.pop("structure_sigmas", None), [0.8, 1.6, 2.8])
    structure_alpha = float(params.pop("structure_alpha", 0.08))
    bph_structure_alpha = float(params.pop("bph_structure_alpha", 0.015))
    background_smooth_alpha = float(params.pop("background_smooth_alpha", 0.04))
    false_edge_suppress_alpha = float(params.pop("false_edge_suppress_alpha", 0.25))
    sharpen_alpha = float(params.pop("sharpen_alpha", 0.02))
    sharpen_sigma = float(params.pop("sharpen_sigma", 1.0))
    max_luma_delta = float(params.pop("max_luma_delta", 4.0))

    grad_low_percentile = float(params.pop("grad_low_percentile", 44.0))
    grad_high_percentile = float(params.pop("grad_high_percentile", 90.0))
    texture_low_percentile = float(params.pop("texture_low_percentile", 54.0))
    texture_high_percentile = float(params.pop("texture_high_percentile", 93.0))
    support_power = float(params.pop("support_power", 1.15))
    texture_risk_power = float(params.pop("texture_risk_power", 1.15))
    mask_blur_ksize = _odd_ksize(params.pop("mask_blur_ksize", 5), minimum=1)
    bilateral_d = int(params.pop("bilateral_d", 5))
    bilateral_sigma_color = float(params.pop("bilateral_sigma_color", 14.0))
    bilateral_sigma_space = float(params.pop("bilateral_sigma_space", 5.0))

    selection_scales = _as_float_list(params.pop("selection_scales", None), [0.50, 0.75, 1.00])
    score_background_weight = float(params.pop("score_background_weight", 0.55))
    score_delta_weight = float(params.pop("score_delta_weight", 1.20))
    score_saturation_weight = float(params.pop("score_saturation_weight", 1.35))
    guard_global_grad_ratio = float(params.pop("guard_global_grad_ratio", 1.006))
    guard_background_grad_ratio = float(params.pop("guard_background_grad_ratio", 1.000))
    guard_mean_abs_delta = float(params.pop("guard_mean_abs_delta", 1.10))
    guard_added_edge_ratio = float(params.pop("guard_added_edge_ratio", 0.0045))
    if params:
        raise ValueError(f"downstream_d01_structure_flow_bph 不支持的参数: {sorted(params.keys())}")

    if isinstance(wb_gain_cap, (int, float)):
        gain_low, gain_high = 1.0 / float(wb_gain_cap), float(wb_gain_cap)
    else:
        if len(wb_gain_cap) != 2:
            raise ValueError("wb_gain_cap must be a number or length-2 list")
        gain_low, gain_high = float(wb_gain_cap[0]), float(wb_gain_cap[1])
    gain_low, gain_high = min(gain_low, gain_high), max(gain_low, gain_high)

    wb_luma_alpha = float(np.clip(wb_luma_alpha, 0.0, 1.0))
    wb_chroma_alpha = float(np.clip(wb_chroma_alpha, 0.0, 1.0))
    bph_chroma_alpha = float(np.clip(bph_chroma_alpha, 0.0, 1.0))
    illum_alpha = float(np.clip(illum_alpha, 0.0, 1.0))
    bph_low_luma_alpha = float(np.clip(bph_low_luma_alpha, 0.0, 1.0))
    local_contrast_alpha = float(np.clip(local_contrast_alpha, 0.0, 1.0))
    structure_alpha = float(np.clip(structure_alpha, 0.0, 1.0))
    bph_structure_alpha = float(np.clip(bph_structure_alpha, 0.0, 1.0))
    background_smooth_alpha = float(np.clip(background_smooth_alpha, 0.0, 1.0))
    false_edge_suppress_alpha = float(np.clip(false_edge_suppress_alpha, 0.0, 1.0))
    sharpen_alpha = float(np.clip(sharpen_alpha, 0.0, 1.0))
    max_luma_delta = max(0.0, max_luma_delta)
    max_chroma_delta = max(0.0, max_chroma_delta)
    low_sigma = max(low_sigma, 1e-6)
    chroma_sigma = max(chroma_sigma, 1e-6)
    sharpen_sigma = max(sharpen_sigma, 1e-6)
    nonuniformity_reference = max(nonuniformity_reference, 1e-6)
    support_power = max(support_power, 1e-6)
    texture_risk_power = max(texture_risk_power, 1e-6)
    bilateral_d = max(1, bilateral_d)
    guard_global_grad_ratio = max(1.0, guard_global_grad_ratio)
    guard_background_grad_ratio = max(1.0, guard_background_grad_ratio)
    guard_mean_abs_delta = max(0.0, guard_mean_abs_delta)
    guard_added_edge_ratio = max(0.0, guard_added_edge_ratio)

    if isinstance(clahe_tile_size, int):
        tile_grid_size = (int(clahe_tile_size), int(clahe_tile_size))
    else:
        if len(clahe_tile_size) != 2:
            raise ValueError("clahe_tile_size must be an int or a length-2 list")
        tile_grid_size = (int(clahe_tile_size[0]), int(clahe_tile_size[1]))
    tile_grid_size = (max(1, tile_grid_size[0]), max(1, tile_grid_size[1]))

    raw_f = original_uint8.astype(np.float32)
    channel_means = np.mean(raw_f.reshape(-1, 3), axis=0)
    mean_all = float(np.mean(channel_means))
    channel_imbalance = float(np.std(channel_means) / max(mean_all, 1e-6))
    gains = np.ones(3, dtype=np.float32)
    if enable_color_consistency and channel_imbalance >= channel_imbalance_skip:
        gains = np.clip(mean_all / np.maximum(channel_means, 1e-6), gain_low, gain_high).astype(np.float32)
    wb_uint8 = np.clip(raw_f * gains.reshape(1, 1, 3), 0, 255).astype(np.uint8)

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    wb_lab = cv2.cvtColor(wb_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    wb_l = wb_lab[..., 0]
    bph_l = bph_lab[..., 0]

    raw_x = cv2.Sobel(raw_l, cv2.CV_32F, 1, 0, ksize=3)
    raw_y = cv2.Sobel(raw_l, cv2.CV_32F, 0, 1, ksize=3)
    raw_grad = cv2.magnitude(raw_x, raw_y)
    edge_conf = _normalize_by_percentiles(raw_grad, grad_low_percentile, grad_high_percentile)

    stable_detail = np.zeros_like(raw_l, dtype=np.float32)
    stable_grad = np.zeros_like(raw_l, dtype=np.float32)
    for sigma in structure_sigmas:
        sigma = max(float(sigma), 1e-6)
        smooth = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=sigma)
        stable_detail += raw_l - smooth
        sx = cv2.Sobel(smooth, cv2.CV_32F, 1, 0, ksize=3)
        sy = cv2.Sobel(smooth, cv2.CV_32F, 0, 1, ksize=3)
        stable_grad += cv2.magnitude(sx, sy)
    stable_detail /= max(len(structure_sigmas), 1)
    stable_grad /= max(len(structure_sigmas), 1)
    stable_edge = _normalize_by_percentiles(stable_grad, grad_low_percentile, grad_high_percentile)

    local_mean = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=1.5)
    local_mean_sq = cv2.GaussianBlur(raw_l * raw_l, (0, 0), sigmaX=1.5)
    local_std = np.sqrt(np.maximum(local_mean_sq - local_mean * local_mean, 0.0))
    texture_risk = _normalize_by_percentiles(local_std, texture_low_percentile, texture_high_percentile)
    hf_risk = _normalize_by_percentiles(np.abs(stable_detail), 60.0, 96.0) * (1.0 - stable_edge)
    texture_risk = np.power(np.clip(0.70 * texture_risk + 0.30 * hf_risk, 0.0, 1.0), texture_risk_power)

    support = np.power(np.clip(np.sqrt(edge_conf * stable_edge), 0.0, 1.0), support_power)
    if not enable_edge_guided_fusion:
        support = np.ones_like(support, dtype=np.float32)
    safe_weight = np.clip(support * (1.0 - texture_risk), 0.0, 1.0)
    if mask_blur_ksize > 1:
        safe_weight = cv2.GaussianBlur(safe_weight, (mask_blur_ksize, mask_blur_ksize), 0)
    safe_weight = np.clip(safe_weight, 0.0, 1.0)
    background_weight = 1.0 - safe_weight

    raw_low = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=low_sigma)
    bph_low = cv2.GaussianBlur(bph_l, (0, 0), sigmaX=low_sigma)
    nonuniformity = float(np.std(raw_low) / (np.std(raw_l) + 1e-6))
    illumination_strength = float(np.clip(nonuniformity / nonuniformity_reference, 0.0, 1.0))
    illum_delta = (float(np.mean(raw_low)) - raw_low) * illumination_strength
    bph_low_delta = bph_low - raw_low

    raw_l_u8 = np.clip(raw_l, 0, 255).astype(np.uint8)
    clahe_l = raw_l.copy()
    if enable_local_contrast and clahe_clip_limit > 0:
        clahe = cv2.createCLAHE(clipLimit=max(clahe_clip_limit, 0.01), tileGridSize=tile_grid_size)
        clahe_l = clahe.apply(raw_l_u8).astype(np.float32)

    bph_detail = bph_l - cv2.GaussianBlur(bph_l, (0, 0), sigmaX=1.2)
    smooth_l = cv2.bilateralFilter(
        raw_l_u8,
        bilateral_d,
        bilateral_sigma_color,
        bilateral_sigma_space,
    ).astype(np.float32)
    raw_grad_sum = float(np.sum(raw_grad)) + 1e-6
    raw_bg_grad_sum = float(np.sum(raw_grad * background_weight)) + 1e-6
    raw_mask = raw_grad > float(np.percentile(raw_grad, np.clip(grad_high_percentile, 0.0, 100.0)))

    def build_luma(scale, gamma, contrast_gain):
        target = raw_l.copy()
        if enable_color_consistency:
            target += wb_luma_alpha * (wb_l - raw_l)
        if enable_lowfreq_correction:
            target += scale * illum_alpha * illum_delta
            target += scale * bph_low_luma_alpha * bph_low_delta
        if enable_local_contrast:
            gamma = max(float(gamma), 1e-6)
            raw_norm = np.clip(raw_l / 255.0, 0.0, 1.0)
            gamma_l = np.power(raw_norm, gamma)
            mean_l = float(np.mean(gamma_l))
            contrast_l = np.clip(mean_l + float(contrast_gain) * (gamma_l - mean_l), 0.0, 1.0) * 255.0
            contrast_residual = 0.60 * (contrast_l - raw_l) + 0.40 * (clahe_l - raw_l)
            target += scale * local_contrast_alpha * safe_weight * contrast_residual
        if enable_structure_branch:
            target += scale * structure_alpha * safe_weight * stable_detail
            target += scale * bph_structure_alpha * safe_weight * bph_detail
        if background_smooth_alpha > 0:
            target += background_smooth_alpha * background_weight * (smooth_l - target)
        if enable_structure_sharpen and sharpen_alpha > 0:
            target_blur = cv2.GaussianBlur(target, (0, 0), sigmaX=sharpen_sigma)
            target += scale * sharpen_alpha * safe_weight * (target - target_blur)
        if enable_false_edge_suppression and false_edge_suppress_alpha > 0:
            residual = target - raw_l
            off_support = np.clip((1.0 - support) * (0.35 + 0.65 * texture_risk), 0.0, 1.0)
            residual *= 1.0 - false_edge_suppress_alpha * off_support
            target = raw_l + residual
        if max_luma_delta > 0:
            target = np.clip(target, raw_l - max_luma_delta, raw_l + max_luma_delta)
        return np.clip(target, 0.0, 255.0)

    def guard_pass(candidate_l):
        cand_x = cv2.Sobel(candidate_l, cv2.CV_32F, 1, 0, ksize=3)
        cand_y = cv2.Sobel(candidate_l, cv2.CV_32F, 0, 1, ksize=3)
        cand_grad = cv2.magnitude(cand_x, cand_y)
        cand_grad_sum = float(np.sum(cand_grad))
        cand_bg_grad_sum = float(np.sum(cand_grad * background_weight))
        mean_abs_delta = float(np.mean(np.abs(candidate_l - raw_l)))
        candidate_mask = cand_grad > float(np.percentile(cand_grad, np.clip(grad_high_percentile, 0.0, 100.0)))
        added_edge_ratio = float(np.count_nonzero(candidate_mask & (~raw_mask))) / max(candidate_l.size, 1)
        return (
            cand_grad_sum <= raw_grad_sum * guard_global_grad_ratio
            and cand_bg_grad_sum <= raw_bg_grad_sum * guard_background_grad_ratio
            and mean_abs_delta <= guard_mean_abs_delta
            and added_edge_ratio <= guard_added_edge_ratio
        )

    best_l = raw_l.copy()
    best_score = -1e18
    candidate_scales = selection_scales if enable_bounded_selection else [1.0]
    for scale in candidate_scales:
        scale = float(np.clip(scale, 0.0, 1.0))
        for gamma in gamma_candidates:
            for contrast_gain in contrast_candidates:
                candidate_l = build_luma(scale, gamma, contrast_gain)
                if enable_bounded_selection and not guard_pass(candidate_l):
                    continue
                score = _candidate_luma_score(
                    raw_l,
                    candidate_l,
                    safe_weight,
                    background_weight,
                    score_background_weight,
                    score_delta_weight,
                    score_saturation_weight,
                )
                if score > best_score:
                    best_score = score
                    best_l = candidate_l
    if best_score <= -1e17:
        best_l = build_luma(0.0, 1.0, 1.0)

    mixed_lab = raw_lab.copy()
    mixed_lab[..., 0] = best_l
    if enable_color_consistency:
        for channel in (1, 2):
            wb_delta = wb_lab[..., channel] - raw_lab[..., channel]
            bph_delta = cv2.GaussianBlur(
                bph_lab[..., channel] - raw_lab[..., channel],
                (0, 0),
                sigmaX=chroma_sigma,
            )
            chroma_delta = wb_chroma_alpha * wb_delta + bph_chroma_alpha * bph_delta
            if max_chroma_delta > 0:
                chroma_delta = np.clip(chroma_delta, -max_chroma_delta, max_chroma_delta)
            mixed_lab[..., channel] = raw_lab[..., channel] + chroma_delta
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _raw_detail_lowfreq_chroma_bph(original_uint8, bph_uint8=None, **params):
    """Preserve raw high-frequency structure while correcting low-frequency color.

    P27 tests a different assumption from the weak-boundary fusion family: the
    fixed edge detectors may already encode the raw high-frequency boundary
    distribution well, so enhancement should avoid creating detector-visible
    edges and should only move low-frequency illumination/chroma. The mode keeps
    raw luminance detail as the anchor, searches a clipped low-frequency luma
    adjustment, transfers blurred BPH chroma away from raw-supported edges, and
    falls back to raw luminance if gradient guards fail.
    """
    if bph_uint8 is None:
        raise ValueError("raw_detail_lowfreq_chroma_bph requires bph_uint8")

    low_sigma = float(params.pop("low_sigma", 10.0))
    chroma_sigma = float(params.pop("chroma_sigma", 12.0))
    gamma_candidates = _as_float_list(params.pop("gamma_candidates", None), [0.965, 1.0, 1.035])
    contrast_candidates = _as_float_list(params.pop("contrast_candidates", None), [0.99, 1.0, 1.015])
    luma_alpha = float(params.pop("luma_alpha", 0.18))
    bph_low_luma_alpha = float(params.pop("bph_low_luma_alpha", 0.04))
    detail_scale = float(params.pop("detail_scale", 1.0))
    background_detail_dampen = float(params.pop("background_detail_dampen", 0.055))
    background_denoise_alpha = float(params.pop("background_denoise_alpha", 0.035))
    support_rescue_alpha = float(params.pop("support_rescue_alpha", 0.48))
    support_rescue_power = float(params.pop("support_rescue_power", 1.35))
    raw_global_blend_alpha = float(params.pop("raw_global_blend_alpha", 0.05))
    max_luma_delta = float(params.pop("max_luma_delta", 3.2))
    off_support_luma_pullback_alpha = float(params.pop("off_support_luma_pullback_alpha", 0.0))
    off_support_luma_delta_floor = float(params.pop("off_support_luma_delta_floor", 0.25))
    off_support_luma_low_percentile = float(params.pop("off_support_luma_low_percentile", 55.0))
    off_support_luma_high_percentile = float(params.pop("off_support_luma_high_percentile", 96.0))
    off_support_luma_blur = _odd_ksize(params.pop("off_support_luma_blur", 5), minimum=1)
    chroma_alpha = float(params.pop("chroma_alpha", 0.16))
    chroma_edge_protect = float(params.pop("chroma_edge_protect", 0.72))
    max_chroma_delta = float(params.pop("max_chroma_delta", 6.0))
    chroma_false_edge_guard_alpha = float(params.pop("chroma_false_edge_guard_alpha", 0.0))
    chroma_guard_grad_ratio = float(params.pop("chroma_guard_grad_ratio", 1.01))
    chroma_guard_delta_floor = float(params.pop("chroma_guard_delta_floor", 0.25))
    chroma_guard_low_percentile = float(params.pop("chroma_guard_low_percentile", 62.0))
    chroma_guard_high_percentile = float(params.pop("chroma_guard_high_percentile", 97.5))
    chroma_guard_blur = _odd_ksize(params.pop("chroma_guard_blur", 5), minimum=1)
    grad_low_percentile = float(params.pop("grad_low_percentile", 49.0))
    grad_high_percentile = float(params.pop("grad_high_percentile", 90.5))
    local_std_sigma = float(params.pop("local_std_sigma", 3.0))
    std_low_percentile = float(params.pop("std_low_percentile", 22.0))
    std_high_percentile = float(params.pop("std_high_percentile", 82.0))
    support_dilate = int(params.pop("support_dilate", 2))
    support_blur = _odd_ksize(params.pop("support_blur", 5), minimum=1)
    guard_added_edge_ratio = float(params.pop("guard_added_edge_ratio", 0.0045))
    guard_background_grad_ratio = float(params.pop("guard_background_grad_ratio", 0.998))
    guard_global_grad_ratio = float(params.pop("guard_global_grad_ratio", 1.004))
    guard_support_grad_ratio = float(params.pop("guard_support_grad_ratio", 0.996))
    guard_mean_abs_delta = float(params.pop("guard_mean_abs_delta", 0.82))
    fallback_scales = _as_float_list(params.pop("fallback_scales", None), [1.0, 0.78, 0.56, 0.34, 0.16, 0.0])
    bilateral_d = int(params.pop("bilateral_d", 5))
    bilateral_sigma_color = float(params.pop("bilateral_sigma_color", 13.0))
    bilateral_sigma_space = float(params.pop("bilateral_sigma_space", 4.5))
    if params:
        raise ValueError(f"raw_detail_lowfreq_chroma_bph 不支持的参数: {sorted(params.keys())}")

    low_sigma = max(low_sigma, 1e-6)
    chroma_sigma = max(chroma_sigma, 1e-6)
    luma_alpha = float(np.clip(luma_alpha, 0.0, 1.0))
    bph_low_luma_alpha = float(np.clip(bph_low_luma_alpha, 0.0, 1.0))
    detail_scale = float(np.clip(detail_scale, 0.0, 1.2))
    background_detail_dampen = float(np.clip(background_detail_dampen, 0.0, 1.0))
    background_denoise_alpha = float(np.clip(background_denoise_alpha, 0.0, 1.0))
    support_rescue_alpha = float(np.clip(support_rescue_alpha, 0.0, 1.0))
    support_rescue_power = max(support_rescue_power, 1e-6)
    raw_global_blend_alpha = float(np.clip(raw_global_blend_alpha, 0.0, 1.0))
    max_luma_delta = max(0.0, max_luma_delta)
    off_support_luma_pullback_alpha = float(np.clip(off_support_luma_pullback_alpha, 0.0, 1.0))
    off_support_luma_delta_floor = max(0.0, off_support_luma_delta_floor)
    chroma_alpha = float(np.clip(chroma_alpha, 0.0, 1.0))
    chroma_edge_protect = float(np.clip(chroma_edge_protect, 0.0, 1.0))
    max_chroma_delta = max(0.0, max_chroma_delta)
    chroma_false_edge_guard_alpha = float(np.clip(chroma_false_edge_guard_alpha, 0.0, 1.0))
    chroma_guard_grad_ratio = max(1e-6, chroma_guard_grad_ratio)
    chroma_guard_delta_floor = max(0.0, chroma_guard_delta_floor)
    local_std_sigma = max(local_std_sigma, 1e-6)
    support_dilate = max(0, support_dilate)
    guard_added_edge_ratio = max(0.0, guard_added_edge_ratio)
    guard_background_grad_ratio = max(1e-6, guard_background_grad_ratio)
    guard_global_grad_ratio = max(1e-6, guard_global_grad_ratio)
    guard_support_grad_ratio = max(0.0, guard_support_grad_ratio)
    guard_mean_abs_delta = max(0.0, guard_mean_abs_delta)
    bilateral_d = max(1, bilateral_d)

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    bph_l = bph_lab[..., 0]

    low_raw = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=low_sigma)
    low_bph = cv2.GaussianBlur(bph_l, (0, 0), sigmaX=low_sigma)
    raw_detail = raw_l - low_raw

    raw_grad, raw_edge_mask = _edge_mask_from_luma(raw_l)
    raw_edge = _normalize_by_percentiles(raw_grad, grad_low_percentile, grad_high_percentile)
    support = raw_edge_mask.copy()
    if support_dilate > 0:
        kernel = np.ones((2 * support_dilate + 1, 2 * support_dilate + 1), dtype=np.uint8)
        support = cv2.dilate(support, kernel, iterations=1)
    support_soft = support.astype(np.float32)
    if support_blur > 1:
        support_soft = cv2.GaussianBlur(support_soft, (support_blur, support_blur), 0)
    support_soft = np.clip(support_soft, 0.0, 1.0)

    local_mean = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=local_std_sigma)
    local_mean_sq = cv2.GaussianBlur(raw_l * raw_l, (0, 0), sigmaX=local_std_sigma)
    local_std = np.sqrt(np.maximum(local_mean_sq - local_mean * local_mean, 0.0))
    low_contrast = 1.0 - _normalize_by_percentiles(local_std, std_low_percentile, std_high_percentile)
    background_mask = np.clip((1.0 - raw_edge) * (0.45 + 0.55 * low_contrast), 0.0, 1.0)

    smooth_l = cv2.bilateralFilter(
        np.clip(raw_l, 0, 255).astype(np.uint8),
        bilateral_d,
        bilateral_sigma_color,
        bilateral_sigma_space,
    ).astype(np.float32)

    raw_bg_grad = float(np.sum(raw_grad * background_mask)) + 1e-6
    raw_grad_mean = float(np.mean(raw_grad)) + 1e-6
    support_weight = np.power(np.clip(raw_edge * support_soft, 0.0, 1.0), support_rescue_power)
    raw_support_grad = float(np.sum(raw_grad * support_weight)) + 1e-6
    pixel_count = float(raw_l.size)

    best_low = low_raw.copy()
    best_score = -float("inf")
    low_norm = np.clip(low_raw / 255.0, 0.0, 1.0)
    low_mean = float(np.mean(low_norm))
    for gamma in gamma_candidates:
        gamma = max(float(gamma), 1e-6)
        gamma_low = np.power(low_norm, gamma)
        for contrast_alpha in contrast_candidates:
            contrast_alpha = float(contrast_alpha)
            adjusted = low_mean + contrast_alpha * (gamma_low - low_mean)
            adjusted_low = np.clip(adjusted, 0.0, 1.0) * 255.0
            candidate_low = (
                low_raw
                + luma_alpha * (adjusted_low - low_raw)
                + bph_low_luma_alpha * (low_bph - low_raw)
            )
            candidate_l = np.clip(candidate_low + raw_detail, 0.0, 255.0)
            score = _candidate_luma_score(
                raw_l,
                candidate_l,
                raw_edge,
                background_mask,
                background_weight=0.85,
                delta_weight=2.4,
                saturation_weight=2.0,
            )
            if score > best_score:
                best_score = score
                best_low = candidate_low

    def build_luma(scale):
        scale = float(np.clip(scale, 0.0, 1.0))
        target_low = low_raw + scale * (best_low - low_raw)
        target = target_low + detail_scale * raw_detail
        target -= background_detail_dampen * background_mask * raw_detail
        target += background_denoise_alpha * background_mask * (smooth_l - target)
        target = (1.0 - support_rescue_alpha * support_weight) * target + (
            support_rescue_alpha * support_weight
        ) * raw_l
        if raw_global_blend_alpha > 0:
            target = (1.0 - raw_global_blend_alpha) * target + raw_global_blend_alpha * raw_l
        if max_luma_delta > 0:
            target = np.clip(target, raw_l - max_luma_delta, raw_l + max_luma_delta)
        return np.clip(target, 0.0, 255.0)

    def guard_pass(candidate_l):
        cand_grad, cand_mask = _edge_mask_from_luma(candidate_l)
        cand_added = (cand_mask > 0) & (support == 0)
        added_ratio = float(np.count_nonzero(cand_added)) / max(pixel_count, 1.0)
        cand_bg_grad = float(np.sum(cand_grad * background_mask))
        cand_grad_mean = float(np.mean(cand_grad))
        cand_support_grad = float(np.sum(cand_grad * support_weight))
        mean_abs_delta = float(np.mean(np.abs(candidate_l - raw_l)))
        return (
            added_ratio <= guard_added_edge_ratio
            and cand_bg_grad <= raw_bg_grad * guard_background_grad_ratio
            and cand_grad_mean <= raw_grad_mean * guard_global_grad_ratio
            and cand_support_grad >= raw_support_grad * guard_support_grad_ratio
            and mean_abs_delta <= guard_mean_abs_delta
        )

    target_l = raw_l.copy()
    accepted = False
    for scale in fallback_scales:
        candidate_l = build_luma(scale)
        if guard_pass(candidate_l):
            target_l = candidate_l
            accepted = True
            break
    if not accepted:
        target_l = raw_l.copy()
    if off_support_luma_pullback_alpha > 0:
        luma_added = np.maximum(np.abs(target_l - raw_l) - off_support_luma_delta_floor, 0.0)
        luma_risk = _normalize_by_percentiles(
            luma_added,
            off_support_luma_low_percentile,
            off_support_luma_high_percentile,
        )
        luma_risk = luma_risk * (1.0 - support_soft) * background_mask
        if off_support_luma_blur > 1:
            luma_risk = cv2.GaussianBlur(luma_risk, (off_support_luma_blur, off_support_luma_blur), 0)
        luma_pullback = np.clip(off_support_luma_pullback_alpha * luma_risk, 0.0, 1.0)
        target_l = raw_l + (1.0 - luma_pullback) * (target_l - raw_l)

    mixed_lab = raw_lab.copy()
    mixed_lab[..., 0] = target_l

    raw_a_low = cv2.GaussianBlur(raw_lab[..., 1], (0, 0), sigmaX=chroma_sigma)
    raw_b_low = cv2.GaussianBlur(raw_lab[..., 2], (0, 0), sigmaX=chroma_sigma)
    bph_a_low = cv2.GaussianBlur(bph_lab[..., 1], (0, 0), sigmaX=chroma_sigma)
    bph_b_low = cv2.GaussianBlur(bph_lab[..., 2], (0, 0), sigmaX=chroma_sigma)
    chroma_gate = np.clip((1.0 - chroma_edge_protect * support_soft) * (0.55 + 0.45 * background_mask), 0.0, 1.0)
    chroma_weight = chroma_alpha * chroma_gate
    delta_a = bph_a_low - raw_a_low
    delta_b = bph_b_low - raw_b_low
    if max_chroma_delta > 0:
        delta_a = np.clip(delta_a, -max_chroma_delta, max_chroma_delta)
        delta_b = np.clip(delta_b, -max_chroma_delta, max_chroma_delta)
    mixed_lab[..., 1] = raw_lab[..., 1] + chroma_weight * delta_a
    mixed_lab[..., 2] = raw_lab[..., 2] + chroma_weight * delta_b
    if chroma_false_edge_guard_alpha > 0:
        def chroma_grad(a_channel, b_channel):
            gx_a = cv2.Sobel(a_channel, cv2.CV_32F, 1, 0, ksize=3)
            gy_a = cv2.Sobel(a_channel, cv2.CV_32F, 0, 1, ksize=3)
            gx_b = cv2.Sobel(b_channel, cv2.CV_32F, 1, 0, ksize=3)
            gy_b = cv2.Sobel(b_channel, cv2.CV_32F, 0, 1, ksize=3)
            return np.sqrt(gx_a * gx_a + gy_a * gy_a + gx_b * gx_b + gy_b * gy_b)

        raw_chroma_grad = chroma_grad(raw_lab[..., 1], raw_lab[..., 2])
        cand_chroma_grad = chroma_grad(mixed_lab[..., 1], mixed_lab[..., 2])
        added_chroma_grad = np.maximum(
            cand_chroma_grad - raw_chroma_grad * chroma_guard_grad_ratio - chroma_guard_delta_floor,
            0.0,
        )
        chroma_risk = _normalize_by_percentiles(
            added_chroma_grad,
            chroma_guard_low_percentile,
            chroma_guard_high_percentile,
        )
        chroma_risk = chroma_risk * (1.0 - support_soft) * background_mask
        if chroma_guard_blur > 1:
            chroma_risk = cv2.GaussianBlur(chroma_risk, (chroma_guard_blur, chroma_guard_blur), 0)
        pullback = np.clip(chroma_false_edge_guard_alpha * chroma_risk, 0.0, 1.0)
        mixed_lab[..., 1] = raw_lab[..., 1] + (1.0 - pullback) * (mixed_lab[..., 1] - raw_lab[..., 1])
        mixed_lab[..., 2] = raw_lab[..., 2] + (1.0 - pullback) * (mixed_lab[..., 2] - raw_lab[..., 2])
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _topology_pruned_microfusion_bph(original_uint8, bph_uint8=None, **params):
    """Prune self-detected pseudo-edge components after P17-style fusion.

    P18 wraps the topology-guarded microfusion candidate with a detector-domain
    prior: edge components newly introduced outside a dilated raw-edge support
    are treated as pseudo-edge/spur risk and pulled back toward raw/base before
    a global gradient budget decides whether to keep the candidate.
    """
    if bph_uint8 is None:
        raise ValueError("topology_pruned_microfusion_bph requires bph_uint8")

    candidate_params = dict(params.pop("candidate_params", {}))
    base_params = dict(params.pop("base_params", {}))
    prune_alpha = float(params.pop("prune_alpha", 0.68))
    spur_prune_alpha = float(params.pop("spur_prune_alpha", 0.58))
    background_prune_alpha = float(params.pop("background_prune_alpha", 0.28))
    raw_edge_dilate = int(params.pop("raw_edge_dilate", 2))
    small_component_max_area = int(params.pop("small_component_max_area", 18))
    edge_support_blur = _odd_ksize(params.pop("edge_support_blur", 5), minimum=1)
    grad_low_percentile = float(params.pop("grad_low_percentile", 48.0))
    grad_high_percentile = float(params.pop("grad_high_percentile", 90.0))
    local_std_sigma = float(params.pop("local_std_sigma", 3.0))
    std_low_percentile = float(params.pop("std_low_percentile", 22.0))
    std_high_percentile = float(params.pop("std_high_percentile", 82.0))
    max_luma_delta = float(params.pop("max_luma_delta", 4.5))
    raw_global_blend_alpha = float(params.pop("raw_global_blend_alpha", 0.14))
    base_blend_alpha = float(params.pop("base_blend_alpha", 0.10))
    guard_added_edge_ratio = float(params.pop("guard_added_edge_ratio", 0.018))
    guard_background_grad_ratio = float(params.pop("guard_background_grad_ratio", 1.0))
    guard_global_grad_ratio = float(params.pop("guard_global_grad_ratio", 1.025))
    fallback_scales = _as_float_list(params.pop("fallback_scales", None), [1.0, 0.75, 0.50, 0.25, 0.0])
    if params:
        raise ValueError(f"topology_pruned_microfusion_bph 不支持的参数: {sorted(params.keys())}")

    prune_alpha = float(np.clip(prune_alpha, 0.0, 1.0))
    spur_prune_alpha = float(np.clip(spur_prune_alpha, 0.0, 1.0))
    background_prune_alpha = float(np.clip(background_prune_alpha, 0.0, 1.0))
    raw_edge_dilate = max(0, raw_edge_dilate)
    small_component_max_area = max(0, small_component_max_area)
    local_std_sigma = max(local_std_sigma, 1e-6)
    max_luma_delta = max(0.0, max_luma_delta)
    raw_global_blend_alpha = float(np.clip(raw_global_blend_alpha, 0.0, 1.0))
    base_blend_alpha = float(np.clip(base_blend_alpha, 0.0, 1.0))
    guard_added_edge_ratio = max(0.0, guard_added_edge_ratio)
    guard_background_grad_ratio = max(1e-6, guard_background_grad_ratio)
    guard_global_grad_ratio = max(1e-6, guard_global_grad_ratio)

    base_uint8 = _microstructure_csp_bph(original_uint8, bph_uint8=bph_uint8, **base_params)
    candidate_uint8 = _topology_guarded_microfusion_bph(
        original_uint8,
        bph_uint8=bph_uint8,
        **candidate_params,
    )

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    base_lab = cv2.cvtColor(base_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    cand_lab = cv2.cvtColor(candidate_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    base_l = base_lab[..., 0]
    cand_l = cand_lab[..., 0]

    raw_grad, raw_edge_mask = _edge_mask_from_luma(raw_l)
    _, cand_edge_mask = _edge_mask_from_luma(cand_l)
    support = raw_edge_mask.copy()
    if raw_edge_dilate > 0:
        kernel = np.ones((2 * raw_edge_dilate + 1, 2 * raw_edge_dilate + 1), dtype=np.uint8)
        support = cv2.dilate(support, kernel, iterations=1)
    added_edge = (cand_edge_mask > 0) & (support == 0)

    local_mean = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=local_std_sigma)
    local_mean_sq = cv2.GaussianBlur(raw_l * raw_l, (0, 0), sigmaX=local_std_sigma)
    local_std = np.sqrt(np.maximum(local_mean_sq - local_mean * local_mean, 0.0))
    low_contrast = 1.0 - _normalize_by_percentiles(local_std, std_low_percentile, std_high_percentile)
    raw_edge = _normalize_by_percentiles(raw_grad, grad_low_percentile, grad_high_percentile)
    background_mask = np.clip((1.0 - raw_edge) * (0.35 + 0.65 * (1.0 - low_contrast)), 0.0, 1.0)

    added_mask = added_edge.astype(np.uint8)
    small_mask = _small_component_mask(added_mask, small_component_max_area)
    pseudo_mask = np.clip(added_mask.astype(np.float32) * background_mask, 0.0, 1.0)
    if edge_support_blur > 1:
        pseudo_mask = cv2.GaussianBlur(pseudo_mask, (edge_support_blur, edge_support_blur), 0)
        small_mask = cv2.GaussianBlur(small_mask, (edge_support_blur, edge_support_blur), 0)
    pseudo_mask = np.clip(pseudo_mask, 0.0, 1.0)
    small_mask = np.clip(small_mask, 0.0, 1.0)

    raw_bg_grad = float(np.sum(raw_grad * background_mask)) + 1e-6
    raw_grad_mean = float(np.mean(raw_grad)) + 1e-6
    pixel_count = float(raw_l.size)

    def build_luma(scale):
        scale = float(np.clip(scale, 0.0, 1.0))
        target = base_l + scale * (cand_l - base_l)
        target = (1.0 - prune_alpha * pseudo_mask) * target + (prune_alpha * pseudo_mask) * raw_l
        target = (1.0 - spur_prune_alpha * small_mask) * target + (spur_prune_alpha * small_mask) * raw_l
        target = (1.0 - background_prune_alpha * background_mask * pseudo_mask) * target + (
            background_prune_alpha * background_mask * pseudo_mask
        ) * base_l
        if base_blend_alpha > 0:
            target = (1.0 - base_blend_alpha) * target + base_blend_alpha * base_l
        if raw_global_blend_alpha > 0:
            target = (1.0 - raw_global_blend_alpha) * target + raw_global_blend_alpha * raw_l
        if max_luma_delta > 0:
            target = np.clip(target, raw_l - max_luma_delta, raw_l + max_luma_delta)
        return np.clip(target, 0.0, 255.0)

    def guard_pass(candidate_l):
        cand_grad, cand_mask = _edge_mask_from_luma(candidate_l)
        cand_added = (cand_mask > 0) & (support == 0)
        added_ratio = float(np.count_nonzero(cand_added)) / max(pixel_count, 1.0)
        cand_bg_grad = float(np.sum(cand_grad * background_mask))
        cand_grad_mean = float(np.mean(cand_grad))
        return (
            added_ratio <= guard_added_edge_ratio
            and cand_bg_grad <= raw_bg_grad * guard_background_grad_ratio
            and cand_grad_mean <= raw_grad_mean * guard_global_grad_ratio
        )

    target_l = raw_l.copy()
    for scale in fallback_scales:
        candidate_l = build_luma(scale)
        target_l = candidate_l
        if guard_pass(candidate_l):
            break

    chroma_weight = np.clip(base_blend_alpha + 0.5 * raw_global_blend_alpha, 0.0, 1.0)
    mixed_lab = cand_lab.copy()
    mixed_lab[..., 0] = target_l
    mixed_lab[..., 1] = (1.0 - chroma_weight) * cand_lab[..., 1] + chroma_weight * base_lab[..., 1]
    mixed_lab[..., 2] = (1.0 - chroma_weight) * cand_lab[..., 2] + chroma_weight * base_lab[..., 2]
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _endpoint_stabilized_weak_boundary_bph(original_uint8, bph_uint8=None, **params):
    """Weak-boundary enhancement with explicit endpoint and false-edge guards.

    P20 uses the P15 weak-boundary branch as the enhancement proposal, then
    pulls newly introduced off-support components, thin spurs and high-risk
    background gradients back toward a conservative microstructure base/raw
    anchor. The guard is intentionally detector-agnostic: it controls added
    edge pixels, background gradient budget and mean luminance drift before the
    fixed MyEdge detectors see the image.
    """
    if bph_uint8 is None:
        raise ValueError("endpoint_stabilized_weak_boundary_bph requires bph_uint8")

    candidate_params = dict(params.pop("candidate_params", {}))
    base_params = dict(params.pop("base_params", {}))
    prune_alpha = float(params.pop("prune_alpha", 0.70))
    line_prune_alpha = float(params.pop("line_prune_alpha", 0.62))
    background_prune_alpha = float(params.pop("background_prune_alpha", 0.34))
    background_denoise_alpha = float(params.pop("background_denoise_alpha", 0.16))
    raw_strong_edge_rescue_alpha = float(params.pop("raw_strong_edge_rescue_alpha", 0.42))
    raw_strong_edge_power = float(params.pop("raw_strong_edge_power", 1.65))
    raw_global_blend_alpha = float(params.pop("raw_global_blend_alpha", 0.10))
    base_global_blend_alpha = float(params.pop("base_global_blend_alpha", 0.06))
    chroma_base_alpha = float(params.pop("chroma_base_alpha", 0.10))
    chroma_candidate_alpha = float(params.pop("chroma_candidate_alpha", 0.05))
    max_luma_delta = float(params.pop("max_luma_delta", 4.8))
    raw_edge_dilate = int(params.pop("raw_edge_dilate", 2))
    edge_support_blur = _odd_ksize(params.pop("edge_support_blur", 7), minimum=1)
    small_component_max_area = int(params.pop("small_component_max_area", 18))
    line_component_max_area = int(params.pop("line_component_max_area", 64))
    line_component_max_minor_axis = int(params.pop("line_component_max_minor_axis", 3))
    line_component_min_aspect_ratio = float(params.pop("line_component_min_aspect_ratio", 2.2))
    local_std_sigma = float(params.pop("local_std_sigma", 3.0))
    grad_low_percentile = float(params.pop("grad_low_percentile", 48.0))
    grad_high_percentile = float(params.pop("grad_high_percentile", 90.0))
    std_low_percentile = float(params.pop("std_low_percentile", 22.0))
    std_high_percentile = float(params.pop("std_high_percentile", 82.0))
    pseudoedge_margin = float(params.pop("pseudoedge_margin", 0.025))
    guard_added_edge_ratio = float(params.pop("guard_added_edge_ratio", 0.012))
    guard_background_grad_ratio = float(params.pop("guard_background_grad_ratio", 0.996))
    guard_global_grad_ratio = float(params.pop("guard_global_grad_ratio", 1.018))
    guard_mean_abs_delta = float(params.pop("guard_mean_abs_delta", 1.9))
    fallback_scales = _as_float_list(params.pop("fallback_scales", None), [1.0, 0.82, 0.62, 0.38, 0.0])
    bilateral_d = int(params.pop("bilateral_d", 5))
    bilateral_sigma_color = float(params.pop("bilateral_sigma_color", 16.0))
    bilateral_sigma_space = float(params.pop("bilateral_sigma_space", 5.0))
    if params:
        raise ValueError(f"endpoint_stabilized_weak_boundary_bph 不支持的参数: {sorted(params.keys())}")

    prune_alpha = float(np.clip(prune_alpha, 0.0, 1.0))
    line_prune_alpha = float(np.clip(line_prune_alpha, 0.0, 1.0))
    background_prune_alpha = float(np.clip(background_prune_alpha, 0.0, 1.0))
    background_denoise_alpha = float(np.clip(background_denoise_alpha, 0.0, 1.0))
    raw_strong_edge_rescue_alpha = float(np.clip(raw_strong_edge_rescue_alpha, 0.0, 1.0))
    raw_global_blend_alpha = float(np.clip(raw_global_blend_alpha, 0.0, 1.0))
    base_global_blend_alpha = float(np.clip(base_global_blend_alpha, 0.0, 1.0))
    chroma_base_alpha = float(np.clip(chroma_base_alpha, 0.0, 1.0))
    chroma_candidate_alpha = float(np.clip(chroma_candidate_alpha, 0.0, 1.0))
    raw_strong_edge_power = max(raw_strong_edge_power, 1e-6)
    max_luma_delta = max(0.0, max_luma_delta)
    raw_edge_dilate = max(0, raw_edge_dilate)
    small_component_max_area = max(0, small_component_max_area)
    local_std_sigma = max(local_std_sigma, 1e-6)
    guard_added_edge_ratio = max(0.0, guard_added_edge_ratio)
    guard_background_grad_ratio = max(1e-6, guard_background_grad_ratio)
    guard_global_grad_ratio = max(1e-6, guard_global_grad_ratio)
    guard_mean_abs_delta = max(0.0, guard_mean_abs_delta)
    bilateral_d = max(1, bilateral_d)

    base_uint8 = _microstructure_csp_bph(original_uint8, bph_uint8=bph_uint8, **base_params)
    candidate_uint8 = _weak_boundary_pyramid_fusion_bph(
        original_uint8,
        bph_uint8=bph_uint8,
        **candidate_params,
    )

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    base_lab = cv2.cvtColor(base_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    cand_lab = cv2.cvtColor(candidate_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    base_l = base_lab[..., 0]
    cand_l = cand_lab[..., 0]

    raw_grad, raw_edge_mask = _edge_mask_from_luma(raw_l)
    _, cand_edge_mask = _edge_mask_from_luma(cand_l)
    support = raw_edge_mask.copy()
    if raw_edge_dilate > 0:
        kernel = np.ones((2 * raw_edge_dilate + 1, 2 * raw_edge_dilate + 1), dtype=np.uint8)
        support = cv2.dilate(support, kernel, iterations=1)
    added_edge = (cand_edge_mask > 0) & (support == 0)
    added_mask = added_edge.astype(np.uint8)

    local_mean = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=local_std_sigma)
    local_mean_sq = cv2.GaussianBlur(raw_l * raw_l, (0, 0), sigmaX=local_std_sigma)
    local_std = np.sqrt(np.maximum(local_mean_sq - local_mean * local_mean, 0.0))
    low_contrast = 1.0 - _normalize_by_percentiles(local_std, std_low_percentile, std_high_percentile)
    raw_edge = _normalize_by_percentiles(raw_grad, grad_low_percentile, grad_high_percentile)
    background_mask = np.clip((1.0 - raw_edge) * (0.35 + 0.65 * (1.0 - low_contrast)), 0.0, 1.0)

    small_mask = _small_component_mask(added_mask, small_component_max_area)
    line_mask = _component_shape_risk_mask(
        added_mask,
        max_area=line_component_max_area,
        max_minor_axis=line_component_max_minor_axis,
        min_aspect_ratio=line_component_min_aspect_ratio,
    )
    cand_x = cv2.Sobel(cand_l, cv2.CV_32F, 1, 0, ksize=3)
    cand_y = cv2.Sobel(cand_l, cv2.CV_32F, 0, 1, ksize=3)
    cand_grad = cv2.magnitude(cand_x, cand_y)
    pseudo_delta = np.maximum(cand_grad - raw_grad * (1.0 + pseudoedge_margin), 0.0)
    pseudo_mask = background_mask * _normalize_by_percentiles(pseudo_delta, 65.0, 96.0)
    risk_mask = np.clip(
        0.50 * added_mask.astype(np.float32) * background_mask
        + 0.28 * small_mask
        + 0.22 * line_mask
        + 0.35 * pseudo_mask,
        0.0,
        1.0,
    )
    if edge_support_blur > 1:
        risk_mask = cv2.GaussianBlur(risk_mask, (edge_support_blur, edge_support_blur), 0)
    risk_mask = np.clip(risk_mask, 0.0, 1.0)

    smooth_l = cv2.bilateralFilter(
        np.clip(base_l, 0, 255).astype(np.uint8),
        bilateral_d,
        bilateral_sigma_color,
        bilateral_sigma_space,
    ).astype(np.float32)

    raw_bg_grad = float(np.sum(raw_grad * background_mask)) + 1e-6
    raw_grad_mean = float(np.mean(raw_grad)) + 1e-6
    pixel_count = float(raw_l.size)

    def build_luma(scale):
        scale = float(np.clip(scale, 0.0, 1.0))
        target = raw_l + scale * (cand_l - raw_l)
        target = (1.0 - prune_alpha * risk_mask) * target + (prune_alpha * risk_mask) * raw_l
        target = (1.0 - line_prune_alpha * line_mask) * target + (line_prune_alpha * line_mask) * raw_l
        target = (1.0 - background_prune_alpha * background_mask * risk_mask) * target + (
            background_prune_alpha * background_mask * risk_mask
        ) * base_l
        target += background_denoise_alpha * background_mask * (smooth_l - target)
        strong_edge = np.power(np.clip(raw_edge, 0.0, 1.0), raw_strong_edge_power)
        target = (1.0 - raw_strong_edge_rescue_alpha * strong_edge) * target + (
            raw_strong_edge_rescue_alpha * strong_edge
        ) * raw_l
        if base_global_blend_alpha > 0:
            target = (1.0 - base_global_blend_alpha) * target + base_global_blend_alpha * base_l
        if raw_global_blend_alpha > 0:
            target = (1.0 - raw_global_blend_alpha) * target + raw_global_blend_alpha * raw_l
        if max_luma_delta > 0:
            target = np.clip(target, raw_l - max_luma_delta, raw_l + max_luma_delta)
        return np.clip(target, 0.0, 255.0)

    def guard_pass(candidate_l):
        candidate_grad, candidate_mask = _edge_mask_from_luma(candidate_l)
        candidate_added = (candidate_mask > 0) & (support == 0)
        added_ratio = float(np.count_nonzero(candidate_added)) / max(pixel_count, 1.0)
        candidate_bg_grad = float(np.sum(candidate_grad * background_mask))
        candidate_grad_mean = float(np.mean(candidate_grad))
        mean_abs_delta = float(np.mean(np.abs(candidate_l - raw_l)))
        return (
            added_ratio <= guard_added_edge_ratio
            and candidate_bg_grad <= raw_bg_grad * guard_background_grad_ratio
            and candidate_grad_mean <= raw_grad_mean * guard_global_grad_ratio
            and mean_abs_delta <= guard_mean_abs_delta
        )

    target_l = raw_l.copy()
    for scale in fallback_scales:
        candidate_l = build_luma(scale)
        target_l = candidate_l
        if guard_pass(candidate_l):
            break

    chroma_sum = min(chroma_base_alpha + chroma_candidate_alpha, 1.0)
    raw_chroma_alpha = 1.0 - chroma_sum
    mixed_lab = raw_lab.copy()
    mixed_lab[..., 0] = target_l
    mixed_lab[..., 1] = (
        raw_chroma_alpha * raw_lab[..., 1]
        + chroma_base_alpha * base_lab[..., 1]
        + chroma_candidate_alpha * cand_lab[..., 1]
    )
    mixed_lab[..., 2] = (
        raw_chroma_alpha * raw_lab[..., 2]
        + chroma_base_alpha * base_lab[..., 2]
        + chroma_candidate_alpha * cand_lab[..., 2]
    )
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _ac_guarded_weak_boundary_bph(original_uint8, bph_uint8=None, **params):
    """P22 weak-boundary candidate with detector-domain AC and false-edge guard.

    The proposal is a P21-style weak-boundary fusion. This wrapper keeps its
    downstream-positive weak-boundary transfer, then pulls off-support pseudo
    edges and thin added components back toward raw/base. It also preserves a
    raw-supported gradient floor so the fixed DiffusionEdge baseline is less
    likely to lose crispness/AC while suppressing background false edges.
    """
    if bph_uint8 is None:
        raise ValueError("ac_guarded_weak_boundary_bph requires bph_uint8")

    candidate_params = dict(params.pop("candidate_params", {}))
    base_params = dict(params.pop("base_params", {}))
    prune_alpha = float(params.pop("prune_alpha", 0.62))
    line_prune_alpha = float(params.pop("line_prune_alpha", 0.54))
    background_prune_alpha = float(params.pop("background_prune_alpha", 0.30))
    background_denoise_alpha = float(params.pop("background_denoise_alpha", 0.08))
    raw_strong_edge_rescue_alpha = float(params.pop("raw_strong_edge_rescue_alpha", 0.34))
    raw_strong_edge_power = float(params.pop("raw_strong_edge_power", 1.55))
    crisp_restore_alpha = float(params.pop("crisp_restore_alpha", 0.22))
    crisp_restore_power = float(params.pop("crisp_restore_power", 1.15))
    support_unsharp_alpha = float(params.pop("support_unsharp_alpha", 0.0))
    support_unsharp_sigma = float(params.pop("support_unsharp_sigma", 1.0))
    support_unsharp_power = float(params.pop("support_unsharp_power", 1.35))
    support_unsharp_max_delta = float(params.pop("support_unsharp_max_delta", 2.0))
    raw_global_blend_alpha = float(params.pop("raw_global_blend_alpha", 0.08))
    base_global_blend_alpha = float(params.pop("base_global_blend_alpha", 0.04))
    chroma_base_alpha = float(params.pop("chroma_base_alpha", 0.06))
    chroma_candidate_alpha = float(params.pop("chroma_candidate_alpha", 0.10))
    max_luma_delta = float(params.pop("max_luma_delta", 6.2))
    raw_edge_dilate = int(params.pop("raw_edge_dilate", 2))
    edge_support_blur = _odd_ksize(params.pop("edge_support_blur", 5), minimum=1)
    small_component_max_area = int(params.pop("small_component_max_area", 18))
    line_component_max_area = int(params.pop("line_component_max_area", 64))
    line_component_max_minor_axis = int(params.pop("line_component_max_minor_axis", 3))
    line_component_min_aspect_ratio = float(params.pop("line_component_min_aspect_ratio", 2.1))
    local_std_sigma = float(params.pop("local_std_sigma", 3.0))
    grad_low_percentile = float(params.pop("grad_low_percentile", 48.0))
    grad_high_percentile = float(params.pop("grad_high_percentile", 90.0))
    std_low_percentile = float(params.pop("std_low_percentile", 22.0))
    std_high_percentile = float(params.pop("std_high_percentile", 82.0))
    pseudoedge_margin = float(params.pop("pseudoedge_margin", 0.025))
    guard_added_edge_ratio = float(params.pop("guard_added_edge_ratio", 0.012))
    guard_background_grad_ratio = float(params.pop("guard_background_grad_ratio", 0.998))
    guard_global_grad_ratio = float(params.pop("guard_global_grad_ratio", 1.020))
    guard_support_grad_ratio = float(params.pop("guard_support_grad_ratio", 0.985))
    guard_mean_abs_delta = float(params.pop("guard_mean_abs_delta", 1.8))
    fallback_scales = _as_float_list(params.pop("fallback_scales", None), [1.0, 0.88, 0.72, 0.55, 0.35, 0.0])
    bilateral_d = int(params.pop("bilateral_d", 5))
    bilateral_sigma_color = float(params.pop("bilateral_sigma_color", 16.0))
    bilateral_sigma_space = float(params.pop("bilateral_sigma_space", 5.0))
    if params:
        raise ValueError(f"ac_guarded_weak_boundary_bph 不支持的参数: {sorted(params.keys())}")

    prune_alpha = float(np.clip(prune_alpha, 0.0, 1.0))
    line_prune_alpha = float(np.clip(line_prune_alpha, 0.0, 1.0))
    background_prune_alpha = float(np.clip(background_prune_alpha, 0.0, 1.0))
    background_denoise_alpha = float(np.clip(background_denoise_alpha, 0.0, 1.0))
    raw_strong_edge_rescue_alpha = float(np.clip(raw_strong_edge_rescue_alpha, 0.0, 1.0))
    crisp_restore_alpha = float(np.clip(crisp_restore_alpha, 0.0, 1.0))
    support_unsharp_alpha = float(np.clip(support_unsharp_alpha, 0.0, 1.0))
    raw_global_blend_alpha = float(np.clip(raw_global_blend_alpha, 0.0, 1.0))
    base_global_blend_alpha = float(np.clip(base_global_blend_alpha, 0.0, 1.0))
    chroma_base_alpha = float(np.clip(chroma_base_alpha, 0.0, 1.0))
    chroma_candidate_alpha = float(np.clip(chroma_candidate_alpha, 0.0, 1.0))
    raw_strong_edge_power = max(raw_strong_edge_power, 1e-6)
    crisp_restore_power = max(crisp_restore_power, 1e-6)
    support_unsharp_sigma = max(support_unsharp_sigma, 1e-6)
    support_unsharp_power = max(support_unsharp_power, 1e-6)
    support_unsharp_max_delta = max(0.0, support_unsharp_max_delta)
    max_luma_delta = max(0.0, max_luma_delta)
    raw_edge_dilate = max(0, raw_edge_dilate)
    small_component_max_area = max(0, small_component_max_area)
    local_std_sigma = max(local_std_sigma, 1e-6)
    guard_added_edge_ratio = max(0.0, guard_added_edge_ratio)
    guard_background_grad_ratio = max(1e-6, guard_background_grad_ratio)
    guard_global_grad_ratio = max(1e-6, guard_global_grad_ratio)
    guard_support_grad_ratio = max(0.0, guard_support_grad_ratio)
    guard_mean_abs_delta = max(0.0, guard_mean_abs_delta)
    bilateral_d = max(1, bilateral_d)

    base_uint8 = _boundary_aware_luma_bph(original_uint8, bph_uint8=bph_uint8, **base_params)
    candidate_uint8 = _weak_boundary_pyramid_fusion_bph(
        original_uint8,
        bph_uint8=bph_uint8,
        **candidate_params,
    )

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    base_lab = cv2.cvtColor(base_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    cand_lab = cv2.cvtColor(candidate_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    base_l = base_lab[..., 0]
    cand_l = cand_lab[..., 0]

    raw_grad, raw_edge_mask = _edge_mask_from_luma(raw_l)
    cand_x = cv2.Sobel(cand_l, cv2.CV_32F, 1, 0, ksize=3)
    cand_y = cv2.Sobel(cand_l, cv2.CV_32F, 0, 1, ksize=3)
    cand_grad = cv2.magnitude(cand_x, cand_y)
    _, cand_edge_mask = _edge_mask_from_luma(cand_l)

    support = raw_edge_mask.copy()
    if raw_edge_dilate > 0:
        kernel = np.ones((2 * raw_edge_dilate + 1, 2 * raw_edge_dilate + 1), dtype=np.uint8)
        support = cv2.dilate(support, kernel, iterations=1)
    added_mask = ((cand_edge_mask > 0) & (support == 0)).astype(np.uint8)

    local_mean = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=local_std_sigma)
    local_mean_sq = cv2.GaussianBlur(raw_l * raw_l, (0, 0), sigmaX=local_std_sigma)
    local_std = np.sqrt(np.maximum(local_mean_sq - local_mean * local_mean, 0.0))
    low_contrast = 1.0 - _normalize_by_percentiles(local_std, std_low_percentile, std_high_percentile)
    raw_edge = _normalize_by_percentiles(raw_grad, grad_low_percentile, grad_high_percentile)
    background_mask = np.clip((1.0 - raw_edge) * (0.35 + 0.65 * (1.0 - low_contrast)), 0.0, 1.0)

    small_mask = _small_component_mask(added_mask, small_component_max_area)
    line_mask = _component_shape_risk_mask(
        added_mask,
        max_area=line_component_max_area,
        max_minor_axis=line_component_max_minor_axis,
        min_aspect_ratio=line_component_min_aspect_ratio,
    )
    pseudo_delta = np.maximum(cand_grad - raw_grad * (1.0 + pseudoedge_margin), 0.0)
    pseudo_mask = background_mask * _normalize_by_percentiles(pseudo_delta, 65.0, 96.0)
    risk_mask = np.clip(
        0.55 * added_mask.astype(np.float32) * background_mask
        + 0.25 * small_mask
        + 0.20 * line_mask
        + 0.30 * pseudo_mask,
        0.0,
        1.0,
    )
    if edge_support_blur > 1:
        risk_mask = cv2.GaussianBlur(risk_mask, (edge_support_blur, edge_support_blur), 0)
        line_mask = cv2.GaussianBlur(line_mask, (edge_support_blur, edge_support_blur), 0)
    risk_mask = np.clip(risk_mask, 0.0, 1.0)
    line_mask = np.clip(line_mask, 0.0, 1.0)

    edge_loss = np.maximum(raw_grad - cand_grad * (1.0 + pseudoedge_margin), 0.0)
    edge_loss_mask = _normalize_by_percentiles(edge_loss, 65.0, 96.0)
    crisp_mask = np.power(np.clip(raw_edge, 0.0, 1.0), crisp_restore_power) * (0.35 + 0.65 * edge_loss_mask)
    crisp_mask *= support.astype(np.float32)
    crisp_mask = np.clip(crisp_mask, 0.0, 1.0)

    smooth_l = cv2.bilateralFilter(
        np.clip(base_l, 0, 255).astype(np.uint8),
        bilateral_d,
        bilateral_sigma_color,
        bilateral_sigma_space,
    ).astype(np.float32)

    raw_bg_grad = float(np.sum(raw_grad * background_mask)) + 1e-6
    raw_grad_mean = float(np.mean(raw_grad)) + 1e-6
    support_weight = np.clip(raw_edge * support.astype(np.float32), 0.0, 1.0)
    raw_support_grad = float(np.sum(raw_grad * support_weight)) + 1e-6
    pixel_count = float(raw_l.size)
    support_unsharp_mask = np.power(np.clip(support_weight, 0.0, 1.0), support_unsharp_power) * (1.0 - risk_mask)
    support_unsharp_mask = np.clip(support_unsharp_mask, 0.0, 1.0)
    raw_support_detail = raw_l - cv2.GaussianBlur(raw_l, (0, 0), sigmaX=support_unsharp_sigma)
    if support_unsharp_max_delta > 0:
        raw_support_detail = np.clip(raw_support_detail, -support_unsharp_max_delta, support_unsharp_max_delta)

    def build_luma(scale):
        scale = float(np.clip(scale, 0.0, 1.0))
        target = raw_l + scale * (cand_l - raw_l)
        target = (1.0 - prune_alpha * risk_mask) * target + (prune_alpha * risk_mask) * raw_l
        target = (1.0 - line_prune_alpha * line_mask) * target + (line_prune_alpha * line_mask) * raw_l
        target = (1.0 - background_prune_alpha * background_mask * risk_mask) * target + (
            background_prune_alpha * background_mask * risk_mask
        ) * base_l
        target += background_denoise_alpha * background_mask * (smooth_l - target)
        strong_edge = np.power(np.clip(raw_edge, 0.0, 1.0), raw_strong_edge_power)
        target = (1.0 - raw_strong_edge_rescue_alpha * strong_edge) * target + (
            raw_strong_edge_rescue_alpha * strong_edge
        ) * raw_l
        target = (1.0 - crisp_restore_alpha * crisp_mask) * target + (
            crisp_restore_alpha * crisp_mask
        ) * raw_l
        if support_unsharp_alpha > 0:
            target += support_unsharp_alpha * support_unsharp_mask * raw_support_detail
        if base_global_blend_alpha > 0:
            target = (1.0 - base_global_blend_alpha) * target + base_global_blend_alpha * base_l
        if raw_global_blend_alpha > 0:
            target = (1.0 - raw_global_blend_alpha) * target + raw_global_blend_alpha * raw_l
        if max_luma_delta > 0:
            target = np.clip(target, raw_l - max_luma_delta, raw_l + max_luma_delta)
        return np.clip(target, 0.0, 255.0)

    def guard_pass(candidate_l):
        candidate_grad, candidate_mask = _edge_mask_from_luma(candidate_l)
        candidate_added = (candidate_mask > 0) & (support == 0)
        added_ratio = float(np.count_nonzero(candidate_added)) / max(pixel_count, 1.0)
        candidate_bg_grad = float(np.sum(candidate_grad * background_mask))
        candidate_grad_mean = float(np.mean(candidate_grad))
        candidate_support_grad = float(np.sum(candidate_grad * support_weight))
        mean_abs_delta = float(np.mean(np.abs(candidate_l - raw_l)))
        return (
            added_ratio <= guard_added_edge_ratio
            and candidate_bg_grad <= raw_bg_grad * guard_background_grad_ratio
            and candidate_grad_mean <= raw_grad_mean * guard_global_grad_ratio
            and candidate_support_grad >= raw_support_grad * guard_support_grad_ratio
            and mean_abs_delta <= guard_mean_abs_delta
        )

    target_l = raw_l.copy()
    for scale in fallback_scales:
        candidate_l = build_luma(scale)
        target_l = candidate_l
        if guard_pass(candidate_l):
            break

    chroma_sum = min(chroma_base_alpha + chroma_candidate_alpha, 1.0)
    raw_chroma_alpha = 1.0 - chroma_sum
    mixed_lab = raw_lab.copy()
    mixed_lab[..., 0] = target_l
    mixed_lab[..., 1] = (
        raw_chroma_alpha * raw_lab[..., 1]
        + chroma_base_alpha * base_lab[..., 1]
        + chroma_candidate_alpha * cand_lab[..., 1]
    )
    mixed_lab[..., 2] = (
        raw_chroma_alpha * raw_lab[..., 2]
        + chroma_base_alpha * base_lab[..., 2]
        + chroma_candidate_alpha * cand_lab[..., 2]
    )
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def _dual_anchor_false_edge_floor_bph(original_uint8, bph_uint8=None, **params):
    """P26 false-edge-floor wrapper for AP-preserving weak-boundary output.

    This mode starts from an AC-guarded weak-boundary anchor, then applies a
    second detector-domain floor only where the anchor introduces off-support
    background edges or thin components. The intent is to reduce the baseline
    false-edge/endpoints trade-off seen in P23/P25 without globally suppressing
    weak-boundary detail as P24 did.
    """
    if bph_uint8 is None:
        raise ValueError("dual_anchor_false_edge_floor_bph requires bph_uint8")

    floor_alpha = float(params.pop("floor_alpha", 0.24))
    raw_floor_alpha = float(params.pop("raw_floor_alpha", 0.18))
    line_floor_alpha = float(params.pop("line_floor_alpha", 0.44))
    small_floor_alpha = float(params.pop("small_floor_alpha", 0.34))
    background_denoise_alpha = float(params.pop("floor_background_denoise_alpha", 0.08))
    support_rescue_alpha = float(params.pop("support_rescue_alpha", 0.18))
    support_rescue_power = float(params.pop("support_rescue_power", 1.35))
    raw_global_blend_alpha = float(params.pop("floor_raw_global_blend_alpha", 0.04))
    max_luma_delta = float(params.pop("floor_max_luma_delta", 4.4))
    raw_edge_dilate = int(params.pop("floor_raw_edge_dilate", 2))
    edge_support_blur = _odd_ksize(params.pop("floor_edge_support_blur", 7), minimum=1)
    small_component_max_area = int(params.pop("floor_small_component_max_area", 34))
    line_component_max_area = int(params.pop("floor_line_component_max_area", 96))
    line_component_max_minor_axis = int(params.pop("floor_line_component_max_minor_axis", 3))
    line_component_min_aspect_ratio = float(params.pop("floor_line_component_min_aspect_ratio", 1.9))
    pseudoedge_margin = float(params.pop("floor_pseudoedge_margin", 0.022))
    grad_low_percentile = float(params.pop("floor_grad_low_percentile", 48.5))
    grad_high_percentile = float(params.pop("floor_grad_high_percentile", 90.2))
    local_std_sigma = float(params.pop("floor_local_std_sigma", 3.0))
    std_low_percentile = float(params.pop("floor_std_low_percentile", 22.0))
    std_high_percentile = float(params.pop("floor_std_high_percentile", 82.0))
    guard_added_edge_ratio = float(params.pop("floor_guard_added_edge_ratio", 0.0075))
    guard_background_grad_ratio = float(params.pop("floor_guard_background_grad_ratio", 0.988))
    guard_global_grad_ratio = float(params.pop("floor_guard_global_grad_ratio", 1.008))
    guard_support_grad_ratio = float(params.pop("floor_guard_support_grad_ratio", 0.992))
    guard_mean_abs_delta = float(params.pop("floor_guard_mean_abs_delta", 1.18))
    fallback_scales = _as_float_list(params.pop("floor_fallback_scales", None), [1.0, 0.82, 0.64, 0.46, 0.28, 0.0])
    bilateral_d = int(params.pop("floor_bilateral_d", 5))
    bilateral_sigma_color = float(params.pop("floor_bilateral_sigma_color", 15.0))
    bilateral_sigma_space = float(params.pop("floor_bilateral_sigma_space", 5.0))
    anchor_params = dict(params)

    floor_alpha = float(np.clip(floor_alpha, 0.0, 1.0))
    raw_floor_alpha = float(np.clip(raw_floor_alpha, 0.0, 1.0))
    line_floor_alpha = float(np.clip(line_floor_alpha, 0.0, 1.0))
    small_floor_alpha = float(np.clip(small_floor_alpha, 0.0, 1.0))
    background_denoise_alpha = float(np.clip(background_denoise_alpha, 0.0, 1.0))
    support_rescue_alpha = float(np.clip(support_rescue_alpha, 0.0, 1.0))
    raw_global_blend_alpha = float(np.clip(raw_global_blend_alpha, 0.0, 1.0))
    support_rescue_power = max(support_rescue_power, 1e-6)
    max_luma_delta = max(0.0, max_luma_delta)
    raw_edge_dilate = max(0, raw_edge_dilate)
    small_component_max_area = max(0, small_component_max_area)
    line_component_max_area = max(0, line_component_max_area)
    line_component_max_minor_axis = max(0, line_component_max_minor_axis)
    line_component_min_aspect_ratio = max(line_component_min_aspect_ratio, 1.0)
    local_std_sigma = max(local_std_sigma, 1e-6)
    guard_added_edge_ratio = max(0.0, guard_added_edge_ratio)
    guard_background_grad_ratio = max(1e-6, guard_background_grad_ratio)
    guard_global_grad_ratio = max(1e-6, guard_global_grad_ratio)
    guard_support_grad_ratio = max(0.0, guard_support_grad_ratio)
    guard_mean_abs_delta = max(0.0, guard_mean_abs_delta)
    bilateral_d = max(1, bilateral_d)

    anchor_uint8 = _ac_guarded_weak_boundary_bph(
        original_uint8,
        bph_uint8=bph_uint8,
        **anchor_params,
    )

    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    anchor_lab = cv2.cvtColor(anchor_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    anchor_l = anchor_lab[..., 0]

    raw_grad, raw_edge_mask = _edge_mask_from_luma(raw_l)
    anchor_grad, anchor_edge_mask = _edge_mask_from_luma(anchor_l)
    support = raw_edge_mask.copy()
    if raw_edge_dilate > 0:
        kernel = np.ones((2 * raw_edge_dilate + 1, 2 * raw_edge_dilate + 1), dtype=np.uint8)
        support = cv2.dilate(support, kernel, iterations=1)
    support_soft = support.astype(np.float32)
    if edge_support_blur > 1:
        support_soft = cv2.GaussianBlur(support_soft, (edge_support_blur, edge_support_blur), 0)
    support_soft = np.clip(support_soft, 0.0, 1.0)

    local_mean = cv2.GaussianBlur(raw_l, (0, 0), sigmaX=local_std_sigma)
    local_mean_sq = cv2.GaussianBlur(raw_l * raw_l, (0, 0), sigmaX=local_std_sigma)
    local_std = np.sqrt(np.maximum(local_mean_sq - local_mean * local_mean, 0.0))
    low_contrast = 1.0 - _normalize_by_percentiles(local_std, std_low_percentile, std_high_percentile)
    raw_edge = _normalize_by_percentiles(raw_grad, grad_low_percentile, grad_high_percentile)
    background_mask = np.clip((1.0 - support_soft) * (0.40 + 0.60 * (1.0 - low_contrast)), 0.0, 1.0)

    added_mask = ((anchor_edge_mask > 0) & (support == 0)).astype(np.uint8)
    small_mask = _small_component_mask(added_mask, small_component_max_area)
    line_mask = _component_shape_risk_mask(
        added_mask,
        max_area=line_component_max_area,
        max_minor_axis=line_component_max_minor_axis,
        min_aspect_ratio=line_component_min_aspect_ratio,
    )
    pseudo_delta = np.maximum(anchor_grad - raw_grad * (1.0 + pseudoedge_margin), 0.0)
    pseudo_mask = background_mask * _normalize_by_percentiles(pseudo_delta, 64.0, 96.0)
    risk_mask = np.clip(
        0.42 * added_mask.astype(np.float32) * background_mask
        + 0.24 * small_mask
        + 0.30 * line_mask
        + 0.34 * pseudo_mask,
        0.0,
        1.0,
    )
    if edge_support_blur > 1:
        risk_mask = cv2.GaussianBlur(risk_mask, (edge_support_blur, edge_support_blur), 0)
        small_mask = cv2.GaussianBlur(small_mask, (edge_support_blur, edge_support_blur), 0)
        line_mask = cv2.GaussianBlur(line_mask, (edge_support_blur, edge_support_blur), 0)
    risk_mask = np.clip(risk_mask, 0.0, 1.0)
    small_mask = np.clip(small_mask, 0.0, 1.0)
    line_mask = np.clip(line_mask, 0.0, 1.0)

    smooth_l = cv2.bilateralFilter(
        np.clip(raw_l, 0, 255).astype(np.uint8),
        bilateral_d,
        bilateral_sigma_color,
        bilateral_sigma_space,
    ).astype(np.float32)
    floor_l = raw_l + background_denoise_alpha * background_mask * (smooth_l - raw_l)

    edge_loss = np.maximum(raw_grad - anchor_grad * (1.0 + pseudoedge_margin), 0.0)
    edge_loss_mask = support_soft * _normalize_by_percentiles(edge_loss, 65.0, 96.0)
    support_rescue_mask = np.power(np.clip(raw_edge, 0.0, 1.0), support_rescue_power) * edge_loss_mask
    support_rescue_mask = np.clip(support_rescue_mask, 0.0, 1.0)

    raw_bg_grad = float(np.sum(raw_grad * background_mask)) + 1e-6
    raw_grad_mean = float(np.mean(raw_grad)) + 1e-6
    support_weight = np.clip(raw_edge * support_soft, 0.0, 1.0)
    raw_support_grad = float(np.sum(raw_grad * support_weight)) + 1e-6
    pixel_count = float(raw_l.size)

    def build_luma(scale):
        scale = float(np.clip(scale, 0.0, 1.0))
        target = raw_l + scale * (anchor_l - raw_l)
        target = (1.0 - floor_alpha * risk_mask) * target + (floor_alpha * risk_mask) * floor_l
        target = (1.0 - raw_floor_alpha * risk_mask) * target + (raw_floor_alpha * risk_mask) * raw_l
        target = (1.0 - small_floor_alpha * small_mask) * target + (small_floor_alpha * small_mask) * floor_l
        target = (1.0 - line_floor_alpha * line_mask) * target + (line_floor_alpha * line_mask) * raw_l
        target = (1.0 - support_rescue_alpha * support_rescue_mask) * target + (
            support_rescue_alpha * support_rescue_mask
        ) * raw_l
        if raw_global_blend_alpha > 0:
            target = (1.0 - raw_global_blend_alpha) * target + raw_global_blend_alpha * raw_l
        if max_luma_delta > 0:
            target = np.clip(target, raw_l - max_luma_delta, raw_l + max_luma_delta)
        return np.clip(target, 0.0, 255.0)

    def guard_pass(candidate_l):
        candidate_grad, candidate_mask = _edge_mask_from_luma(candidate_l)
        candidate_added = (candidate_mask > 0) & (support == 0)
        added_ratio = float(np.count_nonzero(candidate_added)) / max(pixel_count, 1.0)
        candidate_bg_grad = float(np.sum(candidate_grad * background_mask))
        candidate_grad_mean = float(np.mean(candidate_grad))
        candidate_support_grad = float(np.sum(candidate_grad * support_weight))
        mean_abs_delta = float(np.mean(np.abs(candidate_l - raw_l)))
        return (
            added_ratio <= guard_added_edge_ratio
            and candidate_bg_grad <= raw_bg_grad * guard_background_grad_ratio
            and candidate_grad_mean <= raw_grad_mean * guard_global_grad_ratio
            and candidate_support_grad >= raw_support_grad * guard_support_grad_ratio
            and mean_abs_delta <= guard_mean_abs_delta
        )

    target_l = raw_l.copy()
    for scale in fallback_scales:
        candidate_l = build_luma(scale)
        target_l = candidate_l
        if guard_pass(candidate_l):
            break

    mixed_lab = anchor_lab.copy()
    mixed_lab[..., 0] = target_l
    return cv2.cvtColor(np.clip(mixed_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)

DOWNSTREAM_FINAL_MODES = {
    "edge_preserve_blend",
    "generic_luma_clahe",
    "generic_luma_gamma",
    "edge_safe_gamma_bph",
    "boundary_aware_luma_bph",
    "microstructure_csp_bph",
    "topology_guarded_microfusion_bph",
    "topology_pruned_microfusion_bph",
    "endpoint_stabilized_weak_boundary_bph",
    "ac_guarded_weak_boundary_bph",
    "dual_anchor_false_edge_floor_bph",
    "raw_detail_lowfreq_chroma_bph",
    "downstream_d01_structure_flow_bph",
    "degradation_aware_pyramid_frequency_bph",
    "weak_boundary_pyramid_fusion_bph",
}


def run_downstream_final_mode(mode, fused_uint8, original_uint8=None, bph_uint8=None, **params):
    """Run an explicit downstream-driven diagnostic final mode.

    Returns ``None`` when ``mode`` is not one of the archived diagnostic modes,
    so the caller can continue with the locked mainline dispatch.
    """
    if mode not in DOWNSTREAM_FINAL_MODES:
        return None
    if mode == "edge_preserve_blend":
        return _edge_preserve_blend(fused_uint8, original_uint8=original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "generic_luma_clahe":
        if original_uint8 is None:
            raise ValueError("generic_luma_clahe requires original_uint8")
        return _generic_luma_clahe(original_uint8, **params)
    if mode == "generic_luma_gamma":
        if original_uint8 is None:
            raise ValueError("generic_luma_gamma requires original_uint8")
        return _generic_luma_gamma(original_uint8, **params)
    if mode == "edge_safe_gamma_bph":
        if original_uint8 is None:
            raise ValueError("edge_safe_gamma_bph requires original_uint8")
        return _edge_safe_gamma_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "boundary_aware_luma_bph":
        if original_uint8 is None:
            raise ValueError("boundary_aware_luma_bph requires original_uint8")
        return _boundary_aware_luma_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "microstructure_csp_bph":
        if original_uint8 is None:
            raise ValueError("microstructure_csp_bph requires original_uint8")
        return _microstructure_csp_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "topology_guarded_microfusion_bph":
        if original_uint8 is None:
            raise ValueError("topology_guarded_microfusion_bph requires original_uint8")
        return _topology_guarded_microfusion_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "topology_pruned_microfusion_bph":
        if original_uint8 is None:
            raise ValueError("topology_pruned_microfusion_bph requires original_uint8")
        return _topology_pruned_microfusion_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "endpoint_stabilized_weak_boundary_bph":
        if original_uint8 is None:
            raise ValueError("endpoint_stabilized_weak_boundary_bph requires original_uint8")
        return _endpoint_stabilized_weak_boundary_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "ac_guarded_weak_boundary_bph":
        if original_uint8 is None:
            raise ValueError("ac_guarded_weak_boundary_bph requires original_uint8")
        return _ac_guarded_weak_boundary_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "dual_anchor_false_edge_floor_bph":
        if original_uint8 is None:
            raise ValueError("dual_anchor_false_edge_floor_bph requires original_uint8")
        return _dual_anchor_false_edge_floor_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "raw_detail_lowfreq_chroma_bph":
        if original_uint8 is None:
            raise ValueError("raw_detail_lowfreq_chroma_bph requires original_uint8")
        return _raw_detail_lowfreq_chroma_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "downstream_d01_structure_flow_bph":
        if original_uint8 is None:
            raise ValueError("downstream_d01_structure_flow_bph requires original_uint8")
        return _downstream_d01_structure_flow_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "degradation_aware_pyramid_frequency_bph":
        if original_uint8 is None:
            raise ValueError("degradation_aware_pyramid_frequency_bph requires original_uint8")
        return _degradation_aware_pyramid_frequency_bph(original_uint8, bph_uint8=bph_uint8, **params)
    if mode == "weak_boundary_pyramid_fusion_bph":
        if original_uint8 is None:
            raise ValueError("weak_boundary_pyramid_fusion_bph requires original_uint8")
        return _weak_boundary_pyramid_fusion_bph(original_uint8, bph_uint8=bph_uint8, **params)
    raise ValueError(f"未知 downstream final mode: {mode}")
