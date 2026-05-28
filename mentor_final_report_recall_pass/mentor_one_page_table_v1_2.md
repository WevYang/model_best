# 多模态大模型幻觉评测 Benchmark 官方分数速览 v1.2（Recall Pass）

本表只收录当前已人工确认或明确标注口径的官方公开分数；空白不代表模型没有相关能力，只代表本次未发现可直接引用的同类官方分数表。

说明：本表是官方公开披露速览，leaderboard 不是模型能力排名。不同 benchmark 的任务形式、指标方向和评测设置不同，不能直接相加；`↓` 表示越低越好。SimpleVQA / FACTS-Grounding 属 factuality-related，不与 pure hallucination 分数混为一类。

| 模型 | 机构 | 报告版本 | HallusionBench / HallBench | MMHal | POPE | CHAIR/ObjHal | CRPE | Factuality-related | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| InternVL3-78B | Shanghai AI Lab | v3.2人工确认 | 59.1 | Score=3.85 | 90.3 | - | 79.2 | - | v3.2人工确认；zero-shot官方报告口径。 |
| InternVL2.5-78B | Shanghai AI Lab | v3.2人工确认 | 57.4 | Score=3.89 | 90.8 | - | 78.8 | - | v3.2人工确认；zero-shot官方报告口径。 |
| MiniCPM-V 4.5 | Tsinghua / ModelBest | MiniCPM-V 4.5技术报告 | 61.2 | Score=5.0；Hallrate↓=19.4 | - | CHAIRs↓=9.3；CHAIRi↓=5.2 | - | - | CHAIR和Hallrate为lower-is-better。 |
| MiniCPM-o 4.5 | Tsinghua / ModelBest | MiniCPM-o 4.5技术报告 | 63.2 | Score=4.7；Hallrate↓=24.3 | - | - | - | - | 公开HallusionBench和MMHal-Bench。 |
| PaliGemma | Google | PaliGemma技术报告 | - | - | 86.0 / 87.0 | - | - | - | VQAv2-transferred / fine-tuning setting，不与zero-shot MLLM直接横比。 |
| Qwen3-VL-235B-A22B | Alibaba / Qwen | Qwen3-VL技术报告 | 66.7 / 63.2 | - | - | - | - | SimpleVQA 61.3 / 63.0 | thinking / instruct；SimpleVQA为factuality-related。 |
| Qwen3-VL-32B | Alibaba / Qwen | Qwen3-VL技术报告 | 67.4 / 63.8 | - | - | - | - | SimpleVQA 55.4 / 56.9 | thinking / instruct。 |
| Qwen3-VL-30B-A3B | Alibaba / Qwen | Qwen3-VL技术报告 | 66.0 / 61.5 | - | - | - | - | SimpleVQA 54.3 / 52.7 | thinking / instruct。 |
| Qwen3-VL-8B | Alibaba / Qwen | Qwen3-VL技术报告 | 65.4 / 61.1 | - | - | - | - | SimpleVQA 49.6 / 50.2 | thinking / instruct。 |
| Qwen3-VL-4B | Alibaba / Qwen | Qwen3-VL技术报告 | 64.1 / 57.6 | - | - | - | - | SimpleVQA 48.8 / 48.0 | thinking / instruct。 |
| Qwen3-VL-2B | Alibaba / Qwen | Qwen3-VL技术报告 | 54.9 / 51.4 | - | - | - | - | SimpleVQA 43.6 / 40.7 | thinking / instruct。 |
| Qwen2.5-VL-72B | Alibaba / Qwen | Qwen2.5-VL技术报告 | 55.2 | - | - | - | 79.2 | - | HallBench_avg + CRPE_relation。 |
| Qwen2.5-VL-7B | Alibaba / Qwen | Qwen2.5-VL技术报告 | 52.9 | - | - | - | 76.4 | - | HallBench_avg + CRPE_relation。 |
| Qwen2.5-VL-3B | Alibaba / Qwen | Qwen2.5-VL技术报告 | 46.3 | - | - | - | 73.6 | - | HallBench_avg + CRPE_relation。 |
| Qwen2-VL-72B | Alibaba / Qwen | Qwen2.5-VL官方对比表 | 58.1 | - | - | - | - | - | medium：本地缺少Qwen2-VL独立报告，分数来自Qwen2.5-VL官方Table 3。 |
| Qwen2.5-Omni-7B | Alibaba / Qwen | Qwen2.5-Omni技术报告 | - | - | - | - | 76.5 | - | CRPE_relation。 |
| GLM-4V-9B | Zhipu AI / Z.ai | GLM官方模型卡 | 46.6 | - | - | - | - | - | 本地GLM 4.1/4.5/4.6 HTML内容实际为GLM-4V-9B模型卡。 |
| VILA-7B | NVIDIA / VILA authors | VILA技术报告 | - | - | 85.5 | - | - | - | POPE官方表格。 |
| VILA-13B | NVIDIA / VILA authors | VILA技术报告 | - | - | 84.2 | - | - | - | POPE官方表格。 |
| CogVLM-Chat | Tsinghua / Zhipu AI | CogVLM技术报告 | - | - | 87.9 | - | - | - | POPE官方表格。 |
| Bunny-8B | Bunny authors | Bunny技术报告 | - | - | 87.2 | - | - | - | POPE averaged F1-score。 |
| Bunny-4B | Bunny authors | Bunny技术报告 | - | - | 87.2 | - | - | - | POPE averaged F1-score。 |
| DeepSeek-VL-7B | DeepSeek | DeepSeek-VL技术报告 | - | - | 88.1 | - | - | - | POPE官方表格。 |
| DeepSeek-VL-1.3B | DeepSeek | DeepSeek-VL技术报告 | - | - | 87.6 | - | - | - | POPE官方表格。 |
| LLaVA-OneVision-2-8B | LLaVA team | LLaVA-OneVision-2技术报告 | - | - | - | - | 77.3 | - | CRPE官方表格。 |
| Phi-4-Multimodal-5.6B | Microsoft | Phi-4-Multimodal技术报告 | - | - | 85.6 | - | - | - | POPE官方表格。 |
| Gemma 3 27B | Google | Gemma 3技术报告 | - | - | - | - | - | FACTS-Grounding 74.9 | factuality/grounding-related，不混入pure分数。 |
| Gemma 3 12B | Google | Gemma 3技术报告 | - | - | - | - | - | FACTS-Grounding 75.8 | factuality/grounding-related。 |
| Gemma 3 4B | Google | Gemma 3技术报告 | - | - | - | - | - | FACTS-Grounding 70.1 | factuality/grounding-related。 |
| Gemma 3 1B | Google | Gemma 3技术报告 | - | - | - | - | - | FACTS-Grounding 36.4 | factuality/grounding-related。 |
| Qwen3.5-Plus-Instruct | Alibaba / Qwen | Qwen3.5-Omni技术报告 | - | - | - | - | - | SimpleVQA 66.1 | factuality-related。 |
| Qwen3.5-Omni-Plus | Alibaba / Qwen | Qwen3.5-Omni技术报告 | - | - | - | - | - | SimpleVQA 65.3 | factuality-related。 |
| Qwen3.5-Omni-Flash | Alibaba / Qwen | Qwen3.5-Omni技术报告 | - | - | - | - | - | SimpleVQA 54.4 | factuality-related。 |

## 闭源模型同类表格披露情况

| 系列 | POPE / CHAIR / HallusionBench / MMHal / CRPE 同类表格 | 备注 |
| --- | --- | --- |
| OpenAI GPT-4V / GPT-4o / GPT-5 系列 | 当前项目未发现公开同类学术视觉幻觉 benchmark 表格 | 公开 system-card 级 factuality、safety、internal hallucination/deception 相关评估；不能把披露缺口误读为未做相关评估。 |
| Anthropic Claude 系列 | 当前项目未发现公开同类学术视觉幻觉 benchmark 表格 | 公开 safety、factuality 和内部风险评估；不能把披露缺口误读为未做相关评估。 |
| Google Gemini 系列 | 当前表未纳入可横比 POPE/CHAIR/HallusionBench/MMHal/CRPE 分数 | Gemini 闭源系列公开了 factuality、grounding、安全与广泛多模态能力评估；PaliGemma 作为 Google 开放模型单独列出，其 POPE 属 transfer/fine-tuning 口径。 |
