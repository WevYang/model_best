# 多模态大模型幻觉评测 Benchmark 技术调研报告 v3（Strict Audit）

**日期：** 2026-05-28  
**事实来源：** `final_report_strict_audit/`。旧版 `final_report/full_research_report_cn.md` 已废弃，不作为事实来源。

## 1. 调研背景与目标

本项目分析主流多模态大模型官方技术报告、system card、model card、官方 GitHub/HuggingFace model card 中对 hallucination benchmark 的公开披露情况。核心问题包括：哪些模型公开报告 pure hallucination benchmark，哪些只报告 proxy benchmark，不同模型族披露口径有何差异，以及自动抽取中的误报如何剔除。

v3 采用保守口径：宁可少报，不可误报。所有结论只基于 strict audit 文件，不引用旧版 25 条 valid 表和旧版 pure hallucination leaderboard。

## 2. 数据来源与目录结构

项目实际根目录为 `/root/rivermind-data/model_best/model_best`。关键输入目录包括：

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

| 误判类型 | 数量 | 说明 |
| --- | --- | --- |
| 引用编号 [N] | 5 | citation_number_error |
| 章节号 N.M | 4 | section_number_error |
| 模型版本号 | 6 | model_version_error |
| 页码 / PDF页眉 | 3 | page_number_error |
| 相邻 benchmark 分数 | 2 | adjacent_benchmark_error |
| 标准差 / 计数 | 3 | std_or_count_error |
| HTML噪声 / intro_mention | 1 | html_noise_error |
| 其他 | 1 | other |

### 3.2 典型错误案例

