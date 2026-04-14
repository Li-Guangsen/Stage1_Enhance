# Wu et al. 2023

## Bibliographic Info

- Title: Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion
- Authors: Geng-Kun Wu et al.
- Venue: Multimedia Tools and Applications
- Year: 2023
- Local source: `paper/1_xujie.pdf`

## Why It Matters

This is the earlier enhancement-only reference and gives the historical baseline for cyclic color compensation plus three-image multi-scale fusion in HAB microscopic images.

## Method Summary

- Cyclic color compensation for color cast correction
- Three-image fusion inputs derived from the compensated image
- Weight maps described with Canny, Butterworth high-pass, and gamma correction
- Evaluation through enhancement metrics, SIFT/keypoint matching, and edge detection

## Experiment Structure Worth Reusing

- White-balance evaluation section
- Enhancement evaluation with Entropy / Contrast / AvgGradient / EME / EMEE / MSSIM
- SIFT keypoint count comparison
- Edge detection before-vs-after enhancement

## What Matches the Current Repository

- Three-branch fusion idea
- Downstream validation through keypoints and edge extraction
- Task-specific motivation for HAB microscopic imagery rather than generic underwater scenes

## What Does Not Match Exactly

- The current repository's white-balance module is more sophisticated than the published cyclic compensation description
- The current fusion implementation is no longer just the paper's original Canny/Butterworth/gamma weighting story
- The current pipeline adds a heavy IMF1Ray branch and a homomorphic refinement stage beyond the original publication framing

## Relevance to Current Paper Writing

Use this paper mainly for:

- historical baseline framing
- early enhancement-paper narrative
- examples of downstream validation for a first-stage enhancement paper
