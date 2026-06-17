# 多模态大模型幻觉评测调研执行摘要 v3（Strict Audit）

本项目在本地官方语料中分析多模态大模型对 hallucination benchmark 的公开披露情况，范围包括技术报告、system card、model card、官方 GitHub/HuggingFace 文档，以及 28 个 benchmark（pure hallucination 与 proxy 分开统计）。

旧版 v2 的 25 条 valid_official_result 已全部作废：strict audit 确认其中 25/25 均为误报，主要来自引用编号 `[N]`、章节号 `N.M`、模型版本号、页码、标准差、计数数字、HTML 噪声，以及 ChartQA/DocVQA/LLaVA-Bench 等相邻 benchmark 分数串行。

v3 的最终可信口径是：只有 confidence=high 或 medium 且 benchmark_type=pure_hallucination 的结果进入 leaderboard；confidence=low 只进入人工确认清单。当前 strict_valid_results 中 high=5 条、medium=4 条、low=2 条；进入最终覆盖统计的模型为：InternVL-2.5、MiniCPM-V、MiniCPM-o、PaliGemma。leaderboard 只按 verified pure benchmark count 统计覆盖数，不按不同 benchmark 的分数高低排名。

Pure hallucination benchmark 指直接测量幻觉输出的 POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER、FaithScore、FACTS-Grounding、SimpleVQA。CharXiv、OCRBench、Video-MME、DocVQA、ChartQA、MMMU 等是 proxy benchmark，可反映相关能力，但不能等价为 hallucination rate，也不进入 pure leaderboard。

OpenAI / Anthropic 在当前语料中未公开 POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER 等视觉幻觉专项 benchmark 的实验表格；但其系统卡披露了 factuality、安全性、内部 hallucination/deception 相关评估，因此只能使用“未公开专项 benchmark 表格”的谨慎口径。FaithScore 在当前语料中未发现正式实验表格披露，不能引申为更强的行业采纳结论。
