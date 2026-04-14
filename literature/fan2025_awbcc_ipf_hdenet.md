# Fan et al. 2025

## Bibliographic Info

- Title: Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy
- Authors: Yi-Ning Fan et al.
- Venue: Image and Vision Computing
- Year: 2025
- Local source: `paper/1_F.pdf`

## Why It Matters

This is the closest reference for the current project because it explicitly links enhancement quality to downstream edge detection on HAB microscopic images.

## Method Summary

- Enhancement framing: AWBCC + IPF/ECH
- White-balance side: ACCC under gray-world assumptions, plus attenuation-guided transfer language in the paper
- Enhancement side: CLAHE, contrast stretching, and EMD-derived detail handling inside image pyramid fusion
- Downstream side: HDEnet edge detector, with ODS/OIS/AP reporting

## Experiment Structure Worth Reusing

- Enhancement quality table with multiple no-reference metrics
- SIFT/keypoint-based downstream validation
- Enhancement-before-vs-after edge detection visualizations
- Ablation on missing components of the enhancement pipeline

## What Matches the Current Repository

- The overall “white balance → multi-branch enhancement → fusion → downstream validation” story
- The emphasis on showing that enhancement improves edge visibility, not just image appearance

## What Does Not Match Exactly

- The current repository does not literally implement the paper's exact attenuation-map-transfer wording
- The current fusion implementation is more feature-driven and differs from the paper-level narrative
- The current repository's strongest novelty is in the actual branch/fusion implementation, not in mirroring the paper section-by-section

## Relevance to Current Paper Writing

Use this paper mainly for:

- enhancement-paper structure
- ablation layout
- edge-validation framing
- how to connect image enhancement to biological morphology visibility