| 模型 | Benchmark | 旧错误分数 | 拒绝原因 |
| --- | --- | --- | --- |
| Claude-Sonnet-4.6 | POPE | `4` | score=4 is model version 'Claude Sonnet 4' in HTML page; location=intro_mention; no experi |
| Gemini-1.5 | POPE | `00` | score='00' is formatting artifact from '(00) for improved quality'; location=intro_mention |
| PaliGemma | POPE | `0.3` | score=0.3 is ±0.3 standard deviation from NoCaps/captioning task table; not a POPE score |
| LLaVA-OneVision | CHAIR | `5` | score=5 from natural-language image description 'item marked as 5 is a white bookshelf'; n |
| Qwen3-VL | HallusionBench | `5.3` | score=5.3 is section heading '5.3 Alignment and Subjective Tasks'; not a HallusionBench ac |
| InternVL-1.5 | HallusionBench | `82` | score=82 is citation reference '[82]' for DocVQA test (not HallusionBench); actual Hallusi |
| InternVL-3 | POPE | `11` | score=11 is page number ('11  MME MMB MMBv1.1...'); not a POPE accuracy score (POPE range  |
| MiniCPM-V | CHAIR | `87.4` | score=87.4 is ChartQA score from adjacent table column ('ChartQA  87.4 87.3 89.5'); CHAIR  |

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

| 模型 | Benchmark | Metric | Score | Source | Evidence |
| --- | --- | --- | --- | --- | --- |
| MiniCPM-V | CHAIR | ObjHalBench-CHAIRs (lower is better) | `9.3` | MiniCPM-V_4.5_technical_report.pdf | ObjHalBench (CHAIRs) ↓  9.3 † 13.7 * 17.0 * 11.3 * 12.3 * -  (MiniCPM-V 4.5 is first column, marked †) |
| MiniCPM-V | CHAIR | ObjHalBench-CHAIRi (lower is better) | `5.2` | MiniCPM-V_4.5_technical_report.pdf | ObjHalBench (CHAIRi) ↓  5.2† 7.7∗ 8.9∗ 6.5∗ 6.4∗ -  (MiniCPM-V 4.5 is first column, marked †) |
| MiniCPM-V | MMHal-Bench | score (0-6 scale) | `5.0` | MiniCPM-V_4.5_technical_report.pdf | MMHal-Bench (Score)  5.0†  4.1∗  4.2∗  4.2∗  4.6∗  -  (MiniCPM-V 4.5 is first column †) |
| MiniCPM-o | HallusionBench | accuracy | `59.1` | MiniCPM-o_4.5_technical_report.pdf | Hallucination  HallusionBench  MMHal-Score  MMHal-Hallrate↓  59.1  4.6  23.9  (followed by competitor values: 54.5  3. . |
| MiniCPM-o | MMHal-Bench | score (0-6 scale) | `4.6` | MiniCPM-o_4.5_technical_report.pdf | Hallucination  HallusionBench  MMHal-Score  MMHal-Hallrate↓  59.1  4.6  23.9 |

### 5.2 Medium confidence results

| 模型 | Benchmark | Metric | Score | 需注意 |
| --- | --- | --- | --- | --- |
| PaliGemma | POPE | accuracy | `86.0 / 87.0` | PaliGemma reports POPE as a transfer/fine-tuning task (prefix with ⌞), not zero-shot. 224px=86.0, 448px=87.0.  |
| InternVL-2.5 | HallusionBench | average of aAcc/fAcc/qAcc | `~62.8 (InternVL2.5-8B)` | Section 5.6.1 is dedicated to hallucination benchmarks. Table row confirmed for InternVL2.5-8B. Column mapping |
| InternVL-2.5 | MMHal-Bench | score (0-6 scale) | `~3.65 (InternVL2.5-8B)` | MMHal score 3.65 is on 0-6 scale (plausible). Section 5.6 explicitly describes MMHal-Bench. Score assigned to  |
| InternVL-2.5 | POPE | average F1 / accuracy | `~90.6 (InternVL2.5-8B)` | POPE score ~90.6 for InternVL2.5-8B (last column in table row). POPE range 60-100%, 90.6 is plausible. Confide |

其中 InternVL-2.5 的 `~62.8 / ~3.65 / ~90.6` 来自 Section 5.6.1 表格列顺序推断，需人工确认列对齐；PaliGemma 的 POPE 为 transfer/fine-tuning 任务形式，不应与 zero-shot POPE 直接比较。

### 5.3 Low confidence / 人工确认条目

| 模型 | Benchmark | 估计分数 | 原因 |
| --- | --- | --- | --- |
| InternVL-3 | HallusionBench | `~59.1 (InternVL3-38B, estimated from table fragment)` | Table structure confirmed: column 'HallBench' exists in InternVL-3 paper table. Score ~59.1 inferred from '59. |
| InternVL-3 | POPE | `~90.7 (InternVL3-1B, cross-ref from InternVL3 comparison table)` | InternVL3-1B POPE=90.7 cross-referenced from InternVL3 comparison table in paper. Confidence=low: column posit |

这些条目不进入最终排名，详见 `manual_check_required.md`。

## 6. 模型族分析

### 6.1 开源模型

开源模型中，MiniCPM-V 4.5 与 MiniCPM-o 4.5 的证据最强，均在 Hallucination 相关评测区给出完整表格行。InternVL-2.5 有专用 Section 5.6.1，覆盖 HallusionBench、MMHal-Bench、POPE，但列顺序仍需人工确认。PaliGemma 报告了 POPE 86.0 / 87.0，但属于 fine-tune/transfer 任务口径。

当前 leaderboard：

| Rank | Model | Organization | Verified pure benchmark count | Benchmarks | Confidence |
| --- | --- | --- | --- | --- | --- |
| 1 | InternVL-2.5 | Shanghai AI Lab | 3 | POPE, HallusionBench, MMHal-Bench | high=0, medium=3 |
| 2 | MiniCPM-V | Tsinghua/ModelBest | 2 | CHAIR, MMHal-Bench | high=3, medium=0 |
| 3 | MiniCPM-o | Tsinghua/ModelBest | 2 | HallusionBench, MMHal-Bench | high=2, medium=0 |
| 4 | PaliGemma | Google | 1 | POPE | high=0, medium=1 |

### 6.2 闭源模型

OpenAI / Anthropic 在当前本地官方公开语料中未公开 POPE、CHAIR、AMBER、HallusionBench、MMHal-Bench 等视觉幻觉专项 benchmark 的实验表格；但其系统卡披露了 factuality、安全性、内部 hallucination/deception 相关评估。正确口径是“未公开这些公开视觉幻觉专项 benchmark 表格”，不得扩大为否定其内部评测。

Google DeepMind 的 Gemini 系列主要披露 CharXiv、DocVQA、ChartQA、MMMU 等 proxy 指标。旧版 Gemini-1.5/POPE 与 Gemini-2.5/FACTS-Grounding 误报已被拒绝。

### 6.3 国内模型

MiniCPM 与 InternVL 是当前语料中 pure hallucination 披露较多的国内模型族。Qwen3-VL、GLM、DeepSeek-VL、Kimi-VL 等在 strict audit 中没有 high/medium verified pure hallucination 结果；其中 Qwen3-VL/SimpleVQA 需要人工确认行-模型对应，GLM 旧 HallusionBench 结果为模型版本号误判。

### 6.4 小模型与端侧模型

MiniCPM-V 4.5 和 MiniCPM-o 4.5 是本次 high confidence 的主体，适合作为端侧/小模型公开披露 pure hallucination benchmark 的代表案例。Bunny 可能存在 POPE F1 值，但当前仅列入人工确认清单，未进入结果。

## 7. Pure benchmark 与 proxy benchmark 的最终拆分

**Pure hallucination benchmark** 直接测量幻觉或事实忠实度输出，包括：POPE, CHAIR, HallusionBench, MMHal-Bench, AMBER, FaithScore, FACTS-Grounding, SimpleVQA。

**Proxy benchmark** 测量 OCR、图表、文档、视频、综合推理、caption 等相关能力，包括：CharXiv, OCRBench, OCRBench-v2, Video-MME, LongVideoBench, TempCompass, DocVQA, ChartQA, InfoVQA, TextVQA, MMBench, MMStar, MathVista, MMMU, MMVet, NoCaps, COCO-Cap, VQAv2, ScienceQA, AI2D。

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
