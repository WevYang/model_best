# Factuality / Grounding Related Benchmark 官方分数全量整理

生成日期：2026-05-29

## 1. 口径说明

本文件只整理 factuality / grounding related benchmark。它们与 hallucination 相关，但不是 POPE、CHAIR、HallusionBench、MMHal-Bench、CRPE 这类 direct visual hallucination benchmark，也不能写成 multimodal hallucination rate。

## 2. Benchmark taxonomy

| benchmark | category | 测什么 | 任务形式 | 指标 | higher/lower better | 是否可横比 | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FACTS-Grounding | factuality_related | Document/source-grounded factual correctness | document-grounded QA/judging | accuracy/score | higher better | yes within same source/config | Not pure multimodal hallucination. |
| SimpleVQA | factuality_related | Visual factuality / simple visual QA | image+question | accuracy | higher better | yes within same source/config | Qwen reports thinking/instruct separately. |
| SimpleQA | factuality_related | Text/world-knowledge factuality | short-answer fact questions | accuracy and/or hallucination rate | accuracy higher, hallucination lower | partly | OpenAI/Gemini report it as factuality, not visual hallucination. |
| LongFact | factuality_related | Long-form factuality | open-ended fact-seeking prompts | claim-level error rate | lower better | no exact table in this pass | GPT-5 system card uses it with FActScore. |
| FActScore | factuality_related | Biography/fact consistency | open-ended biography prompts | claim-level error rate | lower better | no exact table in this pass | GPT-5 system card reports figure-level results. |
| HealthBench Hard Hallucinations | factuality_related | Medical factuality/safety hard cases | health QA / rubric eval | score / hallucination subset | higher score better | only within OpenAI system-card context | Not multimodal direct hallucination. |
| system-card factuality/internal eval | factuality_related | Provider-specific internal factuality/risk eval | internal/red-team/system-card tests | varies | varies | no | Keep separate from public academic benchmark tables. |

## 3. 全量模型分数表

共整理 47 条 factuality_related 记录。完整机器可读版本见 `factuality_proxy_scorebook_full.xlsx` 的 `Factuality Related Scores` sheet。

