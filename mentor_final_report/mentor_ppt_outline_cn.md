# Mentor PPT 大纲：多模态大模型幻觉评测 Benchmark 调研

## Slide 1: 调研问题

- 目标不是给模型做能力总排名，而是梳理官方报告中公开了哪些幻觉评测benchmark和分数。
- 关注三件事：benchmark测什么、哪些模型公开了分数、哪些分数不能直接横比。
- 本轮主表只收录verified或v3.2人工确认的官方公开分数。
- 闭源模型单独讨论披露方式，避免误读为未做相关评估。

建议插入：无，使用问题列表页。  
讲解备注：先把口径立住，避免听众把公开披露覆盖度误解成模型质量排名。

## Slide 2: Benchmark 分类图

- Pure hallucination：POPE、CHAIR/ObjHalBench、HallusionBench、MMHal-Bench、CRPE、AMBER、FaithScore。
- Factuality / grounding related：FACTS-Grounding、SimpleVQA。
- Proxy capability：CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、TextVQA、MMMU、MME、MathVista。
- 三类可以共同解释风险，但不能混成一个幻觉率。

建议插入：`mentor_score_table.xlsx` Sheet 2 或重新绘制三层分类图。  
讲解备注：强调proxy是能力背景，不是直接hallucination benchmark。

## Slide 3: Pure Hallucination Benchmark 说明

- POPE主要测对象存在性幻觉。
- CHAIR/ObjHalBench主要测caption或描述中的对象幻觉，指标为lower-is-better。
- HallusionBench覆盖视觉错觉、语言先验和视觉推理幻觉。
- MMHal-Bench覆盖开放式多模态回答中的幻觉，score越高越好，Hallrate越低越好。
- CRPE补充关系幻觉和组合关系错误。

建议插入：`mentor_summary_cn.md` 第2节benchmark表。  
讲解备注：这页是后续模型分数表的读表说明。

## Slide 4: 模型官方分数总表

- InternVL3-78B：HallusionBench 59.1，MMHal 3.85，POPE 90.3，CRPE 79.2。
- InternVL2.5-78B：HallusionBench 57.4，MMHal 3.89，POPE 90.8，CRPE 78.8。
- MiniCPM-V 4.5：HallusionBench 61.2，MMHal Score 5.0，Hallrate↓ 19.4，CHAIRs↓ 9.3，CHAIRi↓ 5.2。
- MiniCPM-o 4.5：HallusionBench 63.2，MMHal Score 4.7，Hallrate↓ 24.3。
- PaliGemma：POPE 86.0 / 87.0，但为transfer/fine-tuning口径。

建议插入：`mentor_one_page_table.md` 核心表或 `mentor_score_table.xlsx` Sheet 1。  
讲解备注：强调这不是排名，重点是“哪些官方报告公开了哪些分数”。

## Slide 5: InternVL / MiniCPM / PaliGemma 重点结果

- InternVL3/2.5的优势是公开覆盖POPE、HallusionBench、MMHal-Bench、CRPE四类direct benchmark。
- MiniCPM-V/o的优势是报告HallusionBench和MMHal，其中MiniCPM-V还给出ObjHalBench/CHAIR指标。
- PaliGemma只放入POPE公开分数，但必须标注VQAv2-transferred / fine-tuning setting。
- 不同模型尺寸、zero-shot与fine-tuning设置不能直接硬比。

建议插入：核心模型分数摘录表。  
讲解备注：这页回答“哪些模型官方公开得比较完整”。

## Slide 6: 闭源模型披露情况

- OpenAI、Anthropic当前未公开POPE/CHAIR/HallusionBench/MMHal/CRPE等学术视觉幻觉benchmark表格。
- 它们公开了system-card级factuality、safety、internal hallucination/deception相关评估。
- Google Gemini闭源系列也应与PaliGemma分开看；PaliGemma是单独的开放模型报告口径。
- 因此结论是“未公开同类学术benchmark表格”，不表示未做相关评估。

建议插入：`mentor_score_table.xlsx` Sheet 3。  
讲解备注：这页处理闭源模型的谨慎表述。

## Slide 7: Proxy Benchmark 为什么不能直接当幻觉率

- OCRBench、DocVQA、ChartQA、TextVQA衡量文字、文档和图表理解，错误可能诱发幻觉，但不是幻觉率。
- Video-MME衡量视频理解和时序推理，不等于视频幻觉评测。
- MMMU、MME、MathVista衡量综合推理或数学推理，不能与POPE/CHAIR相加。
- proxy适合做风险解释变量，不适合作为direct hallucination leaderboard。

建议插入：`mentor_score_table.xlsx` Sheet 4。  
讲解备注：这页解释为什么报告没有把所有常见benchmark都放进幻觉主表。

## Slide 8: 结论与建议

- 公开披露最清晰的direct hallucination分数来自InternVL、MiniCPM和PaliGemma部分结果。
- 若要内部横评，建议最低组合为POPE + HallusionBench + MMHal-Bench。
- 关注关系幻觉时增加CRPE；关注文档/OCR场景时增加OCRBench/DocVQA并标注proxy。
- 对外表述使用“官方公开披露覆盖度”，不要写成模型质量排名。

建议插入：结论三点或路线图。  
讲解备注：收束到下一步实验设计建议。
