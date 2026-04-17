# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import re
from pathlib import Path
from textwrap import dedent

EXPORT_DATE = "2026-04-17"
ROOT_TITLE = "水下图像增强项目主页"
ROOT_URL = "https://www.notion.so/344bb1f4e23e8190a24adc78e66587ff"
REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_ROOT = REPO_ROOT / "notion_mirror"
HOME_DIR = EXPORT_ROOT / ROOT_TITLE


def clean(text: str) -> str:
    return dedent(text).strip() + "\n"


def safe_component(name: str, max_length: int = 80) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    if len(name) > max_length:
        name = name[:max_length].rstrip(" .")
    return name or "untitled"


def page_filename(page: dict[str, object]) -> str:
    short_id = str(page["id"]).split("-")[0]
    return f"{safe_component(str(page['title']))} [{short_id}].md"


def rel(from_path: Path, to_path: Path) -> str:
    return Path(os.path.relpath(to_path, from_path.parent)).as_posix()


def format_value(value: object) -> str:
    if value in (None, ""):
        return "(empty)"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else "(empty)"
    return str(value)


def render_properties(props: dict[str, object]) -> str:
    return "\n".join(f"- **{k}**: {format_value(v)}" for k, v in props.items()) or "- (none)"


def read_body(page: dict[str, object]) -> str:
    if page.get("body_file"):
        return (REPO_ROOT / str(page["body_file"])) .read_text(encoding="utf-8").strip()
    body = str(page.get("body", "")).strip()
    return body or "_This Notion page had no body content._"


def render_page(page: dict[str, object], ancestor: str) -> str:
    body = read_body(page)
    properties = render_properties(page['properties'])
    return clean(
        f"""
# {page['title']}

- **Notion URL**: {page['url']}
- **Ancestor Path**: {ancestor}
- **Exported On**: {EXPORT_DATE}

## Properties
{properties}

## Content
{body}
"""
    )


def notion_url(page_id: str) -> str:
    return f"https://www.notion.so/{page_id.replace('-', '')}"


