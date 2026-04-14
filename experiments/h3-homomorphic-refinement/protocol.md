# H3 Protocol: Homomorphic Refinement Ablation

## Hypothesis

The final L-channel homomorphic filtering step improves illumination uniformity and readability, but it is a secondary refinement rather than the main driver of the method's gains.

## Why This Matters

This step is useful in practice, but it risks being over-claimed if not tested separately. A clean ablation lets the paper present it honestly as a finishing refinement.

## Locked Evaluation Setup

- Subset: `pilot92-v1`
- Output format for metrics: PNG
- Primary decision metrics: `Mean_SIFT_KP`, `Mean_AvgGra`, `Mean_MS_SSIM`

## Planned Variants

1. `no_lvbo`
   - Stop after the fused output.
2. `baseline_lvbo`
   - Current `Gaussian_lvbo` post-processing as implemented.
3. `weaker_lvbo`
   - A softer homomorphic setting to test whether the current configuration is stronger than necessary.

## Prediction

- `baseline_lvbo` should provide a modest readability gain over `no_lvbo`, mostly in contrast uniformity and final visual polish.
- The delta should be smaller than the H2 fusion delta. If it is not, that implies the method story has been framed around the wrong module.

## Sanity Checks

- Compare dark-background regions for halo artifacts or artificial brightness washout.
- Confirm that any contrast gain does not come with a structure-preservation collapse.

## Success Criterion

H3 is supported if the homomorphic stage gives a small but repeatable additive benefit beyond the fused image.

## Failure Interpretation

If `no_lvbo` and `baseline_lvbo` are nearly identical, the paper should either demote this step to implementation detail or remove it from the core claim set.
