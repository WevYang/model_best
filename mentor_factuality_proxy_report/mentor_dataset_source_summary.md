# Benchmark 数据集来源补充说明

## 1. 关键结论

- 不能简单说“幻觉评测都基于 COCO2017”。POPE/CHAIR 与 COCO 关系较强，但 HallusionBench、MMHal-Bench、AMBER、FaithScore、SimpleVQA、FACTS-Grounding 的构造方式各不相同。
- 模型技术报告通常只列 benchmark 分数，不一定列底层 dataset / split / sample size；复现时需要查 benchmark 原论文、官方 release 或 evaluation config。
- POPE 是最需要固定配置的：底层图像集合、object annotation、负样本采样策略都会影响结果。
- Proxy benchmark 要单独解释：OCRBench、DocVQA、ChartQA、Video-MME 等能反映幻觉风险相关能力，但不是 hallucination rate。

## 2. Direct hallucination benchmark 数据来源速览

| benchmark | source dataset | split / size | notes |
| --- | --- | --- | --- |
| POPE | Object-annotated image datasets; original paper evaluates MSCOCO validation and also SEEM-based POPE on MSCOCO / A-OKVQA / GQA. | Implementation-dependent. Original MSCOCO setting randomly selects 500 images with more than 3 annotated objects; random / popular / adversarial negative sampling. / MSCOCO setting: 500 images x 6 yes/no questions per sampling setting; paper appendix also uses 2,000 MSCOCO val images for CHAIR-style analysis. | Only seeing “POPE” in a model report is not enough to know COCO2014 vs COCO2017 vs other source dataset; check evaluation config such as lmms-eval. |
| CHAIR | MSCOCO captions and 80 COCO object annotations; CHAIR itself is a caption-object hallucination metric rather than a fixed dataset. | Depends on caption evaluation protocol; the hallucination paper samples MSCOCO validation images for analysis. / Paper appendix: 2,000 MSCOCO validation images with object annotations and human captions. | The local CHAIR PDF text appears mismatched; COCO/CHAIR details are cross-checked from POPE paper citations and CHAIR metric description. |
| ObjHalBench | Not confirmed in local materials; used by MiniCPM-V 4.5 with CHAIRs/CHAIRi outputs. | 未在本地材料中确认 / 未在本地材料中确认 | MiniCPM report lists ObjHalBench but does not expose the underlying dataset/split in the evaluated table. |
| HallusionBench / HallBench | Curated / human-crafted image-context reasoning benchmark; includes original online images and manually edited images, not a single COCO/OpenImages split. | Fixed benchmark with control pairs; original / edited / no-visual variants. / 346 images, 181 human-edited images, 1,129 questions, 455 visual-question control pairs. | Model reports usually write only HallusionBench/HallBench; the underlying curated data details are in the benchmark paper. |
| MMHal-Bench / MMHal-Score | Images selected from OpenImages validation/test sets; questions cover 12 common object meta-categories from COCO. | Adversarially designed fixed benchmark from OpenImages val/test; 8 question types. / 96 image-question pairs. | Do not confuse MMHal with general MME/MMBench proxy benchmarks. |
| CRPE / CRPE_relation | Relation-comprehension benchmark associated with The All-Seeing Project v2 / general relation comprehension; local model reports cite it but do not include source split details. | 未在本地材料中确认 / 未在本地材料中确认 | Need benchmark paper or official config to confirm source dataset and exact split. |
| AMBER | Images sourced from MS-COCO 2014 test set and Unsplash; annotations cover existence, attribute and relation hallucination. | Fixed AMBER benchmark; no train split for model training. / 1,004 images; 337 objects; prompt/question counts vary by generation/existence/attribute/relation subtask. | Direct hallucination benchmark, but model reports in this project rarely provide official AMBER scores. |
| FaithScore | Two benchmark datasets: LLaVA-1k and MSCOCO-Cap. | LLaVA-1k visual instruction-following questions and MSCOCO validation image captioning prompts. / Paper reports 90 questions per LLaVA-1k question type and 180 annotated samples for human evaluation; full evaluation uses LLaVA-1k and MSCOCO-Cap. | Metric/benchmark source is clear, but exact per-split sample counts should be checked in the original release if reproducing. |

