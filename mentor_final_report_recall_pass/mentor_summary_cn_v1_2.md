# 多模态大模型幻觉评测 Benchmark 调研总结 v1.2（Recall Pass）

## 1. 一句话结论

- 本轮召回复查确认：此前只列 InternVL、MiniCPM、PaliGemma 过度保守，确实漏掉了 Qwen、VILA、CogVLM、Bunny、DeepSeek-VL、LLaVA-OneVision-2、Phi-4-Multimodal、GLM-4V-9B、Gemma 3 等官方表格中的 direct hallucination 或 factuality-related 分数。
- Qwen 系列是最大新增来源：Qwen2.5-VL 公开 HallBench_avg 与 CRPE，Qwen3-VL 公开 HallusionBench 与 SimpleVQA，Qwen2.5-Omni 公开 CRPE，Qwen3.5-Omni 公开 SimpleVQA。
- 公开披露覆盖度不是模型能力排名：不同 benchmark 的任务形式、指标方向和评测设置不同，不能把分数相加，也不能跨设置硬排高低。
- SimpleVQA 与 FACTS-Grounding 属 factuality/grounding related，不与 POPE、CHAIR、HallusionBench、MMHal-Bench、CRPE 等 pure hallucination benchmark 混为一类。
- CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、TextVQA、MMMU、MME、MathVista 等仍然只作为 proxy 能力背景，不能直接当作 hallucination rate。

## 2. 常用幻觉评测 Benchmark

| Benchmark | 主要测什么 | 幻觉类型 | 任务形式 | 指标 | 是否直接测 hallucination | 本次官方确认得分模型 | 常见研究/第三方使用场景 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| POPE | 判断模型是否把图像中不存在的物体说成存在 | 对象幻觉 | yes/no probing、二分类 VQA | accuracy / F1 / precision / recall | 是 | InternVL3、InternVL2.5、PaliGemma、VILA、CogVLM、Bunny、DeepSeek-VL、Phi-4-Multimodal | LLaVA 系、开源 MLLM 横评、对象幻觉评测 |
| CHAIR / ObjHalBench | 图像描述里是否生成不存在的对象 | 对象幻觉 | caption 或开放描述后与对象标注比对 | CHAIRs↓ / CHAIRi↓ | 是 | MiniCPM-V | captioning、open-ended MLLM 描述评测、对象幻觉分析 |
| HallusionBench / HallBench | 视觉错觉、视觉推理和语言先验导致的错误 | 视觉推理幻觉 | 多选/问答 | accuracy | 是 | InternVL3、InternVL2.5、MiniCPM-V、MiniCPM-o、Qwen2.5-VL、Qwen3-VL、GLM-4V-9B、Qwen2-VL-72B（medium） | 开源 MLLM 幻觉/错觉评测 |
| MMHal-Bench | open-ended 回答中的幻觉程度 | 回答级幻觉 | 开放式多模态问答 | score / Hallrate↓ | 是 | InternVL3、InternVL2.5、MiniCPM-V、MiniCPM-o | 开放式多模态回答幻觉评估 |
| CRPE | 关系和组合关系是否被错误描述 | 关系幻觉 | 关系/组合推理问答 | accuracy | 是 | InternVL3、InternVL2.5、Qwen2.5-VL、Qwen2.5-Omni、LLaVA-OneVision-2 | 关系幻觉/组合关系错误评测 |
| AMBER | 对象、属性、关系等多类型幻觉 | 综合多模态幻觉 | 判别式与生成式混合 | accuracy / F1 / hallucination metrics | 是 | 本次未确认官方模型分数 | 开源 MLLM 综合幻觉评测 |
| FaithScore | 生成内容与图像证据是否一致 | faithfulness / factual hallucination | 事实单元拆解与一致性判断 | faithfulness score / F1 等 | 是 | 本次未确认官方模型分数 | faithfulness / atomic fact consistency 研究 |
| FACTS-Grounding | 回答是否有证据支撑、是否 grounded | factuality / grounding | grounded QA 或事实判断 | score / accuracy | 相关但非 pure | Gemma 3 | system-card、factuality、grounding 相关评估 |
| SimpleVQA | 简单事实问答准确性 | factuality | 短问答/事实查询 | accuracy | 相关但非 pure | Qwen3-VL、Qwen3.5-Omni | factuality 相关评估 |
| CharXiv / OCRBench / Video-MME / DocVQA / ChartQA / TextVQA / MMMU 等 | 图表、OCR、视频、文档、通用推理能力 | proxy 能力 | QA、多选、推理 | accuracy / score 等 | 否 | 不混入 pure 表 | OCR、chart、video、document、通用推理能力背景评估 |

## 3. 模型官方公开分数总表

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

说明：这张表是“官方公开分数速览”，不是模型能力排行榜。不同 benchmark 之间不能直接相加，同一 benchmark 也要检查 zero-shot、fine-tuning、thinking/instruct、模型尺寸和指标方向。

## 4. 闭源模型披露情况

| 模型系列 | 是否公开 POPE / CHAIR / HallusionBench / MMHal / CRPE 等学术幻觉 benchmark | 是否公开 factuality / safety / internal hallucination eval | 备注 |
| --- | --- | --- | --- |
| OpenAI GPT-4V / GPT-4o / GPT-5 系列 | 当前项目未发现公开同类学术视觉幻觉 benchmark 表格 | 是，system card 级 factuality、safety、internal hallucination/deception 相关评估 | 不能把披露缺口误读为未做相关评估；只能说未公开这些学术 benchmark 的可横比表格。 |
| Google Gemini 系列 | 当前表未纳入可横比 POPE/CHAIR/HallusionBench/MMHal/CRPE 分数 | 是，公开 factuality、grounding、安全与广泛多模态能力评估 | Gemini 闭源系列与 PaliGemma/Gemma 3 不是同一比较口径；PaliGemma 的 POPE 属 transfer/fine-tuning 口径，Gemma 3 的 FACTS-Grounding 属 factuality-related。 |
| Anthropic Claude 系列 | 当前项目未发现公开同类学术视觉幻觉 benchmark 表格 | 是，system card 级 safety、factuality 和内部风险评估 | 不能把披露缺口误读为未做相关评估。 |

## 5. Proxy benchmark 单独说明

CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、TextVQA、MMMU、MME、MathVista、AI2D、RefCOCO 等应该单独看。它们能反映图表、OCR、文档、视频、通用推理和 grounding 能力，很多错误会诱发幻觉，但这些 benchmark 本身不是 hallucination rate。报告中可以把它们作为“风险解释变量”或“能力背景”，不要和 POPE、CHAIR、HallusionBench、MMHal-Bench、CRPE 等 direct hallucination benchmark 合并排名。

## 6. 后续建议

- 如果要做模型横评，建议至少跑 POPE + HallusionBench + MMHal-Bench：一个覆盖对象存在性，一个覆盖视觉推理幻觉，一个覆盖开放式回答幻觉。
- 如果关注关系幻觉，建议增加 CRPE；Qwen2.5-VL、Qwen2.5-Omni、LLaVA-OneVision-2 都已在本轮确认 CRPE 官方分数。
- 如果关注文档/OCR 场景的幻觉，建议加 OCRBench / DocVQA / ChartQA / TextVQA，但必须标注为 proxy，并补充人工错误分析或直接幻觉评测。

## 附录：数据质量说明

本轮只做定向人工式召回复查：通过关键词定位候选页，再对官方 PDF/HTML 的表格截图或 HTML 表格结构核对行列，排除引用编号、章节号、模型版本号、页码、标准差、相邻 benchmark 分数等误报；未重跑全量自动抽取。
