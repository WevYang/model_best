#!/usr/bin/env python3
"""
Incremental download & manifest builder for model_best.
Skips files already present. Downloads PDFs from arxiv/official sources,
falls back to HTML/MD for items without official PDFs.
"""
import os, sys, hashlib, json, re, time, datetime, subprocess, io
from pathlib import Path
import requests

BASE = Path(__file__).parent
MANIFEST_PATH = BASE / "_download_manifest.json"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# ── directory layout ──────────────────────────────────────────────────────────
DIRS = {
    "model_reports":           BASE / "model_reports",
    "official_model_cards_html": BASE / "official_model_cards_html",
    "benchmark_papers":        BASE / "benchmark_papers",
    "ocr_document_models":     BASE / "ocr_document_models",
    "repo_snapshots":          BASE / "repo_snapshots",
}
for d in DIRS.values():
    d.mkdir(exist_ok=True)

# ── helpers ───────────────────────────────────────────────────────────────────
def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def is_pdf(data: bytes) -> bool:
    return data[:4] == b"%PDF"

def extract_pdf_title_snippet(path: Path):
    """Extract first-page text via pdfminer. Returns (title_guess, snippet)."""
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(str(path), maxpages=1)
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        title = lines[0] if lines else ""
        snippet = " ".join(lines[:6])[:400]
        return title, snippet
    except Exception as e:
        return "", f"[pdfminer error: {e}]"

def download(url: str, dest: Path, timeout=90, retries=2) -> tuple[bool, str]:
    """Download url → dest. Returns (success, reason)."""
    if dest.exists() and dest.stat().st_size > 0:
        return True, "already_exists"
    for attempt in range(retries + 1):
        try:
            r = SESSION.get(url, timeout=timeout, allow_redirects=True)
            if r.status_code == 200 and len(r.content) > 1000:
                dest.write_bytes(r.content)
                return True, "downloaded"
            elif r.status_code == 404:
                return False, "http_404"
            else:
                time.sleep(3)
        except Exception as e:
            if attempt < retries:
                time.sleep(5)
            else:
                return False, str(e)
    return False, "failed_after_retries"

def build_entry(
    *,
    model_name, version, organization, doc_type, source_type,
    source_url, local_path: Path, modality,
    hallucination_related_benchmarks_mentioned=False,
    notes="", tags=None
) -> dict:
    fetched_at = datetime.datetime.utcnow().isoformat() + "Z"
    exists = local_path.exists()
    file_size = local_path.stat().st_size if exists else 0
    sha = sha256_file(local_path) if exists else ""
    is_pdf_ok = False
    parsed_title = ""
    snippet = ""
    if exists and local_path.suffix.lower() == ".pdf":
        data = local_path.read_bytes()
        is_pdf_ok = is_pdf(data)
        if is_pdf_ok:
            parsed_title, snippet = extract_pdf_title_snippet(local_path)
    return {
        "model_or_benchmark_name": model_name,
        "version": version,
        "organization": organization,
        "doc_type": doc_type,
        "source_type": source_type,
        "source_url": source_url,
        "local_path": str(local_path.relative_to(BASE.parent)),
        "fetched_at": fetched_at,
        "sha256": sha,
        "file_size_bytes": file_size,
        "pdf_header_ok": is_pdf_ok,
        "parsed_title": parsed_title,
        "parsed_first_page_text_snippet": snippet,
        "modality": modality,
        "hallucination_related_benchmarks_mentioned": hallucination_related_benchmarks_mentioned,
        "notes": notes,
    }

# ── load existing manifest ────────────────────────────────────────────────────
manifest: list[dict] = []
if MANIFEST_PATH.exists():
    try:
        manifest = json.loads(MANIFEST_PATH.read_text())
    except Exception:
        manifest = []

existing_paths = {e["local_path"] for e in manifest}

def already_in_manifest(local_path: Path) -> bool:
    rel = str(local_path.relative_to(BASE.parent))
    return rel in existing_paths

def add_entry(entry: dict):
    manifest.append(entry)
    existing_paths.add(entry["local_path"])

def save_manifest():
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"[manifest] Saved {len(manifest)} entries → {MANIFEST_PATH}")

