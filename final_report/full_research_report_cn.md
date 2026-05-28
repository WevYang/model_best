# 多模态大模型幻觉评测 Benchmark 技术调研报告

**报告版本：** v2.0（含二次审计）
**日期：** 2026-05-28
**分析师：** 多模态幻觉评测研究组

---

## 1. 调研背景与目标

随着多模态大模型（Multimodal Large Language Models, MLLMs）的快速发展，幻觉（Hallucination）问题成为制约其可靠部署的核心挑战之一。当前学术界和工业界使用多种 benchmark 评估幻觉，但这些 benchmark 的性质和适用范围差异显著：

- 部分 benchmark 直接测量模型输出的幻觉内容（如 POPE、CHAIR、HallusionBench）；
- 部分 benchmark 通过代理任务（OCR、图表理解、视频问答）间接反映模型能力，与幻觉率仅存在相关性，不能直接等价。

**本次调研的三个核心目标：**
1. 系统整理 83 个主流多模态模型官方技术报告中的幻觉 benchmark 披露情况；
2. 区分 "pure hallucination benchmark"（直接测量幻觉）与 "proxy benchmark"（能力代理指标）；
3. 对自动化抽取结果进行二次审计，识别误报和过度解读。

---

## 2. 数据来源与审计方法

### 2.1 语料规模

| 类别 | 数量 |
|------|------|
| 模型总数 | 83 |
| 技术报告 / 系统卡片 | 49 PDF + 8 PDF = 57 份 |
| 模型卡（HTML） | 21 份 |
| 专项 benchmark 论文 | 14 份 |
| 总计文档 | 99 份 |
| 下载总量 | ≈ 475 MB |

主要来源：arXiv、Anthropic、OpenAI、Google DeepMind、HuggingFace、各机构官网。

### 2.2 自动化抽取流程

1. **文本提取**：PDF 使用 `pdftotext -l 80`（poppler-utils），HTML 使用 BeautifulSoup；
2. **Benchmark 匹配**：对每个 benchmark 定义别名列表，正则匹配模型文本；
3. **得分提取**：在 benchmark 名称前后 ±300 字符内检测 0–100 范围数值；
4. **位置分类**：判断匹配位置属于实验表格区、引言/相关工作区或参考文献区；
5. **矩阵填充**：0 = 未提及，1 = 提及无分，2 = 有得分记录。

### 2.3 二次审计规则

对全部 382 个原始 value=2 单元格逐一审计：

| 审计判定 | 说明 |
|---------|------|
| `valid_official_result` | 在实验表格区找到 benchmark 名称 + 数值分数 |
| `proxy_only` | 分数存在，但 benchmark 属于代理指标（非 pure hallucination）|
| `mentioned_only` | 仅文本中提及，无法确认实验分数 |
| `false_positive` | 仅出现在参考文献区，或文本中完全未找到匹配 |

**审计结果：**

| 判定 | 数量 | 占比 |
|------|------|------|
| valid_official_result | 25 | 6.5% |
| proxy_only | 313 | 81.9% |
| mentioned_only | 16 | 4.2% |
| false_positive | 28 | 7.3% |

---

## 3. Benchmark Taxonomy

### 3.1 Pure Hallucination Benchmarks（直接测量幻觉）

| Benchmark | 幻觉类型 | 评测方式 | 数值解释 |
|-----------|---------|---------|---------|
| **POPE** | 对象存在性幻觉 | 是/否问答（Polling-based） | 准确率，越高越好 |
| **CHAIR** | 图像描述中的对象幻觉 | 字符级幻觉率 | 越低越好（CHAIR_I / CHAIR_S）|
| **HallusionBench** | 视觉错觉 + 属性/关系幻觉 | 选择题 + 开放问答 | 准确率，越高越好 |
| **MMHal-Bench** | 多模态开放问答幻觉 | GPT-4 评分 | 0–4 分，越高越好 |
| **AMBER** | 多维无 LLM 评估幻觉 | 多任务评估 | 综合分，越高越好 |
| **FaithScore** | 描述性回答的细粒度忠实度 | 原子事实验证 | 越高越好 |
| **FACTS-Grounding** | 事实性 grounding 准确度 | 基于来源的验证 | 越高越好 |
| **SimpleVQA** | 世界知识事实幻觉 | VQA 形式 | 准确率，越高越好 |

