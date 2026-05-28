"""E01 task-guided HAB enhancement candidate family.

E01 is separate from the archived Pxx/Dxx/FF/TLVC diagnostic families. The
first implemented candidate, E01-A, tests a color/illumination-dominant
mechanism: low-frequency color and illumination may change, while raw
high-frequency luma topology remains the detector-facing anchor. E01-B changes
the primary representation to wavelet-like frequency bands and only injects
stable directional weak-boundary evidence.
"""

from __future__ import annotations

import cv2
import numpy as np


MODE_E01_A = "e01_a_color_illumination_task_guided_v1"
MODE_E01_B = "e01_b_wavelet_pyramid_weak_boundary_v1"
MODE_NAMES = {MODE_E01_A, MODE_E01_B}


def is_e01_task_guided_mode(mode):
    return mode in MODE_NAMES


def _to_uint8_lab(lab):
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


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


def _blur(mask, ksize):
    k = _odd_ksize(ksize, minimum=1)
    if k <= 1:
        return np.clip(mask.astype(np.float32), 0.0, 1.0)
    return np.clip(cv2.GaussianBlur(mask.astype(np.float32), (k, k), 0), 0.0, 1.0)


def _local_std(luma, ksize):
    k = _odd_ksize(ksize, minimum=3)
    mean = cv2.boxFilter(luma, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    mean2 = cv2.boxFilter(luma * luma, -1, (k, k), borderType=cv2.BORDER_REFLECT)
    return np.sqrt(np.maximum(mean2 - mean * mean, 0.0)).astype(np.float32)


def _scharr_mag(luma):
    gx = cv2.Scharr(luma.astype(np.float32), cv2.CV_32F, 1, 0)
    gy = cv2.Scharr(luma.astype(np.float32), cv2.CV_32F, 0, 1)
    return np.sqrt(gx * gx + gy * gy).astype(np.float32)


def _edge_confidence(luma, low_percentile, high_percentile):
    mag = _scharr_mag(luma)
    lo = float(np.percentile(mag, low_percentile))
    hi = float(np.percentile(mag, high_percentile))
    if hi <= lo + 1e-8:
        return np.zeros_like(luma, dtype=np.float32)
    return np.clip((mag - lo) / (hi - lo), 0.0, 1.0).astype(np.float32)


def _multi_scale_edge_support(luma, low_percentile, high_percentile):
    supports = []
    for sigma in (0.0, 1.2, 2.4):
        src = luma if sigma <= 0 else cv2.GaussianBlur(luma, (0, 0), sigma)
        supports.append(_edge_confidence(src, low_percentile, high_percentile))
    mean_support = np.mean(supports, axis=0).astype(np.float32)
    stable_support = np.minimum.reduce(supports).astype(np.float32)
    return np.clip(0.68 * mean_support + 0.32 * stable_support, 0.0, 1.0)


def _diagnose(original_uint8, params):
    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0]
    edge_support = _multi_scale_edge_support(
        raw_l / 255.0,
        float(params.get("edge_low_percentile", 70.0)),
        float(params.get("edge_high_percentile", 99.2)),
    )
    local_contrast = _normalize01(_local_std(raw_l / 255.0, int(params.get("local_std_ksize", 15))))
    texture_risk = _normalize01(_local_std(raw_l / 255.0, int(params.get("texture_std_ksize", 7))))
    weak_need = np.power(np.clip(edge_support, 0.0, 1.0), 0.70) * (1.0 - 0.55 * local_contrast)
    weak_need = _blur(weak_need, int(params.get("mask_blur_ksize", 5)))
    background_risk = (1.0 - edge_support) * np.power(texture_risk, 0.90)
    background_risk = _blur(background_risk, int(params.get("mask_blur_ksize", 5)))
    saturation = np.max(original_uint8.astype(np.float32), axis=2) / 255.0
    saturation_risk = _blur(np.clip((saturation - 0.92) / 0.08, 0.0, 1.0), 5)
    return {
        "raw_lab": raw_lab,
        "raw_l": raw_l,
        "edge_support": edge_support,
        "local_contrast": local_contrast,
        "texture_risk": texture_risk,
        "weak_need": weak_need,
        "background_risk": background_risk,
        "saturation_risk": saturation_risk,
    }


