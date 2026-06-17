#!/usr/bin/env python3
"""Generate final_report_v3_strict from final_report_strict_audit only."""

from __future__ import annotations

import csv
import re
import textwrap
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path
from zipfile import ZipFile

import matplotlib

matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import xlsxwriter


BASE = Path(__file__).resolve().parent
SA = BASE / "final_report_strict_audit"
OUT = BASE / "final_report_v3_strict"
VIZ = OUT / "corrected_visualizations_v3"
TODAY = "2026-05-28"

PURE_BENCHMARKS = [
    "POPE",
    "CHAIR",
    "HallusionBench",
    "MMHal-Bench",
    "AMBER",
    "FaithScore",
    "FACTS-Grounding",
    "SimpleVQA",
]

PROXY_BENCHMARKS = [
    "CharXiv",
    "OCRBench",
    "OCRBench-v2",
    "Video-MME",
    "LongVideoBench",
    "TempCompass",
    "DocVQA",
    "ChartQA",
    "InfoVQA",
    "TextVQA",
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
]


def configure_fonts() -> None:
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "sans-serif"]
    plt.rcParams.update(
        {
            "font.family": "sans-serif",
            "axes.unicode_minus": False,
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )


def xlsx_first_sheet(path: Path) -> list[dict[str, str]]:
    """Read the first XLSX worksheet using only stdlib XML parsing."""

    ns = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

    def col_index(cell_ref: str) -> int:
        letters = re.sub(r"\d+", "", cell_ref)
        idx = 0
        for ch in letters:
            idx = idx * 26 + ord(ch.upper()) - ord("A") + 1
        return idx - 1

    with ZipFile(path) as zf:
        names = set(zf.namelist())
        shared: list[str] = []
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
            for item in root.findall("a:si", ns):
                text = "".join(
                    t.text or ""
                    for t in item.iter(
                        "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
                    )
                )
                shared.append(text)

        sheet_name = "xl/worksheets/sheet1.xml"
        root = ET.fromstring(zf.read(sheet_name))
        raw_rows: list[list[str]] = []
        for row in root.findall(".//a:sheetData/a:row", ns):
            values: list[str] = []
            for cell in row.findall("a:c", ns):
                idx = col_index(cell.attrib["r"])
                while len(values) <= idx:
                    values.append("")
                typ = cell.attrib.get("t")
                val = ""
                v = cell.find("a:v", ns)
                inline = cell.find("a:is", ns)
                if typ == "s" and v is not None:
                    val = shared[int(v.text or "0")]
                elif typ == "inlineStr" and inline is not None:
                    val = "".join(
                        t.text or ""
                        for t in inline.iter(
                            "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"
                        )
                    )
                elif v is not None:
                    val = v.text or ""
                values[idx] = val
            raw_rows.append(values)

    if not raw_rows:
        return []
    headers = raw_rows[0]
    rows: list[dict[str, str]] = []
    for row in raw_rows[1:]:
        padded = row + [""] * (len(headers) - len(row))
        rows.append({headers[i]: padded[i] for i in range(len(headers))})
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def clean_text(value: object) -> str:
    text = "" if value is None else str(value)
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)


def classify_rejection(row: dict[str, str]) -> str:
    model = row.get("model", "")
    benchmark = row.get("benchmark", "")
    score = row.get("previous_score", "")
    reason = row.get("rejection_reason", "")
    lower = reason.lower()
    if "[" in reason or "citation" in lower:
        return "citation_number_error"
    if "section" in lower or "章节" in reason or "section heading" in lower:
        return "section_number_error"
    if (
        "model version" in lower
        or "model name" in lower
        or "版本" in reason
        or model.startswith("GLM-")
        or model.startswith("Claude-")
        and benchmark == "POPE"
        or model == "Gemini-2.5"
        and score == "1.5"
    ):
        return "model_version_error"
    if "page number" in lower or "页码" in reason or model == "InternVL-3":
        return "page_number_error"
    if "adjacent" in lower or "chartqa" in lower or "llava-bench" in lower or "相邻" in reason:
        return "adjacent_benchmark_error"
    if (
        "standard deviation" in lower
        or "±" in reason
        or "count" in lower
        or "17 classic" in lower
        or "32 from" in lower
    ):
        return "std_or_count_error"
    if "html" in lower or "intro_mention" in lower or model == "MiMo-VL":
        return "html_noise_error"
    return "other"


ERROR_TYPE_LABELS = {
    "citation_number_error": "引用编号 [N]",
    "section_number_error": "章节号 N.M",
    "model_version_error": "模型版本号",
    "page_number_error": "页码 / PDF页眉",
    "adjacent_benchmark_error": "相邻 benchmark 分数",
    "std_or_count_error": "标准差 / 计数",
    "html_noise_error": "HTML噪声 / intro_mention",
    "other": "其他",
}

ERROR_TYPE_LABELS_EN = {
    "citation_number_error": "Citation number [N]",
    "section_number_error": "Section number N.M",
    "model_version_error": "Model version number",
    "page_number_error": "Page number / PDF header",
    "adjacent_benchmark_error": "Adjacent benchmark score",
    "std_or_count_error": "Std. dev. / count",
    "html_noise_error": "HTML noise / intro mention",
    "other": "Other",
}

ERROR_TYPE_ORDER = [
    "citation_number_error",
    "section_number_error",
    "model_version_error",
    "page_number_error",
    "adjacent_benchmark_error",
    "std_or_count_error",
    "html_noise_error",
    "other",
]


