# final_report/ — 目录说明

**生成日期：** 2026-05-28
**基于：** analysis_results/（二次审计完成后的输出）

---

## 文件清单与用途

### 📄 核心报告（推荐首先阅读）

| 文件 | 用途 | 推荐读者 |
|------|------|---------|
| `executive_summary_cn.md` | **一页纸中文摘要**，适合快速了解结论 | 研究负责人、项目经理 |
| `full_research_report_cn.md` | **完整中文研究报告**，含 benchmark 分类、模型分析、发现和建议 | 研究员、论文调研 |
| `quality_check.md` | **质量自检报告**，含风险提示和人工确认项 | 技术审查者 |

### 📊 数据文件（推荐用于后续分析）

| 文件 | 用途 | 格式 |
|------|------|------|
| `model_family_summary.xlsx` | 按模型族的覆盖统计（5 sheets，含颜色标注） | Excel |
| `pure_hallucination_leaderboard.csv` | **只含 pure hallucination 口径的排名**，可直接导入 | CSV |
| `proxy_benchmark_coverage.csv` | 代理 benchmark 覆盖统计 | CSV |

### 🖼️ 可视化（corrected_visualizations/）

| 文件 | 适合放入 PPT | 说明 |
|------|------------|------|
| `pure_hallucination_coverage_heatmap.png` | ✅ **强烈推荐** | Top 30 模型 × 8 个 pure hal benchmark |
| `audit_reclassification_bar.png` | ✅ **强烈推荐** | 382 个 value=2 的审计重分类结果 |
| `pure_vs_proxy_stacked_bar.png` | ✅ 推荐 | 按模型族的 pure vs proxy 对比 |
| `benchmark_adoption_bar.png` | ✅ 推荐 | 两个子图：pure 和 proxy benchmark 采用率 |
| `proxy_benchmark_coverage_heatmap.png` | ⚠️ 参考用 | 代理 benchmark 覆盖热力图（较宽）|
| `pure_hallucination_coverage_heatmap_full83.png` | ⚠️ 参考用 | 全部 83 个模型（图较高）|

---

## 推荐阅读顺序

1. `executive_summary_cn.md` — 5 分钟了解核心结论
2. `corrected_visualizations/audit_reclassification_bar.png` — 直观理解审计结果
3. `corrected_visualizations/pure_hallucination_coverage_heatmap.png` — 了解各模型披露情况
4. `model_family_summary.xlsx` → Sheet2（Pure Hallucination Coverage）— 细节查询
5. `full_research_report_cn.md` — 完整技术报告
6. `quality_check.md` — 确认风险提示

---

## 适合放进 PPT 的图表（Top 5）

1. `pure_hallucination_coverage_heatmap.png` — 展示幻觉评测披露现状
2. `audit_reclassification_bar.png` — 展示"误报率"和分析严谨性
3. `pure_vs_proxy_stacked_bar.png` — 展示模型族对比
4. `benchmark_adoption_bar.png`（左子图）— 展示 pure hal benchmark 覆盖率
5. `benchmark_adoption_bar.png`（右子图）— 展示 proxy benchmark 覆盖率

---

## 适合程序读取的文件

- `pure_hallucination_leaderboard.csv` — UTF-8，逗号分隔，有表头
- `proxy_benchmark_coverage.csv` — UTF-8，逗号分隔，有表头
- `../analysis_results/audit_validated_matrix.csv` — 修正后的完整矩阵
- `../analysis_results/audit_evidence_for_all_2s.xlsx` — 详细证据（4 sheets）

---

## 审计证据文件（不可修改）

- `../analysis_results/audit_evidence_for_all_2s.xlsx` — 382 条证据记录
- `../analysis_results/false_positive_report.csv` — 44 条重分类记录
- `../analysis_results/corrected_summary.md` — 二次审计摘要

---

## 注意事项

1. **CharXiv / OCRBench / Video-MME 是 proxy**，报告时需明确标注，勿写成"幻觉 benchmark"
2. **OpenAI / Anthropic 无 POPE/CHAIR 等专项结果**，请勿写成"这些公司不做幻觉评测"
3. **FaithScore 的结论**：仅限当前语料，不代表工业界整体
4. **Claude 的 POPE = 2** 来自 HTML 系统卡片，需人工确认（见 quality_check.md 风险提示 1）
5. 所有图表提供 PNG（高清）和 SVG（矢量，可缩放）两种格式
