# H2 full506 直跑调参

- 创建时间：`2026-04-16T11:55:29`
- 最近更新：`2026-04-16T13:28:58`
- 总状态：`completed`
- 基线配置：`D:\Desktop\Stage1Codex\experiments\optimization_v1\configs\locked_full506_mainline.json`
- 基线结果：`D:\Desktop\Stage1Codex\experiments\h1-graypixel-bph-ablation\outputs\full506\runs\full506_locked_mainline`
- full506 manifest：`D:\Desktop\Stage1Codex\metrics\outputs\evaluate_protocol_v2\full506_c25\complete_case_manifest.txt`
- smoke manifest：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\smoke_manifest.txt`
- 当前接受统一配置：`D:\Desktop\Stage1Codex\experiments\optimization_v1\configs\locked_full506_final_mainline.json`
- 当前正式结果目录：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\outputs\full506\runs\full506_final_mainline`
- 当前正式评测目录：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\outputs\full506\eval`
- 结果来源清单：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\outputs\full506\runs\full506_final_mainline\artifact_manifest.json`

## RGHS

- 状态：`completed`
- 排序：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\scores\rghs_official\ranked.json`
- Final 回退检查：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\scores\rghs_final_backstop\ranked.json`
- winner：`rghs_s07`
- 参数文件：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\configs\rghs\rghs_s07.json`
- 官方胜出：ΔMS-SSIM=`0.09835547821323853`，ΔPSNR=`1.578050093773296`，ΔUCIQE=`0.06798007171380216`，ΔUIQM=`-4.307617887714276`
- Final 回退：ΔMS-SSIM=`0.05182853606143023`，ΔPSNR=`0.7310886944707455`，ΔUCIQE=`0.08022506582171562`，ΔUIQM=`-4.099832650152848`

## CLAHE

- 状态：`completed`
- 排序：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\scores\clahe_official\ranked.json`
- Final 回退检查：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\scores\clahe_final_backstop\ranked.json`
- winner：`clahe_s05`
- 参数文件：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\configs\clahe\clahe_s05.json`
- 官方胜出：ΔMS-SSIM=`0.03508339760449575`，ΔPSNR=`0.7239718524878036`，ΔUCIQE=`0.022733694803808824`，ΔUIQM=`-1.119371862401362`
- Final 回退：ΔMS-SSIM=`0.05301789895230136`，ΔPSNR=`0.7172492078205828`，ΔUCIQE=`0.0912767365398146`，ΔUIQM=`-4.111068278086655`

## FUSION

- 状态：`completed`
- 排序：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\scores\fusion_final\ranked.json`
- Final 回退检查：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\scores\fusion_final\ranked.json`
- winner：`fusion_s10`
- 参数文件：`D:\Desktop\Stage1Codex\experiments\h2-full506-direct\configs\fusion\fusion_s10.json`
- 官方胜出：ΔMS-SSIM=`0.06751017078109411`，ΔPSNR=`1.436174225745912`，ΔUCIQE=`-0.6234540835670801`，ΔUIQM=`-5.033166729304039`
- Final 回退：ΔMS-SSIM=`0.06751017078109411`，ΔPSNR=`1.436174225745912`，ΔUCIQE=`-0.6234540835670801`，ΔUIQM=`-5.033166729304039`