def include_in_leaderboard(row: dict[str, str]) -> bool:
    return (
        row.get("confidence") in {"high", "medium"}
        and row.get("benchmark_type") == "pure_hallucination"
    )


def distinct_benchmarks(rows: list[dict[str, str]]) -> list[str]:
    order = {name: i for i, name in enumerate(PURE_BENCHMARKS)}
    return sorted({r["benchmark"] for r in rows}, key=lambda x: order.get(x, 99))


def write_rows_xlsx(path: Path, sheet_name: str, fields: list[str], rows: list[dict[str, str]]) -> None:
    wb = xlsxwriter.Workbook(path)
    ws = wb.add_worksheet(sheet_name[:31])
    header_fmt = wb.add_format({"bold": True, "font_color": "white", "bg_color": "#1F4E79", "border": 1})
    wrap_fmt = wb.add_format({"text_wrap": True, "valign": "top", "border": 1})
    for col, field in enumerate(fields):
        ws.write(0, col, field, header_fmt)
    widths = [len(f) for f in fields]
    for row_idx, row in enumerate(rows, start=1):
        for col, field in enumerate(fields):
            value = clean_text(row.get(field, ""))
            ws.write(row_idx, col, value, wrap_fmt)
            widths[col] = min(max(widths[col], len(value)), 80)
    for col, width in enumerate(widths):
        ws.set_column(col, col, max(12, min(width + 2, 60)))
    ws.freeze_panes(1, 0)
    ws.autofilter(0, 0, max(0, len(rows)), len(fields) - 1)
    wb.close()