DATABASES = [
    {
        "name": "文献库",
        "url": "https://www.notion.so/2faaeb5ec59b4369a2368547e6ba5fa2",
        "data_source_url": "collection://75a0fea5-a117-4c22-9057-2f583650e048",
        "view_url": "https://www.notion.so/2faaeb5ec59b4369a2368547e6ba5fa2?v=0c544e6dfa0242f2959aadf17b2f93ae",
        "schema": [
            "论文标题: title",
            "Bucket: select (同方向师兄 / 对比方法)",
            "Concepts: multi_select (wavelet, histogram, multi-scale, white-balance, color-compensation, retinex, semantic-guidance, transformer, hab-microscopy)",
            "DOI: text",
            "Method Family: select (传统融合 / 物理先验 / Retinex/优化 / 深度学习 / Transformer / 白平衡 / 混合方法)",
            "PDF Link: url",
            "Status: select (待读 / 关键基线 / 已写入 related work)",
            "Summary: text",
            "Venue: text",
            "Zotero Key: text",
            "年份: number",
            "被引用笔记: relation -> 研究笔记",
        ],
        "items": [
            {"id": "344bb1f4-e23e-8120-b865-f97f8f565e70", "title": "Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion", "url": notion_url("344bb1f4-e23e-8120-b865-f97f8f565e70"), "properties": {"Bucket": "对比方法", "DOI": "10.1109/TCSVT.2023.3336518", "Method Family": "传统融合", "Status": "关键基线", "Summary": "结合衰减感知颜色校正和加权小波视觉感知融合的传统增强方法。", "Venue": "IEEE Transactions on Circuits and Systems for Video Technology", "Zotero Key": "U6DBLZMV", "年份": 2024, "论文标题": "Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion"}},
            {"id": "344bb1f4-e23e-8125-9531-d33c2c1a0f44", "title": "SGUIE-Net: Semantic Attention Guided Underwater Image Enhancement With Multi-Scale Perception", "url": notion_url("344bb1f4-e23e-8125-9531-d33c2c1a0f44"), "properties": {"Bucket": "对比方法", "DOI": "10.1109/TIP.2022.3216208", "Method Family": "深度学习", "Status": "关键基线", "Summary": "以语义注意力和多尺度感知为核心的深度水下增强网络。", "Venue": "IEEE Transactions on Image Processing", "Zotero Key": "P4E22T2E", "年份": 2022, "论文标题": "SGUIE-Net: Semantic Attention Guided Underwater Image Enhancement With Multi-Scale Perception"}},
            {"id": "344bb1f4-e23e-812e-a60f-d4e9965cd80b", "title": "ABC-Former: Auxiliary Bimodal Cross-domain Transformer with Interactive Channel Attention for White Balance", "url": notion_url("344bb1f4-e23e-812e-a60f-d4e9965cd80b"), "properties": {"Bucket": "对比方法", "DOI": "10.1109/CVPR52734.2025.01980", "Method Family": "白平衡", "Status": "已写入 related work", "Summary": "联合直方图与图像输入的白平衡 Transformer，可为颜色校正建模提供借鉴。", "Venue": "CVPR 2025", "Zotero Key": "LF9HP7DR", "年份": 2025, "论文标题": "ABC-Former: Auxiliary Bimodal Cross-domain Transformer with Interactive Channel Attention for White Balance"}},
            {"id": "344bb1f4-e23e-815b-bc05-fe4ea42f7590", "title": "HVDualformer: Histogram-Vision Dual Transformer for White Balance", "url": notion_url("344bb1f4-e23e-815b-bc05-fe4ea42f7590"), "properties": {"Bucket": "对比方法", "DOI": "10.1609/aaai.v39i6.32697", "Method Family": "白平衡", "Status": "已写入 related work", "Summary": "通过 histogram-vision dual transformer 建模白平衡校正过程的参考工作。", "Venue": "AAAI 2025", "Zotero Key": "TEKJDF6M", "年份": 2025, "论文标题": "HVDualformer: Histogram-Vision Dual Transformer for White Balance"}},
            {"id": "344bb1f4-e23e-8182-9bf4-ebeca95bd466", "title": "Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion", "url": notion_url("344bb1f4-e23e-8182-9bf4-ebeca95bd466"), "properties": {"Bucket": "同方向师兄", "DOI": "10.1007/s11042-023-17410-y", "Method Family": "传统融合", "Status": "已写入 related work", "Summary": "将循环颜色补偿与多尺度融合结合，用于 HAB 显微图像增强和下游验证。", "Venue": "Multimedia Tools and Applications", "Zotero Key": "GS2RFTEL", "年份": 2023, "论文标题": "Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion"}},
            {"id": "344bb1f4-e23e-8189-9d12-ce678091ef4b", "title": "Generalization of the Dark Channel Prior for Single Image Restoration", "url": notion_url("344bb1f4-e23e-8189-9d12-ce678091ef4b"), "properties": {"Bucket": "对比方法", "DOI": "10.1109/TIP.2018.2813092", "Method Family": "物理先验", "Status": "关键基线", "Summary": "基于广义暗通道先验和成像模型的恢复方法，代表物理先验路线。", "Venue": "IEEE Transactions on Image Processing", "Zotero Key": "V87JDUST", "年份": 2018, "论文标题": "Generalization of the Dark Channel Prior for Single Image Restoration"}},
            {"id": "344bb1f4-e23e-8191-9763-f1f5d80016f7", "title": "Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy", "url": notion_url("344bb1f4-e23e-8191-9763-f1f5d80016f7"), "properties": {"Bucket": "同方向师兄", "DOI": "10.1016/j.imavis.2025.105466", "Method Family": "混合方法", "Status": "已写入 related work", "Summary": "结合自适应白平衡颜色补偿、注意力引导和金字塔融合的 HAB 显微增强方法。", "Venue": "Image and Vision Computing", "Zotero Key": "LTE9U599", "年份": 2025, "论文标题": "Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy"}},
            {"id": "344bb1f4-e23e-81a7-a56f-c5c7d3a8c4df", "title": "Histoformer: Histogram-Based Transformer for Efficient Underwater Image Enhancement", "url": notion_url("344bb1f4-e23e-81a7-a56f-c5c7d3a8c4df"), "properties": {"Bucket": "对比方法", "DOI": "10.1109/JOE.2024.3474919", "Method Family": "Transformer", "Status": "关键基线", "Summary": "通过直方图分布学习和 Transformer 建模实现高效水下图像增强。", "Venue": "IEEE Journal of Oceanic Engineering", "Zotero Key": "V5H7FQTY", "年份": 2025, "论文标题": "Histoformer: Histogram-Based Transformer for Efficient Underwater Image Enhancement"}},
            {"id": "344bb1f4-e23e-81c9-b52c-e3a4a70fc551", "title": "Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion", "url": notion_url("344bb1f4-e23e-81c9-b52c-e3a4a70fc551"), "properties": {"Bucket": "同方向师兄", "DOI": "10.1007/s10489-023-04502-x", "Method Family": "传统融合", "Status": "已写入 related work", "Summary": "面向 HAB 显微图像的早期分解融合路线，使用经验模态分解和小波融合。", "Venue": "Applied Intelligence", "Zotero Key": "DQIVG34J", "年份": 2023, "论文标题": "Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion"}},
            {"id": "344bb1f4-e23e-81cb-afdd-cec60c6b09b2", "title": "Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors", "url": notion_url("344bb1f4-e23e-81cb-afdd-cec60c6b09b2"), "properties": {"Bucket": "对比方法", "DOI": "10.1109/TIP.2022.3196546", "Method Family": "Retinex/优化", "Status": "关键基线", "Summary": "通过高阶反射先验与 Retinex 变分建模恢复细节和自然颜色。", "Venue": "IEEE Transactions on Image Processing", "Zotero Key": "PWKRPBPJ", "年份": 2022, "论文标题": "Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors"}},
            {"id": "344bb1f4-e23e-81d8-9e82-e7b9cadd23be", "title": "Color Balance and Fusion for Underwater Image Enhancement", "url": notion_url("344bb1f4-e23e-81d8-9e82-e7b9cadd23be"), "properties": {"Bucket": "对比方法", "DOI": "10.1109/TIP.2017.2759252", "Method Family": "传统融合", "Status": "关键基线", "Summary": "经典单幅水下增强方法，结合颜色平衡、白平衡和多尺度融合。", "Venue": "IEEE Transactions on Image Processing", "Zotero Key": "AFLVZ4KR", "年份": 2018, "论文标题": "Color Balance and Fusion for Underwater Image Enhancement"}},
        ],
    },
    {
        "name": "研究笔记",
        "url": "https://www.notion.so/877b9d99392b4561855f33f1e418c550",
        "data_source_url": "collection://2d7ffbcc-19ff-4fe2-a8fc-e8138f2542f1",
        "view_url": "https://www.notion.so/877b9d99392b4561855f33f1e418c550?v=9f00ee9c086544f787eef1b6ebf0074c",
        "schema": [
            "标题: title", "关联文献: relation -> 文献库", "摘要: text", "日期: date", "标签: multi_select (enhancement, edge, fusion, ablation, writing)", "状态: select (草稿 / 整理中 / 完成)", "类型: select (论文笔记 / 方法想法 / 阶段总结 / 问题记录)"
        ],
        "items": [
            {"id": "344bb1f4-e23e-8175-8d65-e0d57bc1e5b3", "title": "阶段命名与模块速查", "url": notion_url("344bb1f4-e23e-8175-8d65-e0d57bc1e5b3"), "properties": {"日期": "2026-04-17", "摘要": "整理 README 中七阶段流水线的真实功能、历史命名和调参关注点，便于论文写作和协作沟通。", "标题": "阶段命名与模块速查", "状态": "完成", "类型": "阶段总结"}, "body": clean("""
## 七阶段主线
`Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`
## 各阶段真实职责
- `BPH`：前置白平衡，负责把偏色和通道失衡拉回稳定起点
- `IMF1Ray`：基于 IMF1 + Rayleigh 的高频细节增强分支
- `RGHS`：历史名 `RGHS`，当前真实功能是白平衡安全对比增强分支
- `CLAHE`：历史名 `CLAHE`，当前真实功能是 CLAHE 引导的局部可见性增强分支
- `Fused`：三分支融合结果
- `Final`：后处理细化后的最终输出
## 命名说明
当前仓库里保留了两套并行名字：
- 历史阶段名，用在结果目录、配置字段和实验记录里，方便兼容旧资产
- 真实功能描述，用来帮助理解模块实际作用
已完成的文件层重命名包括：
- `RGHS.py` 的主实现已经转移到 `wb_safe_contrast.py`
- `CLAHE.py` 的主实现已经转移到 `clahe_guided_visibility.py`
但阶段名 `RGHS / CLAHE` 仍在结果目录、配置字段和实验记录中继续保留。
## 调参时的理解
- `BPH` 负责先把颜色拉回可控区间，不适合承担全部观感增强压力
- `IMF1Ray / RGHS / CLAHE` 更适合各司其职，不应指望某一条单独解决所有问题
- `Fused` 是分工协调层，重点在于不同分支在哪些区域和频段发言
- `Final` 是收口层，优先做温和整理，而不是去硬救上游问题
""")},
            {"id": "344bb1f4-e23e-813d-9cc4-fdd155d8a463", "title": "项目现状与关键发现（2026-04-17）", "url": notion_url("344bb1f4-e23e-813d-9cc4-fdd155d8a463"), "properties": {"日期": "2026-04-17", "摘要": "总结当前仓库的方法定位、关键结果、最强叙事和未决问题。", "标题": "项目现状与关键发现（2026-04-17）", "状态": "完成", "类型": "阶段总结"}, "body": clean("""
## 研究问题
How can we strengthen underwater harmful algal bloom microscopic image enhancement so that color recovery, fine texture visibility, and downstream edge extractability all improve in a measurable and publishable way?
## 当前理解
当前仓库已经形成一条完整增强链路，而不是几个松散滤波器的堆叠。主线可以概括为：任务相关的白平衡与颜色补偿、三个互补增强分支、特征门控多分支融合，以及最终照明细化。
当前项目最有说服力的科学区分点，不在于单独使用 EMD、CLAHE 或 RGHS，而在于如何针对 HAB 显微图像组织这些模块，并让增强结果服务于下游边缘可提取性。
## 核心结果
- 当前增强工作流已经在仓库中完整实现并可运行。
- 现有指标日志显示方法在若干无参考质量指标和下游友好指标上表现较强，但不同文件使用的数据子集还不完全一致，正式论文前仍需统一协议。
- 现有参考文献支持“增强提升边缘检测与结构感知”这一论证路径。
- 目前最强的论文叙事是：增强方法本身 + 下游边缘验证，而不是同时宣称一个完全成熟的新边缘网络。
## 当前最强叙事
- 白平衡阶段已经比公开参考方法更项目化。
- 三分支特征门控融合是最清楚的代码级创新点。
- 整个项目更像一篇面向 HAB 显微图像的增强论文，而不是一篇泛泛的图像增强论文。
## 当前约束
- 论文不能直接继承参考论文的表述，因为当前代码和公开方法已经有实质差异。
- 现有指标不能直接作为终版论文表格，需要在锁定协议下重跑。
- IMF1/EMD 是当前最昂贵的运行瓶颈，实验计划需要显式考虑这一点。
## 未决问题
- 最终主指标组合应该如何锁定？
- 实际提升里，IMF1 分支、门控融合和白平衡改造各自贡献有多大？
- 第一篇论文的下游验证更适合走经典边缘/SIFT 路线，还是神经边缘基线路线？
""")},
            {"id": "344bb1f4-e23e-8159-9d42-e7cdc36942fc", "title": "主线方法与假设框架", "url": notion_url("344bb1f4-e23e-8159-9d42-e7cdc36942fc"), "properties": {"日期": "2026-04-17", "摘要": "梳理当前七阶段增强流水线、H1-H3 假设以及 H2→H1→H3 的实验优先级。", "标题": "主线方法与假设框架", "状态": "完成", "类型": "方法想法"}, "body": clean("""
## 当前主线方法
当前项目已经对齐为一条七阶段增强流水线：
1. 改进的灰像素引导白平衡
2. IMF1Ray 细节分支
3. RGHS 对比分支
4. CLAHE 分支
5. 特征门控三分支融合
6. 同态照明细化
7. 面向边缘可读性的下游验证
## 三个核心假设
### H1
Gray-pixel-guided pre-white-balance plus clipped ACCC yields more stable color recovery and better downstream edge extractability than plain cyclic compensation.
### H2
The three-branch IMF1Ray/RGHS/CLAHE feature-gated fusion produces better edge-visible enhancement than any single branch or naive equal-weight fusion.
### H3
L-channel homomorphic refinement improves illumination uniformity and final edge readability, but should be treated as a refinement module rather than the main innovation.
## 为什么优先做 H2
当前最值得先打实的并不是白平衡，而是融合：
- H2 直接对应项目最清楚的代码级创新点
- H2 的实验可控性更强，更适合先形成第一轮可发表证据
- H3 更像辅助细化，不适合被过度声明为核心贡献
## 锁定评测设定
- pilot 子集：`pilot92-v1`
- 正式全量：`full506-original-v1`
- 当前主评估强调结构与边缘友好指标，而不是纯 PSNR 叙事
## 当前优先级
1. H2
2. H1
3. H3
""")},
            {"id": "344bb1f4-e23e-8136-ad07-d45f9b3caf32", "title": "水下图像增强文献对比表", "url": notion_url("344bb1f4-e23e-8136-ad07-d45f9b3caf32"), "properties": {"日期": "2026-04-17", "摘要": "整理当前 11 篇核心论文的分组、核心思路、价值和使用边界。", "标题": "水下图像增强文献对比表", "状态": "完成", "类型": "论文笔记"}, "body": clean("""
这份笔记整理当前项目最核心的 11 篇论文，用于 baseline 选择和 related work 写作。
<table fit-page-width="true" header-row="true">
<tr><td>Paper</td><td>Bucket</td><td>Core idea</td><td>Main use</td></tr>
<tr><td>Color Balance and Fusion for Underwater Image Enhancement</td><td>对比方法</td><td>颜色平衡 + 白平衡 + 多尺度融合</td><td>经典传统融合基线</td></tr>
<tr><td>Generalization of the Dark Channel Prior for Single Image Restoration</td><td>对比方法</td><td>广义暗通道先验 + 成像模型恢复</td><td>物理先验路线代表</td></tr>
<tr><td>Underwater Image Enhancement With Hyper-Laplacian Reflectance Priors</td><td>对比方法</td><td>Retinex 变分建模 + 反射先验</td><td>优化模型基线</td></tr>
<tr><td>Underwater Image Enhancement via Weighted Wavelet Visual Perception Fusion</td><td>对比方法</td><td>衰减感知校正 + 小波视觉感知融合</td><td>现代传统融合基线</td></tr>
<tr><td>Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion</td><td>同方向师兄</td><td>经验模态分解 + 小波融合</td><td>HAB 方向早期分解融合脉络</td></tr>
<tr><td>Underwater enhancement computing of ocean HABs based on cyclic color compensation and multi-scale fusion</td><td>同方向师兄</td><td>循环颜色补偿 + 多尺度融合</td><td>HAB 方向历史基线</td></tr>
<tr><td>Innovative underwater image enhancement algorithm: Combined application of adaptive white balance color compensation and pyramid image fusion to submarine algal microscopy</td><td>同方向师兄</td><td>自适应白平衡 + 注意力引导 + 金字塔融合</td><td>最接近当前项目的结构参考</td></tr>
<tr><td>SGUIE-Net: Semantic Attention Guided Underwater Image Enhancement With Multi-Scale Perception</td><td>对比方法</td><td>语义注意力 + 多尺度感知</td><td>深度学习增强代表</td></tr>
<tr><td>Histoformer: Histogram-Based Transformer for Efficient Underwater Image Enhancement</td><td>对比方法</td><td>直方图分布学习 + Transformer</td><td>现代 Transformer 基线</td></tr>
<tr><td>ABC-Former: Auxiliary Bimodal Cross-domain Transformer with Interactive Channel Attention for White Balance</td><td>对比方法</td><td>双模态直方图与图像建模 + 通道注意力</td><td>白平衡与颜色建模参考</td></tr>
<tr><td>HVDualformer: Histogram-Vision Dual Transformer for White Balance</td><td>对比方法</td><td>Histogram-vision dual transformer</td><td>白平衡与统计建模参考</td></tr>
</table>
## 推荐写作分组
- 传统方法：AFLVZ4KR, V87JDUST, PWKRPBPJ, U6DBLZMV
- HAB 显微方向：DQIVG34J, GS2RFTEL, LTE9U599
- 深度增强：P4E22T2E, V5H7FQTY
- 对比方法（白平衡参考）：LF9HP7DR, TEKJDF6M
""")},
        ],
    },
    {
        "name": "实验记录",
        "url": "https://www.notion.so/0d00e7c7cbc64d5c8dd9e1f6ee6b22b1",
        "data_source_url": "collection://b8182f16-5ee8-4c2a-8d8c-e6546686f04f",
        "view_url": "https://www.notion.so/0d00e7c7cbc64d5c8dd9e1f6ee6b22b1?v=9b4c93f63b664b9ca792865a2da196dd",
        "schema": ["实验名称: title", "关联文献: relation -> 文献库", "日期: date", "状态: select (待运行 / 运行中 / 已完成 / 需复查)", "结果摘要: text", "配置路径: text", "阶段: select (预实验 / 主实验 / 消融 / 可视化 / 失败记录)"],
        "items": [
            {"id": "344bb1f4-e23e-81ba-8fbc-da37b35b47b6", "title": "optimization_v1 full506 后处理搜索与主线锁定", "url": notion_url("344bb1f4-e23e-81ba-8fbc-da37b35b47b6"), "properties": {"配置路径": "experiments/optimization_v1/configs/best_full506_r4_03.json ; experiments/optimization_v1/configs/locked_full506_mainline.json", "结果摘要": "在 full506 上完成四轮后处理/融合细化搜索后，选出 r4_03 作为当前 full506 指标最优配置；随后将 H1 的白平衡 winner 与 r4_03 组合锁定为 locked_full506_mainline.json。", "阶段": "主实验", "状态": "已完成", "日期": "2026-04-13", "实验名称": "optimization_v1 full506 后处理搜索与主线锁定"}, "body": clean("""
## 结果概览
- 数据规模：506 / 506 complete-case
- 失败数：0
- 当前最优后处理：`r4_03`
- 当前锁定主线：`locked_full506_mainline.json`
## 锁定理由
在 full506 上完成四轮后处理/融合细化搜索后，`r4_03` 在当前指标组合下表现最好，因此被选为当前主线的后处理 winner。随后将 H1 的白平衡 winner 与 `r4_03` 组合，锁定为 `locked_full506_mainline.json`。
## 关键路径
- 最优配置：`experiments/optimization_v1/configs/best_full506_r4_03.json`
- 主线锁定：`experiments/optimization_v1/configs/locked_full506_mainline.json`
""")},
            {"id": "344bb1f4-e23e-8123-9f82-e1ef8343f86c", "title": "H1 白平衡 full506 正式实验", "url": notion_url("344bb1f4-e23e-8123-9f82-e1ef8343f86c"), "properties": {"配置路径": "experiments/h1-graypixel-bph-ablation/outputs/full506 ; experiments/optimization_v1/configs/locked_full506_mainline.json", "结果摘要": "full506 四套白平衡方法全部完成 506/506 complete-case 评测、零失败；自动 metric winner 为 r2_02_G_P，人工最终锁定 r2_05_G_P_A_B 作为正式上游白平衡胜者。", "阶段": "主实验", "状态": "已完成", "日期": "2026-04-15", "实验名称": "H1 白平衡 full506 正式实验"}, "body": clean("""
## 结果概览
- 数据规模：506 / 506 complete-case
- 失败数：0
- 自动 metric winner：`r2_02_G_P`
- 人工最终锁定：`r2_05_G_P_A_B`
## 锁定理由
在保留自动评测结果的同时，人工最终将 `r2_05_G_P_A_B` 锁定为正式胜者。理由是：它相对 `r2_00_baseline` 同时提升了 `MS-SSIM` 与 `PSNR`，且在“双增”候选中综合分回撤最小，更适合作为稳健的前置白平衡方案。
## 关键路径
- 输出目录：`experiments/h1-graypixel-bph-ablation/outputs/full506`
- 主线锁定配置：`experiments/optimization_v1/configs/locked_full506_mainline.json`
""")},
            {"id": "344bb1f4-e23e-8154-a98b-ca37f9ee96a3", "title": "H2 RGHS/CLAHE/Fusion 顺序优化", "url": notion_url("344bb1f4-e23e-8154-a98b-ca37f9ee96a3"), "properties": {"配置路径": "experiments/h2-full506-direct/analysis.md ; experiments/optimization_v1/configs/locked_full506_final_mainline.json", "结果摘要": "H2 full506 直跑调参已完成；当前接受 winner 为 RGHS=rghs_s07、CLAHE=clahe_s05、Fusion=fusion_s10，并已固化为 locked_full506_final_mainline.json。", "阶段": "消融", "状态": "已完成", "日期": "2026-04-16", "实验名称": "H2 RGHS/CLAHE/Fusion 顺序优化"}, "body": clean("""
# H2 full506 直跑调参
## 当前状态
- 总状态：`completed`
- 基线配置：`experiments/optimization_v1/configs/locked_full506_mainline.json`
- 当前接受统一配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
- 当前正式结果目录：`experiments/h2-full506-direct/outputs/full506/runs/full506_final_mainline`
- 当前正式评测目录：`experiments/h2-full506-direct/outputs/full506/eval`
## 当前接受 winner
- `RGHS = rghs_s07`
- `CLAHE = clahe_s05`
- `Fusion = fusion_s10`
## 阶段结论
### RGHS
- winner：`rghs_s07`
- 参数文件：`experiments/h2-full506-direct/configs/rghs/rghs_s07.json`
- 官方胜出：ΔMS-SSIM=`0.09836`，ΔPSNR=`1.57805 dB`，ΔUCIQE=`0.06798`，ΔUIQM=`-4.30762`
### CLAHE
- winner：`clahe_s05`
- 参数文件：`experiments/h2-full506-direct/configs/clahe/clahe_s05.json`
- 官方胜出：ΔMS-SSIM=`0.03508`，ΔPSNR=`0.72397 dB`，ΔUCIQE=`0.02273`，ΔUIQM=`-1.11937`
### FUSION
- winner：`fusion_s10`
- 参数文件：`experiments/h2-full506-direct/configs/fusion/fusion_s10.json`
- 官方胜出：ΔMS-SSIM=`0.06751`，ΔPSNR=`1.43617 dB`，但 `UCIQE / UIQM` 出现明显回撤
## 当前解释
当前 H2 的结论不是三层联调，而是在固定上游 `BPH / IMF1Ray` 的前提下做顺序优化：先选 `RGHS`，再选 `CLAHE`，最后选 `Fusion`。其中 `fusion_s10` 在结构相关指标上提升明显，但视觉项回撤较大，因此如果后续继续开 H2，最优先重开的应当是 Fusion 阶段，并把视觉项退化纳入更强硬的护栏。
## 关键文件
- 分析文档：`experiments/h2-full506-direct/analysis.md`
- 最终状态：`experiments/h2-full506-direct/selection.json`
- 主线锁定配置：`experiments/optimization_v1/configs/locked_full506_final_mainline.json`
""")},
        ],
    },
    {
        "name": "任务计划",
        "url": "https://www.notion.so/614efab7ebc54c49a22e0b66715e0791",
        "data_source_url": "collection://c7d20675-db3f-419a-a456-ab5435b90fee",
        "view_url": "https://www.notion.so/614efab7ebc54c49a22e0b66715e0791?v=9bb7264360ec4198a8c1e661aa9e26be",
        "schema": ["任务: title", "优先级: select (高 / 中 / 低)", "关联文献: relation -> 文献库", "备注: text", "截止日期: date", "状态: status (未开始 / 进行中 / 完成)"],
        "items": [
            {"id": "344bb1f4-e23e-811c-b7ac-fdc12ebf52c4", "title": "重开 Fusion 调参并加入视觉护栏", "url": notion_url("344bb1f4-e23e-811c-b7ac-fdc12ebf52c4"), "properties": {"任务": "重开 Fusion 调参并加入视觉护栏", "优先级": "高", "备注": "当前 fusion_s10 在结构指标上提升明显，但 UCIQE / UIQM 回撤过大。下一轮应明确把视觉项退化纳入硬约束或 guardrail。", "状态": "未开始"}},
            {"id": "344bb1f4-e23e-819e-a242-e96de0579c4f", "title": "完成 H2 的 Fusion pilot 并决定是否进入 full506", "url": notion_url("344bb1f4-e23e-819e-a242-e96de0579c4f"), "properties": {"任务": "完成 H2 的 Fusion pilot 并决定是否进入 full506", "优先级": "高", "备注": "Fusion 阶段 winner 已锁定为 fusion_s10，并已决定进入当前接受的 full506 主线，但后续仍建议重开并加入更强视觉护栏。", "状态": "完成"}},
            {"id": "344bb1f4-e23e-81a0-a195-e884bc150a85", "title": "完成 H2 的 CLAHE pilot 与排序", "url": notion_url("344bb1f4-e23e-81a0-a195-e884bc150a85"), "properties": {"任务": "完成 H2 的 CLAHE pilot 与排序", "优先级": "高", "备注": "CLAHE 阶段 winner 已锁定为 clahe_s05，相关 full506 直跑结果已整理入实验记录。", "状态": "完成"}},
            {"id": "344bb1f4-e23e-81be-b1a8-f3a84b379b30", "title": "锁定论文主指标组合与正式表格协议", "url": notion_url("344bb1f4-e23e-81be-b1a8-f3a84b379b30"), "properties": {"任务": "锁定论文主指标组合与正式表格协议", "优先级": "中", "备注": "在 paper 前冻结 primary / secondary metrics、统一 PNG 协议和最终表格口径。", "状态": "未开始"}},
            {"id": "344bb1f4-e23e-815e-8f90-e49252e777b2", "title": "把实验记录逐步迁入 Notion", "url": notion_url("344bb1f4-e23e-815e-8f90-e49252e777b2"), "properties": {"任务": "把实验记录逐步迁入 Notion", "优先级": "高", "备注": "优先迁入关键实验、消融和失败记录，保持与本地仓库版本同步。", "状态": "未开始"}},
            {"id": "344bb1f4-e23e-81a5-84f0-d3731b8c8b23", "title": "补齐文献库 Concepts 标签", "url": notion_url("344bb1f4-e23e-81a5-84f0-d3731b8c8b23"), "properties": {"任务": "补齐文献库 Concepts 标签", "优先级": "中", "备注": "Notion API 对 multi-select 批量写入比较挑，后续单独补齐 wavelet / histogram / multi-scale / white-balance 等概念标签。", "状态": "未开始"}},
        ],
    },
    {
        "name": "论文写作",
        "url": "https://www.notion.so/100c78dba4dc43a49823e6ab76cc4e07",
        "data_source_url": "collection://0a07c42c-b54a-4279-a8b8-b34dcfd3d356",
        "view_url": "https://www.notion.so/100c78dba4dc43a49823e6ab76cc4e07?v=5dccda7e7131445a8bb77880c1fa3470",
        "schema": ["条目: title", "关联文献: relation -> 文献库", "内容摘要: text", "截止日期: date", "状态: select (待写 / 草稿中 / 已完成)", "类型: select (related work / method / experiment / figure / todo)"],
        "items": [
            {"id": "344bb1f4-e23e-811e-8cd5-c5b5c9c29102", "title": "水下图像增强 方法总览图初稿", "url": notion_url("344bb1f4-e23e-811e-8cd5-c5b5c9c29102"), "properties": {"内容摘要": "已生成方法总览图的 Mermaid 源文件及 SVG/PNG 初稿，当前本地文件位于 paper/figures/underwater_method_overview.mmd、.svg、.png，可直接继续微调布局、文案和图中示例图。", "条目": "水下图像增强 方法总览图初稿", "状态": "草稿中", "类型": "figure"}, "body": clean("""
## 当前产物
- Mermaid 源文件：`D:\\Desktop\\Stage1Codex\\paper\\figures\\underwater_method_overview.mmd`
- SVG 导出：`D:\\Desktop\\Stage1Codex\\paper\\figures\\underwater_method_overview.svg`
- PNG 预览：`D:\\Desktop\\Stage1Codex\\paper\\figures\\underwater_method_overview.png`
## 当前图的结构
主链采用：
`Input -> Pre-White-Balance -> {Detail, Contrast, Visibility} -> Fusion -> Refinement -> Output`
并从 `Output` 用虚线连接到：
`Downstream Edge-Oriented Validation`
## 当前图中强调的点
- 方法是分阶段增强框架；
- 三条中间分支职责互补，而不是三张相似增强图；
- `Feature-Gated Three-Branch Fusion` 是结构中心；
- `Final` 是轻量收口，不是主要创新承载点；
- 下游边缘验证是任务化评估路径，而不是增强算子的一部分。
## 当前图注
### 中文图注
`图 X. 本文提出的分阶段增强框架总览。输入图像首先经过灰像素引导的前置白平衡模块，以稳定颜色起点；随后，从白平衡结果并行生成 IMF1-Rayleigh 高频细节分支、白平衡安全对比分支和 CLAHE 引导的局部可见性分支；三条分支在亮度空间中通过特征门控的拉普拉斯金字塔融合进行协同整合，并经过轻量照明与对比收口得到最终输出。下游边缘友好验证作为任务化评估路径单独呈现，不属于增强算子本体。`
### English caption
`Fig. X. Overview of the proposed stage-wise enhancement framework. The input image is first stabilized by a gray-pixel-guided pre-white-balance module. Three complementary branches are then constructed for IMF1-Rayleigh detail recovery, white-balance-safe contrast enhancement, and CLAHE-guided local visibility compensation. Their outputs are integrated by feature-gated Laplacian-pyramid fusion in the luminance domain, followed by lightweight illumination and contrast refinement. Downstream edge-oriented validation is presented as a task-facing evaluation path rather than part of the enhancement operator itself.`
## 还可继续打磨的点
- 将 `Input` 和 `Output` 替换成真实样例图缩略图；
- 调整各分支框中文字密度，使论文版更紧凑；
- 如需投幻灯片版本，可改成更宽的横向链式布局；
- 之后可将该图直接嵌入论文主稿。
## 关联说明
更完整的布局原则、节点命名和引用句说明见：`水下图像增强 方法总览图说明`。
""")},
            {"id": "344bb1f4-e23e-8169-a234-efde00a8a703", "title": "水下图像增强 方法总览图说明", "url": notion_url("344bb1f4-e23e-8169-a234-efde00a8a703"), "properties": {"内容摘要": "整理方法总览图的结构布局、节点命名、图中应展示与应避免暗示的内容、图注草稿和正文引用句；对应本地主文件为仓库根目录下的 method-figure-underwater-enhancement.md。", "条目": "水下图像增强 方法总览图说明", "状态": "草稿中", "类型": "figure"}, "body_file": "method-figure-underwater-enhancement.md"},
            {"id": "344bb1f4-e23e-8149-bd61-c0a4d25cf894", "title": "水下图像增强 method section 精简稿", "url": notion_url("344bb1f4-e23e-8149-bd61-c0a4d25cf894"), "properties": {"内容摘要": "将 method 说明稿进一步压成更接近论文成稿的版本，包含正式的 3 Method 小节结构、英文骨架、图注草稿和实验过渡句；对应本地主文件为仓库根目录下的 method-underwater-enhancement-paper-ready.md。", "条目": "水下图像增强 method section 精简稿", "状态": "草稿中", "类型": "method"}, "body_file": "method-underwater-enhancement-paper-ready.md"},
            {"id": "344bb1f4-e23e-81d7-952a-fa49b59827c1", "title": "水下图像增强 method section 草稿", "url": notion_url("344bb1f4-e23e-81d7-952a-fa49b59827c1"), "properties": {"内容摘要": "基于当前仓库真实实现整理一版 method section 草稿，覆盖灰像素引导白平衡、IMF1Ray 细节分支、白平衡安全对比分支、CLAHE 引导局部可见性分支、特征门控融合与最终收口；对应本地主文件为仓库根目录下的 method-underwater-enhancement.md。", "条目": "水下图像增强 method section 草稿", "状态": "草稿中", "类型": "method"}, "body_file": "method-underwater-enhancement.md"},
            {"id": "344bb1f4-e23e-815c-b020-dc95c392a3d3", "title": "方法命名与七阶段流程说明", "url": notion_url("344bb1f4-e23e-815c-b020-dc95c392a3d3"), "properties": {"内容摘要": "整理 BPH / IMF1Ray / RGHS / CLAHE / Fused / Final 的真实职责、历史命名和论文写法边界，供 method section 复用。", "条目": "方法命名与七阶段流程说明", "状态": "草稿中", "类型": "method"}, "body": clean("""
## 主线流程
`Original -> BPH -> IMF1Ray -> RGHS -> CLAHE -> Fused -> Final`
## 论文写法建议
- `BPH` 写成前置白平衡与颜色校正模块
- `IMF1Ray` 写成高频细节增强分支
- `RGHS` 不建议只沿用历史缩写，更建议描述为白平衡安全对比增强分支
- `CLAHE` 不建议写成普通 CLAHE，而应强调它是 CLAHE 引导的局部可见性增强分支
- `Fused` 写成三分支特征门控融合层
- `Final` 写成后处理照明与对比细化层
## 命名边界
实验记录、结果目录和配置字段可以继续保留历史名 `RGHS / CLAHE`，但论文正文中应优先使用真实功能描述，避免读者误以为这是标准 RGHS 或普通 CLAHE 的直接实现。
## 当前价值
这份说明可以直接服务于：
- method section 的模块介绍
- ablation section 的阶段划分
- README / 报告 / 幻灯片中的统一命名
""")},
            {"id": "344bb1f4-e23e-813d-af65-ea3e3477674d", "title": "水下图像增强 related work 初稿", "url": notion_url("344bb1f4-e23e-813d-af65-ea3e3477674d"), "properties": {"内容摘要": "已完成一版文献对比表、完整版中文相关工作、短版中文和英文骨架，当前主文件保存在本地仓库根目录 related-work-underwater-enhancement.md。", "条目": "水下图像增强 related work 初稿", "状态": "草稿中", "类型": "related work"}, "body_file": "related-work-underwater-enhancement.md"},
        ],
    },
]