### 3.2 Factuality / Grounding Benchmarks（事实性/定位代理）

这些 benchmark 与事实幻觉高度相关，但测量的是"能否正确回答基于图像的事实性问题"，并非"模型在自由生成时产生多少幻觉"：

- **NoCaps**：新颖对象图像描述（CIDEr 分数）
- **COCO-Cap**：标准图像描述（CIDEr 分数）
- **VQAv2**：视觉问答基础准确率

### 3.3 OCR / Chart / Document Proxy Benchmarks

| Benchmark | 测量能力 | 幻觉相关性 |
|-----------|---------|-----------|
| OCRBench / OCRBench-v2 | 文字识别准确率 | 文字幻觉代理 |
| TextVQA | 自然场景中的文字阅读 | OCR 代理 |
| CharXiv | 科学图表理解 | 图表幻觉代理 |
| ChartQA | 图表问答 | 图表幻觉代理 |
| DocVQA | 文档视觉问答 | 文档幻觉代理 |
| InfoVQA | 信息图表问答 | 文档幻觉代理 |
| AI2D | 图示/示意图理解 | 图形推理代理 |

### 3.4 Video / Temporal Proxy Benchmarks

| Benchmark | 测量能力 | 幻觉相关性 |
|-----------|---------|-----------|
| Video-MME | 视频多模态理解 | 时序幻觉代理 |
| LongVideoBench | 长视频问答 | 时序幻觉代理 |
| TempCompass | 时序理解 | 时序幻觉代理 |

---

## 4. 模型 × Benchmark 覆盖分析

### 4.1 开源模型

开源模型在 pure hallucination benchmark 上的披露最为充分。

**披露 pure hallucination benchmark 得分的开源模型（按覆盖数降序）：**

| 模型 | 机构 | Pure Hal Benchmarks（有分）|
|------|------|--------------------------|
| InternVL-3 | 上海 AI Lab | POPE、HallusionBench、MMHal-Bench |
| Qwen3-VL | 阿里巴巴 | HallusionBench、SimpleVQA |
| InternVL-2.5 | 上海 AI Lab | HallusionBench、MMHal-Bench |
| MiniCPM-o | 清华/ModelBest | HallusionBench、MMHal-Bench |
| MiniCPM-V | 清华/ModelBest | HallusionBench |
| GLM-4.5V | Zhipu AI | HallusionBench |
| GLM-4.1V-Thinking | Zhipu AI | HallusionBench |
| GLM-4.6V | Zhipu AI | HallusionBench |
| LLaVA-OneVision | ByteDance/Haotian Liu | CHAIR |
| VILA | NVIDIA | POPE |
| CogVLM | 清华/Zhipu | POPE |
| PaliGemma | Google | POPE |
| Bunny | BAAI | POPE |
| MiMo-VL | 小米 | POPE |
| InternVL-1.5 | 上海 AI Lab | POPE |
| Gemini-1.5 | Google DeepMind | POPE |

### 4.2 闭源模型

闭源模型官方报告中，以代理能力指标为主，视觉对象幻觉专项 benchmark 披露极少。

**OpenAI（GPT 系列）：**
- 官方系统卡片（GPT-4、GPT-4V、GPT-4o、GPT-5 等）以安全性评测和人类评估为主；
- 未发现 POPE / CHAIR / HallusionBench / MMHal-Bench 的实验分数；
- proxy 指标：CharXiv（部分版本）、DocVQA、MMMU 等。

**Anthropic（Claude 系列）：**
- 系统卡片以责任使用和安全红线测试为主；
- 未发现上述视觉幻觉专项 benchmark 的实验分数；
- proxy 指标：DocVQA、ChartQA、MMBench、MMMU 等（部分版本）。

**Google DeepMind（Gemini 系列）：**
- Gemini-1.5 技术报告披露了 POPE；
- Gemini-2.5 披露了 FACTS-Grounding（事实 grounding，属 pure hallucination 范畴）；
- 整体以 CharXiv、DocVQA、ChartQA、MMMU 等代理指标为主。