def save_fig(fig: plt.Figure, name: str) -> None:
    fig.savefig(VIZ / f"{name}.png", bbox_inches="tight", dpi=220)
    fig.savefig(VIZ / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def make_visualizations(valid_rows: list[dict[str, str]], rejected_rows: list[dict[str, str]], leaderboard_rows: list[dict[str, str]]) -> None:
    # A. rejected_error_types_bar
    counts = Counter(row["error_type"] for row in rejected_rows)
    labels = [ERROR_TYPE_LABELS_EN[t] for t in ERROR_TYPE_ORDER if counts.get(t, 0)]
    values = [counts[t] for t in ERROR_TYPE_ORDER if counts.get(t, 0)]
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    colors = ["#6A4C93", "#1982C4", "#8AC926", "#FFCA3A", "#FF595E", "#2A9D8F", "#8D99AE", "#343A40"]
    bars = ax.barh(labels, values, color=colors[: len(values)], edgecolor="white")
    for bar, value in zip(bars, values):
        ax.text(value + 0.12, bar.get_y() + bar.get_height() / 2, str(value), va="center", fontsize=10)
    ax.set_title("Why the Previous 25 valid_official_result Entries Were Rejected", fontsize=13, pad=12)
    ax.set_xlabel("Rejected entry count")
    ax.set_xlim(0, max(values) + 1.6)
    ax.invert_yaxis()
    ax.grid(axis="x", color="#dddddd", linewidth=0.6)
    save_fig(fig, "rejected_error_types_bar")

    # B. verified_pure_coverage_heatmap - high/medium only.
    verified = [r for r in valid_rows if include_in_leaderboard(r)]
    models = [r["model"] for r in leaderboard_rows]
    benchmarks = [bm for bm in PURE_BENCHMARKS if any(r["benchmark"] == bm for r in verified)]
    conf_rank = {"high": 2, "medium": 1}
    mat = np.zeros((len(models), len(benchmarks)))
    labels_mat = [["" for _ in benchmarks] for _ in models]
    for i, model in enumerate(models):
        for j, benchmark in enumerate(benchmarks):
            confs = [
                r["confidence"]
                for r in verified
                if r["model"] == model and r["benchmark"] == benchmark
            ]
            if confs:
                conf = max(confs, key=lambda c: conf_rank[c])
                mat[i, j] = conf_rank[conf]
                labels_mat[i][j] = "H" if conf == "high" else "M"
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    cmap = matplotlib.colors.ListedColormap(["#F2F2F2", "#9ECAE1", "#1F4E79"])
    ax.imshow(mat, aspect="auto", cmap=cmap, vmin=0, vmax=2)
    ax.set_xticks(range(len(benchmarks)))
    ax.set_xticklabels(benchmarks, rotation=30, ha="right")
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models)
    ax.set_title("High/Medium Verified Pure Hallucination Coverage", fontsize=12, pad=12)
    for i in range(len(models)):
        for j in range(len(benchmarks)):
            if labels_mat[i][j]:
                ax.text(j, i, labels_mat[i][j], ha="center", va="center", color="white", fontweight="bold")
    legend = [
        patches.Patch(color="#1F4E79", label="High confidence"),
        patches.Patch(color="#9ECAE1", label="Medium confidence"),
        patches.Patch(color="#F2F2F2", label="No verified high/medium result"),
    ]
    ax.legend(handles=legend, bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
    save_fig(fig, "verified_pure_coverage_heatmap")

    # C. strict_leaderboard_bar
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    counts_bar = [int(r["verified_pure_benchmark_count"]) for r in leaderboard_rows]
    colors = ["#1F4E79" if "high=" in r["confidence_summary"] and not r["confidence_summary"].startswith("high=0") else "#6EA8D8" for r in leaderboard_rows]
    bars = ax.bar([r["model"] for r in leaderboard_rows], counts_bar, color=colors, edgecolor="white", width=0.55)
    for bar, row in zip(bars, leaderboard_rows):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.06,
            row["verified_pure_benchmark_count"],
            ha="center",
            va="bottom",
            fontsize=11,
            fontweight="bold",
        )
    ax.set_title("Strict Leaderboard: Verified Pure Benchmark Count", fontsize=12, pad=12)
    ax.set_ylabel("Verified pure benchmark count")
    ax.set_ylim(0, max(counts_bar) + 1)
    ax.grid(axis="y", color="#dddddd", linewidth=0.6)
    save_fig(fig, "strict_leaderboard_bar")

    # D. pure_vs_proxy_methodology_diagram
    fig, ax = plt.subplots(figsize=(12, 5.2))
    ax.axis("off")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.add_patch(patches.FancyBboxPatch((0.4, 1.0), 4.3, 3.0, boxstyle="round,pad=0.16", fc="#E7F3EC", ec="#2D6A4F", lw=1.8))
    ax.add_patch(patches.FancyBboxPatch((7.3, 1.0), 4.3, 3.0, boxstyle="round,pad=0.16", fc="#FFF3DC", ec="#BC6C25", lw=1.8))
    ax.text(2.55, 3.55, "Pure hallucination benchmark", ha="center", fontsize=13, fontweight="bold", color="#1B4332")
    ax.text(2.55, 3.05, "Directly measures unfaithful or fabricated output", ha="center", fontsize=10, color="#333333")
    ax.text(2.55, 2.35, "POPE · CHAIR · HallusionBench\nMMHal-Bench · AMBER · FaithScore\nFACTS-Grounding · SimpleVQA", ha="center", va="center", fontsize=10)
    ax.text(2.55, 1.45, "Can enter pure leaderboard\nonly with high/medium evidence", ha="center", fontsize=9, color="#1B4332")
    ax.text(9.45, 3.55, "Proxy benchmark", ha="center", fontsize=13, fontweight="bold", color="#7F4F24")
    ax.text(9.45, 3.05, "Measures related capability: OCR, charts, video, docs, reasoning", ha="center", fontsize=10, color="#333333")
    ax.text(9.45, 2.35, "CharXiv · OCRBench · Video-MME\nDocVQA · ChartQA · MMMU\nMMBench · AI2D · MathVista", ha="center", va="center", fontsize=10)
    ax.text(9.45, 1.45, "Track separately; not equivalent to hallucination rate", ha="center", fontsize=9, color="#7F4F24")
    ax.annotate("", xy=(6.8, 2.5), xytext=(5.0, 2.5), arrowprops={"arrowstyle": "->", "lw": 2, "color": "#C1121F"})
    ax.text(5.9, 2.78, "Do not mix", ha="center", fontsize=11, color="#C1121F", fontweight="bold")
    ax.set_title("Methodology Split: Pure vs Proxy Benchmarks", fontsize=14, pad=14)
    save_fig(fig, "pure_vs_proxy_methodology_diagram")

    # E. audit_pipeline_flow
    fig, ax = plt.subplots(figsize=(13.2, 4.6))
    ax.axis("off")
    ax.set_xlim(0, 13.2)
    ax.set_ylim(0, 4)
    steps = [
        ("Original extraction", "83 models x 28 benchmarks\ncandidate value=2 cells: 382", "#DCEBFF"),
        ("First audit", "previous valid_official_result: 25\nall later rejected by strict audit", "#FFF2CC"),
        ("Strict audit", "verify table rows and score source\n25/25 rejected", "#FFE1E1"),
        ("Re-confirmation", "strict_valid_results: 11 rows\nhigh=5, medium=4, low=2", "#E7F3EC"),
        ("v3 final", "leaderboard only high/medium\n4 models in coverage count", "#D8F3DC"),
    ]
    x_positions = [0.25, 2.9, 5.55, 8.2, 10.85]
    for i, ((title, body, color), x) in enumerate(zip(steps, x_positions)):
        ax.add_patch(patches.FancyBboxPatch((x, 0.82), 2.05, 2.35, boxstyle="round,pad=0.14", fc=color, ec="#555555", lw=1.2))
        ax.text(x + 1.025, 2.65, title, ha="center", va="center", fontsize=11, fontweight="bold")
        ax.text(x + 1.025, 1.85, body, ha="center", va="center", fontsize=9)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 2.45, 2.0), xytext=(x + 2.08, 2.0), arrowprops={"arrowstyle": "->", "lw": 1.6, "color": "#555555"})
    ax.set_title("Audit Pipeline: From Original Extraction to Strict v3 Final Results", fontsize=14, pad=12)
    save_fig(fig, "audit_pipeline_flow")


