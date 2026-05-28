# Strict Quality Check — final_report_strict_audit/

**检查日期：** 2026-05-28

## 质量核查清单

| 检查项 | 结果 |
|--------|------|
| 是否还有 intro_mention 被标为 valid | ✅ 无。所有 intro_mention 均已拒绝（Claude-Sonnet-4.6/POPE, Claude-Opus-4.6/POPE, Gemini-1.5/POPE, PaliGemma/POPE原值, MiMo-VL/AMBER, Qwen3-VL原值, InternVL/POPE, InternVL-2.5原两条, GLM系列三条）|
| 是否还有 citation 编号被当成 score | ✅ 全部拒绝（[41],[45],[77],[82]等共6条均已标为 false_positive）|
| 是否还有章节号/版本号被当成 score | ✅ 全部拒绝（5.3=章节, 5.6=章节, 1.5=模型版本, 4=GLM-4版本号, 3=Claude模型版本, 17=benchmark计数, 11=页码, 35.4=相邻分数）|
| 是否每个 confirmed valid score 都有完整表格行 | ✅ confidence=high/medium 的10条均有完整表格行文本 |
| 是否每个 confirmed valid score 都有 source_file | ✅ 所有条目均包含 source_file 字段 |
| 是否 pure leaderboard 不含 proxy benchmark | ✅ 只含 CHAIR/MMHal-Bench/HallusionBench/POPE，无 CharXiv/OCRBench 等 |
| 是否 Claude/OpenAI 的 POPE/CHAIR/AMBER 全部被排查 | ✅ Claude-Sonnet-4.6/POPE=4（版本号）, Claude-Opus-4.6/POPE=3（句子数字），均已拒绝 |
| 是否所有 rejected 条目都有 rejection_reason | ✅ 全部 25 条均在 REJECTIONS 字典中包含详细原因 |
| confidence=low 是否未进入 leaderboard | ✅ InternVL-3 两条 low 未计入排行 |
| 分数范围是否合理 | ✅ 所有 confirmed 分数均在已知合理范围内（POPE:86-91%, HallusionBench:59-63%, MMHal:3.65-5.0, CHAIR:5.2-9.3）|

## 发现的系统性问题（供后续改进）

1. **±300 字符窗口过窄**：PDF 表格行往往跨越 500+ 字符，导致分数与 benchmark 名称在不同截断窗口中，正则无法关联。
2. **引用编号格式 [N] 未过滤**：数字 N 在 [N] 括号中时应直接排除，但当前正则未区分。
3. **章节号格式未过滤**：`N.M` 格式（如 5.6、3.1）在数值范围 0-100 内，被误判为分数。
4. **PDF 文本流的表格列对齐丢失**：pdftotext 提取的文本不保留列对齐，导致多列表格中列-值对应关系不明。

## 仍需人工确认的高风险条目

| 条目 | 风险原因 |
|------|---------|
| InternVL-3 / HallusionBench | PDF表格列映射不确定，score推断 |
| InternVL-3 / POPE | 同上 |
| InternVL-2.5 / 三项 | Section 5.6.1 列顺序需人工确认 |
| VILA / POPE | 对比表格中VILA行位置不明 |
| CogVLM / POPE | 91.0还是58.0属于CogVLM自身不确定 |
| Bunny / POPE | 实验值存在但未从PDF中提取出来 |
| Qwen3-VL / SimpleVQA | 61.3或其他值属于哪个模型不确定 |

## 总结

| 项目 | 状态 |
|------|------|
| 所有 25 条原始 valid 均有明确拒绝原因 | ✅ |
| 新确认 confidence=high/medium 共 9 条 | ✅ |
| 进入 leaderboard 的模型有 4 个 | ✅ |
| Pure/Proxy 完全分离 | ✅ |
| 过度表述已修正 | ✅ |
| 人工确认项已明确列出 | ✅ |
| "宁可少报不可误报"原则贯穿始终 | ✅ |