## 3. Factuality / proxy benchmark 数据来源速览

### Factuality / grounding

| benchmark | source dataset | split / size | notes |
| --- | --- | --- | --- |
| FACTS-Grounding | Document-grounded prompts: each example includes user request plus long context document; public examples are from Google DeepMind / Google Research / Kaggle. | Open/public split plus Blind/private held-out split. / 860 public examples and 859 private examples in the original leaderboard description; HuggingFace public card currently lists public examples. | Factuality/grounding-related, not multimodal visual hallucination. Gemini report says SimpleQA results come from repo and FACTS Grounding results from Kaggle. |
| SimpleVQA | Curated multimodal factuality benchmark; human/GPT-assisted image-question-answer collection, fact-checked against authoritative sources such as Wikipedia and Baidu Encyclopedia; includes some Dynamath-derived math Q&A. | Released as test parquet / benchmark set; paper reports final curated set rather than train/val/test split. / 2,025 samples across 9 core tasks, 9 primary domains and 244 image types; filtered from 8,360 initial Q&A pairs. | Factuality-related. Qwen3-VL reports thinking/instruct SimpleVQA scores; do not count as direct hallucination rate. |
| SimpleQA | Human-written short fact-seeking questions with single, indisputable answers; text-only factuality benchmark. | Public benchmark in OpenAI simple-evals; no vision input. / 4,326 questions. | Relevant for factual hallucination, but not multimodal hallucination. |
| LongFact | LLM-generated fact-seeking prompts asking for detailed responses about specific objects or broad concepts. | OpenAI GPT-5 system card uses LongFact-Concepts and LongFact-Objects; underlying split size not stated in local materials. / 未在本地材料中确认 | OpenAI system card describes the prompt source and claim-level grading, but does not provide full dataset source/split in this local copy. |
| FActScore | Questions seeking biographies on notable individuals; responses decomposed into factual claims and checked. | OpenAI GPT-5 system card uses FActScore prompts; local copy does not state exact split size. / 未在本地材料中确认 | Factuality benchmark, not visual hallucination benchmark. |
| HealthBench Hard Hallucinations | Subset of intersection of HealthBench Hard and HealthBench Consensus; challenging health conversations validated by at least two physicians. | HealthBench Hard Hallucinations subset; exact public split size not stated in local GPT-5 system card excerpt. / 未在本地材料中确认 | High-stakes factuality/safety eval; not comparable with POPE/CHAIR/HallusionBench. |

### Proxy