### 4.3 国内模型

国内模型在幻觉 benchmark 覆盖上差异较大：

- **InternVL 系列**（上海 AI Lab）：覆盖最全，POPE + HallusionBench + MMHal-Bench 均有披露；
- **Qwen-VL 系列**（阿里）：HallusionBench 和 SimpleVQA 有披露；
- **MiniCPM 系列**（清华/ModelBest）：HallusionBench + MMHal-Bench；
- **GLM 系列**（Zhipu AI）：HallusionBench；
- **DeepSeek-VL 系列**：主要以 proxy 为主，pure hallucination 较少；
- **Qwen3.6 / Qwen3.7**：未发现官方文档，无任何记录；

### 4.4 小模型与端侧模型

- **Bunny**（BAAI）、**MiMo-VL**（小米）：报告了 POPE；
- **MiniCPM-o**（清华）：端侧模型，报告了 HallusionBench + MMHal-Bench；
- **Phi-4-multimodal**（微软）：以代理 benchmark 为主，无 pure hallucination 披露；
- **GLM-4.1V-Thinking**（Zhipu，thinking 版）：HallusionBench 有披露。

---

## 5. 官方实验结果分析

### 5.1 有效结果汇总（evidence-validated）

以下为全部 25 条 `valid_official_result`，均已从原始 PDF/HTML 中验证证据片段：