def _cap_delta(delta, cap):
    cap = float(cap)
    if cap <= 0:
        return delta
    return np.clip(delta, -cap, cap)


def _build_color_illumination_lane(original_uint8, bph_uint8, diagnosis, params):
    raw_lab = diagnosis["raw_lab"]
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    out = raw_lab.copy()

    low_sigma = float(params.get("low_sigma", 13.0))
    raw_low = cv2.GaussianBlur(raw_lab[..., 0], (0, 0), low_sigma)
    bph_low = cv2.GaussianBlur(bph_lab[..., 0], (0, 0), low_sigma)
    illum_delta = _cap_delta(bph_low - raw_low, float(params.get("illum_max_delta", 8.0)))
    illum_alpha = float(params.get("illum_alpha", 0.48))
    illum_support = np.clip(
        0.45 + 0.40 * diagnosis["weak_need"] + 0.20 * (1.0 - diagnosis["background_risk"]),
        0.0,
        1.0,
    )
    if not bool(params.get("enable_low_frequency_luma_correction", True)):
        illum_alpha = 0.0
    out[..., 0] = np.clip(raw_lab[..., 0] + illum_alpha * illum_support * illum_delta, 0.0, 255.0)

    color_alpha = float(params.get("color_alpha", 0.68))
    if not bool(params.get("enable_color_illumination_lane", True)):
        color_alpha = 0.0
    color_conf = np.clip(
        float(params.get("color_support_floor", 0.48))
        + 0.32 * (1.0 - diagnosis["saturation_risk"])
        + 0.20 * (1.0 - diagnosis["background_risk"]),
        0.0,
        1.0,
    )
    max_chroma_delta = float(params.get("max_chroma_delta", 18.0))
    for channel in (1, 2):
        delta = _cap_delta(bph_lab[..., channel] - raw_lab[..., channel], max_chroma_delta)
        out[..., channel] = np.clip(raw_lab[..., channel] + color_alpha * color_conf * delta, 0.0, 255.0)
    return out, _to_uint8_lab(out)


def _build_weak_boundary_lane(raw_lab, diagnosis, params):
    out = raw_lab.copy()
    raw_l = raw_lab[..., 0]
    low_sigma = float(params.get("low_sigma", 13.0))
    raw_low = cv2.GaussianBlur(raw_l, (0, 0), low_sigma)
    raw_detail = raw_l - raw_low

    contrast = cv2.createCLAHE(
        clipLimit=float(params.get("weak_clahe_clip", 1.10)),
        tileGridSize=tuple(params.get("weak_clahe_tile", [8, 8])),
    ).apply(np.clip(raw_l, 0, 255).astype(np.uint8)).astype(np.float32)
    weak_residual = _cap_delta(
        contrast - raw_l,
        float(params.get("weak_residual_max_delta", 4.0)),
    )
    support = diagnosis["weak_need"] * (1.0 - diagnosis["background_risk"])
    if not bool(params.get("enable_weak_boundary_support", True)):
        support = np.zeros_like(support)
    out[..., 0] = np.clip(
        raw_l
        + float(params.get("raw_detail_alpha", 1.0)) * raw_detail * 0.0
        + float(params.get("weak_residual_alpha", 0.20)) * support * weak_residual,
        0.0,
        255.0,
    )
    return out, _to_uint8_lab(out)


def _reconstruct(raw_lab, color_lab, weak_lab, diagnosis, params):
    low_sigma = float(params.get("low_sigma", 13.0))
    raw_l = raw_lab[..., 0]
    raw_low = cv2.GaussianBlur(raw_l, (0, 0), low_sigma)
    raw_detail = raw_l - raw_low

    color_low = cv2.GaussianBlur(color_lab[..., 0], (0, 0), low_sigma)
    low_delta = _cap_delta(color_low - raw_low, float(params.get("recon_low_max_delta", 7.0)))
    weak_delta = _cap_delta(weak_lab[..., 0] - raw_l, float(params.get("recon_weak_max_delta", 4.0)))
    weak_gate = diagnosis["weak_need"] * (1.0 - diagnosis["background_risk"])

    luma = raw_low + float(params.get("recon_low_alpha", 0.72)) * low_delta
    if bool(params.get("enable_raw_detail_preservation", True)):
        luma = luma + raw_detail
    luma = luma + float(params.get("recon_weak_alpha", 0.45)) * weak_gate * weak_delta
    if bool(params.get("enable_background_false_edge_suppression", True)):
        new_delta = luma - raw_l
        suppress = float(params.get("background_suppression_alpha", 0.80)) * diagnosis["background_risk"]
        luma = raw_l + new_delta * (1.0 - np.clip(suppress, 0.0, 1.0))

    out = raw_lab.copy()
    out[..., 0] = np.clip(luma, 0.0, 255.0)
    chroma_alpha = float(params.get("recon_chroma_alpha", 0.88))
    for channel in (1, 2):
        delta = _cap_delta(color_lab[..., channel] - raw_lab[..., channel], float(params.get("max_chroma_delta", 18.0)))
        out[..., channel] = np.clip(raw_lab[..., channel] + chroma_alpha * delta, 0.0, 255.0)
    return out, _to_uint8_lab(out)


