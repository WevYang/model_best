#!/usr/bin/env python3
"""Second-pass: fix bad manifest entries, save HTML fallbacks, run PDF text extraction."""
import os, hashlib, json, datetime
from pathlib import Path
import requests

BASE = Path(__file__).parent
MANIFEST_PATH = BASE / "_download_manifest.json"
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}

manifest = json.loads(MANIFEST_PATH.read_text())

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def extract_pdf_text(path: Path):
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(str(path), maxpages=1)
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return lines[0] if lines else "", " ".join(lines[:6])[:400]
    except Exception as e:
        return "", f"[pdfminer error: {e}]"

def save_html(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        return True
    try:
        r = requests.get(url, timeout=30, headers=HEADERS, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 500:
            dest.write_bytes(r.content)
            return True
        return False
    except Exception:
        return False

# ── 1. Fix zero-byte / bad PDF entries → save HTML fallback ──────────────────
ANTHROPIC_FALLBACKS = [
    ("Claude-Sonnet-4.6",    "4.6",     "https://www.anthropic.com/news/claude-sonnet-4-6",
     "official_model_cards_html/Claude-Sonnet-4.6_system_card_page.html"),
    ("Claude-Opus-4.6",      "4.6",     "https://www.anthropic.com/news/claude-opus-4-6",
     "official_model_cards_html/Claude-Opus-4.6_system_card_page.html"),
    ("Claude-Mythos-Preview","preview", "https://www.anthropic.com/research",
     "official_model_cards_html/Claude-Mythos-Preview_research_page.html"),
]

for model_name, version, url, rel_path in ANTHROPIC_FALLBACKS:
    dest = BASE / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    ok = save_html(url, dest)
    print(f"  [{'OK' if ok else 'FAIL'}] {rel_path}")

    # Update the manifest: remove the bad 0-byte entry, add correct HTML entry
    manifest = [e for e in manifest if e["model_or_benchmark_name"] != model_name]
    fetched = datetime.datetime.utcnow().isoformat() + "Z"
    file_size = dest.stat().st_size if dest.exists() else 0
    sha = sha256_file(dest) if dest.exists() and file_size > 0 else ""
    manifest.append({
        "model_or_benchmark_name": model_name,
        "version": version,
        "organization": "Anthropic",
        "doc_type": "official_html",
        "source_type": "anthropic_system_card",
        "source_url": url,
        "local_path": str(dest.relative_to(BASE.parent)),
        "fetched_at": fetched,
        "sha256": sha,
        "file_size_bytes": file_size,
        "pdf_header_ok": False,
        "parsed_title": "",
        "parsed_first_page_text_snippet": "",
        "modality": "text-image",
        "hallucination_related_benchmarks_mentioned": False,
        "notes": (
            f"{model_name} system card: no official PDF found at Anthropic CDN; "
            "saved Anthropic news/research page as HTML; "
            "无可验证官方 PDF — check anthropic.com for official system card release"
        ),
    })

# ── 2. Fix GPT-5.2 entry (failed HTML) → try again ───────────────────────────
gpt52_dest = BASE / "official_model_cards_html/GPT-5.2_system_card.html"
gpt52_dest.parent.mkdir(parents=True, exist_ok=True)
gpt52_urls = [
    "https://openai.com/research/gpt-5-2",
    "https://openai.com/index/gpt-5",
    "https://openai.com/chatgpt",
]
gpt52_ok = False
gpt52_used_url = ""
for url in gpt52_urls:
    if save_html(url, gpt52_dest):
        gpt52_ok = True
        gpt52_used_url = url
        break

# Update manifest entry
manifest = [e for e in manifest if e["model_or_benchmark_name"] != "GPT-5.2"]
fetched = datetime.datetime.utcnow().isoformat() + "Z"
file_size = gpt52_dest.stat().st_size if gpt52_dest.exists() else 0
sha = sha256_file(gpt52_dest) if gpt52_ok else ""
manifest.append({
    "model_or_benchmark_name": "GPT-5.2",
    "version": "5.2",
    "organization": "OpenAI",
    "doc_type": "official_html",
    "source_type": "openai_system_card",
    "source_url": gpt52_used_url or "https://openai.com",
    "local_path": str(gpt52_dest.relative_to(BASE.parent)) if gpt52_ok else "",
    "fetched_at": fetched,
    "sha256": sha,
    "file_size_bytes": file_size,
    "pdf_header_ok": False,
    "parsed_title": "",
    "parsed_first_page_text_snippet": "",
    "modality": "text-image",
    "hallucination_related_benchmarks_mentioned": False,
    "notes": (
        "GPT-5.2 system card update: no dedicated PDF found at openai.com; "
        "无可验证官方 PDF — verify that GPT-5.2 is an officially released model version; "
        f"saved {'HTML fallback' if gpt52_ok else 'nothing (URL unavailable)'}"
    ),
})
print(f"  [{'OK' if gpt52_ok else 'FAIL'}] GPT-5.2 HTML → {gpt52_used_url}")

# ── 3. Fix GLM-4.1V-Thinking and GLM-4.6V entries → try alternative HF URLs ──
GLM_FIXES = [
    ("GLM-4.1V-Thinking", "4.1V-Thinking",
     ["https://huggingface.co/THUDM/GLM-4.1V-Thinking-7B",
      "https://huggingface.co/THUDM/GLM-4V-9B"],
     "official_model_cards_html/GLM-4.1V-Thinking_model_card.html"),
    ("GLM-4.6V", "4.6V",
     ["https://huggingface.co/THUDM/glm-4v-9b",
      "https://huggingface.co/THUDM"],
     "official_model_cards_html/GLM-4.6V_model_card.html"),
]

for model_name, version, urls, rel_path in GLM_FIXES:
    dest = BASE / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)
    ok = False
    used_url = ""
    for url in urls:
        if save_html(url, dest):
            ok = True
            used_url = url
            break
    print(f"  [{'OK' if ok else 'FAIL'}] {rel_path}")
    manifest = [e for e in manifest if e["model_or_benchmark_name"] != model_name]
    fetched = datetime.datetime.utcnow().isoformat() + "Z"
    file_size = dest.stat().st_size if dest.exists() and ok else 0
    sha = sha256_file(dest) if ok else ""
    manifest.append({
        "model_or_benchmark_name": model_name,
        "version": version,
        "organization": "Zhipu AI",
        "doc_type": "official_model_card",
        "source_type": "huggingface_official",
        "source_url": used_url or urls[0],
        "local_path": str(dest.relative_to(BASE.parent)) if ok else "",
        "fetched_at": fetched,
        "sha256": sha,
        "file_size_bytes": file_size,
        "pdf_header_ok": False,
        "parsed_title": "",
        "parsed_first_page_text_snippet": "",
        "modality": "text-image",
        "hallucination_related_benchmarks_mentioned": False,
        "notes": (
            f"{model_name} model card on HuggingFace; "
            "无可验证官方 PDF; verify exact GLM version naming on Zhipu AI GitHub"
        ),
    })

# ── 4. Extract PDF text for all valid PDFs that have empty parsed_title ───────
print("\n=== Extracting PDF text snippets ===")
for i, entry in enumerate(manifest):
    lp = entry.get("local_path", "")
    if not lp or not lp.endswith(".pdf"):
        continue
    if entry.get("parsed_title") or not entry.get("pdf_header_ok"):
        continue
    pdf_path = BASE.parent / lp
    if not pdf_path.exists():
        continue
    print(f"  Extracting: {pdf_path.name}")
    title, snippet = extract_pdf_text(pdf_path)
    manifest[i]["parsed_title"] = title
    manifest[i]["parsed_first_page_text_snippet"] = snippet

# ── 5. Validate all PDF headers for entries that claim pdf_header_ok=True ────
print("\n=== Validating PDF headers ===")
for i, entry in enumerate(manifest):
    lp = entry.get("local_path", "")
    if not lp or not lp.endswith(".pdf"):
        continue
    pdf_path = BASE.parent / lp
    if not pdf_path.exists():
        manifest[i]["pdf_header_ok"] = False
        manifest[i]["file_size_bytes"] = 0
        continue
    data = pdf_path.read_bytes()
    is_ok = data[:4] == b"%PDF"
    manifest[i]["pdf_header_ok"] = is_ok
    manifest[i]["file_size_bytes"] = len(data)
    if not is_ok:
        print(f"  BAD HEADER: {lp}")

# ── 6. Update sha256 for entries that are missing it ────────────────────────
print("\n=== Updating SHA256 ===")
for i, entry in enumerate(manifest):
    if entry.get("sha256"):
        continue
    lp = entry.get("local_path", "")
    if not lp:
        continue
    path = BASE.parent / lp
    if path.exists() and path.stat().st_size > 0:
        manifest[i]["sha256"] = sha256_file(path)
        manifest[i]["file_size_bytes"] = path.stat().st_size
        print(f"  sha256 updated: {path.name}")

# ── Save ─────────────────────────────────────────────────────────────────────
MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
print(f"\n[manifest] Final: {len(manifest)} entries → {MANIFEST_PATH}")

# Summary
from collections import Counter
dt = Counter(e["doc_type"] for e in manifest)
print("\nBy doc_type:")
for k,v in sorted(dt.items()):
    print(f"  {k}: {v}")

pdf_ok = sum(1 for e in manifest if e.get("pdf_header_ok"))
pdf_fail = [e for e in manifest if e["local_path"].endswith(".pdf") and not e.get("pdf_header_ok") and e["local_path"]]
print(f"\nPDF OK: {pdf_ok}")
print(f"PDF FAIL (bad header or missing): {len(pdf_fail)}")
for e in pdf_fail:
    print(f"  {e['model_or_benchmark_name']} → {e['local_path']}")
