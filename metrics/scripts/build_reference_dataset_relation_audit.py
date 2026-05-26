from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


THIS_DIR = Path(__file__).resolve().parent
METRICS_DIR = THIS_DIR.parent
PROJECT_ROOT = METRICS_DIR.parent
DEFAULT_DATE = datetime.now().date().strftime("%Y%m%d")
DEFAULT_OUTPUT_MD = PROJECT_ROOT / "docs" / f"reference_dataset_relation_audit_{DEFAULT_DATE}_cn.md"
DEFAULT_OUTPUT_JSON = PROJECT_ROOT / "docs" / f"reference_dataset_relation_audit_{DEFAULT_DATE}_cn.json"

ESWA_ZOTERO_CACHE = Path(r"D:\Zotero\zoteroData\storage\KPT9MVGB\.zotero-ft-cache")
EAAI_ZOTERO_CACHE = Path(r"D:\Zotero\zoteroData\storage\WU7DISPR\.zotero-ft-cache")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a read-only audit for the relationship between the Stage1 full algae image pool "
            "and the two Wu et al. 2026 same-direction HAB references. This script does not run "
            "enhancement, MyEdge sampling, edge evaluation, training, or metric recomputation."
        )
    )
    parser.add_argument("--output-md", default=str(DEFAULT_OUTPUT_MD))
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON))
    return parser.parse_args()


def read_json(path: Path) -> Dict[str, object]:
    if not path.exists():
        return {"_missing": True, "_path": str(path)}
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def manifest_count(path: Path) -> int:
    if not path.exists():
        return 0
    count = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        item = line.strip().lstrip("\ufeff")
        if item and not item.startswith("#"):
            count += 1
    return count


def rel(path: Path, root: Path = PROJECT_ROOT) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def source_ref(path: Path, root: Path = PROJECT_ROOT) -> str:
    suffix = "" if path.exists() else " (missing)"
    return f"`{rel(path, root)}`{suffix}"


def table_escape(value: object) -> str:
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False)
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def has_terms(text: str, terms: Iterable[str]) -> bool:
    low = text.lower()
    return all(term.lower() in low for term in terms)


def verification_status(cache_path: Path, text: str, terms: Sequence[str]) -> str:
    if not cache_path.exists():
        return "zotero_cache_missing"
    if has_terms(text, terms):
        return "verified_in_local_zotero_cache"
    return "cache_present_terms_not_all_found"


def audit_row(
    item_id: str,
    source: str,
    field: str,
    verified_value: object,
    status: str,
    evidence: str,
    usable_wording_cn: str,
    forbidden_wording_cn: str,
    missing_for_submission: str,
    boundary: str,
) -> Dict[str, object]:
    return {
        "item_id": item_id,
        "source": source,
        "field": field,
        "verified_value": verified_value,
        "status": status,
        "evidence": evidence,
        "usable_wording_cn": usable_wording_cn,
        "forbidden_wording_cn": forbidden_wording_cn,
        "missing_for_submission": missing_for_submission,
        "boundary": boundary,
    }


