# 多模态大模型幻觉评测 Benchmark 调研 — 执行摘要

**报告日期：** 2026-05-28
**分析师：** 多模态幻觉评测研究组

---

## 一、调研范围

| 维度 | 数量 |
|------|------|
| 覆盖模型 | 83 个 |
| 官方报告/系统卡片/模型卡 | 99 份（PDF 78份 + HTML 21份）|
| 跟踪 Benchmark | 28 个（纯幻觉 8 个 + 代理指标 20 个）|
| 来自机构 | OpenAI、Google、Anthropic、阿里、DeepSeek、腾讯、字节、清华、上海 AI Lab 等 27 家 |

原始自动化抽取发现 382 个 value=2 单元格（官方有得分），经二次审计：

| 审计结果 | 数量 | 占比 |
|----------|------|------|
| ✅ 真实官方幻觉实验结果 | 25 | 6.5% |
| 🔶 代理 benchmark 得分（非幻觉专项） | 313 | 81.9% |
| ⚠️ 仅提及，无实验分数 | 16 | 4.2% |
| ❌ 误报（引用区或未找到） | 28 | 7.3% |

---

## 二、最重要的 5 条结论

### 结论 1：绝大多数"幻觉评测"实为能力代理指标，并非直接幻觉测量
原始矩阵 382 个有分数单元格中，**81.9%（313个）属于代理 benchmark**（如 CharXiv、MMMU、DocVQA、ChartQA、OCRBench、Video-MME 等）。这些指标衡量的是模型在图表理解、文字识别、视频问答等方面的能力，与直接测量"模型输出了多少幻觉内容"存在本质差异。

### 结论 2：主流闭源模型（OpenAI / Google / Anthropic）几乎不报告视觉对象幻觉专项 Benchmark
在当前官方语料范围内：
- **OpenAI（GPT 系列）**：官方报告中未发现 POPE / CHAIR / HallusionBench / MMHal-Bench / AMBER 的实验分数。
- **Anthropic（Claude 系列）**：同上。系统卡片中涉及安全性评测，但不含上述视觉幻觉专项。
- **Google（Gemini 系列）**：Gemini-1.5 报告了 POPE，Gemini-2.5 报告了 FACTS-Grounding，但整体仍以 proxy 指标为主。

> 注意：这一结论仅限于"官方公开报告语料"，不能推论为"这些公司未在内部进行幻觉评测"。

### 结论 3：开源社区在纯幻觉 Benchmark 上的披露更充分
明确披露 pure hallucination benchmark 实验结果的模型集中于：
- **InternVL 系列**：InternVL-3（POPE+HallusionBench+MMHal-Bench），InternVL-2.5（HallusionBench+MMHal-Bench）
- **Qwen-VL 系列**：Qwen3-VL（HallusionBench+SimpleVQA）
- **MiniCPM 系列**：HallusionBench+MMHal-Bench
- **GLM 系列（Zhipu AI）**：HallusionBench
- **LLaVA / VILA 系列**：POPE
- **Gemini-1.5**（Google DeepMind）：POPE

### 结论 4：FaithScore 在当前官方语料中无模型正式披露
在全部 83 个模型的官方技术报告、系统卡片和模型卡中，**未发现任何模型将 FaithScore 作为公开实验 benchmark 报告得分**。FaithScore 在部分论文中被提及（value=1），但不在任何模型的主评测表格中出现。

> 这一结论仅针对当前语料，不代表工业界整体未使用 FaithScore。

### 结论 5：CharXiv 是覆盖最广的 Benchmark，但属于 Chart 理解代理指标
CharXiv 在 83 个模型中有 36 个报告了得分，是本次调研中覆盖面最广的 benchmark。但 **CharXiv 测量的是模型对科学图表的理解能力，属于 chart/document proxy benchmark**，不应等价为幻觉率（hallucination rate）。

---

## 三、Pure Hallucination Benchmark vs Proxy Benchmark 区分

| 类型 | 典型代表 | 含义 |
|------|----------|------|
| **Pure Hallucination Benchmark** | POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER、FaithScore、FACTS-Grounding、SimpleVQA | **直接测量**模型输出中的幻觉内容，分数与幻觉率强相关 |
| **Proxy Benchmark（代理指标）** | CharXiv、OCRBench、Video-MME、MMMU、DocVQA、ChartQA、TextVQA、AI2D 等 | **间接**反映模型在特定任务上的能力；高分不等于低幻觉率 |

**避免的误读举例：**
- ❌ "该模型 CharXiv 得分高，因此幻觉率低" → 错误，CharXiv 是图表理解 proxy
- ❌ "OCRBench 得分高，说明幻觉少" → 错误，OCRBench 是 OCR 能力指标
- ❌ "Video-MME 高分代表时序幻觉少" → 不准确，Video-MME 是视频理解能力 benchmark
- ✅ "POPE 分数 85.3（实验表格记录）代表该模型在对象存在性幻觉上的官方披露结果"

---

## 四、最认真披露幻觉 Benchmark 的模型

（按 pure hallucination benchmark 有分数条数排序，仅统计 pure hallucination 口径）

| 排名 | 模型 | 机构 | 披露的 Pure Hal Benchmarks |
|------|------|------|--------------------------|
| 1 | InternVL-3 | 上海 AI Lab | POPE、HallusionBench、MMHal-Bench |
| 2 | Qwen3-VL | 阿里巴巴 | HallusionBench、SimpleVQA |
| 3 | InternVL-2.5 | 上海 AI Lab | HallusionBench、MMHal-Bench |
| 4 | MiniCPM-o | 清华/ModelBest | HallusionBench、MMHal-Bench |
| 5 | InternVL-1.5 | 上海 AI Lab | POPE |

---

## 五、哪些闭源模型仅披露内部/系统卡片评测

| 机构 | 模型系列 | 评测形式 | 是否包含 POPE/CHAIR 等 |
|------|----------|----------|----------------------|
| OpenAI | GPT-4 / GPT-5 系列 | 系统卡片 + 内部安全评测 | 否 |
| Anthropic | Claude-3.5 / Claude-4 系列 | 系统卡片 + 内部安全评测 | 否（POPE 疑为误报） |
| Google DeepMind | Gemini-2.5/3.x 系列 | 技术报告 + 模型卡 | 极少（Gemini-1.5 有 POPE） |

---

## 六、需要避免的误读

1. **误读：原始矩阵中 value=2 即代表"有幻觉评测结果"**
   → 正确理解：81.9% 的 value=2 是代理 benchmark，不是幻觉专项。

2. **误读：CharXiv / OCRBench / Video-MME 是幻觉 benchmark**
   → 这三类是 chart/OCR/video proxy，属于能力指标，不应等价为幻觉测量。

3. **误读：OpenAI/Anthropic 没有做幻觉评测**
   → 应表述为：在其公开官方报告中，未披露 POPE/CHAIR/HallusionBench 等视觉对象幻觉专项 benchmark 的实验分数。

4. **误读：FaithScore 未被工业界采纳**
   → 应表述为：在当前本地官方报告语料（83 个模型）中，未发现 FaithScore 作为正式实验 benchmark 的得分记录。

---

*本报告基于 2026-05-28 前下载的官方技术报告、系统卡片和模型卡，共 99 份文档。*
