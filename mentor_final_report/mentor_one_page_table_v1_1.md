# 多模态大模型幻觉评测 Benchmark 官方分数速览

本表只收录当前已人工确认或明确标注口径的官方公开分数；空白不代表模型没有相关能力，只代表本次未发现可直接引用的同类官方分数表。

说明：本表是官方公开披露速览，leaderboard 不是模型能力排名。不同 benchmark 的任务形式、指标方向和评测设置不同，不能直接相加；`↓` 表示越低越好。

| 模型 | HallusionBench | MMHal | POPE | CHAIR/ObjHal | CRPE | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| InternVL3-78B | 59.1 | Score=3.85 | 90.3 | - | 79.2 | v3.2 人工确认；zero-shot 官方报告口径。 |
| InternVL2.5-78B | 57.4 | Score=3.89 | 90.8 | - | 78.8 | v3.2 人工确认；zero-shot 官方报告口径。 |
| MiniCPM-V 4.5 | 61.2 | Score=5.0；Hallrate↓=19.4 | - | CHAIRs↓=9.3；CHAIRi↓=5.2 | - | CHAIR 和 Hallrate 为 lower-is-better。 |
| MiniCPM-o 4.5 | 63.2 | Score=4.7；Hallrate↓=24.3 | - | - | - | 公开 HallusionBench 和 MMHal-Bench。 |
| PaliGemma | - | - | 86.0 / 87.0 | - | - | VQAv2-transferred / fine-tuning setting，不与 zero-shot MLLM 直接横比。 |

## 闭源模型同类表格披露情况

| 系列 | POPE / CHAIR / HallusionBench / MMHal / CRPE 同类表格 | 备注 |
| --- | --- | --- |
| OpenAI GPT-4V / GPT-4o / GPT-5 系列 | 当前项目未发现公开同类学术视觉幻觉 benchmark 表格 | 公开 system-card 级 factuality、safety、internal hallucination/deception 相关评估；不能把披露缺口误读为未做相关评估。 |
| Anthropic Claude 系列 | 当前项目未发现公开同类学术视觉幻觉 benchmark 表格 | 公开 safety、factuality 和内部风险评估；不能把披露缺口误读为未做相关评估。 |
| Google Gemini 系列 | 当前项目未发现公开同类学术视觉幻觉 benchmark 表格 | Gemini 闭源系列公开了 factuality、grounding、安全与广泛多模态能力评估；当前表未纳入可横比 POPE/CHAIR/HallusionBench/MMHal/CRPE 分数。PaliGemma 作为 Google 开放模型单独列出，其 POPE 属 transfer/fine-tuning 口径。 |
