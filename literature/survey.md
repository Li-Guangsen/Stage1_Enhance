# Literature Survey

## Project Scope

This project is currently centered on HAB underwater microscopic image enhancement, with downstream validation through edge-relevant tasks rather than a purely aesthetic enhancement claim.

## Core Local References

1. **Wu et al. 2023** — enhancement-only baseline for cyclic color compensation + multi-scale fusion
2. **Fan et al. 2025** — enhancement + edge-detection validation/extension
3. **Wu et al. 2023 (EMD + wavelet fusion)** — decomposition-oriented predecessor for detail extraction in HAB image enhancement
4. **Frontiers Marine Science 2024 edge paper** — downstream HAB edge-detection reference using diffusion-probability and Sobel-attention language

## Current Synthesis

- The literature supports a strong paper line where enhancement is justified by downstream edge/feature extraction, not only by no-reference image quality metrics.
- The current repository already diverges enough from the published methods that the paper should be written as a project-specific method, not as a literal reproduction of either reference.
- The strongest reproducible story at present is:
  1. task-specific white balance and color correction,
  2. complementary detail/contrast branches,
  3. feature-aware multiscale fusion,
  4. downstream edge-oriented validation.
- The literature lineage around this project now has a useful three-step story:
  1. decomposition/fusion enhancement precursors,
  2. cyclic compensation plus multiscale fusion for HAB microscopy,
  3. enhancement validated by downstream edge-sensitive tasks.

## Immediate Next Literature Needs

- Broaden outward from the two local papers to 2021-2026 work on underwater image enhancement, microscopic image enhancement, and edge-sensitive enhancement validation.
- Identify 3-5 comparison methods that are both credible and realistically reproducible in this environment.
- Build a clean citation list for the eventual enhancement paper draft.
- Separate "paper-structure references" from "true method baselines" so the final paper does not over-claim direct implementation equivalence.
