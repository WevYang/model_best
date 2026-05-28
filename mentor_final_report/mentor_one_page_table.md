# 官方公开的多模态幻觉 Benchmark 分数速览

说明：本表是官方公开披露速览，不是模型能力排名。不同benchmark的任务形式、指标方向和评测设置不同，不能直接相加；`↓`表示越低越好。

| 模型 | HallusionBench | MMHal | POPE | CHAIR/ObjHal | CRPE | 备注 |
| --- | --- | --- | --- | --- | --- | --- |
| InternVL3-78B | 59.1 | Score=3.85 | 90.3 | - | 79.2 | v3.2人工确认；zero-shot官方报告口径。 |
| InternVL2.5-78B | 57.4 | Score=3.89 | 90.8 | - | 78.8 | v3.2人工确认；zero-shot官方报告口径。 |
| MiniCPM-V 4.5 | 61.2 | Score=5.0；Hallrate↓=19.4 | - | CHAIRs↓=9.3；CHAIRi↓=5.2 | - | CHAIR和Hallrate为lower-is-better。 |
| MiniCPM-o 4.5 | 63.2 | Score=4.7；Hallrate↓=24.3 | - | - | - | 公开HallusionBench和MMHal-Bench。 |
| PaliGemma | - | - | 86.0 / 87.0 | - | - | VQAv2-transferred / fine-tuning setting，不与zero-shot MLLM直接横比。 |

## 闭源模型同类表格披露情况

| 系列 | POPE / CHAIR / HallusionBench / MMHal / CRPE 同类表格 | 备注 |
| --- | --- | --- |
| OpenAI GPT-4V / GPT-4o / GPT-5系列 | 当前项目未发现公开同类学术视觉幻觉benchmark表格 | 公开system-card级factuality、safety、internal hallucination/deception相关评估；不能把披露缺口误读为未做相关评估。 |
| Anthropic Claude系列 | 当前项目未发现公开同类学术视觉幻觉benchmark表格 | 公开safety、factuality和内部风险评估；不能把披露缺口误读为未做相关评估。 |
| Google Gemini系列 | 当前mentor表不纳入可横比pure hallucination分数 | 公开安全、事实性和广泛能力评估；PaliGemma作为单独open model/fine-tuning口径列出。 |
