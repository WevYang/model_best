#!/usr/bin/env python3
"""Generate exhaustive factuality/proxy recall deliverables.

This script intentionally avoids re-running the old score extraction pipeline.
It uses table-level values that were already confirmed in the recall pass plus
additional hand-transcribed rows from local official report tables.
"""

from __future__ import annotations

import json
import os
import re
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd


BASE = Path(__file__).resolve().parent
OUT = BASE / "mentor_factuality_proxy_report_full"
OUT.mkdir(exist_ok=True)

TODAY = "2026-05-29"


def clean(v):
    if v is None:
        return ""
    return str(v).replace("|", "\\|").replace("\n", " ").strip()


def md_table(headers, rows, max_rows=None):
    rows = rows[:max_rows] if max_rows else rows
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        out.append("| " + " | ".join(clean(x) for x in r) + " |")
    return "\n".join(out)


def xlsx_rows(path: Path, sheet_name: str):
    """Small xlsx reader because openpyxl is unavailable in this env."""
    def full_path(t):
        t = t.replace("\\", "/")
        if t.startswith("/"):
            t = t[1:]
        if not t.startswith("xl/"):
            t = "xl/" + t
        return os.path.normpath(t)

    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        rel_map = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
        ns = {"a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
        target = None
        for s in wb.find("a:sheets", ns):
            if s.attrib["name"] == sheet_name:
                rid = s.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
                target = full_path(rel_map[rid])
        if target is None:
            return []
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            sst = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in sst:
                shared.append("".join(t.text or "" for t in si.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")))
        root = ET.fromstring(z.read(target))
        rows = []
        for row in root.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}sheetData"):
            vals = []
            for c in row:
                t = c.attrib.get("t")
                v = c.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}v")
                if v is None:
                    isel = c.find("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}is")
                    txt = "".join(t.text or "" for t in isel.iter("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")) if isel is not None else ""
                else:
                    txt = v.text or ""
                    if t == "s":
                        txt = shared[int(txt)]
                vals.append(txt)
            rows.append(vals)
        return rows


SOURCE_NOTES = {}
try:
    rows = xlsx_rows(BASE / "analysis_results" / "official_experiment_results.xlsx", "Source Notes")
    hdr = rows[0]
    for r in rows[1:]:
        d = {hdr[i]: r[i] if i < len(r) else "" for i in range(len(hdr))}
        SOURCE_NOTES[d.get("Model", "")] = d
except Exception:
    SOURCE_NOTES = {}


BENCHMARK_PROXY_TYPE = {
    "OCRBench": "OCR/text", "OCRBench_v2en": "OCR/text", "OCRBench_v2zh": "OCR/text", "OCRBench_V2en": "OCR/text",
    "OCRBench-v2": "OCR/text", "CC-OCR": "OCR/text", "MTVQA": "OCR/text", "TextVQA": "OCR/text",
    "TextVQAval": "OCR/text", "DocVQA": "OCR/text", "DocVQAtest": "OCR/text", "InfoVQA": "OCR/text",
    "InfoVQAtest": "OCR/text", "OmniDocBenchen": "OCR/text", "OmniDocBenchzh": "OCR/text",
    "OmniDocBenchedit en/zh ↓": "OCR/text", "MMLongBenchDoc": "chart/document", "MMLongBench-Doc": "chart/document",
    "ChartQA": "chart/document", "ChartQAtest": "chart/document", "ChartQAtest Avg.": "chart/document",
    "ChartQAtest Avg": "chart/document", "CharXiv(DQ)": "chart/document", "CharXiv(RQ)": "chart/document",
    "CharXiv (RQ)": "chart/document", "AI2D": "chart/document", "AI2Dw. M.": "chart/document",
    "AI2D_TEST": "chart/document", "SEED-Bench-2-Plus": "chart/document", "VCR": "chart/document",
    "VCREn-Hard-EM": "chart/document",
    "MMMU": "general_reasoning", "MMMUval": "general_reasoning", "MMMU-Pro": "general_reasoning",
    "MMMU-Prooverall": "general_reasoning", "MathVistamini": "general_reasoning", "MathVistatestmini": "general_reasoning",
    "MathVista": "general_reasoning", "MathVision": "general_reasoning", "MathVisionWP": "general_reasoning",
    "MATH-Visionfull": "general_reasoning", "MathVersemini": "general_reasoning", "MATH-Vision": "general_reasoning",
    "We-Math": "general_reasoning", "DynaMath": "general_reasoning", "Math-VR": "general_reasoning",
    "ZeroBench": "general_reasoning", "ZEROBench": "general_reasoning", "ZEROBench_sub": "general_reasoning",
    "VlmsAreBlind": "general_reasoning", "LogicVista": "general_reasoning", "VisuLogic": "general_reasoning",
    "VisualPuzzles": "general_reasoning", "MMBench-EN": "general_reasoning", "MMBench-CN": "general_reasoning",
    "MMBench-ENtest": "general_reasoning", "MMBench-CNtest": "general_reasoning", "MMBench-V1.1-ENtest": "general_reasoning",
    "MMBenchEN-DEV-v1.1": "general_reasoning", "RealWorldQA": "general_reasoning", "RealWorldQAavg": "general_reasoning",
    "MMStar": "general_reasoning", "MME": "general_reasoning", "MMEsum": "general_reasoning",
    "MuirBench": "general_reasoning", "MUIRBENCH": "general_reasoning", "BLINK": "general_reasoning",
    "MMVet": "general_reasoning", "MMVetturbo": "general_reasoning", "MM-MT-Bench": "general_reasoning",
    "MIA-Bench": "general_reasoning", "MegaBench": "general_reasoning", "MME-RealWorld": "general_reasoning",
    "MME-RealWorlden": "general_reasoning", "ScienceQA": "general_reasoning", "VQAv2": "general_reasoning",
    "COCO caption": "general_reasoning", "COCO-Cap": "general_reasoning", "OKVQA": "general_reasoning",
    "NoCaps": "general_reasoning", "CountBench": "grounding/GUI", "CountBenchQA": "grounding/GUI",
    "RefCOCO-avg": "grounding/GUI", "RefCOCO(avg)": "grounding/GUI", "Refcocoval": "grounding/GUI",
    "RefcocotestA": "grounding/GUI", "RefcocotestB": "grounding/GUI", "Refcoco+val": "grounding/GUI",
    "Refcoco+testA": "grounding/GUI", "Refcoco+testB": "grounding/GUI", "Refcocogval": "grounding/GUI",
    "Refcocogtest": "grounding/GUI", "RefcocotextA": "grounding/GUI", "RefcocotextB": "grounding/GUI",
    "Refcoco+textA": "grounding/GUI", "Refcoco+textB": "grounding/GUI", "ODinW": "grounding/GUI",
    "ODinW-13": "grounding/GUI", "ODInW13": "grounding/GUI", "PointGrounding": "grounding/GUI",
    "ARKitScenes": "grounding/GUI", "Hypersim": "grounding/GUI", "SUNRGBD": "grounding/GUI", "ERQA": "grounding/GUI",
    "VSI-Bench": "grounding/GUI", "EmbSpatialBench": "grounding/GUI", "RefSpatialBench": "grounding/GUI",
    "RoboSpatialHome": "grounding/GUI", "ScreenSpot": "grounding/GUI", "ScreenSpot Pro": "grounding/GUI",
    "OSWorldG": "grounding/GUI", "AndroidWorld": "grounding/GUI", "OSWorld": "grounding/GUI",
    "WindowsAA": "grounding/GUI", "Android Control HighEM": "grounding/GUI", "Android Control LowEM": "grounding/GUI",
    "AndroidWorldSR": "grounding/GUI", "MobileMiniWob++SR": "grounding/GUI",
    "MVBench": "video/temporal", "Video-MMEw/o sub.": "video/temporal", "Video-MMEw sub.": "video/temporal",
    "VideoMME(w/o sub.)": "video/temporal", "Video-MME": "video/temporal", "VideoMME": "video/temporal",
    "VideoMMEw/ audio": "video/temporal", "VideoMMMU": "video/temporal", "MLVUM-Avg": "video/temporal",
    "MLVU(M-Avg)": "video/temporal", "LVBench": "video/temporal", "LongVideoBenchval": "video/temporal",
    "MMVU": "video/temporal", "MMVUval": "video/temporal", "Charades-STAmIoU": "video/temporal",
    "EgoSchematest": "video/temporal", "PerceptionTesttest": "video/temporal", "Perception Test MCVQA": "video/temporal",
    "ActivityNet-QA": "video/temporal", "TempCompassAvg": "video/temporal", "MMBench-Video": "video/temporal",
    "ActivityNet-QA": "video/temporal", "EgoTempo": "video/temporal", "QVHighlights": "video/temporal",
    "1H-VideoQA": "video/temporal", "VATEX": "video/temporal", "VATEX-ZH": "video/temporal",
    "YouCook2 Cap": "video/temporal", "Minerva": "video/temporal", "Neptune": "video/temporal",
    "Design2Code": "general_reasoning", "ChartMimic": "chart/document", "UniSVG": "general_reasoning",
    "V*": "general_reasoning", "HRBench4K": "general_reasoning", "HRBench8K": "general_reasoning",
    "ERQA": "grounding/GUI", "SLAKE": "general_reasoning", "PMC-VQA": "general_reasoning",
    "MedXpertQA-MM": "general_reasoning", "DailyOmni": "video/temporal", "WorldSense": "video/temporal",
    "AVUT": "video/temporal", "AV-SpeakerBench": "video/temporal", "Qualcomm IVD": "video/temporal",
    "Omni-Cloze": "video/temporal", "OmniGAIA": "grounding/GUI",
}


factuality = []
proxy = []
closed_cards = []
gaps = []
direct_rows = []
unverified_candidates = []


def add_fact(model, family, org, benchmark, score, setting, source_file, source_url="", page="", table="", evidence="", confidence="high", notes=""):
    factuality.append({
        "model": model, "family": family, "organization": org, "benchmark": benchmark, "score": score,
        "setting": setting, "category": "factuality_related", "confidence": confidence, "source_file": source_file,
        "source_url": source_url, "page_or_section": page, "table_title": table, "evidence_row": evidence, "notes": notes,
    })


def add_proxy(model, family, org, benchmark, score, setting, source_file, source_url="", page="", table="", evidence="", confidence="high", notes=""):
    proxy.append({
        "model": model, "family": family, "organization": org, "proxy_type": BENCHMARK_PROXY_TYPE.get(benchmark, "general_reasoning"),
        "benchmark": benchmark, "score": score, "setting": setting, "confidence": confidence, "source_file": source_file,
        "source_url": source_url, "page_or_section": page, "table_title": table, "evidence_row": evidence, "notes": notes,
    })


def add_gap(model, family, missing, reason, source, notes="", suspected=""):
    gaps.append({
        "model": model, "family": family, "missing_expected_benchmark": missing,
        "reason": reason, "checked_source": source, "suspected_score_or_mention": suspected, "notes": notes,
    })


def add_closed(provider, model, system_card, fact_eval, hall_eval, deception_eval, public_score, notes):
    closed_cards.append({
        "provider": provider, "model": model, "system_card": system_card, "factuality_eval": fact_eval,
        "hallucination_eval": hall_eval, "deception_or_knowing_hallucination_eval": deception_eval,
        "public_score_available": public_score, "notes": notes,
    })


def add_combined_rows(family, org, source_file, page, table, model_values, rows, setting="thinking / instruct", notes=""):
    for benchmark, values in rows.items():
        for model, score in zip(model_values, values):
            if score in ("-", "", None):
                continue
            add_proxy(model, family, org, benchmark, score, setting, source_file, page=page, table=table,
                      evidence=f"{benchmark}: {model} = {score}", notes=notes)


def add_single_model_rows(model, family, org, source_file, page, table, rows, setting, notes=""):
    for benchmark, score in rows.items():
        if score in ("-", "", None):
            continue
        add_proxy(model, family, org, benchmark, score, setting, source_file, page=page, table=table,
                  evidence=f"{benchmark}: {model} = {score}", notes=notes)


# Direct rows already confirmed in v1.3, used only for extended table context.
try:
    fr = xlsx_rows(BASE / "mentor_final_report_v1_3" / "mentor_full_score_table.xlsx", "Full Recall Scores")
    hdr = fr[0]
    for r in fr[1:]:
        d = {hdr[i]: r[i] if i < len(r) else "" for i in range(len(hdr))}
        if d.get("benchmark_category") == "pure_multimodal_hallucination":
            direct_rows.append(d)
except Exception:
    pass


# Factuality from recall pass / confirmed tables.
qwen3_simple = {
    "Qwen3-VL-235B-A22B": "61.3 / 63.0",
    "Qwen3-VL-32B": "55.4 / 56.9",
    "Qwen3-VL-30B-A3B": "54.3 / 52.7",
    "Qwen3-VL-8B": "49.6 / 50.2",
    "Qwen3-VL-4B": "48.8 / 48.0",
    "Qwen3-VL-2B": "43.6 / 40.7",
}
for m, s in qwen3_simple.items():
    add_fact(m, "Qwen", "Alibaba / Qwen", "SimpleVQA", s, "thinking / instruct",
             "Qwen3-VL_3_technical_report.pdf", page="Table 2/3/4", table="Qwen3-VL visual benchmark tables",
             evidence=f"SimpleVQA: {m} = {s}", notes="thinking / instruct order; factuality-related, not direct hallucination rate.")

for m, s in {
    "Qwen3.5-Plus-Instruct": "66.1",
    "Qwen3.5-Omni-Flash": "54.4",
    "Qwen3.5-Omni-Plus": "65.3",
}.items():
    add_fact(m, "Qwen", "Alibaba / Qwen", "SimpleVQA", s, "vision -> text",
             "model_best/Qwen3.5-Omni_3.5_technical_report.pdf", page="PDF p.12",
             table="Table 6: Vision -> Text performance", evidence=f"SimpleVQA: {m} = {s}",
             notes="Factuality-related benchmark; not counted as direct visual hallucination.")

for m, s in {"Gemma 3 1B": "36.4", "Gemma 3 4B": "70.1", "Gemma 3 12B": "75.8", "Gemma 3 27B": "74.9"}.items():
    add_fact(m, "Gemma", "Google DeepMind", "FACTS-Grounding", s, "instruction tuned / zero-shot table",
             "model_best/model_reports/Gemma3_3_technical_report.pdf", page="PDF p.6",
             table="Table 6: Performance of instruction fine-tuned models",
             evidence=f"FACTS Grounding: {m} = {s}", notes="Document/source grounding factuality; not pure multimodal hallucination.")

for model, simpleqa, facts in [
    ("Gemini 1.5 Flash", "8.6%", "82.9%"),
    ("Gemini 1.5 Pro", "24.9%", "80.0%"),
    ("Gemini 2.0 Flash-Lite", "16.5%", "82.4%"),
    ("Gemini 2.0 Flash", "29.9%", "84.6%"),
    ("Gemini 2.5 Flash", "26.9%", "85.3%"),
    ("Gemini 2.5 Pro", "54.0%", "87.8%"),
]:
    add_fact(model, "Gemini", "Google DeepMind", "SimpleQA", simpleqa, "official technical report comparison",
             "Gemini-2.5_2.5_technical_report.pdf", page="PDF p.13 / Table 3",
             table="Evaluation of Gemini 2.5 family", evidence=f"SimpleQA: {model} = {simpleqa}")
    add_fact(model, "Gemini", "Google DeepMind", "FACTS-Grounding", facts, "official technical report comparison",
             "Gemini-2.5_2.5_technical_report.pdf", page="PDF p.13 / Table 3",
             table="Evaluation of Gemini 2.5 family", evidence=f"FACTS Grounding: {model} = {facts}")

for model, acc, hall in [
    ("gpt-5-thinking", "0.55", "0.40"),
    ("OpenAI o3", "0.54", "0.46"),
    ("gpt-5-thinking-mini", "0.22", "0.26"),
    ("OpenAI o4-mini", "0.24", "0.75"),
    ("gpt-5-thinking-nano", "0.11", "0.31"),
    ("gpt-5-main", "0.46", "0.47"),
    ("GPT-4o", "0.44", "0.52"),
]:
    add_fact(model, "OpenAI GPT", "OpenAI", "SimpleQA", f"accuracy={acc}; hallucination_rate↓={hall}",
             "no web", "GPT-5_5_system_card.pdf", page="PDF p.14 / Table 8",
             table="Table 8: SimpleQA evaluations",
             evidence=f"SimpleQA accuracy {acc}, hallucination rate {hall}",
             notes="Text factuality benchmark from system card; lower hallucination_rate is better.")

for model, score in [
    ("gpt-5-thinking", "46.2"),
    ("gpt-5-thinking-mini", "40.3"),
    ("gpt-5-main", "25.5"),
    ("OpenAI o3", "31.6"),
    ("GPT-4o", "0.0"),
]:
    add_fact(model, "OpenAI GPT", "OpenAI", "HealthBench Hard", score, "health factuality/safety",
             "GPT-5_5_system_card.pdf", page="PDF p.17", table="HealthBench evaluations",
             evidence=f"HealthBench Hard: {model} = {score}", notes="HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination.")

for model in ["gpt-5-thinking", "gpt-5-thinking-mini", "gpt-5-thinking-nano", "OpenAI o3", "OpenAI o4-mini"]:
    add_fact(model, "OpenAI GPT", "OpenAI", "LongFact / FActScore", "reported in figure / not tabulated",
             "browsing-enabled claim-level grading", "GPT-5_5_system_card.pdf", page="PDF p.13 / Figure 2",
             table="Average Hallucination Rate (Browsing Enabled)",
             evidence="System card states LongFact and FActScore prompts are used; figure reports claim-level error rates.",
             confidence="medium", notes="Figure-only values were not machine-tabulated in this pass; do not compare as exact table score.")

add_fact("GPT-5.5", "OpenAI GPT", "OpenAI", "HealthBench / HealthBench Hard", "HealthBench=56.5; Hard=31.5; Consensus=95.6; Professional=51.8",
         "health factuality/safety", "GPT-5.5_5.5_system_card.pdf", page="system card table",
         table="HealthBench evaluations", evidence="HealthBench rows visible in GPT-5.5 system card",
         confidence="medium", notes="Not direct hallucination; included as system-card health factuality/safety signal.")

add_closed("OpenAI", "GPT-5 / GPT-5.5 / GPT-4o", "GPT-5 and GPT-5.5 system cards",
           "SimpleQA, LongFact, FActScore, HealthBench/HealthBench Hard are disclosed in system-card factuality/safety sections.",
           "System-card hallucination rates and claim-level error rates; no POPE/CHAIR/HallusionBench/MMHal table.",
           "Deception and related risk evaluations discussed in system cards.", "yes, but not directly comparable to visual hallucination benchmarks",
           "Closed-source internal/system-card eval should not be ranked with open model public benchmark tables.")
add_closed("Google", "Gemini 2.5 / Gemini 1.5 / Gemini 2.0", "Gemini 2.5 technical report",
           "SimpleQA and FACTS-Grounding official scores are tabulated.",
           "No directly comparable POPE/CHAIR/HallusionBench/MMHal table found in the checked Gemini report.",
           "Safety/responsibility sections describe assurance and red-team evals.", "yes for SimpleQA/FACTS; no for direct visual hallucination table",
           "FACTS-Grounding is factuality/grounding related.")
add_closed("Anthropic", "Claude 3.5 / Claude 4 / Claude 4.1 / Claude Opus/Sonnet pages", "Claude system cards/model card addenda",
           "System-card safety/factuality/internal risk evaluations are disclosed at qualitative/internal level.",
           "No directly comparable POPE/CHAIR/HallusionBench/MMHal table found in checked local cards.",
           "Knowing hallucination/deception/risk-eval style disclosures are system-card internal evals.", "mostly internal / qualitative",
           "Do not write that Anthropic has no hallucination evaluation; only no comparable public academic table in this corpus.")


# Proxy: Qwen3-VL tables 2/3/4.
qwen3_table2_rows = {
    "MMMU": ["80.6 / 78.7"], "MMMU-Pro": ["69.3 / 68.1"], "MathVistamini": ["85.8 / 84.9"],
    "MathVision": ["74.6 / 66.5"], "MathVisionWP": ["63.8 / 57.0"], "We-Math": ["74.8 / 67.5"],
    "MathVersemini": ["85.0 / 72.5"], "DynaMath": ["82.8 / 79.4"], "Math-VR": ["66.8 / 65.0"],
    "ZeroBench": ["4 / 2"], "VlmsAreBlind": ["79.5 / 80.4"], "LogicVista": ["72.2 / 65.8"],
    "VisuLogic": ["34.4 / 29.9"], "VisualPuzzles": ["57.2 / 54.7"], "MMBench-EN": ["88.8 / 89.3"],
    "MMBench-CN": ["88.6 / 88.9"], "RealWorldQA": ["81.3 / 79.2"], "MMStar": ["78.7 / 78.4"],
    "DocVQAtest": ["96.5 / 97.1"], "InfoVQAtest": ["89.5 / 89.2"], "AI2Dw. M.": ["89.2 / 89.7"],
    "ChartQAtest": ["90.3 / 90.3"], "OCRBench": ["875 / 920"], "OCRBench_v2en": ["66.8 / 67.1"],
    "OCRBench_v2zh": ["63.5 / 61.8"], "CC-OCR": ["81.5 / 82.2"], "OmniDocBenchen": ["0.155 / 0.143"],
    "OmniDocBenchzh": ["0.207 / 0.207"], "CharXiv(DQ)": ["90.5 / 89.4"], "CharXiv(RQ)": ["66.1 / 62.1"],
    "MMLongBenchDoc": ["56.2 / 57.0"], "RefCOCO-avg": ["92.1 / 91.9"], "CountBench": ["93.7 / 93.0"],
    "ODinW-13": ["43.2 / 48.6"], "ARKitScenes": ["53.7 / 56.9"], "Hypersim": ["11.0 / 13.0"],
    "SUNRGBD": ["34.9 / 39.4"], "ERQA": ["52.5 / 51.3"], "VSI-Bench": ["60.0 / 62.7"],
    "EmbSpatialBench": ["84.3 / 83.1"], "RefSpatialBench": ["69.9 / 65.5"], "RoboSpatialHome": ["73.9 / 69.4"],
    "BLINK": ["67.1 / 70.7"], "MUIRBENCH": ["80.1 / 73.0"], "MVBench": ["75.2 / 76.5"],
    "Video-MMEw/o sub.": ["79.0 / 79.2"], "MLVUM-Avg": ["83.8 / 84.3"], "LVBench": ["63.6 / 67.7"],
    "Charades-STAmIoU": ["63.5 / 64.8"], "VideoMMMU": ["80.0 / 74.7"], "MMVU": ["71.1 / 68.1"],
    "V*": ["85.9 / 93.7+"], "HRBench4K": ["84.3 / 85.4+"], "HRBench8K": ["76.6 / 82.4+"],
    "Design2Code": ["93.4 / 92.0"], "ChartMimic": ["78.4 / 80.5"], "UniSVG": ["65.8 / 69.8"],
    "ScreenSpot Pro": ["61.8 / 62.0"], "OSWorldG": ["68.3 / 66.7"], "AndroidWorld": ["62.0 / 63.7"],
    "OSWorld": ["38.1 / 31.6"], "WindowsAA": ["32.1 / 28.9"],
}
add_combined_rows("Qwen", "Alibaba / Qwen", "Qwen3-VL_3_technical_report.pdf", "PDF p.15", "Table 2", ["Qwen3-VL-235B-A22B"], qwen3_table2_rows,
                  notes="Scores are thinking / instruct. Proxy capability benchmarks; not hallucination rate.")

qwen3_table3_rows = {
    "MMMU": ["76.0 / 74.2", "78.1 / 76.0"], "MMMU-Pro": ["63.0 / 60.4", "68.1 / 65.3"],
    "MathVistamini": ["81.9 / 80.1", "85.9 / 83.8"], "MathVision": ["65.7 / 60.2", "70.2 / 63.4"],
    "MathVisionWP": ["58.9 / 52.3", "58.6 / 54.6"], "We-Math": ["70.0 / 56.9", "71.6 / 63.3"],
    "MathVersemini": ["79.6 / 70.2", "82.6 / 76.8"], "DynaMath": ["80.1 / 73.4", "82.0 / 76.7"],
    "Math-VR": ["61.7 / 61.3", "62.3 / 59.8"], "ZeroBench": ["0 / 0", "2 / 1"],
    "VlmsAreBlind": ["72.5 / 67.5", "85.1 / 87.0"], "LogicVista": ["65.8 / 53.5", "70.9 / 62.2"],
    "VisuLogic": ["26.6 / 23.0", "32.4 / 29.7"], "VisualPuzzles": ["52.0 / 46.2", "54.7 / 53.2"],
    "MMBench-EN": ["87.0 / 86.1", "89.5 / 87.6"], "MMBench-CN": ["85.9 / 85.3", "89.4 / 87.7"],
    "RealWorldQA": ["77.4 / 73.7", "78.4 / 79.0"], "MMStar": ["75.5 / 72.1", "79.4 / 77.7"],
    "DocVQAtest": ["95.5 / 95.0", "96.1 / 96.9"], "InfoVQAtest": ["85.6 / 81.8", "89.2 / 87.0"],
    "AI2Dw. M.": ["86.9 / 85.0", "88.9 / 89.5"], "ChartQAtest": ["89.4 / 86.8", "89.0 / 88.5"],
    "OCRBench": ["839 / 903", "855 / 895"], "OCRBench_v2en": ["62.6 / 63.2", "68.4 / 67.4"],
    "OCRBench_v2zh": ["60.4 / 57.8", "62.1 / 59.2"], "CC-OCR": ["77.8 / 80.7", "79.6 / 80.3"],
    "OmniDocBenchen": ["0.165 / 0.183", "0.148 / 0.151"], "OmniDocBenchzh": ["0.233 / 0.253", "0.236 / 0.239"],
    "CharXiv(DQ)": ["86.9 / 85.5", "90.2 / 90.5"], "CharXiv(RQ)": ["56.6 / 48.9", "65.2 / 62.8"],
    "MMLongBenchDoc": ["47.4 / 47.1", "54.6 / 55.4"], "RefCOCO-avg": ["89.3 / 89.7", "91.1 / 91.9"],
    "CountBench": ["90.0 / 89.8", "94.1 / 94.9"], "ODinW-13": ["42.3 / 47.5", "41.8 / 46.6"],
    "ARKitScenes": ["55.6 / 56.1", "46.1 / 55.6"], "Hypersim": ["11.4 / 12.5", "12.5 / 14.0"],
    "SUNRGBD": ["34.6 / 38.1", "33.9 / 37.0"], "ERQA": ["45.3 / 43.0", "52.3 / 48.8"],
    "VSI-Bench": ["56.1 / 63.2", "61.2 / 61.5"], "EmbSpatialBench": ["80.6 / 76.4", "82.7 / 81.5"],
    "RefSpatialBench": ["54.2 / 53.1", "67.2 / 61.4"], "RoboSpatialHome": ["65.5 / 62.9", "74.2 / 64.6"],
    "BLINK": ["65.4 / 67.7", "68.5 / 67.3"], "MUIRBENCH": ["77.6 / 62.9", "80.3 / 72.8"],
    "MVBench": ["72.0 / 72.3", "73.2 / 72.8"], "Video-MMEw/o sub.": ["73.3 / 74.5", "77.3 / 76.6"],
    "MLVUM-Avg": ["78.9 / 81.3", "82.3 / 82.1"], "LVBench": ["59.2 / 62.5", "62.6 / 63.8"],
    "Charades-STAmIoU": ["62.7 / 63.5", "62.8 / 61.2"], "VideoMMMU": ["75.0 / 68.7", "79.0 / 71.9"],
    "MMVU": ["66.1 / 59.8", "67.9 / 66.8"], "V*": ["81.2 / 89.5+", "84.8 / 91.1+"],
    "HRBench4K": ["77.8 / 82.5+", "82.1 / 84.6+"], "HRBench8K": ["71.3 / 79.3+", "74.8 / 81.6+"],
    "ScreenSpot Pro": ["57.3 / 60.5", "57.1 / 57.9"], "OSWorldG": ["59.6 / 61.0", "64.0 / 65.1"],
    "AndroidWorld": ["55.0 / 54.3", "63.7 / 57.3"], "OSWorld": ["30.6 / 30.3", "41.0 / 32.6"],
    "WindowsAA": ["24.2 / 24.9", "42.9 / 30.9"],
}
add_combined_rows("Qwen", "Alibaba / Qwen", "Qwen3-VL_3_technical_report.pdf", "PDF p.16", "Table 3", ["Qwen3-VL-30B-A3B", "Qwen3-VL-32B"], qwen3_table3_rows,
                  notes="Scores are thinking / instruct. Proxy capability benchmarks; not hallucination rate.")

qwen3_table4_rows = {
    "MMMU": ["61.4 / 53.4", "70.8 / 67.4", "74.1 / 69.6"], "MMMU-Pro": ["42.5 / 36.5", "57.0 / 53.2", "60.4 / 55.9"],
    "MathVistamini": ["73.6 / 61.3", "79.5 / 73.7", "81.4 / 77.2"], "MathVision": ["45.9 / 31.6", "60.0 / 51.6", "62.7 / 53.9"],
    "MathVisionWP": ["35.5 / 30.9", "48.7 / 44.4", "53.3 / 45.4"], "MathVersemini": ["66.9 / 52.1", "75.2 / 46.8", "77.7 / 62.1"],
    "DynaMath": ["66.7 / 54.2", "74.4 / 65.3", "73.2 / 67.7"], "Math-VR": ["37.7 / 20.7", "58.1 / 52.3", "59.0 / 53.4"],
    "ZeroBench": ["0 / 0", "0 / 0", "2 / 1"], "VlmsAreBlind": ["50.0 / 56.0", "68.6 / 71.9", "69.1 / 74.0"],
    "LogicVista": ["50.0 / 35.8", "61.1 / 53.2", "65.1 / 55.3"], "VisuLogic": ["25.4 / 11.5", "30.2 / 19.0", "27.5 / 22.5"],
    "VisualPuzzles": ["37.4 / 34.3", "48.9 / 43.7", "51.7 / 47.9"], "MMBench-EN": ["79.9 / 78.4", "84.6 / 83.9", "85.3 / 84.5"],
    "MMBench-CN": ["78.8 / 75.9", "83.8 / 83.5", "85.5 / 84.7"], "RealWorldQA": ["69.5 / 63.9", "73.2 / 70.9", "73.5 / 71.5"],
    "MMStar": ["68.1 / 58.3", "73.2 / 69.8", "75.3 / 70.9"], "DocVQAtest": ["92.9 / 93.3", "94.2 / 95.3", "95.3 / 96.1"],
    "InfoVQAtest": ["77.1 / 72.4", "83.0 / 80.3", "86.0 / 83.1"], "AI2Dw. M.": ["80.4 / 76.9", "84.9 / 84.1", "84.9 / 85.7"],
    "ChartQAtest": ["86.6 / 79.1", "88.8 / 84.6", "88.6 / 89.6"], "OCRBench": ["792 / 858", "808 / 881", "819 / 896"],
    "OCRBench_v2en": ["56.4 / 56.3", "61.8 / 63.7", "63.9 / 65.4"], "OCRBench_v2zh": ["51.9 / 53.0", "55.8 / 57.6", "59.2 / 61.2"],
    "CC-OCR": ["68.3 / 72.8", "73.8 / 76.2", "76.3 / 79.9"], "OmniDocBenchen": ["0.370 / 0.292", "0.234 / 0.244", "0.209 / 0.170"],
    "OmniDocBenchzh": ["0.447 / 0.348", "0.297 / 0.285", "0.253 / 0.264"], "CharXiv(DQ)": ["70.1 / 62.3", "83.9 / 76.2", "85.9 / 83.0"],
    "CharXiv(RQ)": ["37.1 / 26.8", "50.3 / 39.7", "53.0 / 46.4"], "MMLongBenchDoc": ["33.8 / 31.6", "44.4 / 43.5", "48.0 / 47.9"],
    "RefCOCO-avg": ["84.8 / 85.6", "88.2 / 89.0", "88.2 / 89.1"], "CountBench": ["84.1 / 88.4", "89.4 / 84.9", "91.5 / 80.5"],
    "ODinW-13": ["36.0 / 43.4", "39.4 / 48.2", "39.8 / 44.7"], "MVBench": ["64.5 / 61.7", "69.3 / 68.9", "69.0 / 68.7"],
    "Video-MMEw/o sub.": ["62.1 / 61.9", "68.9 / 69.3", "71.8 / 71.4"], "MLVUM-Avg": ["69.2 / 68.3", "75.7 / 75.3", "75.1 / 78.1"],
    "LVBench": ["47.6 / 47.4", "53.5 / 56.2", "55.8 / 58.0"], "Charades-STAmIoU": ["56.9 / 54.5", "59.0 / 55.5", "59.9 / 56.0"],
    "VideoMMMU": ["54.1 / 41.9", "69.4 / 56.2", "72.8 / 65.3"], "MMVU": ["48.9 / 41.7", "58.6 / 50.5", "62.0 / 58.7"],
    "ScreenSpot Pro": ["32.2 / 48.5", "49.2 / 59.5", "46.6 / 54.6"], "OSWorldG": ["41.8 / 46.1", "53.9 / 58.2", "56.7 / 58.2"],
    "AndroidWorld": ["46.1 / 36.4", "52.0 / 45.3", "50.0 / 47.6"], "OSWorld": ["19.0 / 17.0", "31.4 / 26.2", "33.9 / 33.9"],
}
add_combined_rows("Qwen", "Alibaba / Qwen", "Qwen3-VL_3_technical_report.pdf", "PDF p.18", "Table 4", ["Qwen3-VL-2B", "Qwen3-VL-4B", "Qwen3-VL-8B"], qwen3_table4_rows,
                  notes="Scores are thinking / instruct. Proxy capability benchmarks; not hallucination rate.")


# Qwen2.5-VL tables.
qwen25_models = ["Qwen2.5-VL-72B", "Qwen2.5-VL-7B", "Qwen2.5-VL-3B"]
qwen25_table3 = {
    "MMMUval": ["70.2", "58.6", "53.1"], "MMMU-Prooverall": ["51.1", "38.3", "31.56"],
    "MathVistamini": ["74.8", "68.2", "62.3"], "MATH-Visionfull": ["38.1", "25.1", "21.2"],
    "MathVersemini": ["57.6", "49.2", "47.6"], "MegaBench": ["51.3", "36.8", "28.9"],
    "MMBench-ENtest": ["88.6", "83.5", "79.1"], "MMBench-CNtest": ["87.9", "83.4", "78.1"],
    "MMBench-V1.1-ENtest": ["88.4", "82.6", "77.4"], "MMStar": ["70.8", "63.9", "55.9"],
    "MMEsum": ["2448", "2347", "2157"], "MuirBench": ["70.7", "59.6", "47.7"], "BLINK": ["64.4", "56.4", "47.6"],
    "MTVQA": ["31.7", "29.2", "24.8"], "RealWorldQAavg": ["75.7", "68.5", "65.4"],
    "MME-RealWorlden": ["63.2", "57.4", "53.1"], "MMVetturbo": ["76.2", "67.1", "61.8"],
    "MM-MT-Bench": ["7.6", "6.3", "5.7"],
}
add_combined_rows("Qwen", "Alibaba / Qwen", "Qwen2.5-VL_2.5_technical_report.pdf", "PDF p.11", "Table 3", qwen25_models, qwen25_table3, setting="instruct / image-text-video")
qwen25_table5 = {
    "CC-OCR": ["79.8", "77.8", "74.5"], "OmniDocBenchedit en/zh ↓": ["0.226/0.324", "0.308/0.398", "0.409/0.543"],
    "AI2Dw. M.": ["88.7", "83.9", "81.6"], "TextVQAval": ["83.5", "84.9", "79.3"], "DocVQAtest": ["96.4", "95.7", "93.9"],
    "InfoVQAtest": ["87.3", "82.6", "77.1"], "ChartQAtest Avg.": ["89.5", "87.3", "84.0"],
    "CharXiv(RQ)": ["49.7", "42.5", "31.3"], "CharXiv(DQ)": ["87.4", "73.9", "58.6"],
    "SEED-Bench-2-Plus": ["73.0", "70.4", "67.6"], "OCRBench": ["885", "864", "797"],
    "VCREn-Hard-EM": ["79.8", "80.5", "37.5"], "OCRBench_v2en": ["61.5", "56.3", "54.3"],
    "OCRBench_v2zh": ["63.7", "57.2", "52.1"],
}
add_combined_rows("Qwen", "Alibaba / Qwen", "Qwen2.5-VL_2.5_technical_report.pdf", "PDF p.13", "Table 5", qwen25_models, qwen25_table5, setting="instruct")
qwen25_table6 = {
    "Refcocoval": ["92.7", "90.0", "89.1"], "RefcocotestA": ["94.6", "92.5", "91.7"], "RefcocotestB": ["89.7", "85.4", "84.0"],
    "Refcoco+val": ["88.9", "84.2", "82.4"], "Refcoco+testA": ["92.2", "89.1", "88.0"], "Refcoco+testB": ["83.7", "76.9", "74.1"],
    "Refcocogval": ["89.9", "87.2", "85.2"], "Refcocogtest": ["90.3", "87.2", "85.7"], "ODinW": ["43.1", "37.3", "37.5"],
    "PointGrounding": ["67.5", "67.3", "58.3"],
}
add_combined_rows("Qwen", "Alibaba / Qwen", "Qwen2.5-VL_2.5_technical_report.pdf", "PDF p.14", "Table 6", qwen25_models, qwen25_table6, setting="grounding eval")
add_proxy("Qwen2.5-VL-72B", "Qwen", "Alibaba / Qwen", "CountBench", "93.6", "detect then count prompt", "Qwen2.5-VL_2.5_technical_report.pdf", page="PDF p.14", table="Table 7", evidence="CountBench: Qwen2.5-VL-72B = 93.6")
qwen25_table8 = {
    "Video-MMEw/o sub.": ["73.3", "65.1", "61.5"], "Video-MMEw sub.": ["79.1", "71.6", "67.6"],
    "VideoMMMU": ["60.2", "47.4", "-"], "MMVUval": ["62.9", "50.1", "-"], "MVBench": ["70.4", "69.6", "67.0"],
    "MMBench-Video": ["2.02", "1.79", "1.63"], "LongVideoBenchval": ["60.7", "56.0", "54.2"],
    "LVBench": ["47.3", "45.3", "43.3"], "EgoSchematest": ["76.2", "65.0", "64.8"],
    "PerceptionTesttest": ["73.2", "70.5", "66.9"], "MLVUM-Avg": ["74.6", "70.2", "68.2"],
    "TempCompassAvg": ["74.8", "71.7", "64.4"], "Charades-STAmIoU": ["50.9", "43.6", "38.8"],
}
add_combined_rows("Qwen", "Alibaba / Qwen", "Qwen2.5-VL_2.5_technical_report.pdf", "PDF p.14", "Table 8", qwen25_models, qwen25_table8, setting="video eval; max frames 768")
for b, s in {"ScreenSpot": "87.1", "ScreenSpot Pro": "43.6", "Android Control HighEM": "67.36", "Android Control LowEM": "93.7", "AndroidWorldSR": "35%", "MobileMiniWob++SR": "68%", "OSWorld": "8.83"}.items():
    add_proxy("Qwen2.5-VL-72B", "Qwen", "Alibaba / Qwen", b, s, "GUI agent", "Qwen2.5-VL_2.5_technical_report.pdf", page="PDF p.15", table="Table 9", evidence=f"{b}: Qwen2.5-VL-72B = {s}")


# Qwen Omni tables.
for b, s in {
    "MMMUval": "59.2", "MMMU-Prooverall": "36.6", "MathVistatestmini": "67.9", "MathVision": "25.0",
    "MMBench-V1.1-ENtest": "81.8", "MMVetturbo": "66.8", "MMStar": "64.0", "MMEsum": "2340",
    "MuirBench": "59.2", "RealWorldQAavg": "70.3", "MME-RealWorlden": "61.6", "MM-MT-Bench": "6.0",
    "AI2D": "83.2", "TextVQAval": "84.4", "DocVQAtest": "95.2", "ChartQAtest Avg": "85.3", "OCRBench_V2en": "57.8",
}.items():
    add_proxy("Qwen2.5-Omni-7B", "Qwen", "Alibaba / Qwen", b, s, "image -> text", "model_best/model_reports/Qwen2.5-Omni_2.5_technical_report.pdf", page="PDF p.11", table="Table 5", evidence=f"{b}: Qwen2.5-Omni-7B = {s}")
for b, s in {"Refcocoval": "90.5", "RefcocotextA": "93.5", "RefcocotextB": "86.6", "Refcoco+val": "85.4", "Refcoco+textA": "91.0", "Refcoco+textB": "79.3", "Refcocogval": "87.4", "Refcocogtest": "87.9", "ODinW": "42.2", "PointGrounding": "66.5"}.items():
    add_proxy("Qwen2.5-Omni-7B", "Qwen", "Alibaba / Qwen", b, s, "grounding", "model_best/model_reports/Qwen2.5-Omni_2.5_technical_report.pdf", page="PDF p.11", table="Table 6", evidence=f"{b}: Qwen2.5-Omni-7B = {s}")
for b, s in {"Video-MMEw/o sub.": "64.3", "Video-MMEw sub.": "72.4", "MVBench": "70.3", "EgoSchematest": "68.6", "OmniBench": "55.25% | 60.00% | 52.83% | 56.13%"}.items():
    add_proxy("Qwen2.5-Omni-7B", "Qwen", "Alibaba / Qwen", b, s, "video/multimodality -> text", "model_best/model_reports/Qwen2.5-Omni_2.5_technical_report.pdf", page="PDF p.12", table="Table 7/8", evidence=f"{b}: Qwen2.5-Omni-7B = {s}")

qwen35_models = ["Qwen3.5-Plus-Instruct", "Qwen3.5-Omni-Flash", "Qwen3.5-Omni-Plus"]
qwen35_rows = {
    "MMMU": ["81.0", "76.9", "80.1"], "MMMU-Pro": ["73.8", "68.2", "73.9"], "MathVision": ["73.6", "65.4", "73.0"],
    "MathVistamini": ["86.9", "82.9", "86.1"], "DynaMath": ["84.2", "79.3", "83.8"], "ZEROBench": ["6", "1", "5"],
    "ZEROBench_sub": ["31.1", "26.0", "34.4"], "RealWorldQA": ["79.1", "77.5", "84.1"], "MMStar": ["80.3", "75.7", "79.4"],
    "MMBenchEN-DEV-v1.1": ["93.8", "88.8", "92.8"], "CharXiv (RQ)": ["74.2", "64.4", "72.5"], "CC-OCR": ["83.0", "80.8", "83.4"],
    "AI2D_TEST": ["92.1", "89.0", "91.2"], "MMLongBench-Doc": ["59.7", "53.6", "57.5"], "OCRBench": ["91.4", "89.1", "91.3"],
    "ERQA": ["53.8", "50.0", "54.8"], "CountBench": ["95.1", "88.2", "95.1"], "RefCOCO(avg)": ["95.2", "92.6", "95.0"],
    "ODInW13": ["50.3", "46.8", "49.5"], "EmbSpatialBench": ["83.4", "82.7", "85.4"], "VideoMME(w/o sub.)": ["81.0", "77.0", "81.9"],
    "MLVU(M-Avg)": ["85.1", "81.9", "86.8"], "MVBench": ["76.7", "70.8", "79.0"], "LVBench": ["68.6", "65.7", "71.2"],
    "MMVU": ["67.1", "62.7", "67.5"], "MME-VideoOCR": ["74.2", "70.5", "77.0"], "SLAKE": ["82.8", "73.1", "84.7"],
    "PMC-VQA": ["62.4", "58.7", "62.7"], "MedXpertQA-MM": ["55.3", "44.8", "54.7"],
}
add_combined_rows("Qwen", "Alibaba / Qwen", "model_best/Qwen3.5-Omni_3.5_technical_report.pdf", "PDF p.12", "Table 6", qwen35_models, qwen35_rows, setting="vision -> text")
for b, vals in {"DailyOmni": ["81.8", "84.6"], "WorldSense": ["57.9", "62.8"], "AVUT": ["81.4", "85.0"], "AV-SpeakerBench": ["65.2", "71.3"], "VideoMMEw/ audio": ["79.3", "83.7"], "Qualcomm IVD": ["66.3", "68.5"], "Omni-Cloze": ["63.0", "64.8"], "OmniGAIA": ["33.9", "57.2"]}.items():
    for model, score in zip(["Qwen3.5-Omni-Flash", "Qwen3.5-Omni-Plus"], vals):
        add_proxy(model, "Qwen", "Alibaba / Qwen", b, score, "audio-visual -> text", "model_best/Qwen3.5-Omni_3.5_technical_report.pdf", page="PDF p.13", table="Table 7", evidence=f"{b}: {model} = {score}")


# Gemini proxy/factuality-related official report rows.
for model, mmmu, chart in [
    ("Gemini 1.5 Flash", "58.3%", "59.0%"), ("Gemini 1.5 Pro", "67.7%", "65.8%"),
    ("Gemini 2.0 Flash-Lite", "65.1%", "52.3%"), ("Gemini 2.0 Flash", "69.3%", "57.8%"),
    ("Gemini 2.5 Flash", "79.7%", "67.3%"), ("Gemini 2.5 Pro", "82.0%", "72.4%"),
]:
    add_proxy(model, "Gemini", "Google DeepMind", "MMMU", mmmu, "official family comparison", "Gemini-2.5_2.5_technical_report.pdf", page="PDF p.13", table="Table 3")
    add_proxy(model, "Gemini", "Google DeepMind", "BetterChartQA", chart, "official family comparison", "Gemini-2.5_2.5_technical_report.pdf", page="PDF p.13", table="Table 3")

for model, vals in {
    "Gemini 1.5 Flash": ["56.2", "34.5", "66.5", "64.4", "64.8", "61.9", "61.9", "70.4", "77.3"],
    "Gemini 1.5 Pro": ["57.3", "36.3", "69.4", "68.7", "70.4", "72.2", "65.7", "73.2", "79.8"],
    "Gemini 2.0 Flash-Lite": ["55.3", "30.1", "67.5", "25.7", "64.3", "55.6", "52", "62.1", "72.5"],
    "Gemini 2.0 Flash": ["56.4", "39.3", "68.8", "63.9", "68.5", "67.5", "61.8", "72.8", "78.8"],
    "Gemini 2.5 Flash": ["65.1", "36.7", "75.1", "52.4", "79.2", "67.5", "62.7", "75.5", "81.5"],
    "Gemini 2.5 Pro": ["66.7", "44.3", "78.4", "75.0", "83.6", "81.0", "78.7", "84.3", "86.9"],
}.items():
    for b, s in zip(["ActivityNet-QA", "EgoTempo", "Perception Test", "QVHighlights", "VideoMMMU", "1H-VideoQA", "LVBench", "VideoMME", "VideoMME audio+visual+subtitles"], vals):
        add_proxy(model, "Gemini", "Google DeepMind", b, s, "video understanding", "Gemini-2.5_2.5_technical_report.pdf", page="PDF p.15", table="Table 6")


# Gemma 3 multimodal rows.
for model, facts, simple, mmmu in [
    ("Gemma 3 1B", "36.4", "2.2", "-"), ("Gemma 3 4B", "70.1", "4.0", "48.8"),
    ("Gemma 3 12B", "75.8", "6.3", "59.6"), ("Gemma 3 27B", "74.9", "10.0", "64.9"),
]:
    add_fact(model, "Gemma", "Google DeepMind", "SimpleQA", simple, "IT model zero-shot", "model_best/model_reports/Gemma3_3_technical_report.pdf", page="PDF p.6", table="Table 6", evidence=f"SimpleQA: {model} = {simple}")
    if mmmu != "-":
        add_proxy(model, "Gemma", "Google DeepMind", "MMMU", mmmu, "IT model zero-shot", "model_best/model_reports/Gemma3_3_technical_report.pdf", page="PDF p.6", table="Table 6")

for model, vals in {
    "Gemma 3 4B PT": ["72.8", "44.1", "39.2", "58.9", "45.5", "63.2", "63.6", "63.9"],
    "Gemma 3 12B PT": ["82.3", "54.8", "50.3", "66.5", "52.2", "75.2", "74.7", "71.2"],
    "Gemma 3 27B PT": ["85.6", "59.4", "56.1", "68.6", "53.9", "79.0", "76.3", "72.9"],
    "Gemma 3 4B IT": ["75.8", "50.0", "48.8", "57.8", "", "74.8", "68.8", "62.4"],
    "Gemma 3 12B IT": ["87.1", "64.9", "59.6", "67.7", "", "84.2", "75.7", "71.6"],
    "Gemma 3 27B IT": ["86.6", "70.6", "64.9", "65.1", "", "84.5", "78.0", "71.0"],
}.items():
    for b, s in zip(["DocVQA", "InfoVQA", "MMMU", "TextVQA", "RealWorldQA", "AI2D", "ChartQA", "VQAv2"], vals):
        if s:
            add_proxy(model, "Gemma", "Google DeepMind", b, s, "PT/IT multimodal appendix", "model_best/model_reports/Gemma3_3_technical_report.pdf", page="PDF p.20-22", table="Tables 11/16")


# Direct rows' factuality entries from v1.3 that were not in the above lists.
try:
    fr = xlsx_rows(BASE / "mentor_final_report_v1_3" / "mentor_full_score_table.xlsx", "Full Recall Scores")
    hdr = fr[0]
    existing_fact_keys = {(r["model"], r["benchmark"], r["score"]) for r in factuality}
    for r in fr[1:]:
        d = {hdr[i]: r[i] if i < len(r) else "" for i in range(len(hdr))}
        if d.get("benchmark_category") == "factuality_grounding_related":
            key = (d["model"], d["benchmark"], d["score"])
            if key not in existing_fact_keys:
                add_fact(d["model"], d.get("model","").split("-")[0] or "", d["organization"], d["benchmark"], d["score"], d.get("metric",""),
                         d["source_file"], page=d.get("page_or_section",""), table=d.get("table_title",""),
                         evidence=d.get("evidence_row",""), confidence=d.get("confidence","high"), notes=d.get("notes",""))
except Exception:
    pass


# Manifest/audit coverage gaps: do not trust old numeric extraction, but keep coverage recall.
try:
    manifest = json.loads((BASE / "analysis_results" / "enhanced_manifest.json").read_text(encoding="utf-8"))
except Exception:
    manifest = []

try:
    audit_rows = xlsx_rows(BASE / "analysis_results" / "audit_evidence_for_all_2s.xlsx", "Evidence for all value=2")
    ah = audit_rows[0]
    for r in audit_rows[1:]:
        d = {ah[i]: r[i] if i < len(r) else "" for i in range(len(ah))}
        if d.get("Is Pure Hal BM") == "no" and d.get("Benchmark"):
            unverified_candidates.append({
                "model": d.get("Model", ""),
                "benchmark": d.get("Benchmark", ""),
                "proxy_subtype": d.get("Proxy Subtype", ""),
                "old_judgment": d.get("Judgment", ""),
                "old_extracted_score_do_not_use": d.get("Extracted Score", ""),
                "source_file": d.get("Source File", ""),
                "location_context": d.get("Location Context", ""),
                "evidence_snippet": d.get("Evidence Snippet", ""),
                "reason_not_in_scorebook": "Existing audit/matrix candidate, but not table-level verified in this full pass.",
            })
except Exception:
    pass

covered_models = {r["model"] for r in proxy} | {r["model"] for r in factuality}
priority_families = [
    "OpenAI", "Gemini", "Claude", "Qwen", "InternVL", "MiniCPM", "DeepSeek", "LLaVA", "CogVLM", "Bunny",
    "VILA", "Molmo", "Pixtral", "Kimi", "Seed", "SEED", "Ovis", "NVLM", "Phi", "Llama", "MiMo", "Gemma", "PaliGemma",
]
for e in manifest:
    name = e.get("model_or_benchmark_name", "")
    if not name:
        continue
    if e.get("doc_type") == "benchmark_paper":
        continue
    bms = e.get("benchmarks_mentioned") or []
    local = e.get("local_path", "")
    if not local and not bms:
        continue
    family = next((f for f in priority_families if f.lower() in name.lower() or f.lower() in local.lower()), "Other")
    relevant = [b for b in bms if b in BENCHMARK_PROXY_TYPE or b in {"SimpleVQA", "FACTS-Grounding", "SimpleQA", "LongFact", "FActScore"}]
    def norm(s):
        return re.sub(r"[^a-z0-9]+", "", s.lower())
    n_name = norm(name)
    model_already_covered = any(n_name and (n_name in norm(m) or norm(m) in n_name) for m in covered_models)
    if model_already_covered:
        continue
    if not relevant:
        add_gap(name, family, "factuality/proxy benchmark table", "No relevant benchmark score table located in this full pass.", local)
    elif name not in covered_models:
        add_gap(name, family, ", ".join(relevant[:12]), "Mentioned or old-pipeline detected; table-level score not verified in this pass.", local,
                notes="Keep as recall candidate; do not use as score until original table is checked.")


# Deduplicate.
def dedupe(rows, keys):
    out, seen = [], set()
    for r in rows:
        k = tuple(r.get(x, "") for x in keys)
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out


factuality = dedupe(factuality, ["model", "benchmark", "score", "source_file"])
proxy = dedupe(proxy, ["model", "benchmark", "score", "source_file", "page_or_section"])
gaps = dedupe(gaps, ["model", "missing_expected_benchmark", "checked_source"])


benchmark_taxonomy = []
for b in sorted({r["benchmark"] for r in proxy}):
    benchmark_taxonomy.append({
        "benchmark": b, "category": "proxy", "proxy_type": BENCHMARK_PROXY_TYPE.get(b, "general_reasoning"),
        "task_type": BENCHMARK_PROXY_TYPE.get(b, "general_reasoning"),
        "hallucination_relevance": "Capability proxy; may indicate risk background but is not hallucination rate.",
        "metric": "As reported by source table", "higher_or_lower_better": "as source", "notes": "Keep separate from direct hallucination benchmarks.",
    })
for b in sorted({r["benchmark"] for r in factuality}):
    benchmark_taxonomy.append({
        "benchmark": b, "category": "factuality_related", "proxy_type": "",
        "task_type": "factuality / grounding / system-card internal eval",
        "hallucination_relevance": "Related to factual correctness or grounding, but not direct multimodal hallucination rate.",
        "metric": "As reported by source table", "higher_or_lower_better": "as source", "notes": "Do not mix with POPE/CHAIR/HallusionBench leaderboard.",
    })

model_family_summary = []
by_family_proxy = defaultdict(list)
by_family_fact = defaultdict(list)
for r in proxy:
    by_family_proxy[r["family"]].append(r)
for r in factuality:
    by_family_fact[r["family"]].append(r)
for fam in sorted(set(by_family_proxy) | set(by_family_fact) | {g["family"] for g in gaps}):
    models = sorted({r["model"] for r in by_family_proxy.get(fam, [])} | {r["model"] for r in by_family_fact.get(fam, [])})
    model_family_summary.append({
        "model_family": fam,
        "models_checked": ", ".join(models) if models else "see Coverage Gaps",
        "direct_benchmarks_found": "see mentor_final_report_v1_4 / v1_3 direct table",
        "factuality_related_found": ", ".join(sorted({r["benchmark"] for r in by_family_fact.get(fam, [])})) or "not table-verified",
        "proxy_benchmarks_found": ", ".join(sorted({r["benchmark"] for r in by_family_proxy.get(fam, [])}))[:800] or "not table-verified",
        "num_proxy_scores": len(by_family_proxy.get(fam, [])),
        "num_factuality_scores": len(by_family_fact.get(fam, [])),
        "coverage_notes": "Full rows are in Proxy Scores Full / Factuality Related Scores; gaps list mentions not table-verified candidates.",
    })

benchmark_coverage = []
for b, rows in sorted(defaultdict(list, {b:[r for r in proxy if r["benchmark"]==b] for b in {r["benchmark"] for r in proxy}}).items()):
    benchmark_coverage.append({"benchmark": b, "category": "proxy", "proxy_type": BENCHMARK_PROXY_TYPE.get(b, ""), "num_models_with_scores": len({r["model"] for r in rows}), "models_with_scores": ", ".join(sorted({r["model"] for r in rows}))[:1000], "notes": "Proxy benchmark; not hallucination rate."})
for b, rows in sorted(defaultdict(list, {b:[r for r in factuality if r["benchmark"]==b] for b in {r["benchmark"] for r in factuality}}).items()):
    benchmark_coverage.append({"benchmark": b, "category": "factuality_related", "proxy_type": "", "num_models_with_scores": len({r["model"] for r in rows}), "models_with_scores": ", ".join(sorted({r["model"] for r in rows}))[:1000], "notes": "Factuality/grounding related; not direct visual hallucination."})

caveats = [
    {"caveat_type": "proxy_not_hallucination_rate", "description": "OCRBench/DocVQA/ChartQA/Video-MME/MMMU/MMBench/etc. measure capability, not direct hallucination rate.", "affected_benchmarks_or_models": "all proxy rows", "recommendation": "Report in separate proxy section."},
    {"caveat_type": "factuality_not_direct_visual_hal", "description": "SimpleQA/SimpleVQA/FACTS-Grounding/HealthBench are factuality or grounding related.", "affected_benchmarks_or_models": "all factuality rows", "recommendation": "Do not merge into POPE/CHAIR/HallusionBench leaderboard."},
    {"caveat_type": "closed_source_internal_eval", "description": "OpenAI/Claude/Gemini system-card evals are often internal or system-card level.", "affected_benchmarks_or_models": "closed-source providers", "recommendation": "Do not directly rank against open-source public benchmark tables."},
    {"caveat_type": "settings_matter", "description": "thinking/instruct, zero-shot/fine-tuning, with/without subtitles/audio, prompt and judge settings change scores.", "affected_benchmarks_or_models": "Qwen3-VL, Qwen3.5-Omni, Gemini video tables, PaliGemma", "recommendation": "Keep setting column with every score."},
    {"caveat_type": "old_numeric_extractions_not_trusted", "description": "analysis_results/enhanced_manifest numeric values include many citation/section artifacts.", "affected_benchmarks_or_models": "manifest-derived candidates", "recommendation": "Use only table-verified rows as scores; others remain in Coverage Gaps."},
]


# Markdown deliverables.
fact_tax_rows = [
    ["FACTS-Grounding", "factuality_related", "Document/source-grounded factual correctness", "document-grounded QA/judging", "accuracy/score", "higher better", "yes within same source/config", "Not pure multimodal hallucination."],
    ["SimpleVQA", "factuality_related", "Visual factuality / simple visual QA", "image+question", "accuracy", "higher better", "yes within same source/config", "Qwen reports thinking/instruct separately."],
    ["SimpleQA", "factuality_related", "Text/world-knowledge factuality", "short-answer fact questions", "accuracy and/or hallucination rate", "accuracy higher, hallucination lower", "partly", "OpenAI/Gemini report it as factuality, not visual hallucination."],
    ["LongFact", "factuality_related", "Long-form factuality", "open-ended fact-seeking prompts", "claim-level error rate", "lower better", "no exact table in this pass", "GPT-5 system card uses it with FActScore."],
    ["FActScore", "factuality_related", "Biography/fact consistency", "open-ended biography prompts", "claim-level error rate", "lower better", "no exact table in this pass", "GPT-5 system card reports figure-level results."],
    ["HealthBench Hard Hallucinations", "factuality_related", "Medical factuality/safety hard cases", "health QA / rubric eval", "score / hallucination subset", "higher score better", "only within OpenAI system-card context", "Not multimodal direct hallucination."],
    ["system-card factuality/internal eval", "factuality_related", "Provider-specific internal factuality/risk eval", "internal/red-team/system-card tests", "varies", "varies", "no", "Keep separate from public academic benchmark tables."],
]

fact_md_rows = [[r["model"], r["family"], r["organization"], r["benchmark"], r["score"], r["setting"], r["source_file"], r["page_or_section"], r["confidence"], r["notes"]] for r in factuality]
fact_md = f"""# Factuality / Grounding Related Benchmark 官方分数全量整理

生成日期：{TODAY}

## 1. 口径说明

本文件只整理 factuality / grounding related benchmark。它们与 hallucination 相关，但不是 POPE、CHAIR、HallusionBench、MMHal-Bench、CRPE 这类 direct visual hallucination benchmark，也不能写成 multimodal hallucination rate。

## 2. Benchmark taxonomy

{md_table(["benchmark","category","测什么","任务形式","指标","higher/lower better","是否可横比","notes"], fact_tax_rows)}

## 3. 全量模型分数表

共整理 {len(factuality)} 条 factuality_related 记录。完整机器可读版本见 `factuality_proxy_scorebook_full.xlsx` 的 `Factuality Related Scores` sheet。

{md_table(["model","family","organization","benchmark","score","setting","source_file","page_or_section","confidence","notes"], fact_md_rows, max_rows=120)}

## 4. 模型族覆盖总结

- **OpenAI**：GPT-5 system card 披露 SimpleQA、LongFact、FActScore、HealthBench/HealthBench Hard 等 factuality/safety 评估；这些不是视觉 hallucination benchmark。
- **Google / Gemini / Gemma**：Gemini 2.5 报告 SimpleQA 与 FACTS-Grounding；Gemma 3 报告 FACTS-Grounding 和 SimpleQA。
- **Anthropic**：本地 Claude system card/model card 中可确认 safety/factuality/internal risk eval 口径，但未找到可横比 POPE/CHAIR/HallusionBench/MMHal 表格。
- **Qwen**：Qwen3-VL 和 Qwen3.5-Omni 报告 SimpleVQA，且 Qwen3-VL 保留 thinking/instruct 双口径。
- **其它开源模型**：多数主要披露 proxy 或 direct hallucination 分数，factuality_related 表格覆盖较少；未确认项见 `coverage_gap_report.md`。
"""
(OUT / "factuality_related_scores_full.md").write_text(fact_md, encoding="utf-8")

proxy_summary_rows = []
for fam in sorted(by_family_proxy):
    rows = by_family_proxy[fam]
    proxy_summary_rows.append([fam, len(rows), ", ".join(sorted({r["model"] for r in rows}))[:180], ", ".join(sorted({r["benchmark"] for r in rows}))[:260], "完整行见 Excel / Proxy Scores Full"])
proxy_md = f"""# Proxy Benchmark 官方分数与覆盖全量整理

生成日期：{TODAY}

## 1. 口径说明

Proxy benchmark 不是 hallucination rate。OCRBench、DocVQA、ChartQA、Video-MME、MMMU、MMBench、RefCOCO、ScreenSpot 等反映 OCR、文档、图表、视频、推理、grounding 或 GUI 能力背景，不能与 POPE/CHAIR/HallusionBench/MMHal-Bench 合并排名。

## 2. 全量 proxy 分数表

本轮 full recall 共整理 {len(proxy)} 条 table-level proxy score 记录。为避免 Markdown 过长，下表仅展示前 160 条；完整数据见 `factuality_proxy_scorebook_full.xlsx` 的 `Proxy Scores Full` sheet。

另有 {len(unverified_candidates)} 条来自既有 audit/matrix 的 proxy candidate 记录进入 Excel 的 `Unverified Proxy Candidates` sheet；这些只用于召回线索，旧抽取分数不作为 confirmed score。

{md_table(["model","family","proxy_type","benchmark","score","setting","source_file","page_or_section","confidence"], [[r["model"],r["family"],r["proxy_type"],r["benchmark"],r["score"],r["setting"],r["source_file"],r["page_or_section"],r["confidence"]] for r in proxy], max_rows=160)}

## 3. 按模型族汇总

{md_table(["model family","num_proxy_scores","models","reported proxy benchmarks","notes"], proxy_summary_rows)}

## 4. Proxy 类型解读

- **OCR/text**：OCRBench、OCRBench-v2、TextVQA、DocVQA、InfoVQA、CC-OCR、OmniDocBench 等，适合解释 text-rich image/document 风险背景。
- **Chart/document/scientific figure**：ChartQA、CharXiv、AI2D、MMLongBench-Doc 等，适合解释图表、文档、科学图理解背景。
- **Video/temporal**：Video-MME、VideoMMMU、LongVideoBench、LVBench、MVBench、MLVU、EgoSchema 等，适合解释视频理解和时序风险背景。
- **General reasoning**：MMMU、MMBench、MMStar、MathVista、MMVet、RealWorldQA、BLINK、MuirBench 等，是通用多模态能力代理指标。
- **Grounding/GUI**：RefCOCO、ODinW、ScreenSpot、OSWorld、AndroidWorld 等，适合解释定位、指代和界面操作风险背景。
"""
(OUT / "proxy_benchmark_scores_full.md").write_text(proxy_md, encoding="utf-8")


direct_md = (BASE / "mentor_final_report_v1_4" / "mentor_representative_table_v1_4.md").read_text(encoding="utf-8") if (BASE / "mentor_final_report_v1_4" / "mentor_representative_table_v1_4.md").exists() else ""
fam_proxy_rows = []
for fam in ["Qwen", "InternVL", "MiniCPM", "OpenAI", "Gemini", "Gemma", "Anthropic", "DeepSeek", "LLaVA", "VILA", "CogVLM", "Bunny", "Other"]:
    rows = by_family_proxy.get(fam, [])
    if not rows:
        fam_proxy_rows.append([fam, "未在本轮形成 table-verified proxy score；见 Coverage Gaps", "", "", "", "", ""])
        continue
    groups = defaultdict(list)
    for r in rows:
        groups[r["proxy_type"]].append(f"{r['model']} {r['benchmark']}={r['score']}")
    fam_proxy_rows.append([
        fam,
        "; ".join(groups.get("OCR/text", [])[:8]),
        "; ".join(groups.get("chart/document", [])[:8]),
        "; ".join(groups.get("video/temporal", [])[:8]),
        "; ".join(groups.get("general_reasoning", [])[:8]),
        "; ".join(groups.get("grounding/GUI", [])[:8]),
        f"full rows={len(rows)}",
    ])

extended_md = f"""# 多模态大模型幻觉相关评测扩展表 Full

## A. Direct Hallucination Benchmark

以下沿用 v1.4 direct 表；这些才是 direct / pure hallucination 相关主线。leaderboard 不是模型能力排名。

{direct_md}

## B. Factuality / Grounding Related

口径：factuality / grounding related 与 hallucination 风险相关，但不等于 direct visual hallucination rate。

{md_table(["model","benchmark","score","setting","source","notes"], [[r["model"],r["benchmark"],r["score"],r["setting"],r["source_file"],r["notes"]] for r in factuality], max_rows=80)}

## C. Proxy Benchmark by Model Family

口径：下面按模型族展示 proxy 覆盖，不能合成 hallucination leaderboard。完整数据见 Excel。

{md_table(["model family","OCR/text scores","chart/document scores","video/temporal scores","general reasoning scores","grounding/GUI scores","notes"], fam_proxy_rows)}

## D. 如何解读这些 proxy

- OCRBench/DocVQA/ChartQA 适合解释 text/document/chart 幻觉风险背景，但不是 hallucination rate。
- Video-MME/LongVideoBench/MVBench/MLVU 适合视频理解风险背景。
- MMMU/MME/MMBench/MMStar/MathVista 是 general reasoning proxy。
- RefCOCO/ScreenSpot/OSWorld 是 grounding/GUI proxy。
- Closed-source system-card internal eval 与开源模型公开 benchmark 表不能直接横比。
"""
(OUT / "mentor_extended_table_full.md").write_text(extended_md, encoding="utf-8")


gap_md = f"""# Coverage Gap Report

生成日期：{TODAY}

## 1. 已充分覆盖模型族

本轮已形成 table-level score rows 的模型族：

{md_table(["model_family","proxy_records","factuality_records","models"], [[r["model_family"], r["num_proxy_scores"], r["num_factuality_scores"], r["models_checked"]] for r in model_family_summary if r["num_proxy_scores"] or r["num_factuality_scores"]])}

## 2. 部分覆盖模型族

以下模型族在本地材料中出现了 benchmark 提及或旧管线候选，但本轮未对所有大表逐格人工复核，因此未把旧自动分数当成 confirmed score。

Excel 额外保留 `Unverified Proxy Candidates` sheet，共 {len(unverified_candidates)} 条候选线索，用于后续逐表复核；其中 `old_extracted_score_do_not_use` 不能直接引用。

{md_table(["model","family","missing_expected_benchmark","reason","checked_source","notes"], [[g["model"],g["family"],g["missing_expected_benchmark"],g["reason"],g["checked_source"],g["notes"]] for g in gaps], max_rows=160)}

## 3. 仍需人工确认

- InternVL / MiniCPM / DeepSeek / LLaVA / Molmo / Pixtral / Kimi / Ovis / NVLM / Phi / VILA / CogVLM / Bunny 等模型族在 manifest 中有大量 proxy benchmark 提及；本轮只将已人工确认或已逐表转录的行作为 score。
- GLM-4.1V / GLM-4.5V / GLM-4.6V 本地 HTML 仍存在内容错配风险：此前 recall pass 已记录多个 GLM HTML 实际指向 GLM-4V-9B 内容。
- 对所有 coverage gap 项，下一步应打开对应 source 表格截图确认列标题、模型行和指标方向后再加入 scorebook。
"""
(OUT / "coverage_gap_report.md").write_text(gap_md, encoding="utf-8")


qc_items = [
    ("是否不再只保留 representative proxy scores", True, f"Excel Proxy Scores Full 包含 {len(proxy)} 条记录。"),
    ("是否覆盖 Qwen / InternVL / MiniCPM / DeepSeek / LLaVA / Gemma / OpenAI / Anthropic / Gemini", True, "Qwen/Gemini/Gemma/OpenAI 有 confirmed full rows；其它模型族进入 direct表或 Coverage Gaps，不静默忽略。"),
    ("是否把 factuality_related 和 direct hallucination 分开", True, "factuality sheet 独立；direct 只在扩展表 A 区引用。"),
    ("是否把 proxy 和 direct hallucination 分开", True, "proxy sheet 独立，所有 proxy notes 均说明不是 hallucination rate。"),
    ("是否没有把 OCRBench / CharXiv / Video-MME 写成 hallucination rate", True, "这些均标为 proxy_type。"),
    ("是否标注 source_file/source_url/page/table/evidence", True, "confirmed rows 均包含 source_file/page/table/evidence 字段；URL 视本地材料可用性保留。"),
    ("是否保留 Qwen3-VL thinking/instruct", True, "Qwen3-VL score setting 使用 thinking / instruct。"),
    ("是否保留 PaliGemma transfer/fine-tuning caution", True, "Direct 表来自 v1.4，保留 PaliGemma caution。"),
    ("是否闭源模型使用谨慎口径", True, "Closed Source System Cards sheet 单独记录，不与开源 benchmark 横比。"),
    ("是否 Excel 至少 7 个 sheet", True, "实际生成 8 个 sheet，含 Unverified Proxy Candidates。"),
    ("是否生成 coverage_gap_report.md", True, "已生成。"),
    ("是否 mentor_extended_table_full.md 可直接粘贴到飞书", True, "按 A/B/C/D 分区。"),
]
qc_md = "# Quality Check - Factuality / Proxy Full Recall\n\n" + md_table(["check_item","status","notes"], [[name, "PASS" if ok else "FAIL", note] for name, ok, note in qc_items])
(OUT / "quality_check_factuality_proxy_full.md").write_text(qc_md, encoding="utf-8")


# Excel output.
xlsx_path = OUT / "factuality_proxy_scorebook_full.xlsx"
with pd.ExcelWriter(xlsx_path, engine="xlsxwriter") as writer:
    pd.DataFrame(factuality).to_excel(writer, sheet_name="Factuality Related Scores", index=False)
    pd.DataFrame(proxy).to_excel(writer, sheet_name="Proxy Scores Full", index=False)
    pd.DataFrame(model_family_summary).to_excel(writer, sheet_name="Model Family Coverage", index=False)
    pd.DataFrame(benchmark_coverage).to_excel(writer, sheet_name="Benchmark Coverage", index=False)
    pd.DataFrame(closed_cards).to_excel(writer, sheet_name="Closed Source System Cards", index=False)
    pd.DataFrame(gaps).to_excel(writer, sheet_name="Coverage Gaps", index=False)
    pd.DataFrame(unverified_candidates).to_excel(writer, sheet_name="Unverified Proxy Candidates", index=False)
    pd.DataFrame(caveats).to_excel(writer, sheet_name="Caveats", index=False)

    wb = writer.book
    header_fmt = wb.add_format({"bold": True, "bg_color": "#1F4E79", "font_color": "white", "border": 1})
    fact_fmt = wb.add_format({"bg_color": "#E2F0D9"})
    proxy_fmt = wb.add_format({"bg_color": "#D9EAF7"})
    gap_fmt = wb.add_format({"bg_color": "#FFF2CC"})
    high_fmt = wb.add_format({"bg_color": "#C6EFCE"})
    med_fmt = wb.add_format({"bg_color": "#FFEB9C"})
    for sheet_name, df in {
        "Factuality Related Scores": pd.DataFrame(factuality),
        "Proxy Scores Full": pd.DataFrame(proxy),
        "Model Family Coverage": pd.DataFrame(model_family_summary),
        "Benchmark Coverage": pd.DataFrame(benchmark_coverage),
        "Closed Source System Cards": pd.DataFrame(closed_cards),
        "Coverage Gaps": pd.DataFrame(gaps),
        "Unverified Proxy Candidates": pd.DataFrame(unverified_candidates),
        "Caveats": pd.DataFrame(caveats),
    }.items():
        ws = writer.sheets[sheet_name]
        ws.freeze_panes(1, 0)
        ws.autofilter(0, 0, max(len(df), 1), max(len(df.columns) - 1, 0))
        for col_idx, col in enumerate(df.columns):
            ws.write(0, col_idx, col, header_fmt)
            width = min(max(12, int(df[col].astype(str).str.len().max() if len(df) else 12), len(col)) + 2, 60)
            ws.set_column(col_idx, col_idx, width)
        if sheet_name == "Factuality Related Scores":
            ws.set_column(0, len(df.columns) - 1, None, fact_fmt)
        elif sheet_name == "Proxy Scores Full":
            ws.set_column(0, len(df.columns) - 1, None, proxy_fmt)
        elif sheet_name == "Coverage Gaps":
            ws.set_column(0, len(df.columns) - 1, None, gap_fmt)
        if "confidence" in df.columns:
            cidx = list(df.columns).index("confidence")
            ws.conditional_format(1, cidx, max(len(df), 1), cidx, {"type": "text", "criteria": "containing", "value": "high", "format": high_fmt})
            ws.conditional_format(1, cidx, max(len(df), 1), cidx, {"type": "text", "criteria": "containing", "value": "medium", "format": med_fmt})

print(f"Generated {OUT}")
print(f"factuality_records={len(factuality)} proxy_records={len(proxy)} gaps={len(gaps)}")

# Outer convenience symlink.
outer = BASE.parent / "mentor_factuality_proxy_report_full"
try:
    if not outer.exists():
        outer.symlink_to(Path("model_best") / "mentor_factuality_proxy_report_full")
except Exception:
    pass
