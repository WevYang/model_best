# 代表模型主表

本表适合直接复制到微信 / 飞书 / 邮件。它不是模型能力排名，只是官方公开分数速览。

| 模型/系列代表 | HallusionBench | MMHal | POPE | CHAIR/ObjHal | CRPE | Factuality-related | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3-VL-235B-A22B | 66.7 / 63.2 | - | - | - | - | SimpleVQA 61.3 / 63.0 | 两个数均为 thinking / instruct；SimpleVQA 属 factuality-related，不计入 pure hallucination。 |
| Qwen2.5-VL-72B | 55.2 (HallBench_avg) | - | - | - | 79.2 | - | HallBench_avg + CRPE_relation；无 POPE/MMHal 官方确认分数。 |
| InternVL3-78B | 59.1 | 3.85 | 90.3 | - | 79.2 | - | v3.2 人工确认；zero-shot 官方报告口径。 |
| InternVL2.5-78B | 57.4 | 3.89 | 90.8 | - | 78.8 | - | v3.2 人工确认；zero-shot 官方报告口径。 |
| MiniCPM-V 4.5 | 61.2 | 5.0 / Hallrate↓ 19.4 | - | CHAIRs↓ 9.3 / CHAIRi↓ 5.2 | - | - | ObjHalBench/CHAIR 口径；lower-is-better。 |
| MiniCPM-o 4.5 | 63.2 | 4.7 / Hallrate↓ 24.3 | - | - | - | - | 公开 HallusionBench 和 MMHal-Bench。 |
| DeepSeek-VL-7B | - | - | 88.1 | - | - | - | POPE 官方表格。 |
| CogVLM-Chat | - | - | 87.9 | - | - | - | POPE 官方表格。 |
| Bunny-8B | - | - | 87.2 | - | - | - | POPE averaged F1-score。 |
| VILA-7B | - | - | 85.5 | - | - | - | POPE 官方表格。 |
| Phi-4-Multimodal-5.6B | - | - | 85.6 | - | - | - | POPE 官方表格。 |
| LLaVA-OneVision-2-8B | - | - | - | - | 77.3 | - | CRPE 官方表格。 |
| GLM-4V-9B | 46.6 | - | - | - | - | - | 本地 GLM 4.1/4.5/4.6 HTML 实际为同一 GLM-4V-9B model card。 |
| PaliGemma | - | - | 86.0 / 87.0 | - | - | - | VQAv2-transferred / fine-tuning setting，不与 zero-shot MLLM 直接横比。 |
| Gemma 3 27B | - | - | - | - | - | FACTS-Grounding 74.9 | factuality/grounding-related only。 |
| OpenAI GPT-4V / GPT-4o / GPT-5 系列 | - | - | - | - | - | system-card factuality / safety / internal eval | 当前未发现可横比 direct 表格。 |
| Anthropic Claude 系列 | - | - | - | - | - | system-card safety / factuality / internal risk eval | 当前未发现可横比 direct 表格。 |
| Google Gemini 闭源系列 | - | - | - | - | - | factuality / grounding / safety / multimodal capability eval | 当前未发现可横比 direct 表格；PaliGemma / Gemma 3 另列，不与 Gemini 闭源混比。 |

附注：Qwen2-VL-72B HallBench_avg=58.1 仅在 Qwen2.5-VL 官方对比表中确认，medium confidence，未放入主表。
