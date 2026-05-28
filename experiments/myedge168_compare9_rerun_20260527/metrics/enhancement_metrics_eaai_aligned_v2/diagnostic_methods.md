# Diagnostic Method Notes

- `raw` is an anchor, not an enhancement method. Its `SIFT_MATCH_RATIO` is `NA` because SIFT matching is defined as raw-enhanced matching.
- `Ours` is the legacy Stage1 reference output for this MyEdge 168 rerun. It is retained for historical comparison and is not a hard target for future candidates.
- `HLRP` and `Histoformer` remain in the numeric table but are marked as `enhancement_high_noise_diagnostic`; high no-reference scores from noisy outputs must not be interpreted as stable positive enhancement.
- `WWPF` is marked as `enhancement_incomplete_166_of_168`; it failed on `chazhuang.3.jpg` and `chazhuang.6.jpg` in the rerun.
- The official main table is therefore the 166-stem complete-case table. Those two samples are excluded from all methods in the main table, not only from WWPF.
- Future candidates should use `UIQM`, `UCIQE`, `SSEQ`, and `SIFT_MATCH_RATIO` on the 166 complete-case as the first screening group. Downstream fixed-detector validation remains the final criterion and should use the same 166-stem set.