| benchmark | source dataset | split / size | notes |
| --- | --- | --- | --- |
| OCRBench | Aggregates text recognition, scene-text VQA, document-oriented VQA, KIE and HMER sources: IIIT5K, SVT, IC13/IC15, SVTP, CT80, COCOText, CTW, Total-Text, WOST/HOST, WordArt, IAM, ReCTS, ORAND-CAR-2014, ST/NST, STVQA, TextVQA, OCRVQA, ESTVQA, DocVQA, InfoVQA, ChartQA, SROIE, FUNSD, POIE, HME100K. | Manually filtered and corrected benchmark subset across five task groups. / 1,000 QA pairs: Text Recognition 300, Scene Text-centric VQA 200, Document-Oriented VQA 200, KIE 200, HMER 100. | Proxy capability benchmark; strong relevance to OCR-related hallucination risk, but not hallucination rate. |
| OCRBench-v2 | Large-scale bilingual text-centric benchmark across 31 scenarios, including street scene, receipt, formula, diagram and other visual-text settings. | Public benchmark plus private test set. / 10,000 human-verified QA pairs; private test set with 1,500 manually annotated images. | Use official OCRBench-v2 paper rather than local mismatched PDF for source details. |
| TextVQA | Images sampled from OpenImages with text in images. | Official TextVQA splits; model reports usually do not restate split. / OCRBench paper describes 45,000+ questions on 28,000+ images. | Proxy OCR/text benchmark. |
| DocVQA | Document images of diverse types and content. | Official DocVQA split; model reports usually omit details. / OCRBench paper describes 12,767 document images and 50,000+ questions/answers. | Proxy document-understanding benchmark; not direct hallucination rate. |
| ChartQA | Charts with human-written and machine-generated questions. | Official ChartQA split; OCRBench uses ChartQA human and augmented subsets. / OCRBench paper describes 4,804 charts with 9,608 human-written questions plus 23,111 generated questions. | Proxy chart benchmark; can reveal chart-reading hallucination risk but is not a hallucination benchmark. |
| CharXiv | Real-world charts from arXiv preprints, re-rendered from vector assets where possible and manually curated. | 1,000 charts validation; 1,323 charts test; no training set. / 2,323 charts; more than 10K questions; each chart has 4 descriptive questions and 1 reasoning question. | Proxy scientific chart-understanding benchmark. |
| Video-MME | Raw videos sourced from YouTube across 6 domains and 30 fine-grained categories; includes subtitles and audio metadata. | Short / medium / long duration groups; public evaluation protocol. / 900 videos, 744 with subtitles, all 900 with audio, 2,700 multiple-choice QA pairs. | Proxy video understanding benchmark; not direct hallucination rate. |
| LongVideoBench | Web-collected long videos from 119 channels; all videos have English subtitles, platform subtitles or Whisper-generated. | Validation 752 videos / 1,337 MCQs; test 3,011 videos / 5,341 MCQs; labels hidden for test. / 3,763 videos and 6,678 human-annotated multiple-choice QA pairs across 17 fine-grained categories. | Proxy long-video/temporal understanding benchmark. |
| TempCompass | Constructed temporal perception videos, including conflicting videos that share static content but differ in speed, direction, event order or attribute change. | 未在本地材料中确认；official paper/repo should be checked for exact release split. / 未在本地材料中确认 | Proxy temporal benchmark; exact size/split should be checked from official repo before reproduction. |
| MathVista | 28 existing multimodal datasets plus 3 newly created datasets: IQTest, FunctionQA, PaperQA. | testmini 1,000 examples; test 5,141 examples. / 6,141 examples total; 736 newly collected. | Proxy reasoning benchmark; included because the local SimpleVQA PDF is actually MathVista. |
| MMMU | Massive multi-discipline multimodal understanding benchmark for expert AGI; local model reports cite it but do not describe raw dataset source/split. | 未在本地材料中确认 / 未在本地材料中确认 | Proxy expert-reasoning benchmark; not hallucination rate. |
| RefCOCO / RefCOCO+ / RefCOCOg | Referring-expression comprehension datasets built on COCO images with human referring expressions. | Official val/testA/testB style splits depending on dataset; model reports rarely restate split. / 未在本地材料中确认 | Proxy grounding/localization benchmark; not a hallucination rate. |
| ScreenSpot / ScreenSpot-Pro | GUI screenshots across devices/apps for UI element grounding and perception; source details not expanded in local model reports. | Official ScreenSpot / ScreenSpot-Pro split; local model reports do not restate. / 未在本地材料中确认 | Proxy GUI grounding benchmark. |

## 4. 对内部评测的建议

- Direct hallucination：POPE + HallusionBench + MMHal-Bench；如关注 caption 对象幻觉，加 CHAIR/ObjHalBench。
- 关系幻觉：加 CRPE，但需要先确认官方 benchmark release / evaluation config。
- Factuality / grounding：SimpleVQA / FACTS-Grounding / SimpleQA 可以做补充，不要和 POPE/CHAIR 混成同一排名。
- OCR/document/chart 场景：OCRBench + DocVQA + ChartQA + TextVQA；必须明确官方 split 和 OCR prompt。
- Video 场景：Video-MME / LongVideoBench / TempCompass；必须说明是否使用 subtitles/audio、帧采样和 hidden test。
- Grounding/GUI：RefCOCO / ScreenSpot；必须说明 bbox/point 输出格式和 IoU 或点击命中标准。