def _global_stats(original_uint8, candidate_uint8):
    raw_lab = cv2.cvtColor(original_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    cand_lab = cv2.cvtColor(candidate_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    raw_l = raw_lab[..., 0] / 255.0
    cand_l = cand_lab[..., 0] / 255.0
    raw_grad = float(np.mean(_scharr_mag(raw_l))) + 1e-8
    cand_grad = float(np.mean(_scharr_mag(cand_l)))
    chroma_delta = np.sqrt(
        (cand_lab[..., 1] - raw_lab[..., 1]) ** 2 + (cand_lab[..., 2] - raw_lab[..., 2]) ** 2
    )
    return {
        "mean_abs_luma_delta": float(np.mean(np.abs(cand_lab[..., 0] - raw_lab[..., 0]))),
        "mean_abs_chroma_delta": float(np.mean(chroma_delta)),
        "grad_ratio": cand_grad / raw_grad,
        "luma_std_ratio": (float(np.std(cand_l)) + 1e-8) / (float(np.std(raw_l)) + 1e-8),
    }


def _blend_bgr(anchor_uint8, candidate_uint8, scale):
    return np.clip(
        np.round(anchor_uint8.astype(np.float32) * (1.0 - scale) + candidate_uint8.astype(np.float32) * scale),
        0,
        255,
    ).astype(np.uint8)


def _bounded_reconstruction(original_uint8, candidate_uint8, params):
    if not bool(params.get("enable_bounded_reconstruction", True)):
        return candidate_uint8
    scales = params.get("bounded_scales", [1.0, 0.85, 0.70, 0.55, 0.40])
    max_grad_ratio = float(params.get("bounded_max_grad_ratio", 1.10))
    max_luma_std_ratio = float(params.get("bounded_max_luma_std_ratio", 1.08))
    max_luma_delta = float(params.get("bounded_max_mean_abs_luma_delta", 5.0))
    max_chroma_delta = float(params.get("bounded_max_mean_abs_chroma_delta", 12.0))
    best = candidate_uint8
    for scale in scales:
        trial = _blend_bgr(original_uint8, candidate_uint8, float(scale))
        stats = _global_stats(original_uint8, trial)
        best = trial
        if (
            stats["grad_ratio"] <= max_grad_ratio
            and stats["luma_std_ratio"] <= max_luma_std_ratio
            and stats["mean_abs_luma_delta"] <= max_luma_delta
            and stats["mean_abs_chroma_delta"] <= max_chroma_delta
        ):
            return trial
    return best


def _bilateral_finish(candidate_uint8, diagnosis, params):
    if not bool(params.get("enable_bilateral_finish", True)):
        return candidate_uint8
    filtered = cv2.bilateralFilter(
        candidate_uint8,
        int(params.get("bilateral_d", 5)),
        float(params.get("bilateral_sigma_color", 16.0)),
        float(params.get("bilateral_sigma_space", 5.0)),
    )
    alpha = float(params.get("bilateral_alpha", 0.22)) * diagnosis["background_risk"]
    out = candidate_uint8.astype(np.float32) * (1.0 - alpha[..., None]) + filtered.astype(np.float32) * alpha[..., None]
    return np.clip(np.round(out), 0, 255).astype(np.uint8)


def _resize_mask(mask, shape):
    return cv2.resize(
        mask.astype(np.float32),
        (int(shape[1]), int(shape[0])),
        interpolation=cv2.INTER_AREA,
    ).astype(np.float32)


def _haar_decompose(luma):
    src = luma.astype(np.float32)
    h, w = src.shape[:2]
    pad_h = h % 2
    pad_w = w % 2
    if pad_h or pad_w:
        src = cv2.copyMakeBorder(src, 0, pad_h, 0, pad_w, cv2.BORDER_REFLECT_101)
    a = src[0::2, 0::2]
    b = src[0::2, 1::2]
    c = src[1::2, 0::2]
    d = src[1::2, 1::2]
    ll = (a + b + c + d) * 0.25
    lh = (a + b - c - d) * 0.25
    hl = (a - b + c - d) * 0.25
    hh = (a - b - c + d) * 0.25
    return ll, lh, hl, hh, (h, w)


def _haar_reconstruct(ll, lh, hl, hh, original_shape):
    a = ll + lh + hl + hh
    b = ll + lh - hl - hh
    c = ll - lh + hl - hh
    d = ll - lh - hl + hh
    out = np.empty((ll.shape[0] * 2, ll.shape[1] * 2), dtype=np.float32)
    out[0::2, 0::2] = a
    out[0::2, 1::2] = b
    out[1::2, 0::2] = c
    out[1::2, 1::2] = d
    h, w = original_shape
    return out[:h, :w]


def _make_luma_bgr(raw_lab, luma):
    lab = raw_lab.copy()
    lab[..., 0] = np.clip(luma, 0.0, 255.0)
    return _to_uint8_lab(lab)


def _build_wavelet_candidate(original_uint8, bph_uint8, diagnosis, params):
    raw_lab = diagnosis["raw_lab"]
    raw_l = raw_lab[..., 0]
    bph_lab = cv2.cvtColor(bph_uint8, cv2.COLOR_BGR2LAB).astype(np.float32)
    clahe_l = cv2.createCLAHE(
        clipLimit=float(params.get("wavelet_clahe_clip", 1.18)),
        tileGridSize=tuple(params.get("wavelet_clahe_tile", [8, 8])),
    ).apply(np.clip(raw_l, 0, 255).astype(np.uint8)).astype(np.float32)

    raw_ll, raw_lh, raw_hl, raw_hh, original_shape = _haar_decompose(raw_l)
    bph_ll, _, _, _, _ = _haar_decompose(bph_lab[..., 0])
    clahe_ll, clahe_lh, clahe_hl, clahe_hh, _ = _haar_decompose(clahe_l)

    weak = _resize_mask(diagnosis["weak_need"], raw_ll.shape)
    edge = _resize_mask(diagnosis["edge_support"], raw_ll.shape)
    risk = _resize_mask(diagnosis["background_risk"], raw_ll.shape)
    directional_gate = np.clip(
        float(params.get("directional_gate_floor", 0.18))
        + float(params.get("directional_weak_weight", 0.62)) * weak
        + float(params.get("directional_edge_weight", 0.28)) * edge
        - float(params.get("directional_risk_weight", 0.62)) * risk,
        0.0,
        1.0,
    )
    directional_gate = _blur(directional_gate, int(params.get("wavelet_gate_blur_ksize", 3)))

    ll = raw_ll.copy()
    if bool(params.get("enable_ll_illumination_field", True)):
        ll_delta = _cap_delta(bph_ll - raw_ll, float(params.get("ll_max_delta", 3.5)))
        ll_support = np.clip(0.38 + 0.32 * weak + 0.22 * (1.0 - risk), 0.0, 1.0)
        ll = raw_ll + float(params.get("ll_alpha", 0.34)) * ll_support * ll_delta

    lh = raw_lh.copy()
    hl = raw_hl.copy()
    if bool(params.get("enable_directional_weak_boundary_boost", True)):
        max_dir = float(params.get("directional_max_delta", 2.4))
        lh_delta = _cap_delta(clahe_lh - raw_lh, max_dir)
        hl_delta = _cap_delta(clahe_hl - raw_hl, max_dir)
        alpha = float(params.get("directional_alpha", 0.42))
        lh = raw_lh + alpha * directional_gate * lh_delta
        hl = raw_hl + alpha * directional_gate * hl_delta

    hh = raw_hh.copy()
    if bool(params.get("enable_hh_texture_suppression", True)):
        hh_suppress = float(params.get("hh_suppression_alpha", 0.42)) * risk
        hh_delta = _cap_delta(clahe_hh - raw_hh, float(params.get("hh_boost_max_delta", 1.2)))
        hh = raw_hh * (1.0 - np.clip(hh_suppress, 0.0, 0.85))
        hh = hh + float(params.get("hh_edge_alpha", 0.08)) * directional_gate * hh_delta

    wavelet_l = _haar_reconstruct(ll, lh, hl, hh, original_shape)
    wavelet_l = np.clip(wavelet_l, 0.0, 255.0)
    if bool(params.get("enable_wavelet_background_control", True)):
        delta = wavelet_l - raw_l
        suppress = float(params.get("wavelet_background_suppression_alpha", 0.62)) * diagnosis["background_risk"]
        wavelet_l = raw_l + delta * (1.0 - np.clip(suppress, 0.0, 0.92))
    wavelet_l = np.clip(wavelet_l, 0.0, 255.0)

    out_lab = raw_lab.copy()
    out_lab[..., 0] = wavelet_l
    if bool(params.get("enable_mild_chroma_lane", True)):
        chroma_alpha = float(params.get("wavelet_chroma_alpha", 0.38))
        chroma_conf = np.clip(0.42 + 0.30 * (1.0 - diagnosis["background_risk"]), 0.0, 1.0)
        max_chroma = float(params.get("wavelet_max_chroma_delta", 10.0))
        for channel in (1, 2):
            delta = _cap_delta(bph_lab[..., channel] - raw_lab[..., channel], max_chroma)
            out_lab[..., channel] = np.clip(raw_lab[..., channel] + chroma_alpha * chroma_conf * delta, 0.0, 255.0)

    final = _to_uint8_lab(out_lab)
    if bool(params.get("enable_wavelet_guided_finish", True)):
        final = _bilateral_finish(final, diagnosis, {
            "enable_bilateral_finish": True,
            "bilateral_d": int(params.get("wavelet_bilateral_d", 5)),
            "bilateral_sigma_color": float(params.get("wavelet_bilateral_sigma_color", 12.0)),
            "bilateral_sigma_space": float(params.get("wavelet_bilateral_sigma_space", 5.0)),
            "bilateral_alpha": float(params.get("wavelet_bilateral_alpha", 0.16)),
        })
    final = _bounded_reconstruction(original_uint8, final, params)

    return {
        "wavelet_l": wavelet_l,
        "clahe_l": clahe_l,
        "ll_l": _haar_reconstruct(ll, raw_lh * 0.0, raw_hl * 0.0, raw_hh * 0.0, original_shape),
        "out_lab": out_lab,
        "final": final,
    }


def _run_e01_a(original_uint8, bph_uint8, params):
    supported = {
        "enable_degradation_diagnosis",
        "enable_color_illumination_lane",
        "enable_low_frequency_luma_correction",
        "enable_raw_detail_preservation",
        "enable_weak_boundary_support",
        "enable_background_false_edge_suppression",
        "enable_bounded_reconstruction",
        "enable_bilateral_finish",
        "edge_low_percentile",
        "edge_high_percentile",
        "local_std_ksize",
        "texture_std_ksize",
        "mask_blur_ksize",
        "low_sigma",
        "illum_alpha",
        "illum_max_delta",
        "color_alpha",
        "color_support_floor",
        "max_chroma_delta",
        "weak_clahe_clip",
        "weak_clahe_tile",
        "weak_residual_alpha",
        "weak_residual_max_delta",
        "raw_detail_alpha",
        "recon_low_alpha",
        "recon_low_max_delta",
        "recon_weak_alpha",
        "recon_weak_max_delta",
        "background_suppression_alpha",
        "recon_chroma_alpha",
        "bilateral_d",
        "bilateral_sigma_color",
        "bilateral_sigma_space",
        "bilateral_alpha",
        "bounded_scales",
        "bounded_max_grad_ratio",
        "bounded_max_luma_std_ratio",
        "bounded_max_mean_abs_luma_delta",
        "bounded_max_mean_abs_chroma_delta",
    }
    unknown = sorted(set(params) - supported)
    if unknown:
        raise ValueError(f"Unsupported E01-A params: {unknown}")

    diagnosis = _diagnose(original_uint8, params)
    raw_lab = diagnosis["raw_lab"]

    color_lab, color_lane = _build_color_illumination_lane(original_uint8, bph_uint8, diagnosis, params)
    weak_lab, weak_lane = _build_weak_boundary_lane(raw_lab, diagnosis, params)
    fused_lab, fused = _reconstruct(raw_lab, color_lab, weak_lab, diagnosis, params)
    final = _bilateral_finish(fused, diagnosis, params)
    final = _bounded_reconstruction(original_uint8, final, params)

    # The stage names keep the existing Stage1/MyEdge asset contract. In E01-A
    # they are evidence slots, not claims that the legacy algorithms dominate.
    return {
        "IMF1Ray": weak_lane,
        "RGHS": color_lane,
        "CLAHE": _to_uint8_lab(fused_lab),
        "Fused": fused,
        "Final": final,
    }


def _run_e01_b(original_uint8, bph_uint8, params):
    supported = {
        "enable_degradation_diagnosis",
        "enable_ll_illumination_field",
        "enable_directional_weak_boundary_boost",
        "enable_hh_texture_suppression",
        "enable_wavelet_background_control",
        "enable_mild_chroma_lane",
        "enable_wavelet_guided_finish",
        "enable_bounded_reconstruction",
        "edge_low_percentile",
        "edge_high_percentile",
        "local_std_ksize",
        "texture_std_ksize",
        "mask_blur_ksize",
        "wavelet_clahe_clip",
        "wavelet_clahe_tile",
        "wavelet_gate_blur_ksize",
        "directional_gate_floor",
        "directional_weak_weight",
        "directional_edge_weight",
        "directional_risk_weight",
        "directional_alpha",
        "directional_max_delta",
        "ll_alpha",
        "ll_max_delta",
        "hh_suppression_alpha",
        "hh_edge_alpha",
        "hh_boost_max_delta",
        "wavelet_background_suppression_alpha",
        "wavelet_chroma_alpha",
        "wavelet_max_chroma_delta",
        "wavelet_bilateral_d",
        "wavelet_bilateral_sigma_color",
        "wavelet_bilateral_sigma_space",
        "wavelet_bilateral_alpha",
        "bounded_scales",
        "bounded_max_grad_ratio",
        "bounded_max_luma_std_ratio",
        "bounded_max_mean_abs_luma_delta",
        "bounded_max_mean_abs_chroma_delta",
    }
    unknown = sorted(set(params) - supported)
    if unknown:
        raise ValueError(f"Unsupported E01-B params: {unknown}")

    diagnosis = _diagnose(original_uint8, params)
    raw_lab = diagnosis["raw_lab"]
    bands = _build_wavelet_candidate(original_uint8, bph_uint8, diagnosis, params)
    color_preview = _to_uint8_lab(bands["out_lab"])
    clahe_preview = _make_luma_bgr(raw_lab, bands["clahe_l"])
    wavelet_lane = _make_luma_bgr(raw_lab, bands["wavelet_l"])
    ll_preview = _make_luma_bgr(raw_lab, bands["ll_l"])

    # Stage slots retain the existing asset contract. In E01-B they correspond
    # to wavelet evidence views: directional bands, mild color, CLAHE driver,
    # reconstructed luma, and final bounded output.
    return {
        "IMF1Ray": wavelet_lane,
        "RGHS": color_preview,
        "CLAHE": clahe_preview,
        "Fused": ll_preview,
        "Final": bands["final"],
    }


def run_e01_task_guided_family(original_uint8, *, bph_uint8, e01_params=None):
    if bph_uint8 is None:
        raise ValueError("E01 task-guided family requires bph_uint8")

    params = dict(e01_params or {})
    mode = params.pop("_mode", MODE_E01_A)
    params.pop("mode", None)
    params.pop("enabled", None)
    if mode not in MODE_NAMES:
        raise ValueError(f"Unsupported E01 mode: {mode}")

    original_uint8 = np.asarray(original_uint8, dtype=np.uint8)
    bph_uint8 = np.asarray(bph_uint8, dtype=np.uint8)
    if mode == MODE_E01_A:
        return _run_e01_a(original_uint8, bph_uint8, params)
    if mode == MODE_E01_B:
        return _run_e01_b(original_uint8, bph_uint8, params)
    raise ValueError(f"Unsupported E01 mode: {mode}")
