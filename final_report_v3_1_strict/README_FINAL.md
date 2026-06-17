# 多模态大模型幻觉评测调研交付说明 v3.1

## 1. 这是哪个版本

这是 `v3.1 strict` 交付版，基于 `strict audit` 和 `v3.1 terminology fix` 生成。  
它不再使用旧版 v2 / v3 中已经被严格审计全部拒绝的错误 valid 结果。

## 2. 推荐阅读顺序

1. `executive_summary_cn_v3_1.md`  
   一页式摘要，适合先快速看结论、范围和口径。
2. `strict_leaderboard_final_v3_1.csv`  
   披露覆盖排行榜，只看 verified coverage，不是能力排名。
3. `full_research_report_cn_v3_1.md`  
   完整中文技术报告，适合内部复核和引用。
4. `strict_verified_results_flat_v3_1.xlsx`  
   扁平化证据表，适合逐条核查字段、置信度和比较口径。
5. `manual_check_required_v3_1.md`  
   人工核查清单，优先看 Priority A。
6. `final_quality_check_v3_1.md`  
   最终质量核查结果，确认哪些口径已经修正。

## 3. 哪些文件可以直接对外引用

- `executive_summary_cn_v3_1.md`：可直接作为摘要引用。
- `full_research_report_cn_v3_1.md`：可作为内部技术报告引用。
- `strict_leaderboard_final_v3_1.csv`：可用于披露覆盖排行榜，但不是模型质量排名。
- `corrected_visualizations_v3_1/*.png` 或 `*.svg`：可用于 PPT，但必须保留图注中的 confidence / caution 信息。

## 4. 哪些旧文件不要再引用

不要再引用以下旧文件或旧口径：

- `final_report/full_research_report_cn.md`
- `final_report/pure_hallucination_leaderboard.csv`
- `analysis_results/audit_evidence_for_all_2s.xlsx` 中的旧 valid 口径
- 任何旧版 25 条 `valid_official_result` 表

原因很简单：旧的 25 条 valid 已经在 strict audit 中被全部拒绝，不能再当作事实来源。

## 5. 当前可信结论

- 只有少数模型公开了可验证的 pure hallucination benchmark 结果。
- `MiniCPM-V` / `MiniCPM-o` 属于 high confidence。
- `InternVL-2.5` / `PaliGemma` 属于 medium confidence，并且需要 caution。
- OpenAI / Anthropic 未公开 POPE / CHAIR / HallusionBench / MMHal 等视觉幻觉专项 benchmark 表格，但有 factuality / safety / internal eval。
- proxy benchmark 不等于 hallucination rate。

## 6. 使用注意事项

- `leaderboard` 是 disclosure coverage，不是 model quality ranking。
- medium confidence 结果必须保留 caution。
- `PaliGemma` 的 POPE 是 transfer / fine-tuning 口径。
- `InternVL-2.5` 仍需要人工确认表格列顺序。
- `FACTS-Grounding` / `SimpleVQA` 是 factuality-related，不属于 pure multimodal hallucination。

