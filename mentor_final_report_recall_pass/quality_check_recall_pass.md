# Quality Check: Recall Pass

| check_item | status | notes |
| --- | --- | --- |
| 是否复查了 Qwen2-VL | PASS | 本地未找到独立报告；在 Qwen2.5-VL 官方 Table 3 中确认 Qwen2-VL-72B HallBench_avg=58.1，标为 medium。 |
| 是否复查了 Qwen2.5-VL | PASS | 确认 HallBench_avg 和 CRPE_relation，已看 PDF p.11 表格截图。 |
| 是否复查了 Qwen3-VL | PASS | 确认 Table 2/3/4 中 HallusionBench 和 SimpleVQA，已看 PDF p.15/16/18 表格截图。 |
| 是否每个新增分数都有完整表格行或明确表格证据 | PASS | 每条新增结果均记录 source_file、page_or_section、table_title、evidence_row。 |
| 是否没有把 proxy benchmark 混入 pure 表 | PASS | OCRBench/CharXiv/Video-MME/DocVQA/ChartQA/MMMU 等只在 notes/proxy 说明中出现。 |
| 是否没有把引用编号/章节号/版本号当分数 | PASS | 新增结果均来自可见表格行；Qwen2-VL 独立报告缺失项没有强行补入。 |
| 是否区分 high/medium/low | PASS | Qwen2-VL-72B 为 medium；低置信/未确认项放入 findings 的继续确认/拒绝清单。 |
| 是否更新了 mentor_one_page_table_v1_2.md | PASS | 已生成 v1.2，包含 recall pass 新增分数。 |
| 是否更新了 mentor_summary_cn_v1_2.md | PASS | 已更新一句话结论、benchmark 表与模型分数总表。 |
| 是否保留 PaliGemma transfer/fine-tuning caution | PASS | PaliGemma 备注仍标注 VQAv2-transferred / fine-tuning setting，不与 zero-shot 横比。 |
| 是否仍然声明 leaderboard 不是模型能力排名 | PASS | v1.2 一页表和 summary 均保留该声明。 |
