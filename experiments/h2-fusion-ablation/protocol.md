# H2 Protocol: Three-Branch Fusion Ablation

## Hypothesis

The IMF1Ray/RGHS/CLAHE feature-gated fusion is the main source of the method's publishable gain and should outperform single-branch outputs and naive fusion baselines.

## Why This Matters

Among the current modules, `fusion_three.py` is the clearest code-level innovation. If this hypothesis holds, the paper can center its method section on complementary branch design plus feature-gated fusion rather than on any single classical enhancement operator.

## Locked Evaluation Setup

- Subset: `pilot92-v1`
- Output format for metrics: PNG
- Primary decision metrics: `Mean_SIFT_KP`, `Mean_AvgGra`, `Mean_MS_SSIM`

## Planned Variants

1. `baseline_current_fusion`
   - Current gated three-branch fusion plus the standard downstream refinement path.
2. `imf1_only`
   - Use the IMF1Ray branch output as the final pre-refinement enhancement.
3. `rghs_only`
   - Use the RGHS branch output as the final pre-refinement enhancement.
4. `clahe_only`
   - Use the CLAHE branch output as the final pre-refinement enhancement.
5. `equal_weight_fusion`
   - Replace the feature-gated fusion with a simple equal-weight average of the three branches.
6. `leave_one_branch_out`
   - Three sub-variants: remove IMF1, remove RGHS, or remove CLAHE while keeping the rest of the fusion procedure.

## Prediction

- The full fusion should outperform any single branch on `SIFT_KP` and `AvgGra`.
- Equal-weight fusion should be more balanced than branch-only baselines but still worse than the gated fusion.
- Removing IMF1 is expected to hurt fine texture visibility most; removing RGHS is expected to reduce global contrast balance; removing CLAHE is expected to weaken some mid-tone local visibility.

## Sanity Checks

- Compare visually against branch-only outputs to ensure the fusion is not merely averaging away useful structure.
- Monitor for over-texturing or noisy background amplification, especially on dense algae samples.
- Verify that improvements are not caused by isolated outliers with extreme keypoint inflation.

## Success Criterion

H2 is supported if the current fusion clearly dominates single-branch and naive-fusion baselines under the locked pilot protocol.

## Failure Interpretation

If equal-weight fusion performs similarly to the current fusion, the paper should down-weight strong claims about the gating design and focus more on branch complementarity itself.