def build_lookup() -> dict[str, tuple[Path, dict[str, object], str]]:
    lookup = {}
    for db in DATABASES:
        db_dir = HOME_DIR / str(db["name"])
        for page in db["items"]:
            lookup[str(page["id"])] = (db_dir / page_filename(page), page, str(db["name"]))
    return lookup


def render_root(page_lookup: dict[str, tuple[Path, dict[str, object], str]]) -> str:
    focus_ids = [
        "344bb1f4-e23e-8136-ad07-d45f9b3caf32", "344bb1f4-e23e-813d-af65-ea3e3477674d", "344bb1f4-e23e-81d7-952a-fa49b59827c1", "344bb1f4-e23e-8149-bd61-c0a4d25cf894", "344bb1f4-e23e-8169-a234-efde00a8a703", "344bb1f4-e23e-811e-8cd5-c5b5c9c29102", "344bb1f4-e23e-813d-9cc4-fdd155d8a463", "344bb1f4-e23e-8159-9d42-e7cdc36942fc", "344bb1f4-e23e-8123-9f82-e1ef8343f86c", "344bb1f4-e23e-8154-a98b-ca37f9ee96a3"
    ]
    focus = []
    for page_id in focus_ids:
        path, page, db_name = page_lookup[page_id]
        focus.append(f"- [{page['title']}]({rel(HOME_DIR / 'index.md', path)}) ({db_name})")
    databases = [f"- [{db['name']}]({rel(HOME_DIR / 'index.md', HOME_DIR / str(db['name']) / 'index.md')})" for db in DATABASES]
    focus_text = "\n".join(focus)
    databases_text = "\n".join(databases)
    return clean(
        f"""
# {ROOT_TITLE}

- **Notion URL**: {ROOT_URL}
- **Exported On**: {EXPORT_DATE}

## 页面说明
这个页面用于组织文献、笔记、实验记录、任务计划和论文写作材料。PDF 和引用继续由 Zotero 管理，Notion 重点保存条目、总结、笔记和项目过程。

## 当前重点页面
{focus_text}

## 当前状态
- 文献库已导入 11 篇核心论文
- 已完成一份文献对比表笔记
- 已同步 related work 的中文完整版、中文短版和英文骨架
- 已新增一份与代码实现对齐的 method section 草稿
- 已新增一份更接近论文成稿的 method section 精简稿
- 已新增一份方法总览图说明与图注草稿
- 已导出方法总览图的 Mermaid / SVG / PNG 初稿
- 后续需要补齐 Concepts 标签，并逐步迁入实验记录

## 数据库
{databases_text}
"""
    )