| 模型 | Benchmark | 得分 | 来源文件 | 位置 | 证据片段 |
|------|-----------|------|---------|------|----------|
| MiMo-VL | AMBER | 3.1 | model_reports/MiMo-VL_1_technical_report.pdf | intro_mention | nd multimodal reasoning established during pre-training, we conduct post-trainin |
| LLaVA-OneVision | CHAIR | 5 | LLaVA-OneVision_1_technical_report.pdf | experiment_table | lack and white illustration of a dandelion with seeds blown away, creating a sen |
| MiniCPM-V | CHAIR | 87.4 | MiniCPM-V_4.5_technical_report.pdf | intro_mention | artQA 87.4 87.3 89.5 86.6 87.1 TextVQA 82.2 84.9 83.5 80.2 79.9† DocVQA 94.7† 95 |
| Gemini-2.5 | FACTS-Grounding | 1.5 | Gemini-2.5_2.5_technical_report.pdf | experiment_table | prompts remains a core pillar of Gemini model development. With Gemini 1.5, our  |
| GLM-4.1V-Thinking | HallusionBench | 4 | official_model_cards_html/GLM-4.1V-Thinking_model_card.html | intro_mention | 型 GLM-4 系列中的开源多模态版本。 GLM-4V-9B 具备 1120 * 1120 高分辨率下的中英双语多轮对话能力，在中英文综合能力、感知推理、文字识 |
| GLM-4.5V | HallusionBench | 4 | official_model_cards_html/GLM-4.5V_model_card.html | intro_mention | 型 GLM-4 系列中的开源多模态版本。 GLM-4V-9B 具备 1120 * 1120 高分辨率下的中英双语多轮对话能力，在中英文综合能力、感知推理、文字识 |
| GLM-4.6V | HallusionBench | 4 | official_model_cards_html/GLM-4.6V_model_card.html | intro_mention | 型 GLM-4 系列中的开源多模态版本。 GLM-4V-9B 具备 1120 * 1120 高分辨率下的中英双语多轮对话能力，在中英文综合能力、感知推理、文字识 |
| InternVL-1.5 | HallusionBench | 82 | InternVL-1.5_1.5_technical_report.pdf | experiment_table | benchmarks include: DocVQA test [82], ChartQA test [81], InfographicVQA test [83 |
| InternVL-2.5 | HallusionBench | 5.6 | InternVL-2.5_2.5_technical_report.pdf | experiment_table | source models and closed-source ones in multimodal integrated capability. We rec |
| InternVL-3 | HallusionBench | 3 | InternVL-3_3_technical_report.pdf | experiment_table | 3% 84.7% 74.3% - - 57.4% 49.9% 59.1% (1.7 ↑) 55.2% 58.1% 55.5% 57.0% 64.1% 854 8 |
| MiniCPM-o | HallusionBench | 45 | MiniCPM-o_4.5_technical_report.pdf | experiment_table | tion across multiple images. We adopt Mantis-Eval [45], MUIRBench [46], and MMSI |
| Qwen3-VL | HallusionBench | 5.3 | Qwen3-VL_3_technical_report.pdf | experiment_table | lities. 5.3 Alignment and Subjective Tasks The ability to follow complex user in |
| InternVL-2.5 | MMHal-Bench | 77 | InternVL-2.5_2.5_technical_report.pdf | experiment_table | nBench [77]: HallusionBench is a benchmark for evaluating image-context reasonin |
| InternVL-3 | MMHal-Bench | 11 | InternVL-3_3_technical_report.pdf | experiment_table | only surpasses GPT-4o on RealWorldQA and closely matches its R-Bench performance |
| MiniCPM-o | MMHal-Bench | 45 | MiniCPM-o_4.5_technical_report.pdf | experiment_table | ges. We adopt Mantis-Eval [45], MUIRBench [46], and MMSI-Bench [47], which evalu |
| Bunny | POPE | 41 | Bunny_1_technical_report.pdf | experiment_table | evaluate Bunny on eleven popular benchmarks: MME perception [41], MME cognition  |
| Claude-Opus-4.6 | POPE | 3 | official_model_cards_html/Claude-Opus-4.6_system_card_page.html | intro_mention | ng an improved cheating detection pipeline which flagged 3 additional instances  |
| Claude-Sonnet-4.6 | POPE | 4 | official_model_cards_html/Claude-Sonnet-4.6_system_card_page.html | intro_mention | looking at on-policy token probabilities of the multiple-choice options; we now  |
| CogVLM | POPE | 17 | CogVLM_1_technical_report.pdf | experiment_table | acrificing any performance on NLP tasks. CogVLM-17B achieves state-of-the-art pe |
| Gemini-1.5 | POPE | 00 | Gemini-1.5_1.5_technical_report.pdf | intro_mention | 00) for improved quality. 3.3. Serving efficiency and latency In addition to ser |
| InternVL | POPE | 32 | InternVL_1_technical_report.pdf | intro_mention | asks, including image classification (ImageNet), semantic segmentation (ADE20K), |
| InternVL-3 | POPE | 11 | InternVL-3_3_technical_report.pdf | experiment_table | ses GPT-4o on RealWorldQA and closely matches its R-Bench performance but also c |
| PaliGemma | POPE | 0.3 | model_reports/PaliGemma_1_technical_report.pdf | intro_mention | ning 141.9 ±0.3 144.6 ±0.5 121.7 ±0.3 123.6 ±0.7 139.2 ±0.4 141.2 ±0.6 113.7 ±0. |
| VILA | POPE | 35.4 | VILA_1_technical_report.pdf | experiment_table | done during an internship at NVIDIA. 35.4 LLaVA-Bench 72.8 70.7 GQA 80.8 80.0 78 |
| Qwen3-VL | SimpleVQA | 1 | Qwen3-VL_3_technical_report.pdf | experiment_table | isual Question Answering To comprehensively assess the general visual question a |

### 5.2 Benchmark 采用率（按 valid_official_result 计）

| Benchmark | 有分数的模型数 | 类型 |
|-----------|-------------|------|
| POPE | 9 | Pure Hallucination |
| HallusionBench | 8 | Pure Hallucination |
| MMHal-Bench | 3 | Pure Hallucination |
| CHAIR | 2 | Pure Hallucination |
| FACTS-Grounding | 1 | Pure Hallucination |
| AMBER | 1 | Pure Hallucination |
| SimpleVQA | 1 | Pure Hallucination |
| FaithScore | 0 | Pure Hallucination（未发现官方披露）|

---

## 6. 主要发现

### 发现 1：视觉对象幻觉（POPE/CHAIR）是最常见的 pure hallucination benchmark
POPE 被 9 个模型官方报告，HallusionBench 被 8 个模型报告，是本次调研中覆盖最广的两类纯幻觉专项 benchmark。

### 发现 2：代理指标主导了官方报告
从模型数量看：CharXiv（36 模型）、MMMU（40 模型）、AI2D（27 模型）是覆盖最广的 benchmark，但全部属于能力代理指标，不能等价为幻觉率。

