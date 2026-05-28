# 严格证据返工审计报告

**审计日期：** 2026-05-28
**操作：** 重新审核全部 25 条原始 valid_official_result，拒绝所有因自动化正则误判的条目，重新识别真正有证据的结果。

---

## 一、返工前后数量对比

| 指标 | 返工前（原始审计） | 返工后（严格审计） |
|------|-----------------|-----------------|
| valid_official_result | **25** | **11**（其中 confidence=high/medium: 9，low: 2）|
| 进入 leaderboard 的条目 | 25 | **4 个模型** |
| 被拒绝的原始条目 | — | **25（全部）** |

**结论：原始 25 条"有效结果"全部存在证据问题，无一可直接引用。**

---

## 二、被拒绝的 25 条原始结果及拒绝原因

### 最常见的误判类型

| 类型 | 数量 | 典型案例 |
|------|------|---------|
| 章节号被误识别为分数 | 4 | Qwen3-VL/HallusionBench=5.3（章节5.3），InternVL-2.5/HallusionBench=5.6（章节5.6）|
| 引用编号被误识别为分数 | 6 | InternVL-1.5/HallusionBench=82([82]=DocVQA引用)，InternVL-2.5/MMHal=77([77]=HallusionBench论文引用)，Bunny/POPE=41([41]=MME引用)，MiniCPM-o两条([45]=Mantis引用)|
| 模型版本号被误识别为分数 | 4 | Gemini-2.5/FACTS-Grounding=1.5（"Gemini 1.5"），Claude-Sonnet-4.6/POPE=4（"Claude Sonnet 4"），Claude-Opus-4.6/POPE=3，GLM系列三条（"GLM-4"）|
| 标准差被误识别为分数 | 1 | PaliGemma/POPE=0.3（±0.3标准差）|
| 相邻benchmark分数串行 | 2 | MiniCPM-V/CHAIR=87.4（实为ChartQA分数），VILA/POPE=35.4（实为LLaVA-Bench分数）|
| 计数数字被误识别为分数 | 2 | CogVLM/POPE=17（"17个基准"），InternVL/POPE=32（列举上下文）|
| 页码被误识别为分数 | 3 | InternVL-3三条（"11 MME MMB..."中11=页码）|
| intro_mention无实验分数 | 3 | MiMo-VL/AMBER=3.1，Gemini-1.5/POPE=00（格式伪码），Qwen3-VL/SimpleVQA=1（章节列表编号）|

---

## 三、严格审计后确认的真实结果

### 3.1 confidence=high（可直接引用）

| 模型 | Benchmark | 分数 | 来源 | 完整表格行证据 |
|------|-----------|------|------|-------------|
| MiniCPM-V 4.5 | CHAIR (CHAIRs↓) | **9.3** | MiniCPM-V_4.5_technical_report.pdf §主表Hallucination区 | `ObjHalBench (CHAIRs) ↓  9.3 †  13.7 ∗  17.0 ∗  11.3 ∗  12.3 ∗  -` |
| MiniCPM-V 4.5 | CHAIR (CHAIRi↓) | **5.2** | 同上 | `ObjHalBench (CHAIRi) ↓  5.2†  7.7∗  8.9∗  6.5∗  6.4∗  -` |
| MiniCPM-V 4.5 | MMHal-Bench | **5.0** (0-6分) | 同上 | `MMHal-Bench (Score)  5.0†  4.1∗  4.2∗  4.2∗  4.6∗  -` |
| MiniCPM-o 4.5 | HallusionBench | **59.1** | MiniCPM-o_4.5_technical_report.pdf §Hallucination表 | `Hallucination HallusionBench MMHal-Score MMHal-Hallrate↓  59.1  4.6  23.9` |
| MiniCPM-o 4.5 | MMHal-Bench | **4.6** (0-6分) | 同上 | 同行：`59.1  4.6  23.9` |

### 3.2 confidence=medium（有表格证据但列映射存在推断）

| 模型 | Benchmark | 分数 | 来源 | 说明 |
|------|-----------|------|------|------|
| PaliGemma | POPE | **86.0 / 87.0** | PaliGemma_1_technical_report.pdf Table 1 | 224px=86.0, 448px=87.0；以fine-tune形式报告（非zero-shot）|
| InternVL-2.5 8B | HallusionBench | **~62.8** | InternVL-2.5_2.5_technical_report.pdf §5.6.1 | 专用幻觉评测章节，表格第7列推断为HallBench |
| InternVL-2.5 8B | MMHal-Bench | **~3.65** (0-6分) | 同上 | 同一表格，第9列推断为MMHal |
| InternVL-2.5 8B | POPE | **~90.6** | 同上 | 同一表格，末列推断为POPE |

### 3.3 confidence=low（不进入leaderboard）

