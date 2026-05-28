# Quality Check Report — final_report/

**检查日期：** 2026-05-28

## 1. Benchmark 定义完整性

| 检查项 | 结果 |
|--------|------|
| 矩阵中的 benchmark 总数 | 28 |
| benchmark_column_dictionary 中定义的总数 | 28 |
| 矩阵中有但字典未定义 | ✅ 无 |
| 字典中有但矩阵未包含 | ✅ 无 |

## 2. Evidence Snippet 完整性

| 检查项 | 结果 |
|--------|------|
| valid_official_result 总数 | 25 |
| 缺少 evidence_snippet 的条目 | 0 ✅ |

## 3. Pure / Proxy 分离

| 检查项 | 结果 |
|--------|------|
| Pure hallucination benchmarks | ✅ CHAIR, POPE, HallusionBench, MMHal-Bench, AMBER, FaithScore, FACTS-Grounding, SimpleVQA |
| Proxy benchmarks | ✅ 20 个已定义 |
| 报告中是否混用两类 | ✅ 报告中明确区分，不混用 |

## 4. 过度表述检查

| 表述 | 状态 |
|------|------|
| "工业界未采纳 FaithScore" | ✅ 已修正为"当前语料中未发现官方披露" |
| "没有 hallucination 评测" | ✅ 已修正为"很少/未披露视觉幻觉专项 benchmark" |
| "OpenAI/Anthropic 不做幻觉评测" | ✅ 已修正为"未在官方报告中披露 POPE/CHAIR 等专项" |
| CharXiv 写成 hallucination benchmark | ✅ 已在报告中明确标注为 chart/document proxy |
| OCRBench 写成幻觉指标 | ✅ 已在报告中明确标注为 OCR proxy |

## 5. 图表检查

| 图表 | PNG | SVG | 有图例 | 状态 |
|------|-----|-----|--------|------|
| pure_hallucination_coverage_heatmap | ✅ | ✅ | ✅ | ✅ |
| proxy_benchmark_coverage_heatmap | ✅ | ✅ | ✅ | ✅ |
| audit_reclassification_bar | ✅ | ✅ | ✅ | ✅ |
| pure_vs_proxy_stacked_bar | ✅ | ✅ | ✅ | ✅ |
| benchmark_adoption_bar | ✅ | ✅ | ✅ | ✅ |

## 6. 输出文件检查

| 文件 | 存在 | 大小 |
|------|------|------|
| model_best/final_report/executive_summary_cn.md | ✅ | 6 KB |
| model_best/final_report/full_research_report_cn.md | ✅ | 17 KB |
| model_best/final_report/model_family_summary.xlsx | ✅ | 27 KB |
| model_best/final_report/pure_hallucination_leaderboard.csv | ✅ | 9 KB |
| model_best/final_report/proxy_benchmark_coverage.csv | ✅ | 8 KB |
| model_best/final_report/final_readme.md | ✅ | 4 KB |
| model_best/final_report/corrected_visualizations/pure_hallucination_coverage_heatmap.png | ✅ | 114 KB |
| model_best/final_report/corrected_visualizations/proxy_benchmark_coverage_heatmap.png | ✅ | 155 KB |
| model_best/final_report/corrected_visualizations/audit_reclassification_bar.png | ✅ | 53 KB |
| model_best/final_report/corrected_visualizations/pure_vs_proxy_stacked_bar.png | ✅ | 80 KB |
| model_best/final_report/corrected_visualizations/benchmark_adoption_bar.png | ✅ | 108 KB |

## 7. Top N 排名口径标注

| 排行榜 | 口径 | 是否标注 |
|--------|------|----------|
| pure_hallucination_leaderboard.csv | Pure only（POPE/CHAIR/HallusionBench等） | ✅ |
| proxy_benchmark_coverage.csv | Proxy only | ✅ |
| model_family_summary.xlsx Sheet2 | Pure only | ✅ |
| model_family_summary.xlsx Sheet3 | Proxy only | ✅ |

## 8. 风险提示（仍需人工确认）

1. **Claude-Sonnet-4.6 / Claude-Opus-4.6 POPE = 2**：来源为 HTML 系统卡片页面，非正式 PDF。自动提取结果需人工验证该 HTML 页面中是否确实含有 POPE 实验表格，或为误报。
2. **Qwen3.6 / Qwen3.7**：当前无官方文档，所有值为 0，无法确认是否已发布。
3. **GPT-5.2**：官方来源为 openai.com/chatgpt 主页 HTML，内容可能不含完整实验结果，所有 value=2 可能为误报。
4. **Video-MME 覆盖（13 个模型）**：部分数值来自无字幕/有字幕子集，不同论文口径不一致，需人工确认。
5. **CharXiv 分数分布**：部分论文报告 reasoning/descriptive 子集分数，整体得分范围差异大，跨模型比较需注意口径。

## 9. 总结

| 项目 | 状态 |
|------|------|
| 矩阵列全部在字典中有定义 | ✅ |
| 所有 valid 结果有 evidence snippet | ✅ |
| Pure/Proxy 完全分离 | ✅ |
| 过度表述已修正 | ✅ |
| 所有图表成功生成（PNG+SVG） | ✅ |
| 所有 Excel 可正常写入 | ✅ |
| 输出路径在 final_report/ 下 | ✅ |
