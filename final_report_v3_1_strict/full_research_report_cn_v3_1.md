# 多模态大模型幻觉评测 Benchmark 技术调研报告 v3.1（Strict Audit + Terminology Fix）

**日期：** 2026-05-28  
**事实来源：** 仅限 `final_report_v3_strict/` 与 `analysis_results/benchmark_column_dictionary.xlsx`。不重新分析原始 PDF，不重新下载文件。

## 1. 调研背景与目标

本项目分析多模态大模型官方公开材料中对 hallucination benchmark 的披露情况。v3.1 只做口径修订：把 pure hallucination、hallucination-related factuality/grounding、proxy capability 三层分开，并把 medium confidence 结果明确标成风险项。

## 2. 数据来源与目录结构

项目实际根目录为 `/root/rivermind-data/model_best/model_best`。v3.1 直接读取 `final_report_v3_strict/`，并以 `analysis_results/benchmark_column_dictionary.xlsx` 作为 benchmark 分类字典。该字典共 28 个 benchmark columns，其中 pure=6、factuality_related=2、proxy=20。正文只列代表性 benchmark，不再硬写完整清单。

## 3. 自动抽取为何失败：旧 25 条 valid 全部被拒绝

strict audit 的结论保持不变：旧版 25 条 valid_official_result 全部作废。本版不重新抽取，只修正表述。

### 3.1 错误类型统计

| 误判类型 | 数量 | 说明 |
| --- | --- | --- |
| 引用编号 [N] | 5 | citation_number_error |
| 章节号 N.M | 4 | section_number_error |
| 模型版本号 | 2 | model_version_error |
| 页码 / PDF页眉 | 1 | page_number_error |
| 相邻 benchmark 分数 | 2 | adjacent_benchmark_error |
| 标准差 / 计数 | 2 | std_or_count_error |
| HTML噪声 / intro_mention | 5 | html_noise_error |
| 其他 | 4 | other |

### 3.2 典型错误案例

| 模型 | Benchmark | 旧错误分数 | 拒绝原因 |
| --- | --- | --- | --- |
| Claude-Sonnet-4.6 | POPE | `4` | score=4 is model version 'Claude Sonnet 4' in HTML page; location=intro_mention; no experiment table |
| Gemini-2.5 | FACTS-Grounding | `1.5` | score=1.5 is 'Gemini 1.5' model name appearing before FACTS-Grounding mention; no score table row fo |
| LLaVA-OneVision | CHAIR | `5` | score=5 from natural-language image description 'item marked as 5 is a white bookshelf'; not a CHAIR |
| Qwen3-VL | HallusionBench | `5.3` | score=5.3 is section heading '5.3 Alignment and Subjective Tasks'; not a HallusionBench accuracy sco |
| Qwen3-VL | SimpleVQA | `1` | score=1 from section enumeration '1. General Visual Question Answering'; not a SimpleVQA score |
| InternVL-2.5 | MMHal-Bench | `77` | score=77 is citation '[77]' for HallusionBench paper (not an MMHal score); MMHal score range is 0-6, |
| MiMo-VL | AMBER | `3.1` | score=3.1 from 'Mixed On-policy Reinforcement Learning (MORL)' section—no numeric score context; loc |

## 4. Strict Audit 方法

### 4.1 valid_official_result 的严格判定标准

证据必须来自官方实验表格或明确的评测区，且能同时对应模型、benchmark、metric 与分数。引用编号 `[N]`、章节号 `N.M`、模型版本号、页码、标准差 `±N`、相邻 benchmark 分数和 HTML 噪声都不能当作 valid。

### 4.2 high / medium / low confidence 定义

- **high**：完整表格行可确认，直接可引用。
- **medium**：有表格证据，但列对齐需要人工确认，必须带风险标记。
- **low**：只能进入人工确认清单，不进 leaderboard。

## 5. 最终 verified results

### 5.1 High confidence results

