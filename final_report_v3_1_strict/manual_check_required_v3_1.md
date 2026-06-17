# 仍需人工确认的条目清单 v3.1

**版本：** v3.1 strict audit + terminology fix  
**原则：** 未人工确认前，Priority A 条目不得被当作无风险结果；Priority B 条目目前不影响 leaderboard，但若未来补证可新增覆盖项。

## Priority A

### 1. InternVL-2.5 Section 5.6.1 列顺序

- **当前是否影响 leaderboard：** 是。当前为 medium confidence，已进入 coverage leaderboard，但带 table-alignment 风险。
- **确认成功如何升级：** 可把 `confidence_display` 从 `medium_verified_needs_table_alignment_check` 升到 `high_verified`，并去掉 `yes_with_caution` 风险说明。
- **确认失败如何剔除：** 降为 `low_manual_check_only`，从 leaderboard 移出。
- **需要打开的文件和页码：** `model_best/InternVL-2.5_2.5_technical_report.pdf`，Section 5.6.1，约第 20 页。

### 2. InternVL-3 第 11 页 HallusionBench / POPE 列对齐

- **当前是否影响 leaderboard：** 否。当前为 low confidence，不在 leaderboard。
- **确认成功如何升级：** 若行-模型对应确认无误，可升为 `medium_verified_needs_table_alignment_check` 或 `high_verified`，并新增到 coverage leaderboard。
- **确认失败如何剔除：** 保持 `low_manual_check_only`，继续不进 leaderboard。
- **需要打开的文件和页码：** `model_best/InternVL-3_3_technical_report.pdf`，第 11 页，Table 1。

## Priority B

### 3. VILA Table 5 POPE 行位置

- **当前是否影响 leaderboard：** 否，当前为 rejected，不在 leaderboard。
- **确认成功如何升级：** 若找到清晰 POPE 行并能对应 VILA 自身数值，可新增 verified row。
- **确认失败如何剔除：** 保持 false_positive，不新增任何 verified row。
- **需要打开的文件和页码：** `model_best/VILA_1_technical_report.pdf`，Table 5。

### 4. CogVLM POPE 自身 vs 对比模型值

- **当前是否影响 leaderboard：** 否，当前为 rejected。
- **确认成功如何升级：** 若确认 `58.0` 或 `91.0` 中哪一个是 CogVLM 自身，可新增 verified row。
- **确认失败如何剔除：** 保持 false_positive。
- **需要打开的文件和页码：** `model_best/CogVLM_1_technical_report.pdf`，POPE 对比表。

### 5. Bunny Table 1 POPE F1 值

- **当前是否影响 leaderboard：** 否，当前为 rejected。
- **确认成功如何升级：** 若确认 Bunny 的 POPE F1 值，可新增 verified row。
- **确认失败如何剔除：** 保持 false_positive。
- **需要打开的文件和页码：** `model_best/Bunny_1_technical_report.pdf`，Table 1。

### 6. Qwen3-VL SimpleVQA 行-模型对应

- **当前是否影响 leaderboard：** 否，当前为 rejected。
- **确认成功如何升级：** 若确认行-模型对应，可新增 SimpleVQA verified row；该 benchmark 属于 hallucination-related factuality/grounding 类，不应写成 pure multimodal hallucination。
- **确认失败如何剔除：** 保持 false_positive。
- **需要打开的文件和页码：** `model_best/Qwen3-VL_3_technical_report.pdf`，Section 5.1。
