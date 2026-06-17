# 多模态大模型幻觉评测 Benchmark 调研总结

## 1. 一句话结论

- 多模态幻觉评测不能只看一个分数：POPE、CHAIR/ObjHalBench、HallusionBench、MMHal-Bench、CRPE、AMBER、FaithScore 分别覆盖对象幻觉、关系幻觉、开放式回答幻觉和 faithfulness 等不同侧面。
- 当前 v3.2 人工确认后，InternVL3-78B、InternVL2.5-78B、MiniCPM-V 4.5、MiniCPM-o 4.5 有可直接引用的官方 pure hallucination benchmark 分数；PaliGemma 有 POPE 分数，但属于 VQAv2-transferred / fine-tuning 口径。
- 公开披露覆盖度不是模型能力排名：不同 benchmark 的任务形式、指标方向和评测设置不同，不能把分数相加，也不能跨设置硬排高低。
- OpenAI、Anthropic 以及 Google Gemini 闭源系列未在当前语料中公开 POPE、CHAIR、HallusionBench、MMHal、CRPE 等学术视觉幻觉 benchmark 表格；但它们公开了 system-card 级 factuality、safety 和内部 hallucination/deception 相关评估。
- CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、TextVQA、MMMU、MME、MathVista 等是相关能力 proxy，能帮助定位风险来源，但不能直接当作 hallucination rate。

## 2. 常用幻觉评测 Benchmark

| Benchmark | 主要测什么 | 幻觉类型 | 任务形式 | 指标 | 是否直接测 hallucination | 本次官方确认得分模型 | 常见研究/第三方使用场景 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| POPE | 判断模型是否把图像中不存在的物体说成存在 | 对象幻觉 | yes/no probing、二分类 VQA | accuracy / F1 / precision / recall | 是 | InternVL3、InternVL2.5、PaliGemma | LLaVA 系、开源 MLLM 横评、对象幻觉评测 |
| CHAIR / ObjHalBench | 图像描述里是否生成不存在的对象 | 对象幻觉 | caption 或开放描述后与对象标注比对 | CHAIRs↓ / CHAIRi↓ | 是 | MiniCPM-V | captioning、open-ended MLLM 描述评测、对象幻觉分析 |
| HallusionBench | 视觉错觉、视觉推理和语言先验导致的错误 | 视觉推理幻觉 | 多选/问答 | accuracy | 是 | InternVL3、InternVL2.5、MiniCPM-V、MiniCPM-o | 开源 MLLM 幻觉/错觉评测 |
| MMHal-Bench | open-ended 回答中的幻觉程度 | 回答级幻觉 | 开放式多模态问答 | score / Hallrate↓ | 是 | InternVL3、InternVL2.5、MiniCPM-V、MiniCPM-o | 开放式多模态回答幻觉评估 |
| CRPE | 关系和组合关系是否被错误描述 | 关系幻觉 | 关系/组合推理问答 | accuracy | 是 | InternVL3、InternVL2.5 | 关系幻觉/组合关系错误评测 |
| AMBER | 对象、属性、关系等多类型幻觉 | 综合多模态幻觉 | 判别式与生成式混合 | accuracy / F1 / hallucination metrics | 是 | 本次未确认官方模型分数 | 开源 MLLM 综合幻觉评测 |
| FaithScore | 生成内容与图像证据是否一致 | faithfulness / factual hallucination | 事实单元拆解与一致性判断 | faithfulness score / F1 等 | 是 | 本次未确认官方模型分数 | faithfulness / atomic fact consistency 研究 |
| FACTS-Grounding | 回答是否有证据支撑、是否 grounded | factuality / grounding | grounded QA 或事实判断 | accuracy / pass rate 等 | 相关但非 pure | 不混入 pure 表 | system-card、factuality、grounding 相关评估 |
| SimpleVQA | 简单事实问答准确性 | factuality | 短问答/事实查询 | accuracy | 相关但非 pure | 不混入 pure 表 | factuality 相关评估 |
| CharXiv | 科学图表和论文图理解 | proxy 能力 | 图形问答/推理 | accuracy | 否 | 不混入 pure 表 | 科学图表理解、论文图推理能力背景评估 |
| OCRBench | OCR 和场景文字理解 | proxy 能力 | OCR 相关问答/识别 | score / accuracy | 否 | 不混入 pure 表 | OCR、text-rich image 理解能力背景评估 |
| Video-MME | 视频理解和时序推理 | proxy 能力 | 视频问答 | accuracy | 否 | 不混入 pure 表 | 视频理解、时序推理能力背景评估 |
| DocVQA / ChartQA / TextVQA / MMMU 等 | 文档、图表、文字和综合推理能力 | proxy 能力 | QA、多选、推理 | accuracy / score 等 | 否 | 不混入 pure 表 | OCR、chart、video、document、通用推理能力背景评估 |

## 3. 模型官方公开分数总表