# ── validate existing PDFs already in model_best/ ────────────────────────────
print("\n=== Validating existing PDFs ===")
EXISTING_PDF_META = [
    # (filename, model_name, version, org, doc_type, source_type, source_url, modality)
    ("BLIP-2_2_technical_report.pdf", "BLIP-2", "2", "Salesforce", "technical_report", "arxiv", "https://arxiv.org/abs/2301.12597", "text-image"),
    ("Bunny_1_technical_report.pdf", "Bunny", "1", "BAAI", "technical_report", "arxiv", "https://arxiv.org/abs/2402.11530", "text-image"),
    ("Claude-3.5-Haiku-Sonnet_3.5_system_card.pdf", "Claude-3.5-Haiku-Sonnet", "3.5", "Anthropic", "system_card", "anthropic_system_card", "https://www.anthropic.com/claude/sonnet", "text-image"),
    ("Claude-3.5_3.5_model_card_addendum.pdf", "Claude-3.5", "3.5", "Anthropic", "model_card", "anthropic_system_card", "https://www.anthropic.com/claude/sonnet", "text-image"),
    ("Claude-4.1_4.1_system_card.pdf", "Claude-4.1", "4.1", "Anthropic", "system_card", "anthropic_system_card", "https://www.anthropic.com/index/claude-4-1-system-card", "text-image"),
    ("Claude-4_4_system_card.pdf", "Claude-4", "4", "Anthropic", "system_card", "anthropic_system_card", "https://www.anthropic.com/index/claude-4-system-card", "text-image"),
    ("Claude-Opus-4.7_4.7_system_card.pdf", "Claude-Opus-4.7", "4.7", "Anthropic", "system_card", "anthropic_system_card", "https://www.anthropic.com/index/claude-opus-4-7-system-card", "text-image"),
    ("CogVLM_1_technical_report.pdf", "CogVLM", "1", "Tsinghua/Zhipu", "technical_report", "arxiv", "https://arxiv.org/abs/2311.03079", "text-image"),
    ("DeepSeek-VL2_2_technical_report.pdf", "DeepSeek-VL2", "2", "DeepSeek", "technical_report", "arxiv", "https://arxiv.org/abs/2412.10302", "text-image"),
    ("DeepSeek-VL_1_technical_report.pdf", "DeepSeek-VL", "1", "DeepSeek", "technical_report", "arxiv", "https://arxiv.org/abs/2403.05525", "text-image"),
    ("Emu2_2_technical_report.pdf", "Emu2", "2", "Beijing Academy of AI", "technical_report", "arxiv", "https://arxiv.org/abs/2312.13286", "text-image"),
    ("Emu_1_technical_report.pdf", "Emu", "1", "Beijing Academy of AI", "technical_report", "arxiv", "https://arxiv.org/abs/2307.05222", "text-image"),
    ("GPT-4V_4_system_card.pdf", "GPT-4V", "4", "OpenAI", "system_card", "openai_system_card", "https://openai.com/research/gpt-4v-system-card", "text-image"),
    ("GPT-4_technical_report.pdf", "GPT-4", "4", "OpenAI", "technical_report", "openai_system_card", "https://arxiv.org/abs/2303.08774", "text-image"),
    ("GPT-4o_4o_system_card.pdf", "GPT-4o", "4o", "OpenAI", "system_card", "openai_system_card", "https://openai.com/index/gpt-4o-system-card", "text-image"),
    ("GPT-5.5_5.5_system_card.pdf", "GPT-5.5", "5.5", "OpenAI", "system_card", "openai_system_card", "https://openai.com/index/gpt-5-5-system-card", "text-image"),
    ("GPT-5_5_system_card.pdf", "GPT-5", "5", "OpenAI", "system_card", "openai_system_card", "https://openai.com/index/gpt-5-system-card", "text-image"),
    ("Gemini-1.5_1.5_technical_report.pdf", "Gemini-1.5", "1.5", "Google DeepMind", "technical_report", "official_site", "https://arxiv.org/abs/2403.05530", "text-image-video"),
    ("Gemini-2.0-Flash_2.0_model_card.pdf", "Gemini-2.0-Flash", "2.0", "Google DeepMind", "model_card", "deepmind_model_card", "https://deepmind.google/models/gemini/flash/", "text-image"),
    ("Gemini-2.5-Flash_2.5_model_card.pdf", "Gemini-2.5-Flash", "2.5", "Google DeepMind", "model_card", "deepmind_model_card", "https://deepmind.google/models/gemini/flash/", "text-image-video"),
    ("Gemini-2.5-Pro_2.5_model_card.pdf", "Gemini-2.5-Pro", "2.5", "Google DeepMind", "model_card", "deepmind_model_card", "https://deepmind.google/models/gemini/pro/", "text-image-video"),
    ("Gemini-2.5_2.5_technical_report.pdf", "Gemini-2.5", "2.5", "Google DeepMind", "technical_report", "official_site", "https://arxiv.org/abs/2503.19786", "text-image-video"),
    ("Gemini-3.1-Pro_3.1_model_card.pdf", "Gemini-3.1-Pro", "3.1", "Google DeepMind", "model_card", "deepmind_model_card", "https://deepmind.google/models/gemini/", "text-image-video"),
    ("Gemini-3.5-Flash_3.5_model_card.pdf", "Gemini-3.5-Flash", "3.5", "Google DeepMind", "model_card", "deepmind_model_card", "https://deepmind.google/models/gemini/flash/", "text-image-video"),
    ("Gemini-Omni-Flash_2026_model_card.pdf", "Gemini-Omni-Flash", "2026", "Google DeepMind", "model_card", "deepmind_model_card", "https://deepmind.google/models/gemini/flash/", "omni"),
    ("HunyuanImage-3.0_3.0_technical_report.pdf", "HunyuanImage-3.0", "3.0", "Tencent", "technical_report", "official_site", "https://arxiv.org/abs/2503.17556", "image", ),
    ("Idefics2_2_technical_report.pdf", "Idefics2", "2", "HuggingFace", "technical_report", "arxiv", "https://arxiv.org/abs/2405.02246", "text-image"),
    ("InternVL-1.5_1.5_technical_report.pdf", "InternVL-1.5", "1.5", "Shanghai AI Lab", "technical_report", "arxiv", "https://arxiv.org/abs/2404.16821", "text-image"),
    ("InternVL-2.5_2.5_technical_report.pdf", "InternVL-2.5", "2.5", "Shanghai AI Lab", "technical_report", "arxiv", "https://arxiv.org/abs/2412.05271", "text-image"),
    ("InternVL-3_3_technical_report.pdf", "InternVL-3", "3", "Shanghai AI Lab", "technical_report", "arxiv", "https://arxiv.org/abs/2504.10479", "text-image"),
    ("InternVL_1_technical_report.pdf", "InternVL", "1", "Shanghai AI Lab", "technical_report", "arxiv", "https://arxiv.org/abs/2312.14238", "text-image"),
    ("Kimi-VL_1_technical_report.pdf", "Kimi-VL", "1", "Moonshot AI", "technical_report", "arxiv", "https://arxiv.org/abs/2504.07491", "text-image"),
    ("Kosmos-1_1_technical_report.pdf", "Kosmos-1", "1", "Microsoft", "technical_report", "arxiv", "https://arxiv.org/abs/2302.14045", "text-image"),
    ("Kosmos-2_2_technical_report.pdf", "Kosmos-2", "2", "Microsoft", "technical_report", "arxiv", "https://arxiv.org/abs/2306.14824", "text-image"),
    ("LLaVA-OneVision-2_2_technical_report.pdf", "LLaVA-OneVision-2", "2", "ByteDance/Haotian Liu", "technical_report", "arxiv", "https://arxiv.org/abs/2503.16779", "text-image-video"),
    ("LLaVA-OneVision_1_technical_report.pdf", "LLaVA-OneVision", "1", "ByteDance/Haotian Liu", "technical_report", "arxiv", "https://arxiv.org/abs/2408.03326", "text-image-video"),
    ("LLaVA_1_technical_report.pdf", "LLaVA", "1", "Haotian Liu et al.", "technical_report", "arxiv", "https://arxiv.org/abs/2304.08485", "text-image"),
    ("MiniCPM-Llama3-V_2.5_technical_report.pdf", "MiniCPM-Llama3-V", "2.5", "Tsinghua/ModelBest", "technical_report", "arxiv", "https://arxiv.org/abs/2408.01800", "text-image"),
    ("MiniCPM-V_2.6_technical_report.pdf", "MiniCPM-V", "2.6", "Tsinghua/ModelBest", "technical_report", "arxiv", "https://arxiv.org/abs/2408.01800", "text-image-video"),
    ("MiniCPM-V_4.5_technical_report.pdf", "MiniCPM-V", "4.5", "Tsinghua/ModelBest", "technical_report", "official_site", "https://arxiv.org/abs/2502.13513", "text-image-video"),
    ("MiniCPM-o_4.5_technical_report.pdf", "MiniCPM-o", "4.5", "Tsinghua/ModelBest", "technical_report", "official_site", "https://arxiv.org/abs/2502.13513", "omni"),
    ("MiniCPM_1_technical_report.pdf", "MiniCPM", "1", "Tsinghua/ModelBest", "technical_report", "arxiv", "https://arxiv.org/abs/2404.06395", "text-image"),
    ("Molmo_1_technical_report.pdf", "Molmo", "1", "Allen AI", "technical_report", "arxiv", "https://arxiv.org/abs/2409.17146", "text-image"),
    ("PaLI-X_X_technical_report.pdf", "PaLI-X", "X", "Google", "technical_report", "arxiv", "https://arxiv.org/abs/2305.18565", "text-image"),
    ("PaLI_1_technical_report.pdf", "PaLI", "1", "Google", "technical_report", "arxiv", "https://arxiv.org/abs/2209.06794", "text-image"),
    ("PaLM-E_1_technical_report.pdf", "PaLM-E", "1", "Google", "technical_report", "arxiv", "https://arxiv.org/abs/2303.03378", "text-image"),
    ("Pixtral-12B_12B_technical_report.pdf", "Pixtral-12B", "12B", "Mistral", "technical_report", "arxiv", "https://arxiv.org/abs/2410.07073", "text-image"),
    ("Qwen2.5-VL_2.5_technical_report.pdf", "Qwen2.5-VL", "2.5", "Alibaba", "technical_report", "arxiv", "https://arxiv.org/abs/2502.13923", "text-image-video"),
    ("Qwen3-VL_3_technical_report.pdf", "Qwen3-VL", "3", "Alibaba", "technical_report", "arxiv", "https://arxiv.org/abs/2505.09175", "text-image-video"),
    ("Qwen3.5-Omni_3.5_technical_report.pdf", "Qwen3.5-Omni", "3.5", "Alibaba", "technical_report", "arxiv", "https://arxiv.org/abs/2507.00698", "omni"),
    ("SEED-LLaMA_1_technical_report.pdf", "SEED-LLaMA", "1", "ByteDance", "technical_report", "arxiv", "https://arxiv.org/abs/2310.01218", "text-image"),
    ("VILA-1.5_1.5_technical_report.pdf", "VILA-1.5", "1.5", "NVIDIA", "technical_report", "arxiv", "https://arxiv.org/abs/2412.04468", "text-image-video"),
    ("VILA_1_technical_report.pdf", "VILA", "1", "NVIDIA", "technical_report", "arxiv", "https://arxiv.org/abs/2312.07533", "text-image"),
]

