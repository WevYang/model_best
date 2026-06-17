# Coverage Gap Report

生成日期：2026-05-29

## 1. 已充分覆盖模型族

本轮已形成 table-level score rows 的模型族：

| model_family | proxy_records | factuality_records | models |
| --- | --- | --- | --- |
| Gemini | 66 | 12 | Gemini 1.5 Flash, Gemini 1.5 Pro, Gemini 2.0 Flash, Gemini 2.0 Flash-Lite, Gemini 2.5 Flash, Gemini 2.5 Pro |
| Gemma | 48 | 8 | Gemma 3 12B, Gemma 3 12B IT, Gemma 3 12B PT, Gemma 3 1B, Gemma 3 27B, Gemma 3 27B IT, Gemma 3 27B PT, Gemma 3 4B, Gemma 3 4B IT, Gemma 3 4B PT |
| OpenAI GPT | 0 | 18 | GPT-4o, GPT-5.5, OpenAI o3, OpenAI o4-mini, gpt-5-main, gpt-5-thinking, gpt-5-thinking-mini, gpt-5-thinking-nano |
| Qwen | 618 | 9 | Qwen2.5-Omni-7B, Qwen2.5-VL-3B, Qwen2.5-VL-72B, Qwen2.5-VL-7B, Qwen3-VL-235B-A22B, Qwen3-VL-2B, Qwen3-VL-30B-A3B, Qwen3-VL-32B, Qwen3-VL-4B, Qwen3-VL-8B, Qwen3.5-Omni-Flash, Qwen3.5-Omni-Plus, Qwen3.5-Plus-Instruct |

## 2. 部分覆盖模型族

以下模型族在本地材料中出现了 benchmark 提及或旧管线候选，但本轮未对所有大表逐格人工复核，因此未把旧自动分数当成 confirmed score。

Excel 额外保留 `Unverified Proxy Candidates` sheet，共 352 条候选线索，用于后续逐表复核；其中 `old_extracted_score_do_not_use` 不能直接引用。

