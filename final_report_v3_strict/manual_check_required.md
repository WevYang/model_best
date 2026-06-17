# 仍需人工确认的条目清单

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