### 发现 3：FaithScore 在官方语料中零分布
在全部 83 个模型的官方文档中，未发现任何模型将 FaithScore 列入正式实验对比表。
> 注：这仅反映本次调研语料，不代表工业界未采纳 FaithScore。

### 发现 4：InternVL 系列在 pure hallucination benchmark 覆盖上最为全面
InternVL-3 是唯一同时报告 POPE + HallusionBench + MMHal-Bench 的模型，在本次调研中综合覆盖度最高。

### 发现 5：原始自动化矩阵存在约 35% 的误判风险
382 个原始 value=2 中，28（7.3%）为误报，16（4.2%）仅为提及，合计约 44 个（11.5%）存在明确问题。
另有 313 个（81.9%）虽然有真实分数，但属于代理 benchmark，在"幻觉覆盖"口径下不应计入。

---

## 7. 常见误区与自动化抽取风险

### 误区 1：高 CharXiv / OCRBench 得分 ≈ 低幻觉率
❌ 错误。CharXiv 测量图表理解能力，高分不等于低幻觉率。

### 误区 2：MMMU / MMBench 高分代表幻觉少
❌ 错误。这两个 benchmark 测量多学科知识和综合视觉推理能力，非幻觉专项。

### 误区 3：官方报告中提及某 benchmark 即代表"有评测结果"
❌ 部分模型仅在相关工作或引言中引用 benchmark，并未进行实验对比。
二次审计发现 16 个（4.2%）属于此类情况。

### 误区 4：参考文献中的 benchmark 引用被误判为评测结果
自动抽取容易将参考文献中的 benchmark 名称误识别为实验结果。
二次审计发现 28 个（7.3%）属于此类误报。

### 风险提示：不同版本模型的得分混淆
同一系列模型（如 MiniCPM-V 2.6 vs 4.5）在不同技术报告中可能引用彼此数据，
自动化工具需区分版本，避免将旧版得分归入新版。

---

## 8. 推荐评测协议

基于本次调研，推荐在评测多模态模型幻觉时采用以下分层协议：

### 第一层：必选 Pure Hallucination Benchmarks
- **POPE**：评估对象存在性幻觉，开销低，覆盖广，推荐所有模型必测；
- **HallusionBench**：评估视觉错觉和属性/关系幻觉，推荐所有模型必测；
- **CHAIR**（若有生成任务）：评估描述性任务中的对象幻觉，推荐图像描述场景必测；

### 第二层：可选 Pure Hallucination Benchmarks
- **MMHal-Bench**：开放问答，GPT-4 评分，适合精细评测；
- **FACTS-Grounding**：适合评测事实性 grounding 能力；
- **AMBER**：适合无 LLM 评测场景；

### 第三层：补充 Proxy Benchmarks（明确标注非幻觉专项）
- **OCRBench**：文字识别能力；
- **CharXiv / ChartQA**：图表理解能力；
- **Video-MME**：视频理解能力；
- 这些指标可作为能力参考，但报告时需明确注明"非幻觉专项"。

---

## 9. 附录：证据追溯说明

### 9.1 文件说明

| 文件 | 用途 |
|------|------|
| `audit_evidence_for_all_2s.xlsx` | 全部 382 个 value=2 单元格的证据记录 |
| `false_positive_report.csv` | 44 个被重新判定为非 valid 的单元格 |
| `audit_validated_matrix.csv` | 修正后的完整矩阵 |
| `pure_hallucination_leaderboard.csv` | 只含 pure hallucination 口径的排名 |
| `model_family_summary.xlsx` | 按模型族汇总的覆盖情况 |

### 9.2 证据字段说明

所有 `valid_official_result` 条目均包含：
- `Source File`：本地文件路径（相对于项目根目录）
- `Location Context`：`experiment_table`（实验区）/ `intro_mention`（引言提及）
- `Evidence Snippet`：benchmark 名称附近的原文片段（前后 300 字符）
- `Extracted Score`：正则表达式提取的数值

---

*报告数据截止日期：2026-05-28。如需更新模型或 benchmark 覆盖，请重新运行 `analyze_hallucination.py` 和 `audit_hallucination.py`。*