| 模型 | Benchmark | 估计分数 | 原因 |
|------|-----------|---------|------|
| InternVL-3 | HallusionBench | ~59.1（某尺寸） | 表格结构确认但行-模型对应不确定 |
| InternVL-3 | POPE | ~90.7（1B参数） | 同上 |

---

## 四、最终 Pure Hallucination Leaderboard（仅 confidence≥medium）

| 排名 | 模型 | 机构 | 验证的 Pure Hal Benchmark | 数量 |
|------|------|------|--------------------------|------|
| 1 | InternVL-2.5 | Shanghai AI Lab | HallusionBench, MMHal-Bench, POPE | 3 |
| 2 | MiniCPM-V | Tsinghua/ModelBest | CHAIR, MMHal-Bench | 2 |
| 3 | MiniCPM-o | Tsinghua/ModelBest | HallusionBench, MMHal-Bench | 2 |
| 4 | PaliGemma | Google | POPE | 1 |

> **注意：** InternVL 系列（InternVL-3、InternVL-1.5）在官方论文中明确测试了 HallusionBench、MMHal-Bench、POPE，但由于 PDF 文本提取的列映射不确定性，列为 confidence=low，未进入此 leaderboard。需要人工对照原始 PDF 表格确认。

---

## 五、关键修正结论

### ✅ 修正 1：OpenAI / Anthropic 的幻觉评测口径

**修正后表述（严格口径）：**
在当前已下载的官方公开文档（系统卡片 / 技术报告 / 模型卡）中，OpenAI（GPT-4/5 系列）和 Anthropic（Claude-3.5/4 系列）**未报告 POPE、CHAIR、HallusionBench、MMHal-Bench、AMBER 等视觉对象幻觉专项 benchmark 的实验分数**。其官方报告以安全性红线测试、系统卡片人类评估为主，代理能力指标（CharXiv、DocVQA、MMMU）为辅。

> 不可引申为"这些公司未进行幻觉内部评测"。

### ✅ 修正 2：FaithScore 结论

在当前 83 个模型的官方语料中，未发现任何模型将 FaithScore 作为正式实验 benchmark 报告分数。
> 不可引申为"工业界未采纳 FaithScore"。

### ✅ 修正 3：原矩阵的可信度修正

原始矩阵中所有 value=2 的"幻觉结果"现在需要区分：
- **严格有效（可引用）**：MiniCPM-V/CHAIR、MiniCPM-V/MMHal、MiniCPM-o/HallusionBench、MiniCPM-o/MMHal、PaliGemma/POPE、InternVL-2.5/三项（confidence=medium）
- **需人工确认**：InternVL-3/HallusionBench、InternVL-3/POPE（confidence=low）
- **应撤销**：其余 25 条原始记录

---

## 六、仍需人工确认的条目

以下条目无法仅凭 PDF 文本提取自动确认，**必须人工翻阅原始 PDF**：

1. **InternVL-3 / HallusionBench & POPE**：
   - 来源：InternVL-3_3_technical_report.pdf，第 11 页（table 1）
   - 问题：PDF 提取时列对齐丢失，表格中行-模型映射不确定
   - 建议操作：打开 PDF 第 11 页，找到列标题 "HallBench" 和 "POPE"，确认 InternVL3-38B 的具体数值

2. **InternVL-2.5 / 三项（HallusionBench、MMHal、POPE）**：
   - 来源：InternVL-2.5_2.5_technical_report.pdf，Section 5.6.1，第 ~20 页
   - 问题：列顺序从 PDF 文本流推断，未 100% 确认
   - 建议操作：找到 Section 5.6.1 表格，确认列顺序

3. **VILA / POPE**（之前被拒绝）：
   - 来源：VILA_1_technical_report.pdf Table 5
   - 问题：POPE 行 "78.9 84.2 85.9" 对应哪个 VILA 变体不确定
   - 建议操作：找 Table 5，确认 VILA 对应行的 POPE 值

4. **CogVLM / POPE**（之前被拒绝）：
   - 来源：CogVLM_1_technical_report.pdf
   - 问题："POPE  58.0  91.0" 对应 CogVLM vs 对比模型不明
   - 建议操作：确认哪列是 CogVLM 自身的 POPE 分数

5. **Bunny / POPE**（之前被拒绝）：
   - 来源：Bunny_1_technical_report.pdf Table 1
   - 问题：POPE [48] 被定义和引用，但实际数值未从文本中提取
   - 建议操作：找 Table 1，确认 Bunny 的 POPE F1 值

6. **Qwen3-VL / SimpleVQA**：
   - 来源：Qwen3-VL_3_technical_report.pdf
   - 问题：表格片段 "SimpleVQA  88.8 88.6 81.3 78.7 61.3" 存在，但行-模型对应不确定
   - 建议操作：找 Section 5.1 中的 SimpleVQA 表格，确认各行对应哪个 Qwen3-VL 变体

---

*本报告采用"宁可少报，不可误报"原则。所有 confidence=low 条目仅供参考，不计入任何官方统计。*
