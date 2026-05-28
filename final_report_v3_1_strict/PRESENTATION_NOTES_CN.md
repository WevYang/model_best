# PPT 讲稿：多模态大模型幻觉评测调研 v3.1

## Slide 1: 研究问题

- 这次只看官方公开材料里，哪些模型真的披露了幻觉相关 benchmark。
- 核心区分不是“有没有跑 benchmark”，而是“是不是 pure hallucination benchmark”。
- 需要把 pure、factuality-related、proxy capability 三层分开。
- 建议图表：`corrected_visualizations_v3_1/benchmark_category_diagram_v3_1.png`
- 讲解备注：先定义口径，再讲结果，避免把 proxy 误讲成幻觉率。

## Slide 2: 为什么自动抽取会错

- 旧版自动抽取把引用编号、章节号、页码、版本号、标准差都当成了分数。
- PDF 文本流还会丢列对齐，造成相邻 benchmark 串行。
- 所以 25 条旧 valid 全部被 strict audit 拒绝。
- 建议图表：`corrected_visualizations_v3_1/audit_pipeline_flow_v3_1.png`
- 讲解备注：强调这是证据问题，不是模型能力问题。

## Slide 3: Strict Audit 后发生了什么

- 旧 25 条 valid 全部作废。
- 只保留 high / medium confidence 的 verified results。
- low confidence 只进入人工确认清单，不进排行榜。
- 建议图表：`corrected_visualizations_v3_1/audit_pipeline_flow_v3_1.png`
- 讲解备注：说明 strict audit 是重新核对证据，不是重新扩张结果。

## Slide 4: Benchmark 三层分类

- Pure multimodal hallucination：POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER、FaithScore。
- Factuality / grounding related：FACTS-Grounding、SimpleVQA。
- Proxy capability：CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、MMMU 等。
- 建议图表：`corrected_visualizations_v3_1/benchmark_category_diagram_v3_1.png`
- 讲解备注：这里是整套报告的口径核心。

## Slide 5: Verified Results

- `MiniCPM-V` / `MiniCPM-o` 是 high confidence。
- `InternVL-2.5` 和 `PaliGemma` 是 medium confidence，需要 caution。
- `InternVL-3` 仍是 low confidence，只能人工确认。
- 建议图表：`corrected_visualizations_v3_1/verified_pure_coverage_heatmap_v3_1.png`
- 讲解备注：高、中、低必须视觉上分开，不能画成一样。

## Slide 6: Leaderboard 只是披露覆盖，不是能力排名

- 排名依据是 verified disclosure coverage count。
- 不是幻觉能力高低排名，也不是 benchmark 分数高低排名。
- medium confidence 必须带风险说明。
- 建议图表：`corrected_visualizations_v3_1/strict_leaderboard_bar_v3_1.png`
- 讲解备注：图注里必须保留 disclosure coverage not model quality 的意思。

## Slide 7: 闭源模型如何理解

- OpenAI / Anthropic 在当前语料中未公开 POPE / CHAIR / HallusionBench / MMHal 等专项表格。
- 但它们有 factuality、安全性、internal eval。
- 所以不能说“没有幻觉评测”。
- 建议图表：`corrected_visualizations_v3_1/benchmark_category_diagram_v3_1.png`
- 讲解备注：用“未公开专项表格”这个更严谨的说法。

## Slide 8: Proxy Benchmark 的正确用法

- Proxy benchmark 只能反映相关能力，不等价于 hallucination rate。
- CharXiv、OCRBench、DocVQA、ChartQA、MMMU 都应该单独看。
- 不能把 proxy 直接塞进 pure leaderboard。
- 建议图表：`corrected_visualizations_v3_1/benchmark_category_diagram_v3_1.png`
- 讲解备注：这页重点是方法学，不是分数。

## Slide 9: 仍需人工确认的条目

- Priority A：InternVL-2.5 列顺序、InternVL-3 第 11 页对齐。
- Priority B：VILA、CogVLM、Bunny、Qwen3-VL。
- 当前不影响结果的是 Priority B 的 rejected 条目。
- 建议图表：`corrected_visualizations_v3_1/audit_pipeline_flow_v3_1.png`
- 讲解备注：只说需要核查，不要说它们已经成立。

## Slide 10: 推荐后续工作

- 先补 Priority A，再考虑是否有新的 verified coverage。
- future model card 也要走 strict audit，不回到旧自动抽取逻辑。
- proxy benchmark 单独报告，不和 pure benchmark 混排。
- 建议图表：`corrected_visualizations_v3_1/audit_pipeline_flow_v3_1.png`
- 讲解备注：收尾要强调“保守、可审计、可复核”。
