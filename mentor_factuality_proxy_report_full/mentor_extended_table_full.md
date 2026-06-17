# 多模态大模型幻觉相关评测扩展表 Full

## A. Direct Hallucination Benchmark

以下沿用 v1.4 direct 表；这些才是 direct / pure hallucination 相关主线。leaderboard 不是模型能力排名。

# 代表模型主表

本表适合直接复制到微信 / 飞书 / 邮件。它不是模型能力排名，只是官方公开分数速览。

| 模型/系列代表 | HallusionBench | MMHal | POPE | CHAIR/ObjHal | CRPE | Factuality-related | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3-VL-235B-A22B | 66.7 / 63.2 | - | - | - | - | SimpleVQA 61.3 / 63.0 | 两个数均为 thinking / instruct；SimpleVQA 属 factuality-related，不计入 pure hallucination。 |
| Qwen2.5-VL-72B | 55.2 (HallBench_avg) | - | - | - | 79.2 | - | HallBench_avg + CRPE_relation；无 POPE/MMHal 官方确认分数。 |
| InternVL3-78B | 59.1 | 3.85 | 90.3 | - | 79.2 | - | v3.2 人工确认；zero-shot 官方报告口径。 |
| InternVL2.5-78B | 57.4 | 3.89 | 90.8 | - | 78.8 | - | v3.2 人工确认；zero-shot 官方报告口径。 |
| MiniCPM-V 4.5 | 61.2 | 5.0 / Hallrate↓ 19.4 | - | CHAIRs↓ 9.3 / CHAIRi↓ 5.2 | - | - | ObjHalBench/CHAIR 口径；lower-is-better。 |
| MiniCPM-o 4.5 | 63.2 | 4.7 / Hallrate↓ 24.3 | - | - | - | - | 公开 HallusionBench 和 MMHal-Bench。 |
| DeepSeek-VL-7B | - | - | 88.1 | - | - | - | POPE 官方表格。 |
| CogVLM-Chat | - | - | 87.9 | - | - | - | POPE 官方表格。 |
| Bunny-8B | - | - | 87.2 | - | - | - | POPE averaged F1-score。 |
| VILA-7B | - | - | 85.5 | - | - | - | POPE 官方表格。 |
| Phi-4-Multimodal-5.6B | - | - | 85.6 | - | - | - | POPE 官方表格。 |
| LLaVA-OneVision-2-8B | - | - | - | - | 77.3 | - | CRPE 官方表格。 |
| GLM-4V-9B | 46.6 | - | - | - | - | - | 本地 GLM 4.1/4.5/4.6 HTML 实际为同一 GLM-4V-9B model card。 |
| PaliGemma | - | - | 86.0 / 87.0 | - | - | - | VQAv2-transferred / fine-tuning setting，不与 zero-shot MLLM 直接横比。 |
| Gemma 3 27B | - | - | - | - | - | FACTS-Grounding 74.9 | factuality/grounding-related only。 |
| OpenAI GPT-4V / GPT-4o / GPT-5 系列 | - | - | - | - | - | system-card factuality / safety / internal eval | 当前未发现可横比 direct 表格。 |
| Anthropic Claude 系列 | - | - | - | - | - | system-card safety / factuality / internal risk eval | 当前未发现可横比 direct 表格。 |
| Google Gemini 闭源系列 | - | - | - | - | - | factuality / grounding / safety / multimodal capability eval | 当前未发现可横比 direct 表格；PaliGemma / Gemma 3 另列，不与 Gemini 闭源混比。 |

附注：Qwen2-VL-72B HallBench_avg=58.1 仅在 Qwen2.5-VL 官方对比表中确认，medium confidence，未放入主表。


## B. Factuality / Grounding Related

口径：factuality / grounding related 与 hallucination 风险相关，但不等于 direct visual hallucination rate。

