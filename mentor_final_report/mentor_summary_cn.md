# 多模态大模型幻觉评测 Benchmark 调研总结

## 1. 一句话结论

- 多模态幻觉评测不能只看一个分数：POPE、CHAIR/ObjHalBench、HallusionBench、MMHal-Bench、CRPE、AMBER、FaithScore分别覆盖对象幻觉、关系幻觉、开放式回答幻觉和faithfulness等不同侧面。
- 当前v3.2人工确认后，InternVL3-78B、InternVL2.5-78B、MiniCPM-V 4.5、MiniCPM-o 4.5有可直接引用的官方pure hallucination benchmark分数；PaliGemma有POPE分数，但属于VQAv2-transferred / fine-tuning口径。
- 公开披露覆盖度不是模型能力排名：不同benchmark的任务形式、指标方向和评测设置不同，不能把分数相加，也不能跨设置硬排高低。
- OpenAI、Anthropic以及Google Gemini闭源系列没有在当前语料中公开POPE、CHAIR、HallusionBench、MMHal、CRPE等学术视觉幻觉benchmark表格；但它们公开了system-card级factuality、safety和内部hallucination/deception相关评估。
- CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、TextVQA、MMMU、MME、MathVista等是相关能力proxy，能帮助定位风险来源，但不能直接当作hallucination rate。

## 2. 常用幻觉评测 Benchmark

| Benchmark | 主要测什么 | 幻觉类型 | 任务形式 | 指标 | 是否直接测 hallucination | 常见使用模型 |
| --- | --- | --- | --- | --- | --- | --- |
| POPE | 判断模型是否把图像中不存在的物体说成存在 | 对象幻觉 | yes/no probing、二分类VQA | accuracy / F1 / precision / recall | 是 | InternVL、PaliGemma、LLaVA系等 |
| CHAIR / ObjHalBench | 图像描述里是否生成不存在的对象 | 对象幻觉 | caption或开放描述后与对象标注比对 | CHAIRs↓ / CHAIRi↓ | 是 | MiniCPM-V、captioning/MLLM报告 |
| HallusionBench | 视觉错觉、视觉推理和语言先验导致的错误 | 视觉推理幻觉 | 多选/问答 | accuracy | 是 | InternVL、MiniCPM等 |
| MMHal-Bench | open-ended回答中的幻觉程度 | 回答级幻觉 | 开放式多模态问答 | score / Hallrate↓ | 是 | InternVL、MiniCPM等 |
| CRPE | 关系和组合关系是否被错误描述 | 关系幻觉 | 关系/组合推理问答 | accuracy | 是 | InternVL系列 |
| AMBER | 对象、属性、关系等多类型幻觉 | 综合多模态幻觉 | 判别式与生成式混合 | accuracy / F1 / hallucination metrics | 是 | 开源MLLM评测较常见 |
| FaithScore | 生成内容与图像证据是否一致 | faithfulness / factual hallucination | 事实单元拆解与一致性判断 | faithfulness score / F1等 | 是 | 研究型评测和部分模型分析 |
| FACTS-Grounding | 回答是否有证据支撑、是否grounded | factuality / grounding | grounded QA或事实判断 | accuracy / pass rate等 | 相关但非pure | 闭源/系统卡或factuality评测 |
| SimpleVQA | 简单事实问答准确性 | factuality | 短问答/事实查询 | accuracy | 相关但非pure | factuality相关报告 |
| CharXiv | 科学图表和论文图理解 | proxy能力 | 图形问答/推理 | accuracy | 否 | 多模态推理模型 |
| OCRBench | OCR和场景文字理解 | proxy能力 | OCR相关问答/识别 | score / accuracy | 否 | Qwen-VL、InternVL、MiniCPM等 |
| Video-MME | 视频理解和时序推理 | proxy能力 | 视频问答 | accuracy | 否 | 视频/多模态模型 |
| DocVQA / ChartQA / TextVQA / MMMU等 | 文档、图表、文字和综合推理能力 | proxy能力 | QA、多选、推理 | accuracy / score等 | 否 | 主流开源和闭源MLLM |

## 3. 模型官方公开分数总表