for (fname, model_name, version, org, doc_type, src_type, src_url, modality, *extras) in EXISTING_PDF_META:
    path = BASE / fname
    notes_extra = extras[0] if extras else ""
    if already_in_manifest(path):
        continue
    notes = ""
    if "HunyuanImage" in fname:
        notes = "image_generation model, NOT a VLM; do not include in VLM hallucination matrix"
    elif notes_extra:
        notes = notes_extra
    entry = build_entry(
        model_name=model_name, version=version, organization=org,
        doc_type=doc_type, source_type=src_type, source_url=src_url,
        local_path=path, modality=modality,
        hallucination_related_benchmarks_mentioned=False,
        notes=notes,
    )
    add_entry(entry)
    print(f"  [indexed] {fname}")

save_manifest()

# ── new downloads ─────────────────────────────────────────────────────────────
print("\n=== Downloading new items ===")

def try_pdf(url: str, dest: Path, notes="") -> tuple[bool, str]:
    """Attempt PDF download. Returns (success, actual_url_used)."""
    ok, reason = download(url, dest)
    if ok and dest.exists():
        data = dest.read_bytes()
        if not is_pdf(data):
            dest.unlink()
            return False, ""
    return ok, url if ok else ""

def save_html(url: str, dest: Path) -> tuple[bool, str]:
    """Fetch and save HTML page."""
    if dest.exists() and dest.stat().st_size > 0:
        return True, "already_exists"
    try:
        r = SESSION.get(url, timeout=30, allow_redirects=True)
        if r.status_code == 200:
            dest.write_bytes(r.content)
            return True, url
        return False, f"http_{r.status_code}"
    except Exception as e:
        return False, str(e)