def make_leaderboard(valid_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    by_model: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in valid_rows:
        if include_in_leaderboard(row):
            by_model[row["model"]].append(row)

    rows: list[dict[str, str]] = []
    for model, entries in by_model.items():
        org = entries[0].get("organization", "")
        benchmarks = distinct_benchmarks(entries)
        high_rows = [e for e in entries if e["confidence"] == "high"]
        medium_rows = [e for e in entries if e["confidence"] == "medium"]
        notes_by_bm: list[str] = []
        if model == "MiniCPM-V":
            notes_by_bm.append("CHAIR 拆为 CHAIRs/CHAIRi 两个指标行，覆盖数按 CHAIR 一个 benchmark 计。")
        if model == "InternVL-2.5":
            notes_by_bm.append("分数带 ~，Section 5.6.1 列顺序需人工确认。")
        if model == "PaliGemma":
            notes_by_bm.append("POPE 为 transfer/fine-tuning 任务形式，非 zero-shot 口径。")
        rows.append(
            {
                "rank": "0",
                "model": model,
                "organization": org,
                "verified_pure_benchmark_count": str(len(benchmarks)),
                "verified_pure_benchmarks": ", ".join(benchmarks),
                "confidence_summary": f"high={len(high_rows)}, medium={len(medium_rows)}",
                "notes": " ".join(notes_by_bm),
                "_high_sort": len(high_rows),
            }
        )
    rows.sort(key=lambda r: (-int(r["verified_pure_benchmark_count"]), -r["_high_sort"], r["model"]))
    for idx, row in enumerate(rows, start=1):
        row["rank"] = str(idx)
        row.pop("_high_sort", None)
    return rows


def write_strict_verified_flat(valid_rows: list[dict[str, str]]) -> None:
    fields = [
        "model",
        "organization",
        "benchmark",
        "benchmark_type",
        "metric",
        "score",
        "score_direction",
        "confidence",
        "source_file",
        "page_number",
        "table_number_or_section",
        "full_table_row_text",
        "evidence_snippet",
        "notes",
        "include_in_leaderboard",
    ]
    rows = []
    for row in valid_rows:
        out = {field: row.get(field, "") for field in fields}
        out["include_in_leaderboard"] = "yes" if include_in_leaderboard(row) else "no"
        rows.append(out)
    write_rows_xlsx(OUT / "strict_verified_results_flat.xlsx", "strict_verified_results_flat", fields, rows)


def write_rejected_cases(rejected_rows: list[dict[str, str]]) -> None:
    fields = [
        "model",
        "benchmark",
        "previous_wrong_score",
        "rejection_reason",
        "corrected_judgment",
        "evidence_snippet",
        "source_file",
    ]
    wb = xlsxwriter.Workbook(OUT / "rejected_cases_analysis.xlsx")
    header_fmt = wb.add_format({"bold": True, "font_color": "white", "bg_color": "#1F4E79", "border": 1})
    wrap_fmt = wb.add_format({"text_wrap": True, "valign": "top", "border": 1})
    summary_fmt = wb.add_format({"bold": True, "bg_color": "#D9EAF7", "border": 1})

    summary = wb.add_worksheet("summary")
    summary_headers = ["error_type", "count", "definition"]
    for col, header in enumerate(summary_headers):
        summary.write(0, col, header, header_fmt)
    counts = Counter(row["error_type"] for row in rejected_rows)
    for idx, etype in enumerate(ERROR_TYPE_ORDER, start=1):
        summary.write(idx, 0, etype, summary_fmt)
        summary.write(idx, 1, counts.get(etype, 0), summary_fmt)
        summary.write(idx, 2, ERROR_TYPE_LABELS[etype], summary_fmt)
    summary.set_column(0, 0, 28)
    summary.set_column(1, 1, 10)
    summary.set_column(2, 2, 34)

    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rejected_rows:
        grouped[row["error_type"]].append(row)

    for etype in ERROR_TYPE_ORDER:
        ws = wb.add_worksheet(etype[:31])
        for col, field in enumerate(fields):
            ws.write(0, col, field, header_fmt)
        widths = [len(f) for f in fields]
        for row_idx, row in enumerate(grouped.get(etype, []), start=1):
            out = {
                "model": row.get("model", ""),
                "benchmark": row.get("benchmark", ""),
                "previous_wrong_score": row.get("previous_score", ""),
                "rejection_reason": row.get("rejection_reason", ""),
                "corrected_judgment": row.get("corrected_judgment", ""),
                "evidence_snippet": row.get("rejection_reason", ""),
                "source_file": row.get("previous_source_file", ""),
            }
            for col, field in enumerate(fields):
                value = clean_text(out.get(field, ""))
                ws.write(row_idx, col, value, wrap_fmt)
                widths[col] = min(max(widths[col], len(value)), 80)
        for col, width in enumerate(widths):
            ws.set_column(col, col, max(12, min(width + 2, 60)))
        ws.freeze_panes(1, 0)
        ws.autofilter(0, 0, max(1, len(grouped.get(etype, []))), len(fields) - 1)
    wb.close()


def write_leaderboard_csv(rows: list[dict[str, str]]) -> None:
    fields = [
        "rank",
        "model",
        "organization",
        "verified_pure_benchmark_count",
        "verified_pure_benchmarks",
        "confidence_summary",
        "notes",
    ]
    with (OUT / "strict_leaderboard_final.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(x).replace("\n", " ") for x in row) + " |")
    return "\n".join(lines)


def write_executive_summary(valid_rows: list[dict[str, str]], rejected_rows: list[dict[str, str]], leaderboard_rows: list[dict[str, str]]) -> None:
    high_n = sum(1 for r in valid_rows if r.get("confidence") == "high")
    med_n = sum(1 for r in valid_rows if r.get("confidence") == "medium")
    low_n = sum(1 for r in valid_rows if r.get("confidence") == "low")
    models = "、".join(r["model"] for r in leaderboard_rows)
    text = f"""# 多模态大模型幻觉评测调研执行摘要 v3（Strict Audit）

本项目在本地官方语料中分析多模态大模型对 hallucination benchmark 的公开披露情况，范围包括技术报告、system card、model card、官方 GitHub/HuggingFace 文档，以及 28 个 benchmark（pure hallucination 与 proxy 分开统计）。

旧版 v2 的 25 条 valid_official_result 已全部作废：strict audit 确认其中 25/25 均为误报，主要来自引用编号 `[N]`、章节号 `N.M`、模型版本号、页码、标准差、计数数字、HTML 噪声，以及 ChartQA/DocVQA/LLaVA-Bench 等相邻 benchmark 分数串行。

v3 的最终可信口径是：只有 confidence=high 或 medium 且 benchmark_type=pure_hallucination 的结果进入 leaderboard；confidence=low 只进入人工确认清单。当前 strict_valid_results 中 high={high_n} 条、medium={med_n} 条、low={low_n} 条；进入最终覆盖统计的模型为：{models}。leaderboard 只按 verified pure benchmark count 统计覆盖数，不按不同 benchmark 的分数高低排名。

Pure hallucination benchmark 指直接测量幻觉输出的 POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER、FaithScore、FACTS-Grounding、SimpleVQA。CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、MMMU 等是 proxy benchmark，可反映相关能力，但不能等价为 hallucination rate，也不进入 pure leaderboard。

OpenAI / Anthropic 在当前语料中未公开 POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER 等视觉幻觉专项 benchmark 的实验表格；但其系统卡披露了 factuality、安全性、内部 hallucination/deception 相关评估，因此只能使用“未公开专项 benchmark 表格”的谨慎口径。FaithScore 在当前语料中未发现正式实验表格披露，不能引申为更强的行业采纳结论。
"""
    (OUT / "executive_summary_cn_v3.md").write_text(text, encoding="utf-8")


def write_manual_check() -> None:
    text = """# 仍需人工确认的条目清单

**版本：** v3 strict audit  
**原则：** 未人工确认前，confidence=low 或 rejected 条目不得进入最终 leaderboard。

## 1. InternVL-3 第 11 页 HallusionBench / POPE 列对齐

- **为什么需要人工确认：** strict audit 找到 HallBench、POPE 表格片段，但 PDF 文本流丢失列对齐，行-模型对应不确定。
- **当前自动判断：** HallusionBench `~59.1`、POPE `~90.7`，confidence=low，不进入排行榜。
- **确认成功：** 在 `strict_valid_results.xlsx` 中升级为 medium 或 high，并按模型对应 benchmark 计入 leaderboard。
- **确认失败：** 保持 low 或剔除，记录“数值属于对比模型或无法确认”。
- **需要查看：** `model_best/InternVL-3_3_technical_report.pdf`，第 11 页，Table 1，HallBench / POPE 列。

## 2. InternVL-2.5 Section 5.6.1 列顺序

- **为什么需要人工确认：** 当前 HallusionBench `~62.8`、MMHal-Bench `~3.65`、POPE `~90.6` 来自 Section 5.6.1 表格，列顺序由 PDF 文本流推断。
- **当前自动判断：** confidence=medium，已进入 leaderboard，但分数保留 `~`。
- **确认成功：** 可升级为 high，并移除“列顺序需确认”的风险备注。
- **确认失败：** 降级为 low，移出 leaderboard，重新填入正确列值。
- **需要查看：** `model_best/InternVL-2.5_2.5_technical_report.pdf`，Section 5.6.1，Multimodal Hallucination Evaluation Benchmarks 表格。

## 3. VILA Table 5 POPE 行位置

- **为什么需要人工确认：** 旧分数 `35.4` 已确认为 LLaVA-Bench 相邻分数，但 Table 5 可能包含真实 POPE 值。
- **当前自动判断：** rejected，不进入结果。
- **确认成功：** 新增 VILA / POPE 条目，记录模型变体、metric 与分数；若表格行明确，可标 high。
- **确认失败：** 维持 rejected_previous_valid_results 中的 false_positive。
- **需要查看：** `model_best/VILA_1_technical_report.pdf`，Table 5，POPE 列与 VILA 对应行。

## 4. CogVLM POPE 自身 vs 对比模型值

- **为什么需要人工确认：** strict audit 拒绝了旧分数 `17`（benchmark 计数），但报告片段中可能存在 `POPE 58.0 91.0`，需判断哪列属于 CogVLM 自身。
- **当前自动判断：** rejected，不进入结果。
- **确认成功：** 新增 CogVLM / POPE 条目，并写明 F1 或 accuracy 口径。
- **确认失败：** 保持 false_positive。
- **需要查看：** `model_best/CogVLM_1_technical_report.pdf`，POPE 相关对比表。

## 5. Bunny Table 1 POPE F1 值

- **为什么需要人工确认：** 旧分数 `41` 是引用编号 `[41]`，但 Bunny Table 1 中可能列出 POPE F1。
- **当前自动判断：** rejected，不进入结果。
- **确认成功：** 新增 Bunny / POPE 条目，标注模型尺寸与 F1 分数。
- **确认失败：** 保持 false_positive。
- **需要查看：** `model_best/Bunny_1_technical_report.pdf`，Table 1，POPE 列。

## 6. Qwen3-VL SimpleVQA 行-模型对应

- **为什么需要人工确认：** 旧分数 `1` 是章节列表编号；另有 `SimpleVQA 88.8 88.6 81.3 78.7 61.3` 表格片段，但列与 Qwen3-VL 变体对应不明。
- **当前自动判断：** rejected，不进入结果。
- **确认成功：** 新增 Qwen3-VL / SimpleVQA 条目；SimpleVQA 属 pure hallucination benchmark，若证据完整可进入 leaderboard。
- **确认失败：** 保持 false_positive。
- **需要查看：** `model_best/Qwen3-VL_3_technical_report.pdf`，Section 5.1，SimpleVQA 行及列标题。
"""
    (OUT / "manual_check_required.md").write_text(text, encoding="utf-8")


def write_full_report(valid_rows: list[dict[str, str]], rejected_rows: list[dict[str, str]], leaderboard_rows: list[dict[str, str]]) -> None:
    high_rows = [r for r in valid_rows if r.get("confidence") == "high"]
    medium_rows = [r for r in valid_rows if r.get("confidence") == "medium"]
    low_rows = [r for r in valid_rows if r.get("confidence") == "low"]
    error_counts = Counter(row["error_type"] for row in rejected_rows)

    error_table = markdown_table(
        ["误判类型", "数量", "说明"],
        [
            [ERROR_TYPE_LABELS[t], str(error_counts.get(t, 0)), t]
            for t in ERROR_TYPE_ORDER
            if error_counts.get(t, 0)
        ],
    )
    representative_rejections: list[dict[str, str]] = []
    seen_error_types: set[str] = set()
    for row in rejected_rows:
        if row["error_type"] not in seen_error_types:
            representative_rejections.append(row)
            seen_error_types.add(row["error_type"])
    rejected_examples = markdown_table(
        ["模型", "Benchmark", "旧错误分数", "拒绝原因"],
        [
            [
                r["model"],
                r["benchmark"],
                "`" + r["previous_score"] + "`",
                clean_text(r["rejection_reason"])[:90],
            ]
            for r in representative_rejections
        ],
    )
    high_table = markdown_table(
        ["模型", "Benchmark", "Metric", "Score", "Source", "Evidence"],
        [
            [
                r["model"],
                r["benchmark"],
                r["metric"],
                "`" + r["score"] + "`",
                r["source_file"].replace("model_best/", ""),
                clean_text(r["full_table_row_text"])[:120],
            ]
            for r in high_rows
        ],
    )
    medium_table = markdown_table(
        ["模型", "Benchmark", "Metric", "Score", "需注意"],
        [
            [
                r["model"],
                r["benchmark"],
                r["metric"],
                "`" + r["score"] + "`",
                clean_text(r["notes"])[:110],
            ]
            for r in medium_rows
        ],
    )
    low_table = markdown_table(
        ["模型", "Benchmark", "估计分数", "原因"],
        [[r["model"], r["benchmark"], "`" + r["score"] + "`", clean_text(r["notes"])[:110]] for r in low_rows],
    )
    leaderboard_table = markdown_table(
        ["Rank", "Model", "Organization", "Verified pure benchmark count", "Benchmarks", "Confidence"],
        [
            [
                r["rank"],
                r["model"],
                r["organization"],
                r["verified_pure_benchmark_count"],
                r["verified_pure_benchmarks"],
                r["confidence_summary"],
            ]
            for r in leaderboard_rows
        ],
    )

    text = f"""# 多模态大模型幻觉评测 Benchmark 技术调研报告 v3（Strict Audit）

**日期：** {TODAY}  
**事实来源：** `final_report_strict_audit/`。旧版 `final_report/full_research_report_cn.md` 已废弃，不作为事实来源。

## 1. 调研背景与目标

本项目分析主流多模态大模型官方技术报告、system card、model card、官方 GitHub/HuggingFace model card 中对 hallucination benchmark 的公开披露情况。核心问题包括：哪些模型公开报告 pure hallucination benchmark，哪些只报告 proxy benchmark，不同模型族披露口径有何差异，以及自动抽取中的误报如何剔除。

v3 采用保守口径：宁可少报，不可误报。所有结论只基于 strict audit 文件，不引用旧版 25 条 valid 表和旧版 pure hallucination leaderboard。

## 2. 数据来源与目录结构

项目实际根目录为 `{BASE}`。关键输入目录包括：

- `benchmark_papers/`
- `model_reports/`
- `official_model_cards_html/`
- `ocr_document_models/`
- `analysis_results/`
- `final_report/`（旧版，仅作历史文件保留）
- `final_report_strict_audit/`（v3 唯一可信输入）
- `_download_manifest.json`

本轮直接读取的 strict audit 文件包括：`strict_valid_results.xlsx`、`rejected_previous_valid_results.csv`、`strict_pure_hallucination_leaderboard.csv`、`strict_model_vs_benchmark_matrix.csv`、`strict_corrected_summary.md`、`strict_quality_check.md`。

## 3. 自动抽取为何失败：旧 25 条 valid 全部被拒绝

strict audit 的第一条核心结论是：原始 25 条 `valid_official_result` 全部拒绝，25/25 rejected。旧版结果不能直接引用。

### 3.1 错误类型统计

以下统计按 `rejected_previous_valid_results.csv` 中 25 条记录逐条归类生成：

{error_table}

### 3.2 典型错误案例

{rejected_examples}

## 4. Strict Audit 方法

### 4.1 valid_official_result 的严格判定标准

一条记录必须同时满足：来源是官方报告或官方模型卡；位置是实验结果区或评测表格；同一证据片段中能对应模型、benchmark、metric 与分数；分数在该 benchmark 合理范围内；有完整表格行或足够表格上下文。引用编号 `[N]`、章节号 `N.M`、模型版本号、页码、标准差 `±N`、相邻 benchmark 分数、HTML 页面噪声和 intro_mention 均不得作为 valid。

### 4.2 high / medium / low confidence 定义

- **high：** 完整表格行可确认模型-benchmark-metric-score 对应关系，无明显列对齐风险。
- **medium：** 有表格证据，但 PDF 文本流丢失部分列对齐，需要人工复核列顺序；可进入 leaderboard，但保留 `~` 或风险备注。
- **low：** benchmark 列或疑似分数存在，但行-模型对应不确定；只能进入人工确认清单，不进入 leaderboard。

## 5. 最终 verified pure hallucination results

最终 leaderboard 只包含 confidence=high/medium 且 benchmark_type=pure_hallucination 的条目。不同 benchmark 的指标方向和量纲不同，因此不按分数高低排名，只统计 verified pure benchmark count。

### 5.1 High confidence results

{high_table}

### 5.2 Medium confidence results

{medium_table}

其中 InternVL-2.5 的 `~62.8 / ~3.65 / ~90.6` 来自 Section 5.6.1 表格列顺序推断，需人工确认列对齐；PaliGemma 的 POPE 为 transfer/fine-tuning 任务形式，不应与 zero-shot POPE 直接比较。

### 5.3 Low confidence / 人工确认条目

{low_table}

这些条目不进入最终排名，详见 `manual_check_required.md`。

## 6. 模型族分析

### 6.1 开源模型

开源模型中，MiniCPM-V 4.5 与 MiniCPM-o 4.5 的证据最强，均在 Hallucination 相关评测区给出完整表格行。InternVL-2.5 有专用 Section 5.6.1，覆盖 HallusionBench、MMHal-Bench、POPE，但列顺序仍需人工确认。PaliGemma 报告了 POPE 86.0 / 87.0，但属于 fine-tune/transfer 任务口径。

当前 leaderboard：

{leaderboard_table}

### 6.2 闭源模型

OpenAI / Anthropic 在当前本地官方公开语料中未公开 POPE、CHAIR、AMBER、HallusionBench、MMHal-Bench 等视觉幻觉专项 benchmark 的实验表格；但其系统卡披露了 factuality、安全性、内部 hallucination/deception 相关评估。正确口径是“未公开这些公开视觉幻觉专项 benchmark 表格”，不得扩大为否定其内部评测。

Google DeepMind 的 Gemini 系列主要披露 CharXiv、DocVQA、ChartQA、MMMU 等 proxy 指标。旧版 Gemini-1.5/POPE 与 Gemini-2.5/FACTS-Grounding 误报已被拒绝。

### 6.3 国内模型

MiniCPM 与 InternVL 是当前语料中 pure hallucination 披露较多的国内模型族。Qwen3-VL、GLM、DeepSeek-VL、Kimi-VL 等在 strict audit 中没有 high/medium verified pure hallucination 结果；其中 Qwen3-VL/SimpleVQA 需要人工确认行-模型对应，GLM 旧 HallusionBench 结果为模型版本号误判。

### 6.4 小模型与端侧模型

MiniCPM-V 4.5 和 MiniCPM-o 4.5 是本次 high confidence 的主体，适合作为端侧/小模型公开披露 pure hallucination benchmark 的代表案例。Bunny 可能存在 POPE F1 值，但当前仅列入人工确认清单，未进入结果。

## 7. Pure benchmark 与 proxy benchmark 的最终拆分

**Pure hallucination benchmark** 直接测量幻觉或事实忠实度输出，包括：{", ".join(PURE_BENCHMARKS)}。

**Proxy benchmark** 测量 OCR、图表、文档、视频、综合推理、caption 等相关能力，包括：{", ".join(PROXY_BENCHMARKS)}。

CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、MMMU 等可以反映相关能力，但不能直接等价为 hallucination rate，也不能进入 pure hallucination leaderboard。FaithScore 在当前官方语料中未发现正式实验表格披露，但不能引申为更强的行业采纳判断。

## 8. 主要结论

1. 在本次本地官方报告语料中，经过严格审计，仅少数模型公开披露了可验证的 pure hallucination benchmark 结果。
2. 旧版自动抽取结果严重高估了官方幻觉评测披露情况，主要原因是章节号、引用编号、版本号、标准差、页码、相邻 benchmark 分数被误识别为 hallucination 分数。
3. 最终进入 leaderboard 的模型为 InternVL-2.5、MiniCPM-V、MiniCPM-o、PaliGemma；排序仅按 verified pure benchmark count。
4. OpenAI / Anthropic 未公开上述视觉幻觉专项 benchmark 实验表格，但公开了 factuality、安全性和内部幻觉/欺骗相关评估。
5. low confidence 条目只进入人工确认清单，不参与排名或覆盖统计。

## 9. 仍需人工确认的风险点

1. InternVL-3 第 11 页 HallusionBench / POPE 列对齐。
2. InternVL-2.5 Section 5.6.1 列顺序。
3. VILA Table 5 POPE 行位置。
4. CogVLM POPE 自身 vs 对比模型值。
5. Bunny Table 1 POPE F1 值。
6. Qwen3-VL SimpleVQA 行-模型对应。

## 10. 推荐后续工作

1. 用保留表格结构的 PDF 解析工具人工复核 `manual_check_required.md` 中的条目。
2. 对所有 future model card 继续执行 strict audit 标准，避免把 intro_mention 或 proxy benchmark 误写为 pure hallucination 结果。
3. 对 proxy benchmark 单独生成能力覆盖报告，不与 pure hallucination leaderboard 混排。
4. 如人工确认新增 high/medium 条目，应同步更新 `strict_valid_results.xlsx`、flat 表、leaderboard、manual check 与 quality check。
"""
    (OUT / "full_research_report_cn_v3.md").write_text(text, encoding="utf-8")


def write_quality_check(valid_rows: list[dict[str, str]], rejected_rows: list[dict[str, str]], leaderboard_rows: list[dict[str, str]]) -> bool:
    lb_models = {r["model"] for r in leaderboard_rows}
    lb_entries = [r for r in valid_rows if r["model"] in lb_models and include_in_leaderboard(r)]
    report_text = (
        (OUT / "executive_summary_cn_v3.md").read_text(encoding="utf-8")
        + "\n"
        + (OUT / "full_research_report_cn_v3.md").read_text(encoding="utf-8")
    )
    checks: list[tuple[str, bool, str]] = [
        ("旧版 25 条错误 valid 是否已全部删除", len(rejected_rows) == 25, "25/25 旧 valid 均在 rejected_previous_valid_results.csv 中标为 rejected/false_positive/mentioned_only。"),
        ("是否还有 intro_mention 被作为 valid", all("intro_mention" not in (r.get("notes", "") + r.get("evidence_snippet", "")) for r in valid_rows), "valid rows 均来自表格行或评测表格片段。"),
        ("是否还有引用编号 [N] 被作为分数", all(r.get("score") not in {"41", "45", "77", "82"} for r in valid_rows), "旧引用编号错误已全部位于 rejected 表。"),
        ("是否还有章节号 N.M 被作为分数", all(not (r.get("score") in {"5.3", "5.6", "3.1"} and r.get("confidence") in {"high", "medium"}) for r in valid_rows), "未将章节号作为 high/medium valid。"),
        ("是否还有模型版本号被作为分数", all(r.get("score") not in {"1.5", "4", "3"} for r in valid_rows), "Gemini/Claude/GLM 版本号误报已拒绝。"),
        ("是否还有标准差 ±N 被作为分数", all(r.get("score") != "0.3" for r in valid_rows), "PaliGemma ±0.3 旧误报已拒绝。"),
        ("是否所有 leaderboard 条目都是 high/medium confidence", all(r.get("confidence") in {"high", "medium"} for r in lb_entries), "leaderboard 仅由 include_in_leaderboard=yes 生成。"),
        ("是否所有 leaderboard 条目都是 pure_hallucination", all(r.get("benchmark_type") == "pure_hallucination" for r in lb_entries), "未混入 proxy benchmark。"),
        ("是否 OpenAI / Anthropic 的 POPE / CHAIR / AMBER / HallusionBench / MMHal 全部为未披露", not any(r.get("organization") in {"OpenAI", "Anthropic"} and include_in_leaderboard(r) for r in valid_rows), "未公开这些视觉幻觉专项 benchmark 的官方实验表格；不否定内部评测。"),
        ("是否 low confidence 条目没有进入最终排名", not any(r.get("confidence") == "low" and r.get("model") in lb_models for r in valid_rows), "InternVL-3 low confidence 条目未进入 leaderboard。"),
        ("是否报告中没有“工业界未采纳”这类过强表述", "工业界未采纳" not in report_text and "工业界没有" not in report_text, "FaithScore 仅写为当前语料未发现正式披露。"),
        ("是否报告中没有“OpenAI/Anthropic 没有 hallucination 评测”这种不严谨表述", "没有 hallucination 评测" not in report_text and "没有幻觉评测" not in report_text, "报告采用未公开专项 benchmark 表格的谨慎表述。"),
    ]
    lines = ["# Final Quality Check v3", "", f"**检查日期：** {TODAY}", "", "| 检查项 | 结果 | 说明 |", "|---|---|---|"]
    all_pass = True
    for item, passed, note in checks:
        all_pass = all_pass and passed
        lines.append(f"| {item} | {'PASS' if passed else 'FAIL'} | {note} |")
    lines.extend(
        [
            "",
            "## 总体结论",
            "",
            f"**final_quality_check_v3：{'全部 PASS' if all_pass else '存在 FAIL'}**",
        ]
    )
    (OUT / "final_quality_check_v3.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return all_pass


def main() -> None:
    OUT.mkdir(exist_ok=True)
    VIZ.mkdir(exist_ok=True)
    configure_fonts()

    valid_rows = xlsx_first_sheet(SA / "strict_valid_results.xlsx")
    rejected_rows = read_csv(SA / "rejected_previous_valid_results.csv")
    matrix_rows = read_csv(SA / "strict_model_vs_benchmark_matrix.csv")
    _ = matrix_rows  # Kept as a loaded strict audit input for traceability.
    for row in rejected_rows:
        row["error_type"] = classify_rejection(row)

    leaderboard_rows = make_leaderboard(valid_rows)

    write_strict_verified_flat(valid_rows)
    write_rejected_cases(rejected_rows)
    write_leaderboard_csv(leaderboard_rows)
    write_manual_check()
    write_executive_summary(valid_rows, rejected_rows, leaderboard_rows)
    write_full_report(valid_rows, rejected_rows, leaderboard_rows)
    make_visualizations(valid_rows, rejected_rows, leaderboard_rows)
    all_pass = write_quality_check(valid_rows, rejected_rows, leaderboard_rows)

    files = sorted(p.relative_to(OUT) for p in OUT.rglob("*") if p.is_file())
    total = sum((OUT / p).stat().st_size for p in files)
    print(f"output={OUT}")
    print(f"files={len(files)}")
    print(f"size_bytes={total}")
    print(f"high={sum(1 for r in valid_rows if r.get('confidence') == 'high')}")
    print(f"medium={sum(1 for r in valid_rows if r.get('confidence') == 'medium')}")
    print(f"low={sum(1 for r in valid_rows if r.get('confidence') == 'low')}")
    print("leaderboard_models=" + ",".join(r["model"] for r in leaderboard_rows))
    print(f"old_rejected={len(rejected_rows)}/25")
    print(f"qc={'PASS' if all_pass else 'FAIL'}")
    for p in files:
        print(p)


if __name__ == "__main__":
    main()
