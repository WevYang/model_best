# Final Quality Check v3

**检查日期：** 2026-05-28

| 检查项 | 结果 | 说明 |
|---|---|---|
| 旧版 25 条错误 valid 是否已全部删除 | PASS | 25/25 旧 valid 均在 rejected_previous_valid_results.csv 中标为 rejected/false_positive/mentioned_only。 |
| 是否还有 intro_mention 被作为 valid | PASS | valid rows 均来自表格行或评测表格片段。 |
| 是否还有引用编号 [N] 被作为分数 | PASS | 旧引用编号错误已全部位于 rejected 表。 |
| 是否还有章节号 N.M 被作为分数 | PASS | 未将章节号作为 high/medium valid。 |
| 是否还有模型版本号被作为分数 | PASS | Gemini/Claude/GLM 版本号误报已拒绝。 |
| 是否还有标准差 ±N 被作为分数 | PASS | PaliGemma ±0.3 旧误报已拒绝。 |
| 是否所有 leaderboard 条目都是 high/medium confidence | PASS | leaderboard 仅由 include_in_leaderboard=yes 生成。 |
| 是否所有 leaderboard 条目都是 pure_hallucination | PASS | 未混入 proxy benchmark。 |
| 是否 OpenAI / Anthropic 的 POPE / CHAIR / AMBER / HallusionBench / MMHal 全部为未披露 | PASS | 未公开这些视觉幻觉专项 benchmark 的官方实验表格；不否定内部评测。 |
| 是否 low confidence 条目没有进入最终排名 | PASS | InternVL-3 low confidence 条目未进入 leaderboard。 |
| 是否报告中没有“工业界未采纳”这类过强表述 | PASS | FaithScore 仅写为当前语料未发现正式披露。 |
| 是否报告中没有“OpenAI/Anthropic 没有 hallucination 评测”这种不严谨表述 | PASS | 报告采用未公开专项 benchmark 表格的谨慎表述。 |

## 总体结论

**final_quality_check_v3：全部 PASS**
