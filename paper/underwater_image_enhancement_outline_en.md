# English Title, Abstract, and Section Skeleton

Updated: 2026-04-22

## Candidate Titles

1. A Staged Enhancement Framework with Feature-Gated Fusion for Underwater HAB Microscopy Images
2. Responsibility-Separated Branch Enhancement and Luminance-Domain Fusion for Underwater Harmful Algal Bloom Microscopy
3. Evidence-Aligned Underwater Microscopy Image Enhancement via White-Balance Stabilization and Structured Fusion

## Abstract Draft

Underwater harmful algal bloom microscopy images often suffer from color cast, low local contrast, blurred fine structures, and uneven illumination. These degradations can affect not only visual quality but also the readability of cell boundaries and texture cues required by downstream analysis. This work organizes the current project implementation into a staged enhancement framework. The pipeline first stabilizes the color baseline through gray-pixel-guided white balance, then constructs three responsibility-separated branches for high-frequency detail recovery, white-balance-safe contrast support, and CLAHE-guided local visibility. A luminance-domain fusion stage coordinates the branch outputs using gradient, texture, saliency, and exposure-related cues, followed by a lightweight illumination and contrast refinement step. Based on the internal full506 protocol, the current evidence supports cautious claims on improved structure-related metrics under the locked mainline configuration, while also revealing a real trade-off between fusion-driven structural gains and some no-reference visual quality scores. The paper positions the method as a reproducible, task-oriented engineering framework for underwater HAB microscopy enhancement rather than as a fully benchmarked general-purpose underwater enhancement model.

## Keywords

Underwater image enhancement; harmful algal bloom microscopy; white balance; multi-branch fusion; feature-gated fusion; structural readability.

## 1. Introduction

Goal: motivate underwater HAB microscopy enhancement as a structure-sensitive restoration problem.

Evidence to use: local project files, full506 protocol, existing Notion method pages, H1/H2 experiment records.

Careful wording: avoid claiming state-of-the-art performance before external baselines and statistical analysis are completed.

## 2. Related Work

### 2.1 Traditional Underwater Enhancement

Discuss color balance, fusion, generalized dark channel prior, Retinex or reflectance-prior methods, and wavelet or perception-based fusion.

Verified references: Ancuti et al. 2018; Peng et al. 2018; Zhuang et al. 2022; Zhang et al. 2024.

### 2.2 HAB Microscopy-Oriented Enhancement

Discuss EMD/wavelet fusion, cyclic color compensation, and adaptive white balance plus pyramid fusion in submarine algal microscopy.

Verified references: Wu et al. 2023 Applied Intelligence; Wu et al. 2023 Multimedia Tools and Applications; Fan et al. 2025 Image and Vision Computing.

### 2.3 Learning-Based and White-Balance-Oriented Models

Discuss SGUIE-Net, Histoformer, and white-balance transformers only as contextual references unless direct experiments are added.

Verified references: Qi et al. 2022; Peng et al. 2025; Chiu et al. 2025; Peng and Chen 2025.

## 3. Method

### 3.1 Overview

Pipeline: Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final.

### 3.2 Gray-Pixel-Guided White-Balance Stabilization

Describe BPH as gray-pixel-guided pre-white-balance plus conservative contrast and brightness restoration.

### 3.3 Responsibility-Separated Enhancement Branches

IMF1Ray: Lab L-channel EMD IMF1 extraction, guided filtering, local energy and Rayleigh matching.

RGHS: white-balance-safe contrast branch, Lab luminance contrast, chroma protection, gamut guard.

CLAHE: CLAHE-guided visibility branch, gain-map smoothing, RGB proportional gain, Lab post adjustment.

### 3.4 Feature-Gated Luminance Fusion

Describe gradient, texture, saliency, exposure, guided alignment, pyramid fusion, and RGHS color anchor.

### 3.5 Final Illumination Refinement

Describe the current homomorphic entropy refinement cautiously as a finishing stage, not the main contribution.

## 4. Experiments

### 4.1 Dataset and Protocol

Internal full506 protocol: 506 images from local project input directory.

### 4.2 Metrics

Report MS-SSIM, PSNR, UCIQE, UIQM, SIFT keypoints, AvgGra, contrast, EME, EMEE, entropy, and internal composite score.

### 4.3 H1 White-Balance Ablation

Use baseline and accepted BPH configuration results from the local experiment summary.

### 4.4 H2 Sequential Branch Optimization

Use locked RGHS, CLAHE, and Fusion selections. Explicitly discuss Fusion's structural improvement and no-reference visual score rollback.

### 4.5 Qualitative Analysis

Add representative image panels after manual selection.

### 4.6 Missing External Baselines

Add Color Balance and Fusion, WWPF, HAB-specific baselines, SGUIE-Net, and Histoformer when runnable.

## 5. Discussion and Limitations

Focus on internal evidence boundaries, historical module names, lack of external benchmarks, missing downstream edge validation, and metric trade-offs.

## 6. Conclusion

Conclude with a cautious claim: the current project provides an implementation-aligned staged enhancement framework with measurable internal structural gains and a clear path toward stronger journal submission evidence.