# ─────────────────────────────────────────────
# BENCHMARK PAPERS (arxiv, high confidence)
# ─────────────────────────────────────────────
BENCHMARK_DOWNLOADS = [
    # (arxiv_id, filename, model_name, version, org, modality, hallucination)
    ("1809.02157", "CHAIR_benchmark_paper.pdf",
     "CHAIR", "1", "UC Berkeley", "text-image", True,
     "Object Hallucination in Image Captioning (CHAIR metric)"),
    ("2305.10355", "POPE_benchmark_paper.pdf",
     "POPE", "1", "DAMO Academy", "text-image", True,
     "Polling-based Object Probing Evaluation for hallucination"),
    ("2310.14566", "HallusionBench_benchmark_paper.pdf",
     "HallusionBench", "1", "UMD/UCLA", "text-image", True,
     "Advanced Visual Hallucination Evaluation benchmark"),
    ("2309.14525", "MMHal-Bench_LLaVA-RLHF_benchmark_paper.pdf",
     "MMHal-Bench / LLaVA-RLHF", "1", "ByteDance/Haotian Liu", "text-image", True,
     "Multimodal Hallucination benchmark; LLaVA-RLHF alignment paper"),
    ("2311.07397", "AMBER_benchmark_paper.pdf",
     "AMBER", "1", "Beihang University", "text-image", True,
     "An LLM-free Multi-dimensional Benchmark for hallucination evaluation"),
    ("2311.01477", "FaithScore_benchmark_paper.pdf",
     "FaithScore", "1", "Various", "text-image", True,
     "Fine-grained faithfulness evaluation for VLMs"),
    ("2305.07895", "OCRBench_benchmark_paper.pdf",
     "OCRBench", "1", "Shanghai AI Lab", "document", False,
     "OCRBench: On the Hidden Mystery of OCR in Large Multimodal Models"),
    ("2404.00773", "OCRBench-v2_benchmark_paper.pdf",
     "OCRBench-v2", "2", "Shanghai AI Lab", "document", False,
     "OCRBench v2 extended evaluation"),
    ("2406.19523", "FACTS-Grounding_benchmark_paper.pdf",
     "FACTS Grounding", "1", "Google DeepMind", "text-image", True,
     "FACTS Grounding: Benchmark for grounded factual generation"),
    ("2406.18521", "CharXiv_benchmark_paper.pdf",
     "CharXiv", "1", "Princeton NLP", "text-image", False,
     "Charting Territories: A Benchmark for Chart Understanding"),
    ("2405.21075", "Video-MME_benchmark_paper.pdf",
     "Video-MME", "1", "Various", "video", False,
     "Video-MME: The First-Ever Comprehensive Evaluation Benchmark of Multi-modal LLMs in Video"),
    ("2407.15754", "LongVideoBench_benchmark_paper.pdf",
     "LongVideoBench", "1", "Various", "video", False,
     "LongVideoBench: A Benchmark for Long-context Interleaved Video-Language Understanding"),
    ("2406.09436", "TempCompass_benchmark_paper.pdf",
     "TempCompass", "1", "Peking University", "video", False,
     "TempCompass: Do Video LLMs Really Understand Videos?"),
    ("2310.02255", "SimpleVQA_benchmark_paper.pdf",
     "SimpleVQA", "1", "Various", "text-image", True,
     "Evaluating hallucination in VQA"),
]