| model | benchmark | score | setting | source | notes |
| --- | --- | --- | --- | --- | --- |
| Qwen3-VL-235B-A22B | SimpleVQA | 61.3 / 63.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3-VL-32B | SimpleVQA | 55.4 / 56.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3-VL-30B-A3B | SimpleVQA | 54.3 / 52.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3-VL-8B | SimpleVQA | 49.6 / 50.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3-VL-4B | SimpleVQA | 48.8 / 48.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3-VL-2B | SimpleVQA | 43.6 / 40.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | thinking / instruct order; factuality-related, not direct hallucination rate. |
| Qwen3.5-Plus-Instruct | SimpleVQA | 66.1 | vision -> text | model_best/Qwen3.5-Omni_3.5_technical_report.pdf | Factuality-related benchmark; not counted as direct visual hallucination. |
| Qwen3.5-Omni-Flash | SimpleVQA | 54.4 | vision -> text | model_best/Qwen3.5-Omni_3.5_technical_report.pdf | Factuality-related benchmark; not counted as direct visual hallucination. |
| Qwen3.5-Omni-Plus | SimpleVQA | 65.3 | vision -> text | model_best/Qwen3.5-Omni_3.5_technical_report.pdf | Factuality-related benchmark; not counted as direct visual hallucination. |
| Gemma 3 1B | FACTS-Grounding | 36.4 | instruction tuned / zero-shot table | model_best/model_reports/Gemma3_3_technical_report.pdf | Document/source grounding factuality; not pure multimodal hallucination. |
| Gemma 3 4B | FACTS-Grounding | 70.1 | instruction tuned / zero-shot table | model_best/model_reports/Gemma3_3_technical_report.pdf | Document/source grounding factuality; not pure multimodal hallucination. |
| Gemma 3 12B | FACTS-Grounding | 75.8 | instruction tuned / zero-shot table | model_best/model_reports/Gemma3_3_technical_report.pdf | Document/source grounding factuality; not pure multimodal hallucination. |
| Gemma 3 27B | FACTS-Grounding | 74.9 | instruction tuned / zero-shot table | model_best/model_reports/Gemma3_3_technical_report.pdf | Document/source grounding factuality; not pure multimodal hallucination. |
| Gemini 1.5 Flash | SimpleQA | 8.6% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 1.5 Flash | FACTS-Grounding | 82.9% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 1.5 Pro | SimpleQA | 24.9% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 1.5 Pro | FACTS-Grounding | 80.0% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 2.0 Flash-Lite | SimpleQA | 16.5% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 2.0 Flash-Lite | FACTS-Grounding | 82.4% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 2.0 Flash | SimpleQA | 29.9% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 2.0 Flash | FACTS-Grounding | 84.6% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 2.5 Flash | SimpleQA | 26.9% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 2.5 Flash | FACTS-Grounding | 85.3% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 2.5 Pro | SimpleQA | 54.0% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| Gemini 2.5 Pro | FACTS-Grounding | 87.8% | official technical report comparison | Gemini-2.5_2.5_technical_report.pdf |  |
| gpt-5-thinking | SimpleQA | accuracy=0.55; hallucination_rate↓=0.40 | no web | GPT-5_5_system_card.pdf | Text factuality benchmark from system card; lower hallucination_rate is better. |
| OpenAI o3 | SimpleQA | accuracy=0.54; hallucination_rate↓=0.46 | no web | GPT-5_5_system_card.pdf | Text factuality benchmark from system card; lower hallucination_rate is better. |
| gpt-5-thinking-mini | SimpleQA | accuracy=0.22; hallucination_rate↓=0.26 | no web | GPT-5_5_system_card.pdf | Text factuality benchmark from system card; lower hallucination_rate is better. |
| OpenAI o4-mini | SimpleQA | accuracy=0.24; hallucination_rate↓=0.75 | no web | GPT-5_5_system_card.pdf | Text factuality benchmark from system card; lower hallucination_rate is better. |
| gpt-5-thinking-nano | SimpleQA | accuracy=0.11; hallucination_rate↓=0.31 | no web | GPT-5_5_system_card.pdf | Text factuality benchmark from system card; lower hallucination_rate is better. |
| gpt-5-main | SimpleQA | accuracy=0.46; hallucination_rate↓=0.47 | no web | GPT-5_5_system_card.pdf | Text factuality benchmark from system card; lower hallucination_rate is better. |
| GPT-4o | SimpleQA | accuracy=0.44; hallucination_rate↓=0.52 | no web | GPT-5_5_system_card.pdf | Text factuality benchmark from system card; lower hallucination_rate is better. |
| gpt-5-thinking | HealthBench Hard | 46.2 | health factuality/safety | GPT-5_5_system_card.pdf | HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination. |
| gpt-5-thinking-mini | HealthBench Hard | 40.3 | health factuality/safety | GPT-5_5_system_card.pdf | HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination. |
| gpt-5-main | HealthBench Hard | 25.5 | health factuality/safety | GPT-5_5_system_card.pdf | HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination. |
| OpenAI o3 | HealthBench Hard | 31.6 | health factuality/safety | GPT-5_5_system_card.pdf | HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination. |
| GPT-4o | HealthBench Hard | 0.0 | health factuality/safety | GPT-5_5_system_card.pdf | HealthBench Hard Hallucinations is a subset; system-card factuality/safety, not visual direct hallucination. |
| gpt-5-thinking | LongFact / FActScore | reported in figure / not tabulated | browsing-enabled claim-level grading | GPT-5_5_system_card.pdf | Figure-only values were not machine-tabulated in this pass; do not compare as exact table score. |
| gpt-5-thinking-mini | LongFact / FActScore | reported in figure / not tabulated | browsing-enabled claim-level grading | GPT-5_5_system_card.pdf | Figure-only values were not machine-tabulated in this pass; do not compare as exact table score. |
| gpt-5-thinking-nano | LongFact / FActScore | reported in figure / not tabulated | browsing-enabled claim-level grading | GPT-5_5_system_card.pdf | Figure-only values were not machine-tabulated in this pass; do not compare as exact table score. |
| OpenAI o3 | LongFact / FActScore | reported in figure / not tabulated | browsing-enabled claim-level grading | GPT-5_5_system_card.pdf | Figure-only values were not machine-tabulated in this pass; do not compare as exact table score. |
| OpenAI o4-mini | LongFact / FActScore | reported in figure / not tabulated | browsing-enabled claim-level grading | GPT-5_5_system_card.pdf | Figure-only values were not machine-tabulated in this pass; do not compare as exact table score. |
| GPT-5.5 | HealthBench / HealthBench Hard | HealthBench=56.5; Hard=31.5; Consensus=95.6; Professional=51.8 | health factuality/safety | GPT-5.5_5.5_system_card.pdf | Not direct hallucination; included as system-card health factuality/safety signal. |
| Gemma 3 1B | SimpleQA | 2.2 | IT model zero-shot | model_best/model_reports/Gemma3_3_technical_report.pdf |  |
| Gemma 3 4B | SimpleQA | 4.0 | IT model zero-shot | model_best/model_reports/Gemma3_3_technical_report.pdf |  |
| Gemma 3 12B | SimpleQA | 6.3 | IT model zero-shot | model_best/model_reports/Gemma3_3_technical_report.pdf |  |
| Gemma 3 27B | SimpleQA | 10.0 | IT model zero-shot | model_best/model_reports/Gemma3_3_technical_report.pdf |  |