def render_db_index(db: dict[str, object], page_lookup: dict[str, tuple[Path, dict[str, object], str]]) -> str:
    db_dir = HOME_DIR / str(db['name'])
    items = []
    for page in db['items']:
        page_path, _, _ = page_lookup[str(page['id'])]
        extras = []
        for key in ('状态', '类型', '优先级', '阶段', 'Bucket', 'Method Family', '年份'):
            if key in page['properties']:
                extras.append(f"{key}: {page['properties'][key]}")
        suffix = f" — {'; '.join(extras)}" if extras else ""
        items.append(f"- [{page['title']}]({rel(db_dir / 'index.md', page_path)}){suffix}")
    schema = '\n'.join(f"- {line}" for line in db['schema'])
    items_text = "\n".join(items)
    return clean(
        f"""
# {db['name']}

- **Notion Database URL**: {db['url']}
- **Data Source URL**: {db['data_source_url']}
- **Default View URL**: {db['view_url']}
- **Item Count**: {len(db['items'])}
- **Exported On**: {EXPORT_DATE}

## Schema Summary
{schema}

## Items
{items_text}
"""
    )


def main() -> None:
    lookup = build_lookup()
    EXPORT_ROOT.mkdir(exist_ok=True)
    HOME_DIR.mkdir(exist_ok=True)

    (EXPORT_ROOT / 'README.md').write_text(clean(f"""
# Notion Mirror

这个目录保存了 Notion 页面 **{ROOT_TITLE}** 及其子页面的本地 Markdown 镜像，便于后续通过 GitHub 访问。

- **Root Page**: [{ROOT_TITLE}]({ROOT_TITLE}/index.md)
- **Notion URL**: {ROOT_URL}
- **Exported On**: {EXPORT_DATE}
"""), encoding='utf-8')

    (HOME_DIR / 'index.md').write_text(render_root(lookup), encoding='utf-8')

    for db in DATABASES:
        db_dir = HOME_DIR / str(db['name'])
        db_dir.mkdir(exist_ok=True)
        (db_dir / 'index.md').write_text(render_db_index(db, lookup), encoding='utf-8')
        for page in db['items']:
            page_path, page_data, db_name = lookup[str(page['id'])]
            page_path.write_text(render_page(page_data, f"{ROOT_TITLE} / {db_name}"), encoding='utf-8')


if __name__ == '__main__':
    main()
