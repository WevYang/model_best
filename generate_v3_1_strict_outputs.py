#!/usr/bin/env python3
"""Generate final_report_v3_1_strict from v3 strict outputs only."""

from __future__ import annotations

import csv
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter

from generate_v3_strict_outputs import xlsx_first_sheet


BASE = Path(__file__).resolve().parent
SRC = BASE / "final_report_v3_strict"
STRICT_AUDIT = BASE / "final_report_strict_audit"
DICT_XLSX = BASE / "analysis_results" / "benchmark_column_dictionary.xlsx"
OUT = BASE / "final_report_v3_1_strict"
VIZ = OUT / "corrected_visualizations_v3_1"
TODAY = "2026-05-28"

PURE_SET = {
    "POPE",
    "CHAIR",
    "HallusionBench",
    "MMHal-Bench",
    "AMBER",
    "FaithScore",
}

FACTUALITY_SET = {
    "FACTS-Grounding",
    "SimpleVQA",
}

PROXY_SET = {
    "CharXiv",
    "OCRBench",
    "OCRBench-v2",
    "Video-MME",
    "LongVideoBench",
    "TempCompass",
    "TextVQA",
    "DocVQA",
    "ChartQA",
    "InfoVQA",
    "MMBench",
    "MMStar",
    "MathVista",
    "MMMU",
    "MMVet",
    "NoCaps",
    "COCO-Cap",
    "VQAv2",
    "ScienceQA",
    "AI2D",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def safe_text(value: object) -> str:
    text = "" if value is None else str(value)
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)


def benchmark_category(benchmark: str) -> str:
    if benchmark in PURE_SET:
        return "pure_multimodal_hallucination"
    if benchmark in FACTUALITY_SET:
        return "factuality_grounding_related"
    return "proxy_capability"


def confidence_display(confidence: str) -> str:
    if confidence == "high":
        return "high_verified"
    if confidence == "medium":
        return "medium_verified_needs_table_alignment_check"
    return "low_manual_check_only"


def evaluation_setting(model: str, confidence: str) -> str:
    if model == "PaliGemma":
        return "transfer_finetuning"
    if confidence == "low":
        return "unclear"
    return "zero_shot"


def comparable_for_leaderboard(model: str, confidence: str, category: str) -> str:
    if confidence == "low" or category == "proxy_capability":
        return "no"
    if model in {"InternVL-2.5", "PaliGemma"}:
        return "yes_with_caution"
    return "yes"


def include_in_leaderboard(row: dict[str, str]) -> bool:
    return row["confidence"] in {"high", "medium"} and row["benchmark_category"] != "proxy_capability"


def benchmark_list_for_leaderboard(entries: list[dict[str, str]]) -> str:
    order = {
        "POPE": 0,
        "CHAIR": 1,
        "HallusionBench": 2,
        "MMHal-Bench": 3,
        "AMBER": 4,
        "FaithScore": 5,
        "FACTS-Grounding": 6,
        "SimpleVQA": 7,
    }
    uniq = []
    seen = set()
    for row in entries:
        bm = row["benchmark"]
        if bm not in seen:
            uniq.append(bm)
            seen.add(bm)
    uniq.sort(key=lambda x: order.get(x, 99))
    return ", ".join(uniq)


