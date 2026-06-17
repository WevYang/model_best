# 多模态大模型幻觉评测 Benchmark 调研最终版

## 1. 一句话结论

- 常用 direct benchmark 主要是 POPE、CHAIR/ObjHalBench、HallusionBench、MMHal-Bench、CRPE。
- Qwen、InternVL、MiniCPM、VILA、CogVLM、Bunny、DeepSeek-VL、Phi-4 等都有部分官方 direct benchmark 分数；Gemma 3 公开的是 factuality / grounding 类分数。
- OpenAI / Anthropic / Gemini 闭源系列没有公开同类可横比学术视觉幻觉表格，但公开了 system-card 级 factuality、safety 和内部 eval。
- Proxy benchmark 单独看，不能直接当作 hallucination rate。

## 2. Benchmark 速览

| Benchmark | 测什么 | 类型 | 指标 | 代表使用模型 |
| --- | --- | --- | --- | --- |
| POPE | 对象存在性幻觉 | pure | accuracy / F1 / precision / recall | InternVL3、InternVL2.5、PaliGemma、VILA、CogVLM、Bunny、DeepSeek-VL、Phi-4 |
| CHAIR / ObjHalBench | caption 里是否生成不存在的对象 | pure | CHAIRs↓ / CHAIRi↓ | MiniCPM-V 4.5 |
| HallusionBench / HallBench | 视觉错觉、视觉推理和语言先验导致的错误 | pure | accuracy | InternVL3、InternVL2.5、MiniCPM-V/o、Qwen2.5-VL、Qwen3-VL、GLM-4V-9B |
| MMHal-Bench | 开放式多模态回答中的幻觉程度 | pure | score / Hallrate↓ | InternVL3、InternVL2.5、MiniCPM-V/o |
| CRPE | 关系与组合关系错误 | pure | accuracy | InternVL3、InternVL2.5、Qwen2.5-VL、Qwen2.5-Omni、LLaVA-OneVision-2 |
| AMBER | 对象/属性/关系等多维幻觉 | pure | accuracy / F1 / mixed | 研究与第三方常见 |
| FaithScore | 生成内容与图像证据的一致性 | pure | faithfulness score / F1 | 研究与第三方常见 |
| FACTS-Grounding | grounded factual generation | factuality_related | score / accuracy | Gemma 3 |
| SimpleVQA | 简单事实问答 | factuality_related | accuracy | Qwen3-VL、Qwen3.5-Omni |
| Proxy bundle | OCR / chart / video / document / general reasoning | proxy | accuracy / score | CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、TextVQA、MMMU、MME、MathVista、AI2D、RefCOCO |

## 3. 代表模型主表

| 模型/系列代表 | HallusionBench | MMHal | POPE | CHAIR/ObjHal | CRPE | Factuality-related | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3-VL-235B-A22B | 66.7 / 63.2 | - | - | - | - | SimpleVQA 61.3 / 63.0 | thinking / instruct；官方表中为 visual benchmark 主表。 |
| Qwen2.5-VL-72B | 55.2 (HallBench_avg) | - | - | - | 79.2 | - | HallBench_avg + CRPE_relation。 |
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
| OpenAI / Anthropic / Gemini 闭源 | - | - | - | - | - | system-card factuality / safety / internal eval | 当前未发现同类可横比 direct 表格。 |

## 4. 全量分数附表说明

完整尺寸表见 Excel，不在正文堆所有模型尺寸。Excel 的 `Full Recall Scores` sheet 已合并 recall pass 新增确认分数与 v3.2 原本确认分数。

## 5. 结论和建议

- 建议最小内部横评组合：POPE + HallusionBench + MMHal-Bench。
- 关系幻觉加 CRPE。
- OCR / document 场景加 OCRBench / DocVQA / ChartQA，但要标注 proxy。

## 附录：数据质量说明

本版只做信息组织与汇报层优化：所有分数沿用 recall pass 已确认结果，未重跑全量抽取；对模型尺寸、thinking/instruct、transfer/fine-tuning 和 proxy 场景保持原有 caution。