| model | family | missing_expected_benchmark | reason | checked_source | notes |
| --- | --- | --- | --- | --- | --- |
| BLIP-2 | Other | TextVQA, VQAv2, NoCaps, COCO-Cap | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/BLIP-2_2_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Bunny | Bunny | ScienceQA, VQAv2, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Bunny_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Claude-3.5-Haiku-Sonnet | Claude | MathVista, AI2D, DocVQA, ChartQA, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Claude-3.5-Haiku-Sonnet_3.5_system_card.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Claude-3.5 | Claude | MathVista, AI2D, DocVQA, ChartQA, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Claude-3.5_3.5_model_card_addendum.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Claude-4.1 | Claude | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/Claude-4.1_4.1_system_card.pdf |  |
| Claude-4 | Claude | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/Claude-4_4_system_card.pdf |  |
| Claude-Opus-4.7 | Claude | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/Claude-Opus-4.7_4.7_system_card.pdf |  |
| CogVLM | CogVLM | ScienceQA, MathVista, TextVQA, VQAv2, NoCaps, MMVet, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/CogVLM_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| DeepSeek-VL2 | DeepSeek | OCRBench, MMStar, MathVista, AI2D, TextVQA, DocVQA, ChartQA, InfoVQA, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/DeepSeek-VL2_2_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| DeepSeek-VL | DeepSeek | OCRBench, ScienceQA, MathVista, MMVet, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/DeepSeek-VL_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Emu2 | Other | TextVQA, VQAv2, COCO-Cap, MMVet, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Emu2_2_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Emu | Other | VQAv2, NoCaps, COCO-Cap, MMVet | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Emu_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| GPT-4V | Other | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/GPT-4V_4_system_card.pdf |  |
| Gemini-3.1-Pro | Gemini | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/Gemini-3.1-Pro_3.1_model_card.pdf |  |
| Gemini-3.5-Flash | Gemini | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/Gemini-3.5-Flash_3.5_model_card.pdf |  |
| Gemini-Omni-Flash | Gemini | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/Gemini-Omni-Flash_2026_model_card.pdf |  |
| HunyuanImage-3.0 | Other | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/HunyuanImage-3.0_3.0_technical_report.pdf |  |
| Idefics2 | Other | ScienceQA, MathVista, AI2D, TextVQA, DocVQA, ChartQA, InfoVQA, VQAv2, NoCaps, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Idefics2_2_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| InternVL-1.5 | InternVL | OCRBench, ScienceQA, MathVista, AI2D, TextVQA, DocVQA, ChartQA, InfoVQA, VQAv2, COCO-Cap, MMVet, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/InternVL-1.5_1.5_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| InternVL-2.5 | InternVL | OCRBench, Video-MME, ScienceQA, MMStar, MathVista, AI2D, TextVQA, DocVQA, ChartQA, InfoVQA, VQAv2, MMVet | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/InternVL-2.5_2.5_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| InternVL-3 | InternVL | OCRBench, Video-MME, MMStar, MathVista, AI2D, TextVQA, DocVQA, ChartQA, InfoVQA, MMVet, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/InternVL-3_3_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| InternVL | InternVL | AI2D, TextVQA, DocVQA, ChartQA, InfoVQA, VQAv2, NoCaps, COCO-Cap | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/InternVL_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Kimi-VL | Kimi | OCRBench, Video-MME, MMStar, MathVista, AI2D, TextVQA, InfoVQA, MMVet, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Kimi-VL_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Kosmos-1 | Other | VQAv2, COCO-Cap | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Kosmos-1_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Kosmos-2 | Other | VQAv2 | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Kosmos-2_2_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| LLaVA-OneVision-2 | LLaVA | OCRBench, Video-MME, MMStar, AI2D, DocVQA, ChartQA, InfoVQA | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/LLaVA-OneVision-2_2_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| LLaVA-OneVision | LLaVA | OCRBench, Video-MME, ScienceQA, MMStar, MathVista, AI2D, DocVQA, ChartQA, InfoVQA, VQAv2, COCO-Cap, MMVet | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/LLaVA-OneVision_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| LLaVA | LLaVA | ScienceQA | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/LLaVA_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| MiniCPM-Llama3-V | MiniCPM | OCRBench, ScienceQA, MathVista, AI2D, TextVQA, DocVQA, ChartQA, VQAv2, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/MiniCPM-Llama3-V_2.5_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| MiniCPM-V | MiniCPM | OCRBench, ScienceQA, MathVista, AI2D, TextVQA, DocVQA, ChartQA, VQAv2, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/MiniCPM-V_2.6_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| MiniCPM-V | MiniCPM | OCRBench, ScienceQA, MathVista, AI2D, TextVQA, DocVQA, ChartQA, VQAv2, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/MiniCPM-V_4.5_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| MiniCPM-o | MiniCPM | OCRBench, Video-MME, MMStar, MathVista, AI2D, TextVQA, DocVQA, MMVet, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/MiniCPM-o_4.5_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| MiniCPM | MiniCPM | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/MiniCPM_1_technical_report.pdf |  |
| Molmo | Molmo | ScienceQA, MathVista, AI2D, TextVQA, DocVQA, ChartQA, VQAv2, COCO-Cap, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Molmo_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| PaLI-X | Other | AI2D, TextVQA, DocVQA, ChartQA, InfoVQA, VQAv2, NoCaps, COCO-Cap | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/PaLI-X_X_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| PaLI | Other | TextVQA, VQAv2, NoCaps, COCO-Cap | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/PaLI_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| PaLM-E | Other | VQAv2, COCO-Cap | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/PaLM-E_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Pixtral-12B | Pixtral | MathVista, DocVQA, ChartQA, VQAv2, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/Pixtral-12B_12B_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| SEED-LLaMA | Seed | TextVQA, VQAv2, COCO-Cap | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/SEED-LLaMA_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| VILA-1.5 | VILA | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/VILA-1.5_1.5_technical_report.pdf |  |
| VILA | VILA | ScienceQA, TextVQA, DocVQA, VQAv2, MMVet | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/VILA_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| PaliGemma | Gemma | ScienceQA, AI2D, TextVQA, DocVQA, ChartQA, InfoVQA, VQAv2, NoCaps, COCO-Cap | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/model_reports/PaliGemma_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| PaliGemma 2 | Gemma | MMStar, VQAv2, MMVet | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/model_reports/PaliGemma2_2_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Phi-4-multimodal | Phi | OCRBench, Video-MME, ScienceQA, MathVista, AI2D, TextVQA, DocVQA, ChartQA, InfoVQA, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/model_reports/Phi-4-multimodal_4_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| NVLM 1.0 | NVLM | OCRBench, ScienceQA, MathVista, AI2D, TextVQA, DocVQA, ChartQA, VQAv2, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/model_reports/NVLM-1.0_1.0_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| MiMo-VL | MiMo | OCRBench, Video-MME, MathVista, AI2D, DocVQA, ChartQA, InfoVQA, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/model_reports/MiMo-VL_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Ovis2.5 | Ovis | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/model_reports/Ovis2.5_2.5_technical_report.pdf |  |
| Ovis-U1 | Ovis | Video-MME, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/model_reports/Ovis-U1_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| Llama-3.2-Vision | Llama | MathVista, TextVQA, DocVQA, ChartQA, VQAv2, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/official_model_cards_html/Llama-3.2-Vision_model_card.html | Keep as recall candidate; do not use as score until original table is checked. |
| Llama-4 | Llama | MathVista, DocVQA, ChartQA, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/official_model_cards_html/Llama-4_model_card.html | Keep as recall candidate; do not use as score until original table is checked. |
| Gemma-3n | Gemma | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/official_model_cards_html/Gemma-3n_model_card.html |  |
| Gemini-3-Pro | Gemini | MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/official_model_cards_html/Gemini-3-Pro_model_card.html | Keep as recall candidate; do not use as score until original table is checked. |
| Gemini-3.1-Flash-Lite | Gemini | MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/official_model_cards_html/Gemini-3.1-Flash-Lite_model_card.html | Keep as recall candidate; do not use as score until original table is checked. |
| Gemini-3.1-Flash-Audio | Gemini | MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/official_model_cards_html/Gemini-3.1-Flash-Audio_model_card.html | Keep as recall candidate; do not use as score until original table is checked. |
| Gemini-3.1-Flash-Image | Gemini | MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/official_model_cards_html/Gemini-3.1-Flash-Image_model_card.html | Keep as recall candidate; do not use as score until original table is checked. |
| GPT-4.1 | Other | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/official_model_cards_html/GPT-4.1_api_model_doc.html |  |
| Qwen3-Omni | Qwen | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/model_reports/Qwen3-Omni_3_technical_report.pdf |  |
| GLM-4.5V | Other | OCRBench, MMStar, AI2D, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/official_model_cards_html/GLM-4.5V_model_card.html | Keep as recall candidate; do not use as score until original table is checked. |
| HunyuanOCR | Other | OCRBench, DocVQA, ChartQA | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/ocr_document_models/HunyuanOCR_1_technical_report.pdf | Keep as recall candidate; do not use as score until original table is checked. |
| DeepSeek-OCR | DeepSeek | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/ocr_document_models/DeepSeek-OCR_1_model_card.html |  |
| PaddleOCR-VL | Other | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/ocr_document_models/PaddleOCR-VL_1_model_card.html |  |
| MinerU2.5 | Other | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/ocr_document_models/MinerU2.5_2.5_model_card.html |  |
| Claude-Sonnet-4.6 | Claude | MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/official_model_cards_html/Claude-Sonnet-4.6_system_card_page.html | Keep as recall candidate; do not use as score until original table is checked. |
| Claude-Opus-4.6 | Claude | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/official_model_cards_html/Claude-Opus-4.6_system_card_page.html |  |
| Claude-Mythos-Preview | Claude | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/official_model_cards_html/Claude-Mythos-Preview_research_page.html |  |
| GPT-5.2 | Other | factuality/proxy benchmark table | No relevant benchmark score table located in this full pass. | model_best/official_model_cards_html/GPT-5.2_system_card.html |  |
| GLM-4.1V-Thinking | Other | OCRBench, MMStar, AI2D, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/official_model_cards_html/GLM-4.1V-Thinking_model_card.html | Keep as recall candidate; do not use as score until original table is checked. |
| GLM-4.6V | Other | OCRBench, MMStar, AI2D, MMMU | Mentioned or old-pipeline detected; table-level score not verified in this pass. | model_best/official_model_cards_html/GLM-4.6V_model_card.html | Keep as recall candidate; do not use as score until original table is checked. |

## 3. 仍需人工确认

- InternVL / MiniCPM / DeepSeek / LLaVA / Molmo / Pixtral / Kimi / Ovis / NVLM / Phi / VILA / CogVLM / Bunny 等模型族在 manifest 中有大量 proxy benchmark 提及；本轮只将已人工确认或已逐表转录的行作为 score。
- GLM-4.1V / GLM-4.5V / GLM-4.6V 本地 HTML 仍存在内容错配风险：此前 recall pass 已记录多个 GLM HTML 实际指向 GLM-4V-9B 内容。
- 对所有 coverage gap 项，下一步应打开对应 source 表格截图确认列标题、模型行和指标方向后再加入 scorebook。