for (arxiv_id, fname, model_name, version, org, modality, halluc, notes) in BENCHMARK_DOWNLOADS:
    dest = DIRS["benchmark_papers"] / fname
    if already_in_manifest(dest):
        print(f"  [skip] {fname} already in manifest")
        continue
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    ok, used_url = try_pdf(url, dest)
    if ok:
        print(f"  [OK-pdf] {fname}")
    else:
        # try abs page as HTML fallback
        html_dest = DIRS["benchmark_papers"] / fname.replace(".pdf", ".html")
        ok2, _ = save_html(f"https://arxiv.org/abs/{arxiv_id}", html_dest)
        if ok2:
            dest = html_dest
            used_url = f"https://arxiv.org/abs/{arxiv_id}"
            print(f"  [OK-html-fallback] {fname}")
        else:
            print(f"  [FAIL] {fname}")
    entry = build_entry(
        model_name=model_name, version=version, organization=org,
        doc_type="benchmark_paper", source_type="arxiv",
        source_url=f"https://arxiv.org/abs/{arxiv_id}",
        local_path=dest, modality=modality,
        hallucination_related_benchmarks_mentioned=halluc,
        notes=notes,
    )
    add_entry(entry)

save_manifest()

# ─────────────────────────────────────────────
# NEW MODEL REPORTS
# ─────────────────────────────────────────────
MODEL_ARXIV_DOWNLOADS = [
    # (arxiv_id, filename, model_name, version, org, doc_type, modality, notes)
    ("2407.07726", "model_reports/PaliGemma_1_technical_report.pdf",
     "PaliGemma", "1", "Google DeepMind", "technical_report", "text-image",
     "PaliGemma: A versatile 3B VLM for transfer"),
    ("2412.10758", "model_reports/PaliGemma2_2_technical_report.pdf",
     "PaliGemma 2", "2", "Google DeepMind", "technical_report", "text-image",
     "PaliGemma 2: A Family of Versatile VLMs for Transfer"),
    ("2503.19786", "model_reports/Gemma3_3_technical_report.pdf",
     "Gemma 3", "3", "Google DeepMind", "technical_report", "text-image",
     "Gemma 3 technical report"),
    ("2503.20215", "model_reports/Qwen2.5-Omni_2.5_technical_report.pdf",
     "Qwen2.5-Omni", "2.5", "Alibaba", "technical_report", "omni",
     "Qwen2.5-Omni: Think with Eyes, Ears, and Voice"),
    ("2503.01743", "model_reports/Phi-4-multimodal_4_technical_report.pdf",
     "Phi-4-multimodal", "4", "Microsoft", "technical_report", "text-image",
     "Phi-4 multimodal technical report"),
    ("2409.11402", "model_reports/NVLM-1.0_1.0_technical_report.pdf",
     "NVLM 1.0", "1.0", "NVIDIA", "technical_report", "text-image",
     "NVLM: Open Frontier-Class Multimodal LLMs"),
    ("2506.03569", "model_reports/MiMo-VL_1_technical_report.pdf",
     "MiMo-VL", "1", "Xiaomi", "technical_report", "text-image",
     "MiMo-VL: Multimodal Reasoning Model from Xiaomi"),
    ("2505.05568", "model_reports/Ovis2.5_2.5_technical_report.pdf",
     "Ovis2.5", "2.5", "Alibaba/DAMO", "technical_report", "text-image",
     "Ovis2.5 VLM technical report"),
    ("2506.07971", "model_reports/Ovis-U1_1_technical_report.pdf",
     "Ovis-U1", "1", "Alibaba/DAMO", "technical_report", "text-image",
     "Ovis-U1 unified VLM technical report"),
]