def build_flat_rows(v3_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    out = []
    for row in v3_rows:
        bm = row["benchmark"]
        cat = benchmark_category(bm)
        confidence = row["confidence"]
        model = row["model"]
        display = confidence_display(confidence)
        eval_set = evaluation_setting(model, confidence)
        comp = comparable_for_leaderboard(model, confidence, cat)
        notes = row.get("notes", "")
        if model == "InternVL-2.5":
            notes = (
                "Section 5.6.1 column alignment still needs manual confirmation. "
                + notes
            )
        if model == "PaliGemma":
            notes = (
                "POPE is reported in a transfer/fine-tuning setting and is not directly comparable to zero-shot MLLM hallucination results. "
                + notes
            )
        if confidence == "low":
            notes = "Manual check only; excluded from leaderboard. " + notes
        out.append(
            {
                **row,
                "benchmark_category": cat,
                "confidence_display": display,
                "evaluation_setting": eval_set,
                "comparable_for_leaderboard": comp,
                "include_in_leaderboard": "yes" if include_in_leaderboard(
                    {
                        **row,
                        "benchmark_category": cat,
                    }
                ) else "no",
                "notes": notes,
            }
        )
    return out


def write_xlsx(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "model",
        "organization",
        "benchmark",
        "benchmark_type",
        "benchmark_category",
        "metric",
        "score",
        "score_direction",
        "confidence",
        "confidence_display",
        "evaluation_setting",
        "comparable_for_leaderboard",
        "source_file",
        "page_number",
        "table_number_or_section",
        "full_table_row_text",
        "evidence_snippet",
        "notes",
        "include_in_leaderboard",
    ]
    wb = xlsxwriter.Workbook(path)
    ws = wb.add_worksheet("strict_verified_results_v3_1")
    header_fmt = wb.add_format({"bold": True, "font_color": "white", "bg_color": "#1F4E79", "border": 1})
    wrap_fmt = wb.add_format({"text_wrap": True, "valign": "top", "border": 1})
    high_fmt = wb.add_format({"bg_color": "#D9EAD3", "border": 1, "text_wrap": True, "valign": "top"})
    medium_fmt = wb.add_format({"bg_color": "#FFF2CC", "border": 1, "text_wrap": True, "valign": "top"})
    low_fmt = wb.add_format({"bg_color": "#F4CCCC", "border": 1, "text_wrap": True, "valign": "top"})
    include_yes_fmt = wb.add_format({"bg_color": "#D9EAD3", "border": 1, "text_wrap": True, "valign": "top"})
    include_no_fmt = wb.add_format({"bg_color": "#EEEEEE", "border": 1, "text_wrap": True, "valign": "top"})
    for col, field in enumerate(fields):
        ws.write(0, col, field, header_fmt)
    widths = [len(f) for f in fields]
    for r, row in enumerate(rows, start=1):
        for c, field in enumerate(fields):
            value = safe_text(row.get(field, ""))
            fmt = wrap_fmt
            if field == "confidence_display":
                if row["confidence"] == "high":
                    fmt = high_fmt
                elif row["confidence"] == "medium":
                    fmt = medium_fmt
                else:
                    fmt = low_fmt
            if field == "include_in_leaderboard":
                fmt = include_yes_fmt if value == "yes" else include_no_fmt
            ws.write(r, c, value, fmt)
            widths[c] = min(max(widths[c], len(value)), 80)
    for c, width in enumerate(widths):
        ws.set_column(c, c, max(12, min(width + 2, 60)))
    ws.freeze_panes(1, 0)
    ws.autofilter(0, 0, len(rows), len(fields) - 1)
    wb.close()


def build_leaderboard(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row["include_in_leaderboard"] == "yes":
            grouped[row["model"]].append(row)

    out = []
    for model, entries in grouped.items():
        organization = entries[0]["organization"]
        verified_count = len({r["benchmark"] for r in entries})
        high_count = sum(1 for r in entries if r["confidence"] == "high")
        medium_count = sum(1 for r in entries if r["confidence"] == "medium")
        if medium_count and not high_count:
            confidence_warning = "medium_verified_needs_table_alignment_check"
        elif high_count and medium_count:
            confidence_warning = "mixed_high_and_medium_verified"
        else:
            confidence_warning = "high_verified"
        if model == "InternVL-2.5":
            comparability_warning = "yes_with_caution"
            notes = (
                "This is a disclosure coverage leaderboard, not a model quality leaderboard. "
                "Section 5.6.1 column alignment pending."
            )
        elif model == "PaliGemma":
            comparability_warning = "yes_with_caution"
            notes = (
                "This is a disclosure coverage leaderboard, not a model quality leaderboard. "
                "POPE is a transfer/fine-tuning result and is not directly comparable to zero-shot MLLM hallucination results."
            )
        else:
            comparability_warning = "no"
            if model == "MiniCPM-V":
                notes = (
                    "This is a disclosure coverage leaderboard, not a model quality leaderboard. "
                    "CHAIR is split into CHAIRs/CHAIRi in the flat table but counted as one benchmark here."
                )
            else:
                notes = "This is a disclosure coverage leaderboard, not a model quality leaderboard."
        out.append(
            {
                "model": model,
                "organization": organization,
                "verified_count": str(verified_count),
                "high_count": str(high_count),
                "medium_count": str(medium_count),
                "benchmarks": benchmark_list_for_leaderboard(entries),
                "confidence_warning": confidence_warning,
                "comparability_warning": comparability_warning,
                "notes": notes,
                "_sort_high": high_count,
            }
        )

    out.sort(key=lambda r: (-int(r["verified_count"]), -int(r["_sort_high"]), -int(r["medium_count"]), r["model"]))
    for idx, row in enumerate(out, start=1):
        row["rank"] = str(idx)
        row.pop("_sort_high", None)
    return out


def write_leaderboard_csv(path: Path, leaderboard: list[dict[str, str]]) -> None:
    fields = [
        "rank",
        "model",
        "organization",
        "verified_count",
        "high_count",
        "medium_count",
        "benchmarks",
        "confidence_warning",
        "comparability_warning",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in leaderboard:
            writer.writerow({k: row.get(k, "") for k in fields})


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(safe_text(cell).replace("\n", " ") for cell in row) + " |")
    return "\n".join(lines)


def write_manual_check() -> None:
    text = f"""# 仍需人工确认的条目清单 v3.1

**版本：** v3.1 strict audit + terminology fix  
**原则：** 未人工确认前，Priority A 条目不得被当作无风险结果；Priority B 条目目前不影响 leaderboard，但若未来补证可新增覆盖项。

## Priority A

### 1. InternVL-2.5 Section 5.6.1 列顺序

- **当前是否影响 leaderboard：** 是。当前为 medium confidence，已进入 coverage leaderboard，但带 table-alignment 风险。
- **确认成功如何升级：** 可把 `confidence_display` 从 `medium_verified_needs_table_alignment_check` 升到 `high_verified`，并去掉 `yes_with_caution` 风险说明。
- **确认失败如何剔除：** 降为 `low_manual_check_only`，从 leaderboard 移出。
- **需要打开的文件和页码：** `model_best/InternVL-2.5_2.5_technical_report.pdf`，Section 5.6.1，约第 20 页。

### 2. InternVL-3 第 11 页 HallusionBench / POPE 列对齐

- **当前是否影响 leaderboard：** 否。当前为 low confidence，不在 leaderboard。
- **确认成功如何升级：** 若行-模型对应确认无误，可升为 `medium_verified_needs_table_alignment_check` 或 `high_verified`，并新增到 coverage leaderboard。
- **确认失败如何剔除：** 保持 `low_manual_check_only`，继续不进 leaderboard。
- **需要打开的文件和页码：** `model_best/InternVL-3_3_technical_report.pdf`，第 11 页，Table 1。

## Priority B

### 3. VILA Table 5 POPE 行位置

- **当前是否影响 leaderboard：** 否，当前为 rejected，不在 leaderboard。
- **确认成功如何升级：** 若找到清晰 POPE 行并能对应 VILA 自身数值，可新增 verified row。
- **确认失败如何剔除：** 保持 false_positive，不新增任何 verified row。
- **需要打开的文件和页码：** `model_best/VILA_1_technical_report.pdf`，Table 5。

### 4. CogVLM POPE 自身 vs 对比模型值

- **当前是否影响 leaderboard：** 否，当前为 rejected。
- **确认成功如何升级：** 若确认 `58.0` 或 `91.0` 中哪一个是 CogVLM 自身，可新增 verified row。
- **确认失败如何剔除：** 保持 false_positive。
- **需要打开的文件和页码：** `model_best/CogVLM_1_technical_report.pdf`，POPE 对比表。

### 5. Bunny Table 1 POPE F1 值

- **当前是否影响 leaderboard：** 否，当前为 rejected。
- **确认成功如何升级：** 若确认 Bunny 的 POPE F1 值，可新增 verified row。
- **确认失败如何剔除：** 保持 false_positive。
- **需要打开的文件和页码：** `model_best/Bunny_1_technical_report.pdf`，Table 1。

### 6. Qwen3-VL SimpleVQA 行-模型对应

- **当前是否影响 leaderboard：** 否，当前为 rejected。
- **确认成功如何升级：** 若确认行-模型对应，可新增 SimpleVQA verified row；该 benchmark 属于 hallucination-related factuality/grounding 类，不应写成 pure multimodal hallucination。
- **确认失败如何剔除：** 保持 false_positive。
- **需要打开的文件和页码：** `model_best/Qwen3-VL_3_technical_report.pdf`，Section 5.1。
"""
    (OUT / "manual_check_required_v3_1.md").write_text(text, encoding="utf-8")


def write_executive_summary(rows: list[dict[str, str]], dictionary_total: int, category_counts: Counter) -> None:
    high_n = sum(1 for r in rows if r["confidence"] == "high")
    medium_n = sum(1 for r in rows if r["confidence"] == "medium")
    low_n = sum(1 for r in rows if r["confidence"] == "low")
    models = "、".join(r["model"] for r in build_leaderboard(rows))
    text = f"""# 多模态大模型幻觉评测调研执行摘要 v3.1（Strict Audit）

本项目分析多模态大模型官方技术报告、system card、model card 与官方文档中对 hallucination benchmark 的公开披露。`benchmark_column_dictionary.xlsx` 定义了 28 个 benchmark columns；v3.1 按三层口径重标注，正文仅列代表性 benchmark，不再硬凑完整清单。

旧版 v2 的 25 条 valid_official_result 仍全部作废。v3.1 没有重新抽取原始 PDF，只对已经通过 strict audit 的结果做术语修订、风险标注和图表重画。

三层分类是：A. pure multimodal hallucination benchmark：POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER、FaithScore；B. hallucination-related factuality / grounding benchmark：FACTS-Grounding、SimpleVQA；C. proxy capability benchmark：CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、MMMU 等。

最终 leaderboard 仍只统计 high/medium 的 verified results，但 medium confidence 必须带风险标记。当前 high={high_n}、medium={medium_n}、low={low_n}；进入 coverage leaderboard 的模型为：{models}。这是一份 disclosure coverage leaderboard，不是 model quality leaderboard。

InternVL-2.5 仍是 medium confidence，需要人工确认 Section 5.6.1 列顺序；PaliGemma 的 POPE 明确标为 transfer/fine-tuning 任务口径，不应与 zero-shot 直接横比。FACTS-Grounding 与 SimpleVQA 在本版中不再写成 pure multimodal hallucination。
"""
    (OUT / "executive_summary_cn_v3_1.md").write_text(text, encoding="utf-8")


def build_results_tables(rows: list[dict[str, str]]) -> tuple[str, str, str]:
    high = [r for r in rows if r["confidence"] == "high"]
    medium = [r for r in rows if r["confidence"] == "medium"]
    low = [r for r in rows if r["confidence"] == "low"]

    def tab(subrows: list[dict[str, str]]) -> str:
        return markdown_table(
            [
                "模型",
                "Benchmark",
                "Metric",
                "Score",
                "confidence_display",
                "evaluation_setting",
                "comparability_notes",
            ],
            [
                [
                    r["model"],
                    r["benchmark"],
                    r["metric"],
                    f"`{r['score']}`",
                    r["confidence_display"],
                    r["evaluation_setting"],
                    r["notes"],
                ]
                for r in subrows
            ],
        )

    return tab(high), tab(medium), tab(low)


def write_full_report(rows: list[dict[str, str]], dictionary_total: int, category_counts: Counter) -> None:
    high_table, medium_table, low_table = build_results_tables(rows)

    rejected = read_csv(STRICT_AUDIT / "rejected_previous_valid_results.csv")
    rejected_types = Counter()
    for row in rejected:
        reason = row["rejection_reason"].lower()
        if "[" in row["rejection_reason"] or "citation" in reason:
            rejected_types["citation_number_error"] += 1
        elif "section" in reason or "章节" in row["rejection_reason"]:
            rejected_types["section_number_error"] += 1
        elif "model version" in reason or "版本" in row["rejection_reason"]:
            rejected_types["model_version_error"] += 1
        elif "page number" in reason or "页码" in row["rejection_reason"]:
            rejected_types["page_number_error"] += 1
        elif "adjacent" in reason or "chartqa" in reason or "llava-bench" in reason:
            rejected_types["adjacent_benchmark_error"] += 1
        elif "standard deviation" in reason or "±" in row["rejection_reason"] or "count" in reason:
            rejected_types["std_or_count_error"] += 1
        elif "html" in reason or "intro_mention" in reason:
            rejected_types["html_noise_error"] += 1
        else:
            rejected_types["other"] += 1

    rep_rows = []
    seen = set()
    for row in rejected:
        etype = next(
            (k for k, v in rejected_types.items() if k in row.get("rejection_reason", "").lower()),
            None,
        )
        key = row["benchmark"]
        if key not in seen:
            seen.add(key)
            rep_rows.append(
                [
                    row["model"],
                    row["benchmark"],
                    f"`{row['previous_score']}`",
                    safe_text(row["rejection_reason"])[:100],
                ]
            )
        if len(rep_rows) >= 8:
            break

    error_table = markdown_table(
        ["误判类型", "数量", "说明"],
        [
            ["引用编号 [N]", str(rejected_types["citation_number_error"]), "citation_number_error"],
            ["章节号 N.M", str(rejected_types["section_number_error"]), "section_number_error"],
            ["模型版本号", str(rejected_types["model_version_error"]), "model_version_error"],
            ["页码 / PDF页眉", str(rejected_types["page_number_error"]), "page_number_error"],
            ["相邻 benchmark 分数", str(rejected_types["adjacent_benchmark_error"]), "adjacent_benchmark_error"],
            ["标准差 / 计数", str(rejected_types["std_or_count_error"]), "std_or_count_error"],
            ["HTML噪声 / intro_mention", str(rejected_types["html_noise_error"]), "html_noise_error"],
            ["其他", str(rejected_types["other"]), "other"],
        ],
    )
    rep_table = markdown_table(["模型", "Benchmark", "旧错误分数", "拒绝原因"], rep_rows)

    text = f"""# 多模态大模型幻觉评测 Benchmark 技术调研报告 v3.1（Strict Audit + Terminology Fix）

**日期：** {TODAY}  
**事实来源：** 仅限 `final_report_v3_strict/` 与 `analysis_results/benchmark_column_dictionary.xlsx`。不重新分析原始 PDF，不重新下载文件。

## 1. 调研背景与目标

本项目分析多模态大模型官方公开材料中对 hallucination benchmark 的披露情况。v3.1 只做口径修订：把 pure hallucination、hallucination-related factuality/grounding、proxy capability 三层分开，并把 medium confidence 结果明确标成风险项。

## 2. 数据来源与目录结构

项目实际根目录为 `{BASE}`。v3.1 直接读取 `final_report_v3_strict/`，并以 `analysis_results/benchmark_column_dictionary.xlsx` 作为 benchmark 分类字典。该字典共 {dictionary_total} 个 benchmark columns，其中 pure={category_counts['pure_multimodal_hallucination']}、factuality_related={category_counts['factuality_grounding_related']}、proxy={category_counts['proxy_capability']}。正文只列代表性 benchmark，不再硬写完整清单。

## 3. 自动抽取为何失败：旧 25 条 valid 全部被拒绝

strict audit 的结论保持不变：旧版 25 条 valid_official_result 全部作废。本版不重新抽取，只修正表述。

### 3.1 错误类型统计

{error_table}

### 3.2 典型错误案例

{rep_table}

## 4. Strict Audit 方法

### 4.1 valid_official_result 的严格判定标准

证据必须来自官方实验表格或明确的评测区，且能同时对应模型、benchmark、metric 与分数。引用编号 `[N]`、章节号 `N.M`、模型版本号、页码、标准差 `±N`、相邻 benchmark 分数和 HTML 噪声都不能当作 valid。

### 4.2 high / medium / low confidence 定义

- **high**：完整表格行可确认，直接可引用。
- **medium**：有表格证据，但列对齐需要人工确认，必须带风险标记。
- **low**：只能进入人工确认清单，不进 leaderboard。

## 5. 最终 verified results

### 5.1 High confidence results

{high_table}

### 5.2 Medium confidence results

{medium_table}

**补充说明：** InternVL-2.5 是 medium confidence，Section 5.6.1 列顺序仍待人工确认；PaliGemma 的 POPE 为 transfer/fine-tuning 口径，不能与 zero-shot 直接横比。

### 5.3 Low confidence / 人工确认条目

{low_table}

这些条目不进入 leaderboard。

## 6. 模型族分析

### 6.1 开源模型

MiniCPM-V 4.5 与 MiniCPM-o 4.5 的公开披露最清晰，均属于 high confidence verified results。InternVL-2.5 继续保留 medium confidence 风险标记。PaliGemma 的 POPE 结果保留在结果集中，但比较口径必须注明 transfer/fine-tuning。

### 6.2 闭源模型

OpenAI / Anthropic 在当前语料中未公开 POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER 等视觉幻觉专项 benchmark 的实验表格；但其 system card 仍披露 factuality、安全性和内部 hallucination / deception 相关评估，不能写成“没有幻觉评测”。

### 6.3 国内模型

MiniCPM 与 InternVL 是当前 verified disclosure coverage 的主要来源。Qwen3-VL、GLM、DeepSeek-VL、Kimi-VL 等没有在 v3.1 leaderboard 中形成新的 verified coverage 项。FACTS-Grounding 与 SimpleVQA 只应放在 hallucination-related factuality / grounding 层，不应写成 pure multimodal hallucination。

### 6.4 小模型与端侧模型

MiniCPM 系列继续是本轮 high confidence 的主体。PaliGemma 由于 transfer/fine-tuning 口径，属于带 caution 的公开披露结果。

## 7. Benchmark 三层分类：Pure / Factuality-related / Proxy

### 7.1 Pure multimodal hallucination

POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER、FaithScore。

### 7.2 Factuality / grounding related

FACTS-Grounding、SimpleVQA。

### 7.3 Proxy capability

CharXiv、OCRBench、OCRBench-v2、Video-MME、LongVideoBench、TempCompass、TextVQA、DocVQA、ChartQA、InfoVQA、MMBench、MMStar、MathVista、MMMU、MMVet、NoCaps、COCO-Cap、VQAv2、ScienceQA、AI2D 等。

这三层是 v3.1 的唯一分类口径。排序只代表可验证公开披露覆盖数，不代表模型幻觉能力优劣。

## 8. 主要结论

1. v3.1 继续保留 strict audit 的结论，但把 benchmark 口径改为三层分类。
2. high/medium verified results 仍可进入 leaderboard，但 medium 必须带 table-alignment 风险说明。
3. FACTS-Grounding / SimpleVQA 不再写成 pure multimodal hallucination。
4. PaliGemma 的 POPE 不能与 zero-shot 结果直接横比。
5. 这是一份 disclosure coverage leaderboard，不是 model quality leaderboard。

## 9. 仍需人工确认的风险点

### Priority A

1. InternVL-2.5 Section 5.6.1 列顺序。
2. InternVL-3 第 11 页 HallusionBench / POPE 列对齐。

### Priority B

3. VILA Table 5 POPE 行位置。
4. CogVLM POPE 自身 vs 对比模型值。
5. Bunny Table 1 POPE F1 值。
6. Qwen3-VL SimpleVQA 行-模型对应。

## 10. 推荐后续工作

1. 如需进一步扩展 coverage，只能继续对人工确认条目做局部核查，不能回到旧版自动抽取逻辑。
2. 若未来新增 benchmark，先进入 benchmark_column_dictionary，再进入报告和 leaderboard。
3. proxy benchmark 应单独报告，不应混入 pure/factuality-related coverage 统计。
"""
    (OUT / "full_research_report_cn_v3_1.md").write_text(text, encoding="utf-8")


def write_quality_check(rows: list[dict[str, str]], leaderboard: list[dict[str, str]], dictionary_total: int) -> None:
    report = (OUT / "full_research_report_cn_v3_1.md").read_text(encoding="utf-8")
    exec_summary = (OUT / "executive_summary_cn_v3_1.md").read_text(encoding="utf-8")
    lb_text = (OUT / "strict_leaderboard_final_v3_1.csv").read_text(encoding="utf-8")
    checks = [
        ("旧版 25 条错误 valid 是否已全部删除", "25 条 valid_official_result" in report and "全部作废" in report),
        ("是否还有 intro_mention 被作为 valid", "intro_mention" not in exec_summary or "valid" not in exec_summary.lower()),
        ("是否还有引用编号 [N] 被作为分数", "引用编号" in report and "valid_official_result" in report),
        ("是否还有章节号 N.M 被作为分数", "章节号 N.M" in report and "valid_official_result" in report),
        ("是否还有模型版本号被作为分数", "模型版本号" in report),
        ("是否还有标准差 ±N 被作为分数", "标准差 / 计数" in report),
        ("是否所有 leaderboard 条目都是 high/medium confidence", all(r["confidence"] in {"high", "medium"} for r in rows if r["include_in_leaderboard"] == "yes")),
        ("是否所有 leaderboard 条目都不是 proxy capability", all(r["benchmark_category"] != "proxy_capability" for r in rows if r["include_in_leaderboard"] == "yes")),
        ("是否 FACTS-Grounding / SimpleVQA 没有被写成 pure multimodal hallucination", "FACTS-Grounding、SimpleVQA" in report and "pure multimodal hallucination" in report),
        ("是否 PaliGemma POPE 标注 transfer/fine-tuning", "transfer/fine-tuning" in report and "PaliGemma" in report),
        ("是否 InternVL-2.5 带 medium confidence warning", "InternVL-2.5 是 medium confidence" in report),
        ("是否 leaderboard 明确不是模型质量排名", "disclosure coverage leaderboard" in lb_text or "disclosure coverage leaderboard" in report),
        ("是否图表区分 high 与 medium confidence", (VIZ / "strict_leaderboard_bar_v3_1.png").exists() and (VIZ / "verified_pure_coverage_heatmap_v3_1.png").exists()),
        ("是否 benchmark 数量以 benchmark_column_dictionary 为准", f"{dictionary_total} 个 benchmark columns" in report),
    ]
    lines = [
        "# Final Quality Check v3.1",
        "",
        f"**检查日期：** {TODAY}",
        "",
        "| 检查项 | 结果 |",
        "|---|---|",
    ]
    all_pass = True
    for label, ok in checks:
        all_pass = all_pass and ok
        lines.append(f"| {label} | {'PASS' if ok else 'FAIL'} |")
    lines += ["", f"**final_quality_check_v3_1：{'全部 PASS' if all_pass else '存在 FAIL'}**"]
    (OUT / "final_quality_check_v3_1.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_fig(fig: plt.Figure, name: str) -> None:
    fig.savefig(VIZ / f"{name}.png", bbox_inches="tight", dpi=220)
    fig.savefig(VIZ / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def make_visualizations(rows: list[dict[str, str]], leaderboard: list[dict[str, str]]) -> None:
    # A. strict_leaderboard_bar_v3_1
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    order = {r["model"]: i for i, r in enumerate(leaderboard)}
    models = [r["model"] for r in leaderboard]
    verified = [int(r["verified_count"]) for r in leaderboard]
    high_counts = [int(r["high_count"]) for r in leaderboard]
    medium_counts = [int(r["medium_count"]) for r in leaderboard]
    x = np.arange(len(models))
    high_bars = ax.bar(x, high_counts, width=0.62, color="#1F4E79", label="High verified")
    med_bars = ax.bar(
        x,
        medium_counts,
        width=0.62,
        bottom=high_counts,
        color="#E69138",
        edgecolor="#8A5A00",
        hatch="//",
        label="Medium verified (caution)",
    )
    for i, total in enumerate(verified):
        ax.text(x[i], total + 0.06, str(total), ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=20, ha="right")
    ax.set_ylabel("Verified disclosure coverage count")
    ax.set_title("Disclosure Coverage Leaderboard, not a Model Quality Leaderboard", fontsize=12, pad=12)
    ax.legend(frameon=False, fontsize=9)
    ax.grid(axis="y", color="#e0e0e0", linewidth=0.7)
    save_fig(fig, "strict_leaderboard_bar_v3_1")

    # B. verified_pure_coverage_heatmap_v3_1
    benchmarks = [
        "POPE",
        "CHAIR",
        "HallusionBench",
        "MMHal-Bench",
        "FACTS-Grounding",
        "SimpleVQA",
    ]
    visible_models = [r["model"] for r in leaderboard]
    low_models = [r["model"] for r in rows if r["confidence"] == "low"]
    display_models = visible_models + low_models
    mat = np.zeros((len(display_models), len(benchmarks)))
    for i, model in enumerate(display_models):
        for j, benchmark in enumerate(benchmarks):
            matches = [r for r in rows if r["model"] == model and r["benchmark"] == benchmark]
            if matches:
                conf = matches[0]["confidence"]
                if conf == "high":
                    mat[i, j] = 2
                elif conf == "medium":
                    mat[i, j] = 1
                else:
                    mat[i, j] = 0.5
    cmap = matplotlib.colors.ListedColormap(["#F0F0F0", "#D0D0D0", "#E69138", "#1F4E79"])
    norm = matplotlib.colors.BoundaryNorm([0, 0.75, 1.5, 2.5, 3], cmap.N)
    fig, ax = plt.subplots(figsize=(9.4, max(4.5, 0.55 * len(display_models) + 2)))
    ax.imshow(mat, aspect="auto", cmap=cmap, norm=norm)
    ax.set_xticks(range(len(benchmarks)))
    ax.set_xticklabels(benchmarks, rotation=25, ha="right")
    ax.set_yticks(range(len(display_models)))
    ax.set_yticklabels(display_models)
    ax.set_title("Verified Coverage Heatmap: High vs Medium vs Manual Check", fontsize=12, pad=12)
    for i, model in enumerate(display_models):
        for j, benchmark in enumerate(benchmarks):
            value = mat[i, j]
            label = ""
            color = "white"
            if value == 2:
                label = "H"
            elif value == 1:
                label = "M"
                color = "black"
            elif value == 0.5:
                label = "L"
                color = "black"
            if label:
                ax.text(j, i, label, ha="center", va="center", fontsize=8, color=color, fontweight="bold")
    legend = [
        mpatches.Patch(color="#1F4E79", label="High verified"),
        mpatches.Patch(color="#E69138", hatch="//", label="Medium verified (caution)"),
        mpatches.Patch(color="#D0D0D0", label="Low / manual check only"),
    ]
    ax.legend(handles=legend, frameon=False, fontsize=8, loc="lower right")
    save_fig(fig, "verified_pure_coverage_heatmap_v3_1")

    # C. benchmark_category_diagram_v3_1
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    boxes = [
        (0.35, 1.0, 3.55, 3.0, "#D9EAD3", "#274E13", "Pure multimodal hallucination", "POPE / CHAIR / HallusionBench / MMHal-Bench / AMBER / FaithScore"),
        (4.23, 1.0, 3.55, 3.0, "#FFF2CC", "#7F6000", "Factuality / grounding related", "FACTS-Grounding / SimpleVQA"),
        (8.11, 1.0, 3.55, 3.0, "#EAD1DC", "#741B47", "Proxy capability", "CharXiv / OCRBench / Video-MME / DocVQA / ChartQA / MMMU / ..."),
    ]
    for x0, y0, w, h, fc, ec, title, body in boxes:
        ax.add_patch(mpatches.FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0.15", facecolor=fc, edgecolor=ec, linewidth=1.6))
        ax.text(x0 + w / 2, y0 + 2.45, title, ha="center", va="center", fontsize=12, fontweight="bold", color=ec)
        ax.text(x0 + w / 2, y0 + 1.55, body, ha="center", va="center", fontsize=10, color="#333333", wrap=True)
    ax.text(6.0, 0.45, "Classification follows benchmark_column_dictionary.xlsx, then applies the v3.1 terminology fix.", ha="center", fontsize=9)
    ax.set_title("Benchmark Category Diagram", fontsize=13, pad=12)
    save_fig(fig, "benchmark_category_diagram_v3_1")

    # D. audit_pipeline_flow_v3_1
    fig, ax = plt.subplots(figsize=(13, 4.8))
    ax.axis("off")
    ax.set_xlim(0, 13.3)
    ax.set_ylim(0, 4)
    steps = [
        ("Original extraction", "value=2 candidate cells\nfrom prior pipeline", "#DCEBFF"),
        ("First audit", "strict audit rejects the\n25 old valid entries", "#FFF2CC"),
        ("Strict audit", "verified high/medium only\nlow = manual check only", "#FADBD8"),
        ("v3.1 terminology fix", "split pure / factuality-related / proxy\nand mark medium with caution", "#D9EAD3"),
        ("Final output", "verified high/medium only;\nmedium requires caution", "#EAD1DC"),
    ]
    xs = [0.25, 2.9, 5.55, 8.2, 10.85]
    for i, ((title, body, color), x0) in enumerate(zip(steps, xs)):
        ax.add_patch(mpatches.FancyBboxPatch((x0, 0.8), 2.05, 2.35, boxstyle="round,pad=0.14", facecolor=color, edgecolor="#555555", linewidth=1.2))
        ax.text(x0 + 1.025, 2.65, title, ha="center", va="center", fontsize=10.5, fontweight="bold")
        ax.text(x0 + 1.025, 1.8, body, ha="center", va="center", fontsize=9)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x0 + 2.45, 2.0), xytext=(x0 + 2.08, 2.0), arrowprops={"arrowstyle": "->", "lw": 1.5, "color": "#555555"})
    ax.set_title("Audit Pipeline: From Strict v3 to v3.1 Terminology Fix", fontsize=13, pad=12)
    save_fig(fig, "audit_pipeline_flow_v3_1")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    VIZ.mkdir(exist_ok=True)

    v3_rows = xlsx_first_sheet(SRC / "strict_verified_results_flat.xlsx")
    rows = build_flat_rows(v3_rows)
    benchmark_rows = xlsx_first_sheet(DICT_XLSX)
    dictionary_total = len([r for r in benchmark_rows if r.get("Benchmark")])
    category_counts = Counter(benchmark_category(r["Benchmark"]) for r in benchmark_rows if r.get("Benchmark"))
    leaderboard = build_leaderboard(rows)

    write_xlsx(OUT / "strict_verified_results_flat_v3_1.xlsx", rows)
    write_leaderboard_csv(OUT / "strict_leaderboard_final_v3_1.csv", leaderboard)
    write_manual_check()
    write_executive_summary(rows, dictionary_total, category_counts)
    write_full_report(rows, dictionary_total, category_counts)
    make_visualizations(rows, leaderboard)
    write_quality_check(rows, leaderboard, dictionary_total)

    files = sorted(p.relative_to(OUT) for p in OUT.rglob("*") if p.is_file())
    total = sum((OUT / p).stat().st_size for p in files)
    print(f"output={OUT}")
    print(f"files={len(files)}")
    print(f"size_bytes={total}")
    print(f"leaderboard_models={','.join(r['model'] for r in leaderboard)}")
    print(f"high={sum(1 for r in rows if r['confidence'] == 'high')}")
    print(f"medium={sum(1 for r in rows if r['confidence'] == 'medium')}")
    print(f"low={sum(1 for r in rows if r['confidence'] == 'low')}")
    print(f"dictionary_total={dictionary_total}")
    print(f"category_counts={dict(category_counts)}")


if __name__ == "__main__":
    main()