| 模型 | Benchmark | Metric | Score | confidence_display | evaluation_setting | comparability_notes |
| --- | --- | --- | --- | --- | --- | --- |
| MiniCPM-V | CHAIR | ObjHalBench-CHAIRs (lower is better) | `9.3` | high_verified | zero_shot | ObjHalBench uses CHAIRs/CHAIRi metrics (same as CHAIR benchmark). MiniCPM-V 4.5 achieves CHAIRs=9.3 (↓ better), CHAIRi=5.2. Benchmark is correctly mapped to CHAIR in our taxonomy. |
| MiniCPM-V | CHAIR | ObjHalBench-CHAIRi (lower is better) | `5.2` | high_verified | zero_shot | CHAIRi metric for MiniCPM-V 4.5. Also: MiniCPM-V MMHal-Bench Score=5.0 found in same table (MMHal is 0-6 scale, 5.0 is plausible). |
| MiniCPM-V | MMHal-Bench | score (0-6 scale) | `5.0` | high_verified | zero_shot | MMHal-Bench Score range 0-6. MiniCPM-V 4.5 = 5.0 (first column, marked †). Hallrate=19.4 (lower is better). |
| MiniCPM-o | HallusionBench | accuracy | `59.1` | high_verified | zero_shot | Clear section header 'Hallucination HallusionBench MMHal-Score MMHal-Hallrate↓' followed by MiniCPM-o scores. HallusionBench=59.1, MMHal-Score=4.6, MMHal-Hallrate=23.9. |
| MiniCPM-o | MMHal-Bench | score (0-6 scale) | `4.6` | high_verified | zero_shot | MMHal-Score=4.6 (0-6 scale, plausible). MMHal-Hallrate=23.9% (lower is better). |

### 5.2 Medium confidence results

| 模型 | Benchmark | Metric | Score | confidence_display | evaluation_setting | comparability_notes |
| --- | --- | --- | --- | --- | --- | --- |
| PaliGemma | POPE | accuracy | `86.0 / 87.0` | medium_verified_needs_table_alignment_check | transfer_finetuning | POPE is reported in a transfer/fine-tuning setting and is not directly comparable to zero-shot MLLM hallucination results. PaliGemma reports POPE as a transfer/fine-tuning task (prefix with ⌞), not zero-shot. 224px=86.0, 448px=87.0. Which variant is 'official' is model-size dependent. |
| InternVL-2.5 | HallusionBench | average of aAcc/fAcc/qAcc | `~62.8 (InternVL2.5-8B)` | medium_verified_needs_table_alignment_check | zero_shot | Section 5.6.1 column alignment still needs manual confirmation. Section 5.6.1 is dedicated to hallucination benchmarks. Table row confirmed for InternVL2.5-8B. Column mapping: the 7th numeric value (62.8) maps to HallBench(avg). Multiple InternVL2.5 sizes reported: 1B=50.1, 2B=53.7, 4B=58.3, 8B=62.8. Confidence=medium because exact column order is inferred from PDF text flow (PDF extraction may lose sub-column structure). |
| InternVL-2.5 | MMHal-Bench | score (0-6 scale) | `~3.65 (InternVL2.5-8B)` | medium_verified_needs_table_alignment_check | zero_shot | Section 5.6.1 column alignment still needs manual confirmation. MMHal score 3.65 is on 0-6 scale (plausible). Section 5.6 explicitly describes MMHal-Bench. Score assigned to 9th numeric position in row. Confidence=medium for same reason as HallusionBench entry. |
| InternVL-2.5 | POPE | average F1 / accuracy | `~90.6 (InternVL2.5-8B)` | medium_verified_needs_table_alignment_check | zero_shot | Section 5.6.1 column alignment still needs manual confirmation. POPE score ~90.6 for InternVL2.5-8B (last column in table row). POPE range 60-100%, 90.6 is plausible. Confidence=medium due to PDF column-order inference. |

**补充说明：** InternVL-2.5 是 medium confidence，Section 5.6.1 列顺序仍待人工确认；PaliGemma 的 POPE 为 transfer/fine-tuning 口径，不能与 zero-shot 直接横比。

### 5.3 Low confidence / 人工确认条目

| 模型 | Benchmark | Metric | Score | confidence_display | evaluation_setting | comparability_notes |
| --- | --- | --- | --- | --- | --- | --- |
| InternVL-3 | HallusionBench | average accuracy | `~59.1 (InternVL3-38B, estimated from table fragment)` | low_manual_check_only | unclear | Manual check only; excluded from leaderboard. Table structure confirmed: column 'HallBench' exists in InternVL-3 paper table. Score ~59.1 inferred from '59.1% (1.7↑)' pattern. Confidence=low because exact model-row mapping in this table fragment is uncertain—multiple model sizes are listed without clear row labels in the extracted text. |
| InternVL-3 | POPE | average accuracy | `~90.7 (InternVL3-1B, cross-ref from InternVL3 comparison table)` | low_manual_check_only | unclear | Manual check only; excluded from leaderboard. InternVL3-1B POPE=90.7 cross-referenced from InternVL3 comparison table in paper. Confidence=low: column position (11th value in row) inferred from table header alignment, and InternVL3 may report multiple model sizes. |

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
