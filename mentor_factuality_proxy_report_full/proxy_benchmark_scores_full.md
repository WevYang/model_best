# Proxy Benchmark 官方分数与覆盖全量整理

生成日期：2026-05-29

## 1. 口径说明

Proxy benchmark 不是 hallucination rate。OCRBench、DocVQA、ChartQA、Video-MME、MMMU、MMBench、RefCOCO、ScreenSpot 等反映 OCR、文档、图表、视频、推理、grounding 或 GUI 能力背景，不能与 POPE/CHAIR/HallusionBench/MMHal-Bench 合并排名。

## 2. 全量 proxy 分数表

本轮 full recall 共整理 732 条 table-level proxy score 记录。为避免 Markdown 过长，下表仅展示前 160 条；完整数据见 `factuality_proxy_scorebook_full.xlsx` 的 `Proxy Scores Full` sheet。

另有 352 条来自既有 audit/matrix 的 proxy candidate 记录进入 Excel 的 `Unverified Proxy Candidates` sheet；这些只用于召回线索，旧抽取分数不作为 confirmed score。

| model | family | proxy_type | benchmark | score | setting | source_file | page_or_section | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | MMMU | 80.6 / 78.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | MMMU-Pro | 69.3 / 68.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | MathVistamini | 85.8 / 84.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | MathVision | 74.6 / 66.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | MathVisionWP | 63.8 / 57.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | We-Math | 74.8 / 67.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | MathVersemini | 85.0 / 72.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | DynaMath | 82.8 / 79.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | Math-VR | 66.8 / 65.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | ZeroBench | 4 / 2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | VlmsAreBlind | 79.5 / 80.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | LogicVista | 72.2 / 65.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | VisuLogic | 34.4 / 29.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | VisualPuzzles | 57.2 / 54.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | MMBench-EN | 88.8 / 89.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | MMBench-CN | 88.6 / 88.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | RealWorldQA | 81.3 / 79.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | MMStar | 78.7 / 78.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | OCR/text | DocVQAtest | 96.5 / 97.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | OCR/text | InfoVQAtest | 89.5 / 89.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | chart/document | AI2Dw. M. | 89.2 / 89.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | chart/document | ChartQAtest | 90.3 / 90.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | OCR/text | OCRBench | 875 / 920 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | OCR/text | OCRBench_v2en | 66.8 / 67.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | OCR/text | OCRBench_v2zh | 63.5 / 61.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | OCR/text | CC-OCR | 81.5 / 82.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | OCR/text | OmniDocBenchen | 0.155 / 0.143 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | OCR/text | OmniDocBenchzh | 0.207 / 0.207 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | chart/document | CharXiv(DQ) | 90.5 / 89.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | chart/document | CharXiv(RQ) | 66.1 / 62.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | chart/document | MMLongBenchDoc | 56.2 / 57.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | RefCOCO-avg | 92.1 / 91.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | CountBench | 93.7 / 93.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | ODinW-13 | 43.2 / 48.6 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | ARKitScenes | 53.7 / 56.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | Hypersim | 11.0 / 13.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | SUNRGBD | 34.9 / 39.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | ERQA | 52.5 / 51.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | VSI-Bench | 60.0 / 62.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | EmbSpatialBench | 84.3 / 83.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | RefSpatialBench | 69.9 / 65.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | RoboSpatialHome | 73.9 / 69.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | BLINK | 67.1 / 70.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | MUIRBENCH | 80.1 / 73.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | video/temporal | MVBench | 75.2 / 76.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | video/temporal | Video-MMEw/o sub. | 79.0 / 79.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | video/temporal | MLVUM-Avg | 83.8 / 84.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | video/temporal | LVBench | 63.6 / 67.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | video/temporal | Charades-STAmIoU | 63.5 / 64.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | video/temporal | VideoMMMU | 80.0 / 74.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | video/temporal | MMVU | 71.1 / 68.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | V* | 85.9 / 93.7+ | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | HRBench4K | 84.3 / 85.4+ | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | HRBench8K | 76.6 / 82.4+ | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | Design2Code | 93.4 / 92.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | chart/document | ChartMimic | 78.4 / 80.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | general_reasoning | UniSVG | 65.8 / 69.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | ScreenSpot Pro | 61.8 / 62.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | OSWorldG | 68.3 / 66.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | AndroidWorld | 62.0 / 63.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | OSWorld | 38.1 / 31.6 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-235B-A22B | Qwen | grounding/GUI | WindowsAA | 32.1 / 28.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.15 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | MMMU | 76.0 / 74.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | MMMU | 78.1 / 76.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | MMMU-Pro | 63.0 / 60.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | MMMU-Pro | 68.1 / 65.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | MathVistamini | 81.9 / 80.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | MathVistamini | 85.9 / 83.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | MathVision | 65.7 / 60.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | MathVision | 70.2 / 63.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | MathVisionWP | 58.9 / 52.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | MathVisionWP | 58.6 / 54.6 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | We-Math | 70.0 / 56.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | We-Math | 71.6 / 63.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | MathVersemini | 79.6 / 70.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | MathVersemini | 82.6 / 76.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | DynaMath | 80.1 / 73.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | DynaMath | 82.0 / 76.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | Math-VR | 61.7 / 61.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | Math-VR | 62.3 / 59.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | ZeroBench | 0 / 0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | ZeroBench | 2 / 1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | VlmsAreBlind | 72.5 / 67.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | VlmsAreBlind | 85.1 / 87.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | LogicVista | 65.8 / 53.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | LogicVista | 70.9 / 62.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | VisuLogic | 26.6 / 23.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | VisuLogic | 32.4 / 29.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | VisualPuzzles | 52.0 / 46.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | VisualPuzzles | 54.7 / 53.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | MMBench-EN | 87.0 / 86.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | MMBench-EN | 89.5 / 87.6 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | MMBench-CN | 85.9 / 85.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | MMBench-CN | 89.4 / 87.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | RealWorldQA | 77.4 / 73.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | RealWorldQA | 78.4 / 79.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | MMStar | 75.5 / 72.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | MMStar | 79.4 / 77.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | OCR/text | DocVQAtest | 95.5 / 95.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | OCR/text | DocVQAtest | 96.1 / 96.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | OCR/text | InfoVQAtest | 85.6 / 81.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | OCR/text | InfoVQAtest | 89.2 / 87.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | chart/document | AI2Dw. M. | 86.9 / 85.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | chart/document | AI2Dw. M. | 88.9 / 89.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | chart/document | ChartQAtest | 89.4 / 86.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | chart/document | ChartQAtest | 89.0 / 88.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | OCR/text | OCRBench | 839 / 903 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | OCR/text | OCRBench | 855 / 895 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | OCR/text | OCRBench_v2en | 62.6 / 63.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | OCR/text | OCRBench_v2en | 68.4 / 67.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | OCR/text | OCRBench_v2zh | 60.4 / 57.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | OCR/text | OCRBench_v2zh | 62.1 / 59.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | OCR/text | CC-OCR | 77.8 / 80.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | OCR/text | CC-OCR | 79.6 / 80.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | OCR/text | OmniDocBenchen | 0.165 / 0.183 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | OCR/text | OmniDocBenchen | 0.148 / 0.151 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | OCR/text | OmniDocBenchzh | 0.233 / 0.253 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | OCR/text | OmniDocBenchzh | 0.236 / 0.239 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | chart/document | CharXiv(DQ) | 86.9 / 85.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | chart/document | CharXiv(DQ) | 90.2 / 90.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | chart/document | CharXiv(RQ) | 56.6 / 48.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | chart/document | CharXiv(RQ) | 65.2 / 62.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | chart/document | MMLongBenchDoc | 47.4 / 47.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | chart/document | MMLongBenchDoc | 54.6 / 55.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | RefCOCO-avg | 89.3 / 89.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | RefCOCO-avg | 91.1 / 91.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | CountBench | 90.0 / 89.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | CountBench | 94.1 / 94.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | ODinW-13 | 42.3 / 47.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | ODinW-13 | 41.8 / 46.6 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | ARKitScenes | 55.6 / 56.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | ARKitScenes | 46.1 / 55.6 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | Hypersim | 11.4 / 12.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | Hypersim | 12.5 / 14.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | SUNRGBD | 34.6 / 38.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | SUNRGBD | 33.9 / 37.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | ERQA | 45.3 / 43.0 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | ERQA | 52.3 / 48.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | VSI-Bench | 56.1 / 63.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | VSI-Bench | 61.2 / 61.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | EmbSpatialBench | 80.6 / 76.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | EmbSpatialBench | 82.7 / 81.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | RefSpatialBench | 54.2 / 53.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | RefSpatialBench | 67.2 / 61.4 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | grounding/GUI | RoboSpatialHome | 65.5 / 62.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | grounding/GUI | RoboSpatialHome | 74.2 / 64.6 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | BLINK | 65.4 / 67.7 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | BLINK | 68.5 / 67.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | general_reasoning | MUIRBENCH | 77.6 / 62.9 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | general_reasoning | MUIRBENCH | 80.3 / 72.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | video/temporal | MVBench | 72.0 / 72.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | video/temporal | MVBench | 73.2 / 72.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | video/temporal | Video-MMEw/o sub. | 73.3 / 74.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | video/temporal | Video-MMEw/o sub. | 77.3 / 76.6 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | video/temporal | MLVUM-Avg | 78.9 / 81.3 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | video/temporal | MLVUM-Avg | 82.3 / 82.1 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | video/temporal | LVBench | 59.2 / 62.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | video/temporal | LVBench | 62.6 / 63.8 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-30B-A3B | Qwen | video/temporal | Charades-STAmIoU | 62.7 / 63.5 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |
| Qwen3-VL-32B | Qwen | video/temporal | Charades-STAmIoU | 62.8 / 61.2 | thinking / instruct | Qwen3-VL_3_technical_report.pdf | PDF p.16 | high |