def build_audit() -> Dict[str, object]:
    paths = {
        "inventory_doc": PROJECT_ROOT / "docs" / "full_enhancement_dataset_inventory_cn.md",
        "inventory_audit": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_audit.json",
        "full_manifest": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1.txt",
        "cv2_manifest": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_cv2_readable_candidate.txt",
        "decode_summary": PROJECT_ROOT / "metrics" / "manifests" / "full_algae_dewatermark_v1_decode_audit.summary.json",
        "manual_validation": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "manual_review_validation_status_20260525.json",
        "clean_manifest": PROJECT_ROOT
        / "metrics"
        / "manifests"
        / "full_algae_dewatermark_v1_manual_review"
        / "derived_review_artifacts"
        / "reviewed_cv2_clean_manifest.txt",
        "eswa_note": PROJECT_ROOT / "literature" / "wu2026_eswa_hab_edge_detection.md",
        "eaai_note": PROJECT_ROOT / "literature" / "wu2026_eaai_hab_segmentation.md",
    }

    inventory_audit = read_json(paths["inventory_audit"])
    decode_summary = read_json(paths["decode_summary"])
    manual_validation = read_json(paths["manual_validation"])
    eswa_text = read_text(ESWA_ZOTERO_CACHE)
    eaai_text = read_text(EAAI_ZOTERO_CACHE)

    full_image_count = int(inventory_audit.get("image_files_total") or 0)
    default_candidate_count = int(inventory_audit.get("candidate_manifest_count") or manifest_count(paths["full_manifest"]))
    cv2_candidate_count = manifest_count(paths["cv2_manifest"])
    decode_failures = 0
    if isinstance(decode_summary.get("candidate_images"), dict):
        decode_failures = int(decode_summary["candidate_images"].get("decode_failures", 0) or 0)
    manual_pending = manual_validation.get("pending_rows")
    clean_manifest_exists = paths["clean_manifest"].exists()

    rows: List[Dict[str, object]] = [
        audit_row(
            "R01",
            "Wu et al. 2026 ESWA edge reference",
            "dataset_source",
            "Applied Microalgal Biology Laboratory at Ocean University of China",
            verification_status(ESWA_ZOTERO_CACHE, eswa_text, ["Applied Microalgal Biology Laboratory", "Ocean University of China"]),
            f"Zotero key `9MCJDQGE`, attachment cache {source_ref(ESWA_ZOTERO_CACHE)}; local note {source_ref(paths['eswa_note'])}",
            "可写：ESWA 参考文献的数据由中国海洋大学相关微藻实验室提供。",
            "不可写：Stage1 当前 2777 图像池已经被证明就是该 676 图边缘数据集。",
            "需要本项目自己的采集说明、物种清单和与 676 图边缘集的文件级对应关系。",
            "该字段只能用于借鉴数据描述结构，不能替代本项目数据证明。",
        ),
        audit_row(
            "R02",
            "Wu et al. 2026 ESWA edge reference",
            "dataset_size_species",
            "676 high-resolution microscopic images, 36 HAB species",
            verification_status(ESWA_ZOTERO_CACHE, eswa_text, ["676", "36", "high-resolution microscopic images"]),
            f"Zotero key `9MCJDQGE`, attachment cache {source_ref(ESWA_ZOTERO_CACHE)}; line-level extraction documented by this audit.",
            "可写：ESWA 参考文献报告 676 张 HAB 显微图像、36 个常见有害藻华物种。",
            "不可写：我们的 2777 图像池自动包含或扩展该 676 图集合。",
            "需要文件名、原始编号或哈希层面的 overlap / subset 证明。",
            "676/36 是参考论文事实，不是 Stage1 当前数据集事实。",
        ),
        audit_row(
            "R03",
            "Wu et al. 2026 ESWA edge reference",
            "acquisition_and_annotation",
            "Olympus CX43 + Canon EOS 5D Mark IV, 400x, bright-field; LabelMe edge maps by two HAB experts",
            verification_status(ESWA_ZOTERO_CACHE, eswa_text, ["Olympus CX43", "Canon EOS 5D Mark IV", "400x", "LabelMe", "two marine biology experts"]),
            f"Zotero key `9MCJDQGE`, attachment cache {source_ref(ESWA_ZOTERO_CACHE)}",
            "可借鉴写法：说明显微镜、相机、倍率、明场条件、专家交叉核验和分歧协商流程。",
            "不可写：当前 Stage1 full-pool 已有同等专家标注或同一设备参数。",
            "需要本项目实际设备、倍率、拍摄协议、标注者资质和标注软件记录。",
            "如果 Stage1 只做增强，没有 GT edge 标注，不能照搬 edge annotation 描述。",
        ),
        audit_row(
            "R04",
            "Wu et al. 2026 ESWA edge reference",
            "split_and_edge_protocol",
            "473 train / 203 test, 70/30 species-level split; ODS/OIS/AP/AC edge evaluation; no NMS",
            verification_status(ESWA_ZOTERO_CACHE, eswa_text, ["473", "203", "species level", "ODS", "OIS", "Average Precision", "Non-Maximum Suppression"]),
            f"Zotero key `9MCJDQGE`, attachment cache {source_ref(ESWA_ZOTERO_CACHE)}",
            "可借鉴：若做 MyEdge/Stage1 coupling，优先报告 ODS/OIS/AP/AC、是否 NMS、split 单位和评估阈值。",
            "不可写：Stage1 502/496 增强主表等价于 ESWA 的 203 张 edge test。",
            "需要 MyEdge 当前 168 张测试集与 ESWA 203 测试集的关系说明，或明确它们是不同本地协议。",
            "Stage1 增强指标与 edge ODS/OIS/AP/AC 是不同任务口径。",
        ),
        audit_row(
            "R05",
            "Wu et al. 2026 EAAI segmentation reference",
            "dataset_source_size_split",
            "AICO/OUC HAB microscopy dataset, 1026 images, 8:2 train/validation split",
            verification_status(EAAI_ZOTERO_CACHE, eaai_text, ["AICO Lab", "1,026", "8:2", "Applied Micro-algae"]),
            f"Zotero key `ZMUBCGCD`, attachment cache {source_ref(EAAI_ZOTERO_CACHE)}; local note {source_ref(paths['eaai_note'])}",
            "可写：EAAI 参考文献在同方向 HAB 显微分割任务中报告 1026 张数据和 8:2 划分。",
            "不可写：Stage1 2777 图像池已经证明与 EAAI 1026 图分割集同一划分或同一标注集合。",
            "需要文件级 overlap、分割 mask 对应关系、训练/验证名单或数据登记表。",
            "1026/8:2 是参考论文事实；当前 Stage1 只能据本仓库写 2777/2774/2770。",
        ),
        audit_row(
            "R06",
            "Wu et al. 2026 EAAI segmentation reference",
            "evidence_chain_to_borrow",
            "task-oriented enhancement + segmentation coupling; enhancement ablation; boundary metrics; efficiency; cross-dataset and downstream analyses",
            verification_status(
                EAAI_ZOTERO_CACHE,
                eaai_text,
                ["enhancement", "segmentation", "HD95", "BIoU", "FLOPs", "FPS", "Cross-dataset", "downstream"],
            ),
            f"Zotero key `ZMUBCGCD`, attachment cache {source_ref(EAAI_ZOTERO_CACHE)}",
            "可借鉴：把增强写成任务驱动结构输入，并用下游边界、效率、失败案例和应用指标支撑。",
            "不可写：Stage1 已经完成这些 EAAI 风格下游分割或分类证据。",
            "需要 Stage1->MyEdge 固定 detector 结果、效率、失败案例、退化子集和至少一种应用级验证。",
            "只能借鉴证据链结构，不能把参考论文结果转写成我们自己的结果。",
        ),
        audit_row(
            "R07",
            "Stage1Codex current full algae pool",
            "current_pool_counts",
            {
                "image_files_total": full_image_count,
                "default_candidate_manifest": default_candidate_count,
                "cv2_readable_candidate_manifest": cv2_candidate_count,
                "decode_failures": decode_failures,
            },
            "verified_in_repo",
            (
                f"{source_ref(paths['inventory_doc'])}; {source_ref(paths['inventory_audit'])}; "
                f"{source_ref(paths['full_manifest'])}; {source_ref(paths['cv2_manifest'])}"
            ),
            f"可写：本项目当前完整增强图像池为 {full_image_count} 个图像文件，默认候选 {default_candidate_count}，OpenCV 可读候选 {cv2_candidate_count}。",
            "不可写：full2770 已经完成增强，或 full2770 已替代正式 502/496 论文口径。",
            "需要人工复核后 clean manifest；如获授权，还需要 full2770 正式长跑和 intake 接收。",
            "当前 2770 是 cv2-readable candidate，不是 reviewed clean protocol。",
        ),
        audit_row(
            "R08",
            "Stage1Codex current full algae pool",
            "manual_review_state",
            {"pending_rows": manual_pending, "clean_manifest_exists": clean_manifest_exists},
            "verified_in_repo",
            f"{source_ref(paths['manual_validation'])}; {source_ref(paths['clean_manifest'])}",
            f"可写：完整图像池仍有 {manual_pending} 条人工复核 pending，clean manifest 尚未生成。",
            "不可写：重复/近重复/质量异常已经人工清洗完毕。",
            "需要人工填写 reviewer_decision 并派生 reviewed clean manifest。",
            "机助建议不能自动变成人工决策。",
        ),
        audit_row(
            "R09",
            "Cross-dataset relation",
            "current_relation_status",
            "same lab is user-reported; exact overlap with ESWA 676 or EAAI 1026 is unproven in local repo",
            "relation_unproven",
            (
                f"Current repo evidence: {source_ref(paths['inventory_doc'])}; "
                f"reference metadata/cache: {source_ref(ESWA_ZOTERO_CACHE)}, {source_ref(EAAI_ZOTERO_CACHE)}"
            ),
            "可写：两篇参考论文提供了同方向同实验室 HAB 显微数据描述模板；本项目需另行给出 2777/2774/2770 图像池的本地证据。",
            "不可写：本项目与两篇论文使用完全相同数据集、同一 split、同一 GT 标注或同一统计口径。",
            "需要文件级清单比对、哈希比对、原始采集编号、标注文件或实验室数据登记证明。",
            "这是当前最大数据描述边界。",
        ),
    ]

    status_counts = Counter(str(row["status"]) for row in rows)
    summary = {
        "overall_status": "reference_dataset_descriptions_verified_exact_overlap_missing",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stage1_full_pool": {
            "image_files_total": full_image_count,
            "default_candidate_manifest": default_candidate_count,
            "cv2_readable_candidate_manifest": cv2_candidate_count,
            "decode_failures": decode_failures,
            "manual_review_pending_rows": manual_pending,
            "clean_manifest_exists": clean_manifest_exists,
        },
        "reference_datasets": {
            "eswa_edge": {
                "zotero_key": "9MCJDQGE",
                "article": "Expert Systems with Applications 298 (2026), Article 129663",
                "reported_images": 676,
                "reported_species": 36,
                "reported_train": 473,
                "reported_test": 203,
                "task": "edge detection",
            },
            "eaai_segmentation": {
                "zotero_key": "ZMUBCGCD",
                "article": "Engineering Applications of Artificial Intelligence 177 (2026), Article 114948",
                "reported_images": 1026,
                "reported_split": "8:2 train/validation",
                "task": "segmentation",
            },
        },
        "relation_status": "exact_overlap_missing",
        "status_counts": dict(status_counts),
    }
    return {"summary": summary, "rows": rows}