| 模型 | 机构 | 报告版本 | HallusionBench | MMHal-Bench | POPE | CHAIR / ObjHalBench | CRPE | AMBER | FaithScore | FACTS-Grounding / SimpleVQA | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| InternVL3-78B | Shanghai AI Lab | InternVL3-78B / v3.2 人工确认 | 59.1 | 3.85 | 90.3 | 官方未公开 verified score | 79.2 | 官方未公开 verified score | 官方未公开 verified score | 未纳入 pure 表 | v3.2 人工确认；zero-shot 官方报告口径。 |
| InternVL2.5-78B | Shanghai AI Lab | InternVL2.5-78B / v3.2 人工确认 | 57.4 | 3.89 | 90.8 | 官方未公开 verified score | 78.8 | 官方未公开 verified score | 官方未公开 verified score | 未纳入 pure 表 | v3.2 人工确认；zero-shot 官方报告口径。 |
| MiniCPM-V 4.5 | Tsinghua / ModelBest | MiniCPM-V 4.5 技术报告 | 61.2 | Score=5.0；Hallrate↓=19.4 | 官方未公开 verified score | CHAIRs↓=9.3；CHAIRi↓=5.2 | 官方未公开 verified score | 官方未公开 verified score | 官方未公开 verified score | 未纳入 pure 表 | CHAIR 和 Hallrate 为 lower-is-better。 |
| MiniCPM-o 4.5 | Tsinghua / ModelBest | MiniCPM-o 4.5 技术报告 | 63.2 | Score=4.7；Hallrate↓=24.3 | 官方未公开 verified score | 官方未公开 verified score | 官方未公开 verified score | 官方未公开 verified score | 官方未公开 verified score | 未纳入 pure 表 | MMHal score 越高越好，Hallrate 越低越好。 |
| PaliGemma | Google | PaliGemma 技术报告 | 官方未公开 verified score | 官方未公开 verified score | 86.0 / 87.0 | 官方未公开 verified score | 官方未公开 verified score | 官方未公开 verified score | 官方未公开 verified score | 未纳入 pure 表 | VQAv2-transferred / fine-tuning setting，不与 zero-shot MLLM 直接横比。 |

说明：这张表是“官方公开分数速览”，不是模型能力排行榜。不同 benchmark 之间不能直接相加，同一 benchmark 也要检查 zero-shot、fine-tuning、模型尺寸和指标方向。

## 4. 闭源模型披露情况

| 模型系列 | 是否公开 POPE / CHAIR / HallusionBench / MMHal / CRPE 等学术幻觉 benchmark | 是否公开 factuality / safety / internal hallucination eval | 备注 |
| --- | --- | --- | --- |
| OpenAI GPT-4V / GPT-4o / GPT-5 系列 | 当前项目未发现公开同类学术视觉幻觉 benchmark 表格 | 是，system card 级 factuality、safety、internal hallucination/deception 相关评估 | 不能把披露缺口误读为未做相关评估；只能说未公开这些学术 benchmark 的可横比表格。 |
| Google Gemini 系列 | 当前项目未发现公开同类学术视觉幻觉 benchmark 表格 | 是，公开 factuality、grounding、安全与广泛多模态能力评估 | Gemini 闭源系列与 PaliGemma 不是同一比较口径；PaliGemma 的 POPE 属 transfer/fine-tuning 口径。 |
| Anthropic Claude 系列 | 当前项目未发现公开同类学术视觉幻觉 benchmark 表格 | 是，system card 级 safety、factuality 和内部风险评估 | 不能把披露缺口误读为未做相关评估。 |

## 5. Proxy benchmark 单独说明

CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、TextVQA、MMMU、MME、MathVista 等应该单独看。它们能反映图表、OCR、文档、视频、通用推理等能力，很多错误会诱发幻觉，但这些 benchmark 本身不是 hallucination rate。报告中可以把它们作为“风险解释变量”或“能力背景”，不要和 POPE、CHAIR、HallusionBench、MMHal-Bench、CRPE 等 direct hallucination benchmark 合并排名。

## 6. 后续建议

- 如果要做模型横评，建议至少跑 POPE + HallusionBench + MMHal-Bench：一个覆盖对象存在性，一个覆盖视觉推理幻觉，一个覆盖开放式回答幻觉。
- 如果关注关系幻觉，建议增加 CRPE，并单独报告关系/组合关系错误，不要只看对象幻觉。
- 如果关注文档/OCR 场景的幻觉，建议加 OCRBench / DocVQA / ChartQA / TextVQA，但必须标注为 proxy，并补充人工错误分析或直接幻觉评测。

## 附录：数据质量说明

本项目的自动抽取结果经过 strict audit 和 v3.2 人工核查，已排除引用编号、章节号、模型版本号、页码、标准差、相邻 benchmark 分数等误报；详细审计过程见 v3.1/v3.2 文件，本报告不展开。
