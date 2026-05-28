# Quality Check - Factuality / Proxy Full Recall

| check_item | status | notes |
| --- | --- | --- |
| 是否不再只保留 representative proxy scores | PASS | Excel Proxy Scores Full 包含 732 条记录。 |
| 是否覆盖 Qwen / InternVL / MiniCPM / DeepSeek / LLaVA / Gemma / OpenAI / Anthropic / Gemini | PASS | Qwen/Gemini/Gemma/OpenAI 有 confirmed full rows；其它模型族进入 direct表或 Coverage Gaps，不静默忽略。 |
| 是否把 factuality_related 和 direct hallucination 分开 | PASS | factuality sheet 独立；direct 只在扩展表 A 区引用。 |
| 是否把 proxy 和 direct hallucination 分开 | PASS | proxy sheet 独立，所有 proxy notes 均说明不是 hallucination rate。 |
| 是否没有把 OCRBench / CharXiv / Video-MME 写成 hallucination rate | PASS | 这些均标为 proxy_type。 |
| 是否标注 source_file/source_url/page/table/evidence | PASS | confirmed rows 均包含 source_file/page/table/evidence 字段；URL 视本地材料可用性保留。 |
| 是否保留 Qwen3-VL thinking/instruct | PASS | Qwen3-VL score setting 使用 thinking / instruct。 |
| 是否保留 PaliGemma transfer/fine-tuning caution | PASS | Direct 表来自 v1.4，保留 PaliGemma caution。 |
| 是否闭源模型使用谨慎口径 | PASS | Closed Source System Cards sheet 单独记录，不与开源 benchmark 横比。 |
| 是否 Excel 至少 7 个 sheet | PASS | 实际生成 8 个 sheet，含 Unverified Proxy Candidates。 |
| 是否生成 coverage_gap_report.md | PASS | 已生成。 |
| 是否 mentor_extended_table_full.md 可直接粘贴到飞书 | PASS | 按 A/B/C/D 分区。 |