## C. Proxy Benchmark by Model Family

口径：下面按模型族展示 proxy 覆盖，不能合成 hallucination leaderboard。完整数据见 Excel。

| model family | OCR/text scores | chart/document scores | video/temporal scores | general reasoning scores | grounding/GUI scores | notes |
| --- | --- | --- | --- | --- | --- | --- |
| Qwen | Qwen3-VL-235B-A22B DocVQAtest=96.5 / 97.1; Qwen3-VL-235B-A22B InfoVQAtest=89.5 / 89.2; Qwen3-VL-235B-A22B OCRBench=875 / 920; Qwen3-VL-235B-A22B OCRBench_v2en=66.8 / 67.1; Qwen3-VL-235B-A22B OCRBench_v2zh=63.5 / 61.8; Qwen3-VL-235B-A22B CC-OCR=81.5 / 82.2; Qwen3-VL-235B-A22B OmniDocBenchen=0.155 / 0.143; Qwen3-VL-235B-A22B OmniDocBenchzh=0.207 / 0.207 | Qwen3-VL-235B-A22B AI2Dw. M.=89.2 / 89.7; Qwen3-VL-235B-A22B ChartQAtest=90.3 / 90.3; Qwen3-VL-235B-A22B CharXiv(DQ)=90.5 / 89.4; Qwen3-VL-235B-A22B CharXiv(RQ)=66.1 / 62.1; Qwen3-VL-235B-A22B MMLongBenchDoc=56.2 / 57.0; Qwen3-VL-235B-A22B ChartMimic=78.4 / 80.5; Qwen3-VL-30B-A3B AI2Dw. M.=86.9 / 85.0; Qwen3-VL-32B AI2Dw. M.=88.9 / 89.5 | Qwen3-VL-235B-A22B MVBench=75.2 / 76.5; Qwen3-VL-235B-A22B Video-MMEw/o sub.=79.0 / 79.2; Qwen3-VL-235B-A22B MLVUM-Avg=83.8 / 84.3; Qwen3-VL-235B-A22B LVBench=63.6 / 67.7; Qwen3-VL-235B-A22B Charades-STAmIoU=63.5 / 64.8; Qwen3-VL-235B-A22B VideoMMMU=80.0 / 74.7; Qwen3-VL-235B-A22B MMVU=71.1 / 68.1; Qwen3-VL-30B-A3B MVBench=72.0 / 72.3 | Qwen3-VL-235B-A22B MMMU=80.6 / 78.7; Qwen3-VL-235B-A22B MMMU-Pro=69.3 / 68.1; Qwen3-VL-235B-A22B MathVistamini=85.8 / 84.9; Qwen3-VL-235B-A22B MathVision=74.6 / 66.5; Qwen3-VL-235B-A22B MathVisionWP=63.8 / 57.0; Qwen3-VL-235B-A22B We-Math=74.8 / 67.5; Qwen3-VL-235B-A22B MathVersemini=85.0 / 72.5; Qwen3-VL-235B-A22B DynaMath=82.8 / 79.4 | Qwen3-VL-235B-A22B RefCOCO-avg=92.1 / 91.9; Qwen3-VL-235B-A22B CountBench=93.7 / 93.0; Qwen3-VL-235B-A22B ODinW-13=43.2 / 48.6; Qwen3-VL-235B-A22B ARKitScenes=53.7 / 56.9; Qwen3-VL-235B-A22B Hypersim=11.0 / 13.0; Qwen3-VL-235B-A22B SUNRGBD=34.9 / 39.4; Qwen3-VL-235B-A22B ERQA=52.5 / 51.3; Qwen3-VL-235B-A22B VSI-Bench=60.0 / 62.7 | full rows=618 |
| InternVL | 未在本轮形成 table-verified proxy score；见 Coverage Gaps |  |  |  |  |  |
| MiniCPM | 未在本轮形成 table-verified proxy score；见 Coverage Gaps |  |  |  |  |  |
| OpenAI | 未在本轮形成 table-verified proxy score；见 Coverage Gaps |  |  |  |  |  |
| Gemini |  |  | Gemini 1.5 Flash ActivityNet-QA=56.2; Gemini 1.5 Flash EgoTempo=34.5; Gemini 1.5 Flash QVHighlights=64.4; Gemini 1.5 Flash VideoMMMU=64.8; Gemini 1.5 Flash 1H-VideoQA=61.9; Gemini 1.5 Flash LVBench=61.9; Gemini 1.5 Flash VideoMME=70.4; Gemini 1.5 Pro ActivityNet-QA=57.3 | Gemini 1.5 Flash MMMU=58.3%; Gemini 1.5 Flash BetterChartQA=59.0%; Gemini 1.5 Pro MMMU=67.7%; Gemini 1.5 Pro BetterChartQA=65.8%; Gemini 2.0 Flash-Lite MMMU=65.1%; Gemini 2.0 Flash-Lite BetterChartQA=52.3%; Gemini 2.0 Flash MMMU=69.3%; Gemini 2.0 Flash BetterChartQA=57.8% |  | full rows=66 |
| Gemma | Gemma 3 4B PT DocVQA=72.8; Gemma 3 4B PT InfoVQA=44.1; Gemma 3 4B PT TextVQA=58.9; Gemma 3 12B PT DocVQA=82.3; Gemma 3 12B PT InfoVQA=54.8; Gemma 3 12B PT TextVQA=66.5; Gemma 3 27B PT DocVQA=85.6; Gemma 3 27B PT InfoVQA=59.4 | Gemma 3 4B PT AI2D=63.2; Gemma 3 4B PT ChartQA=63.6; Gemma 3 12B PT AI2D=75.2; Gemma 3 12B PT ChartQA=74.7; Gemma 3 27B PT AI2D=79.0; Gemma 3 27B PT ChartQA=76.3; Gemma 3 4B IT AI2D=74.8; Gemma 3 4B IT ChartQA=68.8 |  | Gemma 3 4B MMMU=48.8; Gemma 3 12B MMMU=59.6; Gemma 3 27B MMMU=64.9; Gemma 3 4B PT MMMU=39.2; Gemma 3 4B PT RealWorldQA=45.5; Gemma 3 4B PT VQAv2=63.9; Gemma 3 12B PT MMMU=50.3; Gemma 3 12B PT RealWorldQA=52.2 |  | full rows=48 |
| Anthropic | 未在本轮形成 table-verified proxy score；见 Coverage Gaps |  |  |  |  |  |
| DeepSeek | 未在本轮形成 table-verified proxy score；见 Coverage Gaps |  |  |  |  |  |
| LLaVA | 未在本轮形成 table-verified proxy score；见 Coverage Gaps |  |  |  |  |  |
| VILA | 未在本轮形成 table-verified proxy score；见 Coverage Gaps |  |  |  |  |  |
| CogVLM | 未在本轮形成 table-verified proxy score；见 Coverage Gaps |  |  |  |  |  |
| Bunny | 未在本轮形成 table-verified proxy score；见 Coverage Gaps |  |  |  |  |  |
| Other | 未在本轮形成 table-verified proxy score；见 Coverage Gaps |  |  |  |  |  |

## D. 如何解读这些 proxy

- OCRBench/DocVQA/ChartQA 适合解释 text/document/chart 幻觉风险背景，但不是 hallucination rate。
- Video-MME/LongVideoBench/MVBench/MLVU 适合视频理解风险背景。
- MMMU/MME/MMBench/MMStar/MathVista 是 general reasoning proxy。
- RefCOCO/ScreenSpot/OSWorld 是 grounding/GUI proxy。
- Closed-source system-card internal eval 与开源模型公开 benchmark 表不能直接横比。
