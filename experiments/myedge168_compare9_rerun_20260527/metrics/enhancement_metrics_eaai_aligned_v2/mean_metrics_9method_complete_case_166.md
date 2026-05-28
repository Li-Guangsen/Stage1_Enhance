# Mean Metrics: 9 Enhancement Methods Complete-Case 166

Official main table for the MyEdge 166 complete-case enhancement-metric baseline. The complete-case set is derived from the MyEdge 168 raw split and excludes `chazhuang.3.jpg` and `chazhuang.6.jpg` from all methods because WWPF has no normalized outputs for those two samples. The no-WWPF 168 table is supplementary only.

`HLRP` and `Histoformer` are retained for numeric traceability but are high-noise diagnostic references. They must not be used in the primary screening conclusion, and high no-reference scores from them should not be interpreted as stable positive enhancement.

| Method | Role | Count | EME | EMEE | Entropy | Contrast | AvgGra | MS_SSIM | PSNR | UCIQE | UIQM | SSEQ | SIFT_GOOD_MATCHES | SIFT_MATCH_RATIO |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| raw | anchor_raw | 166 | 2.2741 | 0.4249 | 3.7840 | 24.1159 | 3.0232 | 1.0000 | 361.2020 | 2.1268 | 7.4419 | 1.1235 |  |  |
| Ours | legacy_ours_reference | 166 | 14.6360 | 1.1212 | 5.9670 | 765.3156 | 22.0485 | 0.7291 | 17.1885 | 4.0310 | 32.0510 | 1.9483 | 26.8554 | 0.2184 |
| HVDualformer | enhancement_reference | 166 | 2.4952 | 0.4371 | 3.9493 | 24.6097 | 3.1785 | 0.9918 | 33.8083 | 1.6590 | 8.1063 | 1.2294 | 90.8735 | 0.7842 |
| ABC-Former | enhancement_reference | 166 | 2.3257 | 0.4277 | 3.8770 | 24.4906 | 3.1244 | 0.9984 | 42.0653 | 2.0849 | 7.4921 | 1.1810 | 110.3253 | 0.9125 |
| GDCP | enhancement_reference | 166 | 6.7235 | 0.6777 | 5.3409 | 95.9529 | 7.4380 | 0.8801 | 24.1671 | 3.5157 | 18.7952 | 1.7853 | 72.4759 | 0.6038 |
| CBF | enhancement_reference | 166 | 8.0925 | 0.7474 | 6.6389 | 119.8897 | 9.4919 | 0.7363 | 17.4156 | 2.8618 | 21.2771 | 2.0564 | 71.2651 | 0.5236 |
| HLRP | enhancement_high_noise_diagnostic | 166 | 13.8528 | 1.0691 | 6.7580 | 154.0878 | 13.3430 | 0.4100 | 13.6732 | 2.7608 | 31.6106 | 2.3704 | 33.8373 | 0.1927 |
| SGUIE-Net | enhancement_reference | 166 | 6.0973 | 0.6423 | 4.8249 | 103.9582 | 6.9491 | 0.8977 | 24.3523 | 3.0095 | 15.9562 | 1.5749 | 77.8253 | 0.6198 |
| Histoformer | enhancement_high_noise_diagnostic | 166 | 22.4028 | 1.5549 | 7.2469 | 749.0457 | 28.4075 | 0.3954 | 15.5026 | 5.2727 | 47.3155 | 2.5013 | 40.8253 | 0.2095 |
| WWPF | enhancement_incomplete_166_of_168 | 166 | 13.0293 | 1.0383 | 6.5547 | 446.4037 | 19.7990 | 0.5732 | 15.2360 | 2.6142 | 29.7317 | 2.2915 | 58.1988 | 0.4840 |