for (arxiv_id, rel_path, model_name, version, org, doc_type, modality, notes) in MODEL_ARXIV_DOWNLOADS:
    dest = BASE / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if already_in_manifest(dest):
        print(f"  [skip] {rel_path} already in manifest")
        continue
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    ok, _ = try_pdf(url, dest)
    used_url = f"https://arxiv.org/abs/{arxiv_id}"
    if not ok:
        # HTML fallback
        html_dest = Path(str(dest).replace(".pdf", ".html"))
        ok2, _ = save_html(f"https://arxiv.org/abs/{arxiv_id}", html_dest)
        dest = html_dest if ok2 else dest
        print(f"  [{'OK-html' if ok2 else 'FAIL'}] {rel_path}")
    else:
        print(f"  [OK-pdf] {rel_path}")
    entry = build_entry(
        model_name=model_name, version=version, organization=org,
        doc_type=doc_type, source_type="arxiv",
        source_url=used_url, local_path=dest, modality=modality,
        notes=notes,
    )
    add_entry(entry)

save_manifest()

# ─────────────────────────────────────────────
# LLAMA MODELS — HuggingFace model cards (HTML)
# ─────────────────────────────────────────────
HF_MODEL_CARDS = [
    ("Llama-3.2-Vision", "3.2", "Meta", "text-image",
     "https://huggingface.co/meta-llama/Llama-3.2-11B-Vision",
     "official_model_cards_html/Llama-3.2-Vision_model_card.html",
     "No standalone technical report PDF; official model card on HuggingFace"),
    ("Llama-4", "4", "Meta", "text-image-video",
     "https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E",
     "official_model_cards_html/Llama-4_model_card.html",
     "No standalone technical report PDF; official model card on HuggingFace"),
    ("Gemma-3n", "3n", "Google DeepMind", "text-image",
     "https://huggingface.co/google/gemma-3n-E4B-it",
     "official_model_cards_html/Gemma-3n_model_card.html",
     "Gemma 3n nano model; model card on HuggingFace"),
    ("Gemini-3-Pro", "3", "Google DeepMind", "text-image-video",
     "https://deepmind.google/models/gemini/",
     "official_model_cards_html/Gemini-3-Pro_model_card.html",
     "Gemini 3 Pro model page; HTML saved as no separate PDF available yet"),
    ("Gemini-3.1-Flash-Lite", "3.1", "Google DeepMind", "text-image-video",
     "https://deepmind.google/models/gemini/flash/",
     "official_model_cards_html/Gemini-3.1-Flash-Lite_model_card.html",
     "Gemini 3.1 Flash-Lite variant; HTML model page"),
    ("Gemini-3.1-Flash-Audio", "3.1", "Google DeepMind", "audio",
     "https://deepmind.google/models/gemini/flash/",
     "official_model_cards_html/Gemini-3.1-Flash-Audio_model_card.html",
     "Gemini 3.1 Flash Audio variant; HTML model page"),
    ("Gemini-3.1-Flash-Image", "3.1", "Google DeepMind", "text-image",
     "https://deepmind.google/models/gemini/flash/",
     "official_model_cards_html/Gemini-3.1-Flash-Image_model_card.html",
     "Gemini 3.1 Flash Image variant; HTML model page"),
]

for (model_name, version, org, modality, url, rel_path, notes) in HF_MODEL_CARDS:
    dest = BASE / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if already_in_manifest(dest):
        print(f"  [skip] {rel_path}")
        continue
    ok, _ = save_html(url, dest)
    print(f"  [{'OK-html' if ok else 'FAIL'}] {rel_path}")
    entry = build_entry(
        model_name=model_name, version=version, organization=org,
        doc_type="official_model_card" if "model_card" in rel_path else "official_html",
        source_type="huggingface_official" if "huggingface" in url else "deepmind_model_card",
        source_url=url, local_path=dest, modality=modality,
        notes=notes + "; 无可验证官方 PDF",
    )
    add_entry(entry)

save_manifest()

# ─────────────────────────────────────────────
# ANTHROPIC SYSTEM CARDS — try CDN patterns
# ─────────────────────────────────────────────
ANTHROPIC_CARDS = [
    # (filename, model_name, version, url_to_try_first, notes)
    ("model_reports/Claude-Sonnet-4.6_4.6_system_card.pdf",
     "Claude-Sonnet-4.6", "4.6",
     "https://www.anthropic.com/index/claude-sonnet-4-6-system-card",
     "Claude Sonnet 4.6 system card; this model is claude-sonnet-4-6"),
    ("model_reports/Claude-Opus-4.6_4.6_system_card.pdf",
     "Claude-Opus-4.6", "4.6",
     "https://www.anthropic.com/index/claude-opus-4-6-system-card",
     "Claude Opus 4.6 system card"),
    ("model_reports/Claude-Mythos-Preview_1_system_card.pdf",
     "Claude-Mythos-Preview", "preview",
     "https://www.anthropic.com/index/claude-mythos-system-card",
     "Claude Mythos Preview system card; verify if model is publicly available"),
]

ANTHROPIC_HTML_FALLBACKS = [
    "https://www.anthropic.com/claude",
    "https://www.anthropic.com/model-card",
    "https://docs.anthropic.com/",
]

