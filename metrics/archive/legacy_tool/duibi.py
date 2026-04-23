# calc_methods_mean.py
import os
import glob
import csv

# 指标列顺序（和你的 txt 一致）
METRIC_NAMES = [
    "EME",
    "EMEE",
    "Entropy",
    "Contrast",
    "AvgGra",
    "SIFT_KP",
    "MS_SSIM",
    "PSNR",
    "UCIQE",
    "UIQM"
]

def parse_metrics_line(line: str):
    """
    解析一行：
    filename  EME  EMEE  Entropy  Contrast  AvgGra  SIFT_KP  MS_SSIM  PSNR  UCIQE  UIQM
    返回 [float list] 或 None
    """
    parts = line.strip().split()
    if not parts:
        return None
    if parts[0].startswith("#"):
        return None
    if len(parts) < 1 + len(METRIC_NAMES):
        return None

    metric_strs = parts[1:1 + len(METRIC_NAMES)]
    values = []
    for s in metric_strs:
        if s.upper() == "NA":
            return None   # 这里简单处理：整行丢弃
        try:
            values.append(float(s))
        except ValueError:
            return None
    return values

def compute_mean_for_file(txt_path: str):
    """
    对单个 txt 文件计算各指标平均值
    返回 (method_name, count, [mean list]) 或 None
    """
    method_name = os.path.splitext(os.path.basename(txt_path))[0]

    sums = [0.0] * len(METRIC_NAMES)
    cnt = 0

    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            vals = parse_metrics_line(line)
            if vals is None:
                continue
            for i, v in enumerate(vals):
                sums[i] += v
            cnt += 1

    if cnt == 0:
        return None

    means = [s / cnt for s in sums]
    return method_name, cnt, means

def main():
    # 1. 找到当前目录下所有 txt 作为“方法文件”
    txt_files = sorted(glob.glob("*.txt"))
    if not txt_files:
        print("当前目录下没有找到任何 .txt 文件。")
        return

    results = []
    for txt in txt_files:
        info = compute_mean_for_file(txt)
        if info is None:
            print(f"[Warning] 文件 {txt} 没有有效数据，跳过。")
            continue
        results.append(info)

    if not results:
        print("没有任何文件计算出平均值，请检查格式。")
        return

    # 2. 写入 CSV
    out_csv = "methods_mean_metrics.csv"
    with open(out_csv, "w", newline="", encoding="utf-8") as fcsv:
        writer = csv.writer(fcsv)
        header = ["Method", "Count"] + [f"Mean_{name}" for name in METRIC_NAMES]
        writer.writerow(header)
        for method, cnt, means in results:
            writer.writerow([method, cnt] + means)

    # 3. 在终端打印一个对齐表格
    print(f"结果已保存到: {out_csv}\n")

    header = ["Method", "Count"] + [f"Mean_{name}" for name in METRIC_NAMES]
    # 每列宽度（可以根据需要调大一点）
    widths = [max(len(h), 8) for h in header]

    def fmt_row(row_vals):
        return "  ".join(
            str(v).ljust(widths[i])
            for i, v in enumerate(row_vals)
        )

    print(fmt_row(header))
    print("-" * (sum(widths) + 2 * len(widths)))

    for method, cnt, means in results:
        row_vals = [method, cnt] + [f"{m:.4f}" for m in means]
        print(fmt_row(row_vals))

if __name__ == "__main__":
    main()
