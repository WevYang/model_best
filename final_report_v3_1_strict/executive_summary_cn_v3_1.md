# 多模态大模型幻觉评测调研执行摘要 v3.1（Strict Audit）

本项目分析多模态大模型官方技术报告、system card、model card 与官方文档中对 hallucination benchmark 的公开披露。`benchmark_column_dictionary.xlsx` 定义了 28 个 benchmark columns；v3.1 按三层口径重标注，正文仅列代表性 benchmark，不再硬凑完整清单。

旧版 v2 的 25 条 valid_official_result 仍全部作废。v3.1 没有重新抽取原始 PDF，只对已经通过 strict audit 的结果做术语修订、风险标注和图表重画。

三层分类是：A. pure multimodal hallucination benchmark：POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER、FaithScore；B. hallucination-related factuality / grounding benchmark：FACTS-Grounding、SimpleVQA；C. proxy capability benchmark：CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、MMMU 等。

最终 leaderboard 仍只统计 high/medium 的 verified results，但 medium confidence 必须带风险标记。当前 high=5、medium=4、low=2；进入 coverage leaderboard 的模型为：InternVL-2.5、MiniCPM-V、MiniCPM-o、PaliGemma。这是一份 disclosure coverage leaderboard，不是 model quality leaderboard。

InternVL-2.5 仍是 medium confidence，需要人工确认 Section 5.6.1 列顺序；PaliGemma 的 POPE 明确标为 transfer/fine-tuning 任务口径，不应与 zero-shot 直接横比。FACTS-Grounding 与 SimpleVQA 在本版中不再写成 pure multimodal hallucination。