for (rel_path, model_name, version, primary_url, notes) in ANTHROPIC_CARDS:
    dest = BASE / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if already_in_manifest(dest):
        print(f"  [skip] {rel_path}")
        continue
    # Try PDF from primary URL
    ok, _ = try_pdf(primary_url, dest)
    used_url = primary_url
    if ok:
        print(f"  [OK-pdf] {rel_path}")
        entry = build_entry(
            model_name=model_name, version=version, organization="Anthropic",
            doc_type="system_card", source_type="anthropic_system_card",
            source_url=used_url, local_path=dest, modality="text-image",
            notes=notes,
        )
    else:
        # Save HTML fallback
        html_dest = Path(str(dest).replace(".pdf", ".html"))
        ok2, _ = save_html(primary_url, html_dest)
        dest_final = html_dest if ok2 else dest
        print(f"  [{'OK-html' if ok2 else 'FAIL-no-official-doc'}] {rel_path}")
        entry = build_entry(
            model_name=model_name, version=version, organization="Anthropic",
            doc_type="official_html", source_type="anthropic_system_card",
            source_url=used_url, local_path=dest_final, modality="text-image",
            notes=notes + "; 无可验证官方 PDF — saved HTML fallback",
        )
        dest = dest_final
    add_entry(entry)

save_manifest()

# ─────────────────────────────────────────────
# GPT-4.1 — no official PDF, save API docs HTML
# ─────────────────────────────────────────────
GPT41_ITEMS = [
    ("official_model_cards_html/GPT-4.1_api_model_doc.html",
     "GPT-4.1", "4.1", "OpenAI",
     "https://platform.openai.com/docs/models/gpt-4.1",
     "No official PDF; saving OpenAI API model doc page as HTML; 无可验证官方 PDF"),
    ("official_model_cards_html/GPT-5.2_system_card.html",
     "GPT-5.2", "5.2", "OpenAI",
     "https://openai.com/index/gpt-5-2-system-card",
     "GPT-5.2 system card update page; saved as HTML; verify if separate PDF exists"),
    ("official_model_cards_html/GPT-5.5-Instant_system_card.html",
     "GPT-5.5-Instant", "5.5-Instant", "OpenAI",
     "https://openai.com/index/gpt-5-5-instant-system-card",
     "GPT-5.5 Instant system card; saved as HTML; check openai.com for official PDF"),
]

for (rel_path, model_name, version, org, url, notes) in GPT41_ITEMS:
    dest = BASE / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if already_in_manifest(dest):
        print(f"  [skip] {rel_path}")
        continue
    ok, _ = save_html(url, dest)
    print(f"  [{'OK-html' if ok else 'FAIL'}] {rel_path}")
    entry = build_entry(
        model_name=model_name, version=version, organization=org,
        doc_type="official_html", source_type="openai_system_card",
        source_url=url, local_path=dest, modality="text-image",
        notes=notes,
    )
    add_entry(entry)

save_manifest()

# ─────────────────────────────────────────────
# QWEN ADDITIONAL — Qwen3-Omni, Qwen3.6/3.7
# ─────────────────────────────────────────────
QWEN_EXTRA = [
    # Try arxiv first; Qwen3-Omni
    ("2507.05261", "model_reports/Qwen3-Omni_3_technical_report.pdf",
     "Qwen3-Omni", "3", "Alibaba", "omni",
     "Qwen3-Omni technical report; may be on arxiv or HuggingFace"),
    # Qwen3 main report covers 3.x; no confirmed 3.6 or 3.7 as of known releases
]

for (arxiv_id, rel_path, model_name, version, org, modality, notes) in QWEN_EXTRA:
    dest = BASE / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if already_in_manifest(dest):
        continue
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    ok, _ = try_pdf(url, dest)
    if not ok:
        # Try HF model card as HTML
        hf_url = f"https://huggingface.co/Qwen/{model_name}"
        html_dest = Path(str(dest).replace(".pdf", ".html"))
        ok2, _ = save_html(hf_url, html_dest)
        dest = html_dest if ok2 else dest
        print(f"  [{'OK-html' if ok2 else 'FAIL'}] {rel_path}")
    else:
        print(f"  [OK-pdf] {rel_path}")
    entry = build_entry(
        model_name=model_name, version=version, organization=org,
        doc_type="technical_report" if ok else "official_html",
        source_type="arxiv",
        source_url=f"https://arxiv.org/abs/{arxiv_id}",
        local_path=dest, modality=modality, notes=notes,
    )
    add_entry(entry)

# Qwen3.6 / Qwen3.7 — not confirmed as official releases; save HF page as HTML
for (model_tag, hf_name) in [("Qwen3.6", "Qwen3.6"), ("Qwen3.7", "Qwen3.7")]:
    rel_path = f"official_model_cards_html/{model_tag}_model_card.html"
    dest = BASE / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if already_in_manifest(dest):
        continue
    hf_url = f"https://huggingface.co/Qwen/{hf_name}"
    ok, _ = save_html(hf_url, dest)
    print(f"  [{'OK-html' if ok else 'FAIL-not-found'}] {rel_path} — note: {model_tag} may not be an official Qwen release version")
    entry = build_entry(
        model_name=model_tag, version=model_tag.replace("Qwen",""),
        organization="Alibaba",
        doc_type="official_model_card",
        source_type="huggingface_official",
        source_url=hf_url,
        local_path=dest, modality="text-image",
        notes=f"{model_tag}: not confirmed as official Qwen release version as of Aug 2025 knowledge cutoff; verify on Qwen GitHub/HuggingFace",
    )
    add_entry(entry)

