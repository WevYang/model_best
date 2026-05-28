# Hallucination Benchmark Audit — Corrected Summary

**Date:** 2026-05-28
**Audited matrix:** `analysis_results/model_vs_benchmark_matrix.csv`
**Models audited:** 83
**Benchmarks tracked:** 28 total (8 pure hallucination, 20 proxy)

---

## 1. Benchmark Classification

### Pure Hallucination Benchmarks (8)
These benchmarks **directly measure hallucination output**:

| Benchmark | Hallucination Type | Lower is Better |
|-----------|-------------------|-----------------|
| CHAIR | Object hallucination in captions | Yes (lower = less hallucination) |
| POPE | Object existence hallucination (yes/no) | No (higher accuracy = better) |
| HallusionBench | Visual illusion + attribute/relation | No |
| MMHal-Bench | Open-ended multimodal hallucination | No |
| AMBER | Multi-dim LLM-free hallucination eval | No |
| FaithScore | Fine-grained caption faithfulness | No |
| SimpleVQA | World-knowledge factual hallucination | No |
| FACTS-Grounding | Factual grounding + attribution | No |

### Proxy Benchmarks (20 in matrix)
These benchmarks measure **capability**; high scores correlate with but do not directly measure hallucination:
OCR proxy: OCRBench, OCRBench-v2, TextVQA
Chart/document proxy: CharXiv, ChartQA, DocVQA, InfoVQA, AI2D
Video proxy: Video-MME, LongVideoBench, TempCompass
Ability proxy: MMBench, MMStar, MathVista, MMMU, MMVet, VQAv2, ScienceQA
Factuality proxy: NoCaps, COCO-Cap

---

## 2. Audit Results — Value=2 Cell Reclassification

Original value=2 cells: **382**

| Judgment | Count | Percentage |
|----------|-------|------------|
| valid_official_result | 25 | 6.5% |
| proxy_only (score reported, but proxy benchmark) | 313 | 81.9% |
| mentioned_only (score not confirmed in experiment section) | 16 | 4.2% |
| false_positive (not found or references-only) | 28 | 7.3% |

**Key finding:** The majority of value=2 cells in the original matrix are for **proxy benchmarks** (CharXiv, MMMU, DocVQA, ChartQA, MMBench, AI2D, VQAv2, etc.), not pure hallucination benchmarks. These are legitimate experiment results but should NOT be counted as evidence of hallucination measurement.

---

## 3. Corrected Pure Hallucination Benchmark Coverage

Models with verified scores on ≥1 pure hallucination benchmark:

| Model | Pure Hal Benchmarks w/ Scores | Benchmarks Mentioned |
|-------|------------------------------|----------------------|
| InternVL-3 | 3/8 | 3/8 |
| Qwen3-VL | 2/8 | 2/8 |
| InternVL-2.5 | 2/8 | 4/8 |
| MiniCPM-o | 2/8 | 2/8 |
| Claude-Sonnet-4.6 | 1/8 | 1/8 |
| Claude-Opus-4.6 | 1/8 | 1/8 |
| Gemini-1.5 | 1/8 | 1/8 |
| Gemini-2.5 | 1/8 | 1/8 |
| PaliGemma | 1/8 | 1/8 |
| LLaVA-OneVision | 1/8 | 1/8 |
| InternVL | 1/8 | 1/8 |
| InternVL-1.5 | 1/8 | 1/8 |

Pure hallucination benchmark score counts (corrected):

| Benchmark | Models with Scores |
|-----------|--------------------|
| CHAIR | 2 |
| POPE | 9 |
| HallusionBench | 8 |
| MMHal-Bench | 3 |
| AMBER | 1 |
| FaithScore | 0 |
| FACTS-Grounding | 1 |
| SimpleVQA | 1 |

---

## 4. Corrected Conclusions

### ✅ CORRECTED: OpenAI and Anthropic Hallucination Reporting

**Original (incorrect) statement:** "OpenAI and Anthropic models show strong performance on hallucination benchmarks."

**Corrected statement:** OpenAI models (GPT-4, GPT-4V, GPT-4o, GPT-4.1, GPT-5, GPT-5.5) and Anthropic models (Claude-3.5, Claude-4, Claude-Opus-4.7, etc.) **do not report results on any of the 8 pure hallucination benchmarks** (POPE, CHAIR, HallusionBench, MMHal-Bench, AMBER, FaithScore, SimpleVQA, FACTS-Grounding) in their official technical reports or system cards. Their value=2 cells in the original matrix were for proxy benchmarks (CharXiv, MMMU, DocVQA, etc.) which measure general capability, not hallucination specifically. FACTS-Grounding appears in GPT-5 / GPT-5.5 system cards but only with 1 model reporting a score.

### ✅ CORRECTED: FaithScore Reporting

**Original statement:** "FaithScore is not reported by any model."

**Corrected statement:** FaithScore is indeed not reported by any model in this corpus. Zero models have FaithScore = 2 in both the original and corrected matrices. FaithScore is mentioned in some papers (value=1) but no official experiment results appear in the papers surveyed. This finding is **confirmed correct**.

---

## 5. Methodology Notes

- Text extraction: `pdftotext -l 80` (primary) with pdfminer fallback for HTML files
- Score detection: regex search for numeric values (0–100) within ±300 chars of benchmark alias
- Location classification:
  - `experiment_table` → benchmark name near "table", "result", "performance", etc.
  - `references_only` → benchmark name appears after References section header
  - `intro_mention` → mentioned in introduction/related work, no score nearby
  - `not_found` → alias not found in extracted text
- Judgment rules:
  - References-only → `false_positive` or `mentioned_only`
  - Score found + pure hal benchmark + experiment context → `valid_official_result`
  - Score found + proxy benchmark → `proxy_only`
  - Alias found, no score confirmed → `mentioned_only`
  - Alias not found → `false_positive`

---

## 6. Output Files

| File | Description |
|------|-------------|
| `audit_validated_matrix.csv` | Corrected matrix (value=2 only for confirmed scores; pure hal columns first) |
| `audit_evidence_for_all_2s.xlsx` | Evidence record for all 382 original value=2 cells |
| `benchmark_column_dictionary.xlsx` | Full 28-benchmark taxonomy with pure_hal classification |
| `corrected_summary.md` | This file |
| `false_positive_report.csv` | 44 cells reclassified from value=2 |