def render_markdown(audit: Dict[str, object]) -> str:
    summary = audit["summary"]
    rows = audit["rows"]
    stage1_pool = summary["stage1_full_pool"]
    refs = summary["reference_datasets"]
    status_counts = summary["status_counts"]

    lines = [
        "# 两篇 Wu et al. 2026 参考论文与 Stage1 完整图像池关系审计",
        "",
        f"生成时间：{summary['generated_at']}",
        "",
        "## 1. 结论",
        "",
        f"- 总状态：`{summary['overall_status']}`。",
        "- 已核验：两篇参考论文的数据集描述可以作为本项目数据说明和证据链设计的参考模板。",
        "- 未核验：当前仓库仍没有文件级证据证明 Stage1 的 2777 图像池与 ESWA 的 676 图边缘数据集或 EAAI 的 1026 图分割数据集存在精确包含、交集或同一划分关系。",
        "- 因此，论文中可以借鉴两篇论文的数据描述字段和实验组织方式，但不能照搬它们的数据规模、split、GT 标注或设备协议作为本项目事实。",
        "",
        "## 2. 数量口径",
        "",
        "| 对象 | 数量/口径 | 当前任务 | 关系状态 |",
        "| --- | --- | --- | --- |",
        f"| Stage1 当前完整图像池 | {stage1_pool['image_files_total']} 图像文件；{stage1_pool['default_candidate_manifest']} 默认候选；{stage1_pool['cv2_readable_candidate_manifest']} OpenCV 可读候选 | 增强覆盖与后续下游输入 | 本仓库已核验，但 clean manifest 仍缺 |",
        f"| ESWA 2026 边缘检测参考 | {refs['eswa_edge']['reported_images']} 张，{refs['eswa_edge']['reported_species']} 个物种，{refs['eswa_edge']['reported_train']}/{refs['eswa_edge']['reported_test']} train/test | HAB edge detection | Zotero 本地缓存核验为参考论文事实；与 Stage1 精确 overlap 未证 |",
        f"| EAAI 2026 分割参考 | {refs['eaai_segmentation']['reported_images']} 张，{refs['eaai_segmentation']['reported_split']} | HAB segmentation | Zotero 本地缓存核验为参考论文事实；与 Stage1 精确 overlap 未证 |",
        "",
        "## 3. 审计矩阵",
        "",
        "| ID | 来源 | 字段 | 核验值 | 状态 | 可用写法 | 禁止写法 | 仍缺证据 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| {item_id} | {source} | {field} | {verified_value} | {status} | {usable} | {forbidden} | {missing} |".format(
                item_id=table_escape(row["item_id"]),
                source=table_escape(row["source"]),
                field=table_escape(row["field"]),
                verified_value=table_escape(row["verified_value"]),
                status=table_escape(row["status"]),
                usable=table_escape(row["usable_wording_cn"]),
                forbidden=table_escape(row["forbidden_wording_cn"]),
                missing=table_escape(row["missing_for_submission"]),
            )
        )

    lines.extend(
        [
            "",
            "## 4. 可借鉴的论文写法",
            "",
            "- 数据描述字段：数据来源实验室、图像规模、物种覆盖、显微设备、倍率、光照条件、重复拍摄、标注工具、专家资质、交叉核验、分歧协商、split 单位。",
            "- ESWA 路线可借鉴：edge GT、ODS/OIS/AP/AC、是否使用 NMS、强 edge baseline、增强前后 edge ablation、CIAFF/Sobel 替换模块对比。",
            "- EAAI 路线可借鉴：task-oriented enhancement coupling、boundary metrics、效率、cross-dataset 解释、下游形态/分类应用、失败案例和局限讨论。",
            "- Stage1 当前只能把这些作为未来补证协议或写作模板，不能把参考论文数值写成 Stage1 结果。",
            "",
            "## 5. 投稿前必须补齐",
            "",
            "1. 建立 Stage1 2777/2774/2770 图像池与两篇参考论文数据集的文件级关系：原始编号、文件名、hash、采集表或人工登记证明至少一种。",
            "2. 补齐本项目自己的数据采集说明：实验室、设备、相机、倍率、明场/照明、物种范围、采样或去水印流程。",
            "3. 若要写下游边缘检测，必须在 MyEdge 协议下补齐 168 张或后续扩展集的 GT、split 和 ODS/OIS/AP/AC，而不是用 Stage1 增强指标代替。",
            "4. 若使用完整图像池作为增强覆盖证据，先完成人工复核并生成 reviewed clean manifest；候选 full2770 长跑需要另行明确授权。",
            "",
            "## 6. 状态计数",
            "",
        ]
    )
    for key, value in sorted(status_counts.items()):
        lines.append(f"- `{key}`: {value}")

    lines.extend(
        [
            "",
            "## 7. 本审计边界",
            "",
            "- 本审计只读取仓库文件和 Zotero 本地缓存，不访问在线页面。",
            "- 本审计不运行 Stage1 增强、不运行 MyEdge sampling/eval/show、不训练、不生成新图表、不重算指标。",
            "- 本审计不是 overlap 证明；它只是把参考论文数据描述和本项目当前数据池之间的可写边界固定下来。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    output_md = Path(args.output_md)
    output_json = Path(args.output_json)
    audit = build_audit()

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(audit), encoding="utf-8")
    print(f"Wrote {output_md}")
    print(f"Wrote {output_json}")


if __name__ == "__main__":
    main()