## 3. 按模型族汇总

| model family | num_proxy_scores | models | reported proxy benchmarks | notes |
| --- | --- | --- | --- | --- |
| Gemini | 66 | Gemini 1.5 Flash, Gemini 1.5 Pro, Gemini 2.0 Flash, Gemini 2.0 Flash-Lite, Gemini 2.5 Flash, Gemini 2.5 Pro | 1H-VideoQA, ActivityNet-QA, BetterChartQA, EgoTempo, LVBench, MMMU, Perception Test, QVHighlights, VideoMME, VideoMME audio+visual+subtitles, VideoMMMU | 完整行见 Excel / Proxy Scores Full |
| Gemma | 48 | Gemma 3 12B, Gemma 3 12B IT, Gemma 3 12B PT, Gemma 3 27B, Gemma 3 27B IT, Gemma 3 27B PT, Gemma 3 4B, Gemma 3 4B IT, Gemma 3 4B PT | AI2D, ChartQA, DocVQA, InfoVQA, MMMU, RealWorldQA, TextVQA, VQAv2 | 完整行见 Excel / Proxy Scores Full |
| Qwen | 618 | Qwen2.5-Omni-7B, Qwen2.5-VL-3B, Qwen2.5-VL-72B, Qwen2.5-VL-7B, Qwen3-VL-235B-A22B, Qwen3-VL-2B, Qwen3-VL-30B-A3B, Qwen3-VL-32B, Qwen3-VL-4B, Qwen3-VL-8B, Qwen3.5-Omni-Flash, Qwen3. | AI2D, AI2D_TEST, AI2Dw. M., ARKitScenes, AV-SpeakerBench, AVUT, Android Control HighEM, Android Control LowEM, AndroidWorld, AndroidWorldSR, BLINK, CC-OCR, CharXiv (RQ), CharXiv(DQ), CharXiv(RQ), Charades-STAmIoU, ChartMimic, ChartQAtest, ChartQAtest Avg, Char | 完整行见 Excel / Proxy Scores Full |

## 4. Proxy 类型解读

- **OCR/text**：OCRBench、OCRBench-v2、TextVQA、DocVQA、InfoVQA、CC-OCR、OmniDocBench 等，适合解释 text-rich image/document 风险背景。
- **Chart/document/scientific figure**：ChartQA、CharXiv、AI2D、MMLongBench-Doc 等，适合解释图表、文档、科学图理解背景。
- **Video/temporal**：Video-MME、VideoMMMU、LongVideoBench、LVBench、MVBench、MLVU、EgoSchema 等，适合解释视频理解和时序风险背景。
- **General reasoning**：MMMU、MMBench、MMStar、MathVista、MMVet、RealWorldQA、BLINK、MuirBench 等，是通用多模态能力代理指标。
- **Grounding/GUI**：RefCOCO、ODinW、ScreenSpot、OSWorld、AndroidWorld 等，适合解释定位、指代和界面操作风险背景。