| model | family | organization | benchmark | score | setting | source_file | page_or_section | confidence | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3-VL-235B-A22B | Qwen | Alibaba / Qwen | SimpleVQA | 61.3 / 63.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | Table 2/3/4 | high | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3-VL-32B | Qwen | Alibaba / Qwen | SimpleVQA | 55.4 / 56.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | Table 2/3/4 | high | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3-VL-30B-A3B | Qwen | Alibaba / Qwen | SimpleVQA | 54.3 / 52.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | Table 2/3/4 | high | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3-VL-8B | Qwen | Alibaba / Qwen | SimpleVQA | 49.6 / 50.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | Table 2/3/4 | high | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3-VL-4B | Qwen | Alibaba / Qwen | SimpleVQA | 48.8 / 48.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | Table 2/3/4 | high | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3-VL-2B | Qwen | Alibaba / Qwen | SimpleVQA | 43.6 / 40.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | Table 2/3/4 | high | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3.5-Plus-Instruct | Qwen | Alibaba / Qwen | SimpleVQA | 66.1 | vision -> text | model_best/Qwen3.5-Omni_3.5_technical_report.pdf | PDF p.12 | high | Factuality-related benchmark; not counted as direct visual hallucination. |
| Qwen3.5-Omni-Flash | Qwen | Alibaba / Qwen | SimpleVQA | 54.4 | vision -> text | model_best/Qwen3.5-Omni_3.5_technical_report.pdf | PDF p.12 | high | Factuality-related benchmark; not counted as direct visual hallucination. |
| Qwen3.5-Omni-Plus | Qwen | Alibaba / Qwen | SimpleVQA | 65.3 | vision -> text | model_best/Qwen3.5-Omni_3.5_technical_report.pdf | PDF p.12 | high | Factuality-related benchmark; not counted as direct visual hallucination. |
| Gemma 3 1B | Gemma | Google DeepMind | FACTS-Grounding | 36.4 | instruction tuned / zero-shot table | model_best/model_reports/Gemma3_3_technical_report.pdf | PDF p.6 | high | Document/source grounding factuality; not pure multimodal hallucination. |
| Gemma 3 4B | Gemma | Google DeepMind | FACTS-Grounding | 70.1 | instruction tuned / zero-shot table | model_best/model_reports/Gemma3_3_technical_report.pdf | PDF p.6 | high | Document/source grounding factuality; not pure multimodal hallucination. |
| Gemma 3 12B | Gemma | Google DeepMind | FACTS-Grounding | 75.8 | instruction tuned / zero-shot table | model_best/model_reports/Gemma3_3_technical_report.pdf | PDF p.6 | high | Document/source grounding factuality; not pure multimodal hallucination. |
| Gemma 3 27B | Gemma | Google DeepMind | FACTS-Grounding | 74.9 | instruction tuned / zero-shot table | model_best/model_reports/Gemma3_3_technical_report.pdf | PDF p.6 | high | Document/source grounding factuality; not pure multimodal hallucination. |
| Gemini 1.5 Flash | Gemini | Google DeepMind | SimpleQA | 8.6% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 1.5 Flash | Gemini | Google DeepMind | FACTS-Grounding | 82.9% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 1.5 Pro | Gemini | Google DeepMind | SimpleQA | 24.9% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 1.5 Pro | Gemini | Google DeepMind | FACTS-Grounding | 80.0% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 2.0 Flash-Lite | Gemini | Google DeepMind | SimpleQA | 16.5% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 2.0 Flash-Lite | Gemini | Google DeepMind | FACTS-Grounding | 82.4% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 2.0 Flash | Gemini | Google DeepMind | SimpleQA | 29.9% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 2.0 Flash | Gemini | Google DeepMind | FACTS-Grounding | 84.6% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 2.5 Flash | Gemini | Google DeepMind | SimpleQA | 26.9% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 2.5 Flash | Gemini | Google DeepMind | FACTS-Grounding | 85.3% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 2.5 Pro | Gemini | Google DeepMind | SimpleQA | 54.0% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| Gemini 2.5 Pro | Gemini | Google DeepMind | FACTS-Grounding | 87.8% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf | PDF p.13 / Table 3 | high |  |
| gpt-5-thinking | OpenAI GPT | OpenAI | SimpleQA | accuracy=0.55; hallucination_rate↓=0.40 | no web | GPT-5_5_system_card.pdf | PDF p.14 / Table 8 | high | Text factuality benchmark from system card; lower hallucination_rate is better. |
| OpenAI o3 | OpenAI GPT | OpenAI | SimpleQA | accuracy=0.54; hallucination_rate↓=0.46 | no web | GPT-5_5_system_card.pdf | PDF p.14 / Table 8 | high | Text factuality benchmark from system card; lower hallucination_rate is better. |
| gpt-5-thinking-mini | OpenAI GPT | OpenAI | SimpleQA | accuracy=0.22; hallucination_rate↓=0.26 | no web | GPT-5_5_system_card.pdf | PDF p.14 / Table 8 | high | Text factuality benchmark from system card; lower hallucination_rate is better. |
| OpenAI o4-mini | OpenAI GPT | OpenAI | SimpleQA | accuracy=0.24; hallucination_rate↓=0.75 | no web | GPT-5_5_system_card.pdf | PDF p.14 / Table 8 | high | Text factuality benchmark from system card; lower hallucination_rate is better. |
| gpt-5-thinking-nano | OpenAI GPT | OpenAI | SimpleQA | accuracy=0.11; hallucination_rate↓=0.31 | no web | GPT-5_5_system_card.pdf | PDF p.14 / Table 8 | high | Text factuality benchmark from system card; lower hallucination_rate is better. |
| gpt-5-main | OpenAI GPT | OpenAI | SimpleQA | accuracy=0.46; hallucination_rate↓=0.47 | no web | GPT-5_5_system_card.pdf | PDF p.14 / Table 8 | high | Text factuality benchmark from system card; lower hallucination_rate is better. |
| GPT-4o | OpenAI GPT | OpenAI | SimpleQA | accuracy=0.44; hallucination_rate↓=0.52 | no web | GPT-5_5_system_card.pdf | PDF p.14 / Table 8 | high | Text factuality benchmark from system card; lower hallucination_rate is better. |
| gpt-5-thinking | OpenAI GPT | OpenAI | HealthBench Hard | 46.2 | health factuality/safety | GPT-5_5_system_card.pdf | PDF p.17 | high | HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination. |
| gpt-5-thinking-mini | OpenAI GPT | OpenAI | HealthBench Hard | 40.3 | health factuality/safety | GPT-5_5_system_card.pdf | PDF p.17 | high | HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination. |
| gpt-5-main | OpenAI GPT | OpenAI | HealthBench Hard | 25.5 | health factuality/safety | GPT-5_5_system_card.pdf | PDF p.17 | high | HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination. |
| OpenAI o3 | OpenAI GPT | OpenAI | HealthBench Hard | 31.6 | health factuality/safety | GPT-5_5_system_card.pdf | PDF p.17 | high | HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination. |
| GPT-4o | OpenAI GPT | OpenAI | HealthBench Hard | 0.0 | health factuality/safety | GPT-5_5_system_card.pdf | PDF p.17 | high | HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination. |
| gpt-5-thinking | OpenAI GPT | OpenAI | LongFact / FActScore | reported in figure / not tabulated | browsing-enabled claim-level grading | GPT-5_5_system_card.pdf | PDF p.13 / Figure 2 | medium | Figure-only values were not machine-tabulated in this pass; do not compare as exact table score. |
| gpt-5-thinking-mini | OpenAI GPT | OpenAI | LongFact / FActScore | reported in figure / not tabulated | browsing-enabled claim-level grading | GPT-5_5_system_card.pdf | PDF p.13 / Figure 2 | medium | Figure-only values were not machine-tabulated in this pass; do not compare as exact table score. |
| gpt-5-thinking-nano | OpenAI GPT | OpenAI | LongFact / FActScore | reported in figure / not tabulated | browsing-enabled claim-level grading | GPT-5_5_system_card.pdf | PDF p.13 / Figure 2 | medium | Figure-only values were not machine-tabulated in this pass; do not compare as exact table score. |
| OpenAI o3 | OpenAI GPT | OpenAI | LongFact / FActScore | reported in figure / not tabulated | browsing-enabled claim-level grading | GPT-5_5_system_card.pdf | PDF p.13 / Figure 2 | medium | Figure-only values were not machine-tabulated in this pass; do not compare as exact table score. |
| OpenAI o4-mini | OpenAI GPT | OpenAI | LongFact / FActScore | reported in figure / not tabulated | browsing-enabled claim-level grading | GPT-5_5_system_card.pdf | PDF p.13 / Figure 2 | medium | Figure-only values were not machine-tabulated in this pass; do not compare as exact table score. |
| GPT-5.5 | OpenAI GPT | OpenAI | HealthBench / HealthBench Hard | HealthBench=56.5; Hard=31.5; Consensus=95.6; Professional=51.8 | health factuality/safety | GPT-5.5_5.5_system_card.pdf | system card table | medium | Not direct hallucination; included as system-card health factuality/safety signal. |
| Gemma 3 1B | Gemma | Google DeepMind | SimpleQA | 2.2 | IT model zero-shot | model_best/model_reports/Gemma3_3_technical_report.pdf | PDF p.6 | high |  |
| Gemma 3 4B | Gemma | Google DeepMind | SimpleQA | 4.0 | IT model zero-shot | model_best/model_reports/Gemma3_3_technical_report.pdf | PDF p.6 | high |  |
| Gemma 3 12B | Gemma | Google DeepMind | SimpleQA | 6.3 | IT model zero-shot | model_best/model_reports/Gemma3_3_technical_report.pdf | PDF p.6 | high |  |
| Gemma 3 27B | Gemma | Google DeepMind | SimpleQA | 10.0 | IT model zero-shot | model_best/model_reports/Gemma3_3_technical_report.pdf | PDF p.6 | high |  |

## 4. 模型族覆盖总结

- **OpenAI**：GPT-5 system card 披露 SimpleQA、LongFact、FActScore、HealthBench/HealthBench Hard 等 factuality/safety 评估；这些不是视觉 hallucination benchmark。
- **Google / Gemini / Gemma**：Gemini 2.5 报告 SimpleQA 与 FACTS-Grounding；Gemma 3 报告 FACTS-Grounding 和 SimpleQA。
- **Anthropic**：本地 Claude system card/model card 中可确认 safety/factuality/internal risk eval 口径，但未找到可横比 POPE/CHAIR/HallusionBench/MMHal 表格。
- **Qwen**：Qwen3-VL 和 Qwen3.5-Omni 报告 SimpleVQA，且 Qwen3-VL 保留 thinking/instruct 双口径。
- **其它开源模型**：多数主要披露 proxy 或 direct hallucination 分数，factuality_related 表格覆盖较少；未确认项见 `coverage_gap_report.md`。