save_manifest()

# ─────────────────────────────────────────────
# GLM VLM MODELS — GitHub repo snapshots
# ─────────────────────────────────────────────
GLM_MODELS = [
    ("GLM-4.1V-Thinking", "4.1V-Thinking", "Zhipu AI",
     "https://huggingface.co/THUDM/GLM-4.1V-Thinking",
     "official_model_cards_html/GLM-4.1V-Thinking_model_card.html",
     "text-image", "GLM-4.1V-Thinking VLM; reasoning-focused model"),
    ("GLM-4.5V", "4.5V", "Zhipu AI",
     "https://huggingface.co/THUDM/glm-4v-9b",
     "official_model_cards_html/GLM-4.5V_model_card.html",
     "text-image", "GLM-4.5V model card on HuggingFace"),
    ("GLM-4.6V", "4.6V", "Zhipu AI",
     "https://huggingface.co/THUDM/GLM-4V-Plus",
     "official_model_cards_html/GLM-4.6V_model_card.html",
     "text-image", "GLM-4.6V model card on HuggingFace; verify exact version naming"),
]

for (model_name, version, org, url, rel_path, modality, notes) in GLM_MODELS:
    dest = BASE / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if already_in_manifest(dest):
        continue
    ok, _ = save_html(url, dest)
    print(f"  [{'OK-html' if ok else 'FAIL'}] {rel_path}")
    entry = build_entry(
        model_name=model_name, version=version, organization=org,
        doc_type="official_model_card", source_type="huggingface_official",
        source_url=url, local_path=dest, modality=modality,
        notes=notes + "; 无可验证官方 PDF",
    )
    add_entry(entry)

save_manifest()

# ─────────────────────────────────────────────
# OCR / DOCUMENT MODELS — arxiv + HTML
# ─────────────────────────────────────────────
OCR_MODELS = [
    # (arxiv_id_or_none, filename, model_name, version, org, url, notes)
    ("2409.01704", "ocr_document_models/HunyuanOCR_1_technical_report.pdf",
     "HunyuanOCR", "1", "Tencent",
     "https://arxiv.org/abs/2409.01704",
     "HunyuanOCR document understanding model"),
    (None, "ocr_document_models/DeepSeek-OCR_1_model_card.html",
     "DeepSeek-OCR", "1", "DeepSeek",
     "https://huggingface.co/deepseek-ai/DeepSeek-VL2",
     "DeepSeek OCR capability; no separate technical report PDF confirmed; 无可验证官方 PDF"),
    (None, "ocr_document_models/PaddleOCR-VL_1_model_card.html",
     "PaddleOCR-VL", "1", "Baidu/PaddlePaddle",
     "https://github.com/PaddlePaddle/PaddleOCR",
     "PaddleOCR-VL repository; no standalone technical report PDF; 无可验证官方 PDF"),
    (None, "ocr_document_models/MinerU2.5_2.5_model_card.html",
     "MinerU2.5", "2.5", "Shanghai AI Lab",
     "https://github.com/opendatalab/MinerU",
     "MinerU document parsing tool; no standalone arXiv paper for v2.5; 无可验证官方 PDF"),
]

for (arxiv_id, rel_path, model_name, version, org, src_url, notes) in OCR_MODELS:
    dest = BASE / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if already_in_manifest(dest):
        continue
    ok = False
    if arxiv_id and rel_path.endswith(".pdf"):
        url = f"https://arxiv.org/pdf/{arxiv_id}"
        ok, _ = try_pdf(url, dest)
    if not ok:
        html_dest = Path(str(dest).replace(".pdf", ".html")) if rel_path.endswith(".pdf") else dest
        ok2, _ = save_html(src_url, html_dest)
        dest = html_dest
        ok = ok2
    print(f"  [{'OK' if ok else 'FAIL'}] {rel_path}")
    doc_type = "technical_report" if arxiv_id and ok and dest.suffix == ".pdf" else "official_html"
    src_type = "arxiv" if arxiv_id else "github_official"
    entry = build_entry(
        model_name=model_name, version=version, organization=org,
        doc_type=doc_type, source_type=src_type,
        source_url=src_url, local_path=dest, modality="document",
        notes=notes,
    )
    add_entry(entry)

save_manifest()

# ─────────────────────────────────────────────
# FINAL SUMMARY
# ─────────────────────────────────────────────
print(f"\n=== Done. Total manifest entries: {len(manifest)} ===")
save_manifest()
print(f"Manifest: {MANIFEST_PATH}")

# Print breakdown by doc_type
from collections import Counter
counts = Counter(e["doc_type"] for e in manifest)
for k, v in sorted(counts.items()):
    print(f"  {k}: {v}")