| 模型 | 机构 | 报告版本 | HallusionBench | MMHal-Bench | POPE | CHAIR / ObjHalBench | CRPE | AMBER | FaithScore | FACTS-Grounding / SimpleVQA | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| InternVL3-78B | Shanghai AI Lab | InternVL3-78B / v3.2人工确认 | 59.1 | 3.85 | 90.3 | 官方未公开verified score | 79.2 | 官方未公开verified score | 官方未公开verified score | 未纳入pure表 | v3.2人工确认；zero-shot官方报告口径。 |
| InternVL2.5-78B | Shanghai AI Lab | InternVL2.5-78B / v3.2人工确认 | 57.4 | 3.89 | 90.8 | 官方未公开verified score | 78.8 | 官方未公开verified score | 官方未公开verified score | 未纳入pure表 | v3.2人工确认；zero-shot官方报告口径。 |
| MiniCPM-V 4.5 | Tsinghua / ModelBest | MiniCPM-V 4.5技术报告 | 61.2 | Score=5.0；Hallrate↓=19.4 | 官方未公开verified score | CHAIRs↓=9.3；CHAIRi↓=5.2 | 官方未公开verified score | 官方未公开verified score | 官方未公开verified score | 未纳入pure表 | CHAIR和Hallrate为lower-is-better。 |
| MiniCPM-o 4.5 | Tsinghua / ModelBest | MiniCPM-o 4.5技术报告 | 63.2 | Score=4.7；Hallrate↓=24.3 | 官方未公开verified score | 官方未公开verified score | 官方未公开verified score | 官方未公开verified score | 官方未公开verified score | 未纳入pure表 | MMHal score越高越好，Hallrate越低越好。 |
| PaliGemma | Google | PaliGemma技术报告 | 官方未公开verified score | 官方未公开verified score | 86.0 / 87.0 | 官方未公开verified score | 官方未公开verified score | 官方未公开verified score | 官方未公开verified score | 未纳入pure表 | VQAv2-transferred / fine-tuning setting，不与zero-shot MLLM直接横比。 |

说明：这张表是“官方公开分数速览”，不是模型能力排行榜。不同benchmark之间不能直接相加，同一benchmark也要检查zero-shot、fine-tuning、模型尺寸和指标方向。

## 4. 闭源模型披露情况

| 模型系列 | 是否公开 POPE / CHAIR / HallusionBench / MMHal / CRPE 等学术幻觉 benchmark | 是否公开 factuality / safety / internal hallucination eval | 备注 |
| --- | --- | --- | --- |
| OpenAI GPT-4V / GPT-4o / GPT-5系列 | 当前项目未发现公开同类学术视觉幻觉benchmark表格 | 是，system card级factuality、safety、internal hallucination/deception相关评估 | 不能把披露缺口误读为未做相关评估；只能说未公开这些学术benchmark的可横比表格。 |
| Google Gemini系列 | 当前mentor表不纳入可横比pure hallucination分数；PaliGemma单独列为POPE fine-tuning口径 | 是，公开安全、事实性和广泛多模态能力评估 | Gemini闭源系列与PaliGemma不是同一比较口径。 |
| Anthropic Claude系列 | 当前项目未发现公开同类学术视觉幻觉benchmark表格 | 是，system card级safety、factuality和内部风险评估 | 不能把披露缺口误读为未做相关评估。 |

## 5. Proxy benchmark 单独说明

CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、TextVQA、MMMU、MME、MathVista等应该单独看。它们能反映图表、OCR、文档、视频、通用推理等能力，很多错误会诱发幻觉，但这些benchmark本身不是hallucination rate。报告中可以把它们作为“风险解释变量”或“能力背景”，不要和POPE、CHAIR、HallusionBench、MMHal-Bench、CRPE等direct hallucination benchmark合并排名。

## 6. 给 mentor 的建议

- 如果要做模型横评，建议至少跑POPE + HallusionBench + MMHal-Bench：一个覆盖对象存在性，一个覆盖视觉推理幻觉，一个覆盖开放式回答幻觉。
- 如果关注关系幻觉，建议增加CRPE，并单独报告关系/组合关系错误，不要只看对象幻觉。
- 如果关注文档/OCR场景的幻觉，建议加OCRBench / DocVQA / ChartQA / TextVQA，但必须标注为proxy，并补充人工错误分析或直接幻觉评测。

## 附录：数据质量说明

本项目的自动抽取结果经过strict audit和v3.2人工核查，已排除引用编号、章节号、模型版本号、页码、标准差、相邻benchmark分数等误报；详细审计过程见v3.1/v3.2文件，本报告不展开。
