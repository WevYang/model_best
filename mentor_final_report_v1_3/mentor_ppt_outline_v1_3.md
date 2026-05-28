# PPT 讲稿：多模态大模型幻觉评测调研 v1.3

## Slide 1: 任务和调研口径

- 目标是梳理官方公开的幻觉评测 benchmark 和分数，不做模型能力总排名。
- 重点看 direct hallucination benchmark、factuality / grounding related benchmark、proxy benchmark 三层。
- 当前版本已覆盖 Qwen、InternVL、MiniCPM、VILA、CogVLM、Bunny、DeepSeek-VL、Phi-4、GLM、Gemma 3。

建议图：总览流程图或研究问题列表。  
讲解备注：先把口径讲清楚，再展示分数。

## Slide 2: Benchmark 分类

- Direct benchmark：POPE、CHAIR/ObjHalBench、HallusionBench、MMHal-Bench、CRPE。
- Factuality-related：FACTS-Grounding、SimpleVQA。
- Proxy benchmark：CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、TextVQA、MMMU、MME、MathVista、AI2D、RefCOCO。

建议图：三层分类图。  
讲解备注：强调 proxy 只作能力背景，不是 hallucination rate。

## Slide 3: 官方公开分数主表

- Qwen3-VL、Qwen2.5-VL、InternVL3/2.5、MiniCPM-V/o、DeepSeek-VL、CogVLM、Bunny、VILA、Phi-4、LLaVA-OneVision-2、GLM-4V-9B、PaliGemma、Gemma 3 都有可引用结果。
- PaliGemma 的 POPE 为 transfer / fine-tuning 口径。
- Gemma 3 公开的是 FACTS-Grounding factuality-related 分数。

建议图：代表模型主表。  
讲解备注：不要把所有空白解读为“没有评测”。

## Slide 4: Qwen / InternVL / MiniCPM 重点发现

- Qwen3-VL 公开 HallusionBench 和 SimpleVQA；Qwen2.5-VL 公开 HallBench_avg 和 CRPE。
- InternVL3 / 2.5 同时公开 HallusionBench、MMHal、POPE、CRPE。
- MiniCPM-V / o 公开 HallusionBench 和 MMHal，MiniCPM-V 还公开 CHAIR 指标。

建议图：Qwen / InternVL / MiniCPM 对比表。  
讲解备注：这页是最容易形成“直接幻觉评测覆盖”的主线。

## Slide 5: 其它开源模型补充

- DeepSeek-VL、CogVLM、Bunny、VILA、Phi-4 都公开了 POPE。
- LLaVA-OneVision-2 公开了 CRPE。
- GLM-4V-9B 在本地模型卡中公开了 HallusionBench。

建议图：补充模型表。  
讲解备注：帮助说明主流开源模型也不是只有 proxy。

## Slide 6: 闭源模型披露情况

- OpenAI / Anthropic / Gemini 闭源没有公开同类可横比学术视觉幻觉表格。
- 但它们公开了 system-card 级 factuality、safety、internal eval。
- 因此结论是“未公开同类表格”，不是“没有相关评测”。

建议图：闭源披露说明表。  
讲解备注：措辞要谨慎，避免过度推断。

## Slide 7: Proxy benchmark 的用法

- OCRBench、DocVQA、ChartQA、TextVQA、MMMU、MME、MathVista、AI2D、RefCOCO 反映相关能力，但不等于 hallucination rate。
- proxy 适合做风险解释变量，不适合混入 direct leaderboard。
- 要看幻觉，需要 direct benchmark；要看泛化能力，proxy 才有意义。

建议图：proxy 与 direct 分层示意图。  
讲解备注：这页是避免误读的关键。

## Slide 8: 结论和建议

- 内部横评最小组合：POPE + HallusionBench + MMHal-Bench。
- 关系幻觉补 CRPE。
- 文档 / OCR 场景再补 OCRBench / DocVQA / ChartQA，并明确标注 proxy。

建议图：推荐评测组合卡片。  
讲解备注：收束到下一步评测设计。

