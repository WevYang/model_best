# 人工核查 Playbook

## 1. 核查目标

只核查 Priority A / B 条目，不重跑全量抽取，不重新分析原始 PDF。  
目标是补足局部表格对齐问题，而不是推翻 v3.1 的 strict audit 结论。

## 2. 核查工具建议

- 优先用 PDF 阅读器打开原始报告。
- 优先看原始 PDF 页面截图，不要只看 `pdftotext` 文本流。
- 如有必要，可以辅助用 `tabula` / `camelot` / `pdfplumber`。
- 最终判定以人工查看表格为准。

## 3. Priority A

### 3.1 InternVL-2.5 Section 5.6.1 列顺序

- 文件：`model_best/InternVL-2.5_2.5_technical_report.pdf`
- 位置：Section 5.6.1，约第 20 页
- 当前自动判断：`medium_verified_needs_table_alignment_check`
- 核查问题：`~62.8` / `~3.65` / `~90.6` 是否对应 HallusionBench / MMHal-Bench / POPE
- 如果确认：更新 `strict_verified_results_flat_v3_1.xlsx`，把 `confidence_display` 提升到 `high_verified`
- 如果否定：降为 `low_manual_check_only`，并从 leaderboard 剔除

### 3.2 InternVL-3 第 11 页 HallusionBench / POPE 列对齐

- 文件：`model_best/InternVL-3_3_technical_report.pdf`
- 位置：第 11 页，Table 1
- 当前自动判断：`low_manual_check_only`
- 核查问题：`HallusionBench ~59.1` 和 `POPE ~90.7` 是否确实对应 InternVL-3 自身行
- 如果确认：可升级为 `medium_verified_needs_table_alignment_check` 或 `high_verified`
- 如果否定：保持低置信度，不进 leaderboard

## 4. Priority B

### 4.1 VILA Table 5 POPE 行位置

- 文件：`model_best/VILA_1_technical_report.pdf`
- 位置：Table 5
- 当前自动判断：rejected，不进 leaderboard
- 核查问题：POPE 列是否有 VILA 自身数值
- 如果确认：可新增 verified row
- 如果否定：保持 rejected

### 4.2 CogVLM POPE 自身 vs 对比模型值

- 文件：`model_best/CogVLM_1_technical_report.pdf`
- 位置：POPE 对比表
- 当前自动判断：rejected
- 核查问题：`58.0` / `91.0` 中哪一个属于 CogVLM 自身
- 如果确认：可新增 verified row
- 如果否定：保持 rejected

### 4.3 Bunny Table 1 POPE F1 值

- 文件：`model_best/Bunny_1_technical_report.pdf`
- 位置：Table 1
- 当前自动判断：rejected
- 核查问题：Bunny 的 POPE F1 值是否在表中清晰可读
- 如果确认：可新增 verified row
- 如果否定：保持 rejected

### 4.4 Qwen3-VL SimpleVQA 行-模型对应

- 文件：`model_best/Qwen3-VL_3_technical_report.pdf`
- 位置：Section 5.1
- 当前自动判断：rejected
- 核查问题：`SimpleVQA 88.8 88.6 81.3 78.7 61.3` 对应哪个 Qwen3-VL 变体
- 如果确认：可新增 verified row；但分类仍应是 factuality-related，不是 pure multimodal hallucination
- 如果否定：保持 rejected

## 5. 更新规则

人工确认后，必须同步更新：

- `strict_verified_results_flat_v3_1.xlsx`
- `strict_leaderboard_final_v3_1.csv`
- `full_research_report_cn_v3_1.md`
- `executive_summary_cn_v3_1.md`
- `final_quality_check_v3_1.md`

