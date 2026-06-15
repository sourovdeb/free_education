#!/usr/bin/env python3
"""
Web Search + Mega Scraper Engine
- Automated search (DuckDuckGo)
- Scrape pages, PDFs, follow links
- NLP summaries & keywords
- Organise with pandas index
- FIXED: _run_batch() implemented (was previously just `pass`)
- NLP via shared nlp_utils.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import re
import time
import urllib.request
from pathlib import Path
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import pandas as pd

# ── Shared NLP ────────────────────────────────────────────────────────────────
from nlp_utils import (
    extract_keywords, pure_python_summarize,
    check_ollama_running, ollama_summarize, keybert_keywords,
)

# ── Optional imports ──────────────────────────────────────────────────────────
try:
    from duckduckgo_search import DDGS
    DDGS_AVAILABLE = True
except ImportError:
    DDGS_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False


# ── Scraping helpers ──────────────────────────────────────────────────────────
def fetch_url(url: str, timeout: int = 10) -> str:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    r = requests.get(url, headers=headers, timeout=timeout)
    r.raise_for_status()
    return r.text


def extract_text_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style"]):
        tag.decompose()
    lines = [l.strip() for l in soup.get_text(separator="\n").splitlines() if l.strip()]
    return "\n".join(lines)


def extract_links(html: str, base_url: str) -> list[str]:
    from urllib.parse import urlparse
    soup   = BeautifulSoup(html, "lxml")
    parsed = urlparse(base_url)
    base   = f"{parsed.scheme}://{parsed.netloc}"
    links  = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http"):
            links.append(href)
        elif href.startswith("/"):
            links.append(base + href)
    return links


def extract_text_from_pdf(pdf_path: Path) -> str:
    if not PDFPLUMBER_AVAILABLE:
        return "[pdfplumber not installed]"
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


def download_file(url: str, dest: Path) -> bool:
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"},
                         stream=True, timeout=15)
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────────────────────────────────
class WebScraperEngine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Web Search + Mega Scraper")
        self.geometry("1200x800")
        self.configure(bg="#0d0d14")

        self.search_query  = tk.StringVar()
        self.max_results   = tk.IntVar(value=10)
        self.output_dir    = tk.StringVar(
            value=str(Path.home() / "Documents" / "Scraper_Output")
        )
        self.depth         = tk.IntVar(value=0)
        self.download_pdfs = tk.BooleanVar(value=True)
        self.follow_links  = tk.BooleanVar(value=False)
        self.use_ollama    = tk.BooleanVar(value=False)
        self.use_keybert   = tk.BooleanVar(value=False)
        self.ollama_model  = tk.StringVar(value="gemma2:9b")
        self.kw_count      = tk.IntVar(value=5)
        self.sum_len       = tk.IntVar(value=5)

        self.log_queue    = queue.Queue()
        self.is_processing = False

        self._build_ui()
        self._start_log_drain()

        if not DDGS_AVAILABLE:
            self.log("⚠️  duckduckgo-search not installed: pip install duckduckgo-search", "system")

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        hdr = tk.Frame(self, bg="#13131f", height=60)
        hdr.pack(fill="x", side="top")
        tk.Label(hdr, text="🕸️ Web Search + Mega Scraper",
                 font=("Arial", 14, "bold"), bg="#13131f", fg="#e8e8f0").pack(
            side="left", padx=20)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        self._tab_scrape()
        self._tab_batch()
        self._tab_settings()

        bar = tk.Frame(self, bg="#13131f", height=28)
        bar.pack(fill="x", side="bottom")
        self.status_label = tk.Label(
            bar, text="Ready.", font=("Arial", 9),
            bg="#13131f", fg="#6b6b8a", anchor="w",
        )
        self.status_label.pack(side="left", padx=16)
        self.progress = ttk.Progressbar(bar, mode="indeterminate", length=200)
        self.progress.pack(side="right", padx=16, pady=6)

    def _tab_scrape(self):
        frame = tk.Frame(self.nb, bg="#0d0d14")
        self.nb.add(frame, text=" 🔎 Search & Scrape ")

        left = tk.Frame(frame, bg="#0d0d14", width=400)
        left.pack(side="left", fill="y", padx=10, pady=10)
        left.pack_propagate(False)

        self._section(left, "1. Search Query")
        card_q = self._card(left)
        tk.Entry(card_q, textvariable=self.search_query,
                 bg="#1a1a2c", fg="#e8e8f0", insertbackground="#e8e8f0",
                 font=("Arial", 10)).pack(fill="x", pady=5)
        tk.Label(card_q, text="e.g., 'artificial intelligence 2025'",
                 font=("Arial", 8), bg="#1a1a2c", fg="#6b6b8a").pack(anchor="w")

        self._section(left, "2. Max Results")
        card_r = self._card(left)
        tk.Spinbox(card_r, from_=1, to=100, textvariable=self.max_results,
                   bg="#1a1a2c", fg="#e8e8f0", width=10).pack(anchor="w")

        self._section(left, "3. Output Folder")
        card_out = self._card(left)
        frow = tk.Frame(card_out, bg="#1a1a2c")
        frow.pack(fill="x")
        tk.Entry(frow, textvariable=self.output_dir,
                 bg="#0d0d14", fg="#e8e8f0",
                 font=("Courier New", 9)).pack(side="left", fill="x", expand=True)
        tk.Button(frow, text="Browse", bg="#ff4d6d", fg="white", relief="flat",
                  command=lambda: self.output_dir.set(
                      filedialog.askdirectory() or self.output_dir.get()
                  )).pack(side="right")

        self._section(left, "4. Scraping Options")
        card_opt = self._card(left)
        tk.Checkbutton(card_opt, text="Download PDFs", variable=self.download_pdfs,
                       bg="#1a1a2c", fg="#e8e8f0", selectcolor="#0d0d14").pack(anchor="w", pady=2)
        tk.Checkbutton(card_opt, text="Follow links (depth)", variable=self.follow_links,
                       bg="#1a1a2c", fg="#e8e8f0", selectcolor="#0d0d14").pack(anchor="w", pady=2)
        dr = tk.Frame(card_opt, bg="#1a1a2c")
        dr.pack(anchor="w", pady=2)
        tk.Label(dr, text="Depth:", bg="#1a1a2c", fg="#6b6b8a").pack(side="left")
        tk.Spinbox(dr, from_=0, to=3, textvariable=self.depth,
                   width=5, bg="#1a1a2c", fg="#e8e8f0").pack(side="left", padx=5)

        self._section(left, "5. NLP Enhancements")
        card_nlp = self._card(left)
        tk.Checkbutton(card_nlp, text="Use Ollama for summary", variable=self.use_ollama,
                       bg="#1a1a2c", fg="#e8e8f0", selectcolor="#0d0d14").pack(anchor="w")
        mr = tk.Frame(card_nlp, bg="#1a1a2c")
        mr.pack(anchor="w", pady=2)
        tk.Label(mr, text="Ollama model:", bg="#1a1a2c", fg="#6b6b8a").pack(side="left")
        ttk.Combobox(mr, textvariable=self.ollama_model,
                     values=["gemma2:9b", "mistral-nemo", "llama3.2:3b", "phi3.5"],
                     state="readonly", width=15).pack(side="left", padx=5)
        tk.Checkbutton(card_nlp, text="Use KeyBERT for keywords", variable=self.use_keybert,
                       bg="#1a1a2c", fg="#e8e8f0", selectcolor="#0d0d14").pack(anchor="w")
        cr = tk.Frame(card_nlp, bg="#1a1a2c")
        cr.pack(anchor="w", pady=5)
        tk.Label(cr, text="Keywords:", bg="#1a1a2c", fg="#6b6b8a").pack(side="left")
        tk.Spinbox(cr, from_=1, to=10, textvariable=self.kw_count,
                   width=5, bg="#1a1a2c", fg="#e8e8f0").pack(side="left", padx=5)
        tk.Label(cr, text="Summary sentences:", bg="#1a1a2c", fg="#6b6b8a").pack(side="left", padx=5)
        tk.Spinbox(cr, from_=1, to=15, textvariable=self.sum_len,
                   width=5, bg="#1a1a2c", fg="#e8e8f0").pack(side="left")

        self.run_btn = tk.Button(
            left, text="▶ START SCRAPE", bg="#3ddc97", fg="#0d0d14",
            font=("Arial", 12, "bold"), pady=12, command=self._run_scrape,
        )
        self.run_btn.pack(fill="x", padx=20, pady=20)

        right = tk.Frame(frame, bg="#0d0d14")
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.log_box = scrolledtext.ScrolledText(
            right, bg="#13131f", fg="#00d4aa",
            font=("Courier New", 10), relief="flat",
        )
        self.log_box.pack(fill="both", expand=True)
        self.log_box.tag_config("err",  foreground="#ff4d6d")
        self.log_box.tag_config("ok",   foreground="#3ddc97")
        self.log_box.tag_config("info", foreground="#4d9fff")

    def _tab_batch(self):
        """Batch tab — FIXED: was previously unimplemented (just `pass`)."""
        frame = tk.Frame(self.nb, bg="#0d0d14")
        self.nb.add(frame, text=" 📁 Batch URLs ")

        left = tk.Frame(frame, bg="#0d0d14", width=400)
        left.pack(side="left", fill="y", padx=10, pady=10)
        left.pack_propagate(False)

        self._section(left, "URL List File")
        card = self._card(left)
        self.batch_file = tk.StringVar()
        frow = tk.Frame(card, bg="#1a1a2c")
        frow.pack(fill="x")
        tk.Entry(frow, textvariable=self.batch_file,
                 bg="#0d0d14", fg="#e8e8f0").pack(side="left", fill="x", expand=True)
        tk.Button(frow, text="Browse", bg="#ff4d6d", fg="white", relief="flat",
                  command=lambda: self.batch_file.set(
                      filedialog.askopenfilename(
                          filetypes=[("Text / CSV", "*.txt *.csv")]
                      ) or self.batch_file.get()
                  )).pack(side="right")
        tk.Label(card, text="One URL per line. CSV: first column used.",
                 bg="#1a1a2c", fg="#6b6b8a", font=("Arial", 8)).pack(anchor="w")

        # Output folder for batch results
        self._section(left, "Output Folder")
        card2 = self._card(left)
        self.batch_out_dir = tk.StringVar(
            value=str(Path.home() / "Documents" / "Scraper_Output")
        )
        frow2 = tk.Frame(card2, bg="#1a1a2c")
        frow2.pack(fill="x")
        tk.Entry(frow2, textvariable=self.batch_out_dir,
                 bg="#0d0d14", fg="#e8e8f0",
                 font=("Courier New", 9)).pack(side="left", fill="x", expand=True)
        tk.Button(frow2, text="Browse", bg="#ff4d6d", fg="white", relief="flat",
                  command=lambda: self.batch_out_dir.set(
                      filedialog.askdirectory() or self.batch_out_dir.get()
                  )).pack(side="right")

        # NLP reuses main settings
        self._section(left, "NLP (uses settings from Search tab)")
        card3 = self._card(left)
        tk.Label(card3, text="Ollama, KeyBERT, keyword count, and summary\n"
                             "settings are shared from the Search & Scrape tab.",
                 bg="#1a1a2c", fg="#6b6b8a", font=("Arial", 8),
                 justify="left").pack(anchor="w")

        self.batch_run_btn = tk.Button(
            left, text="▶ PROCESS BATCH", bg="#ff8c42", fg="white",
            font=("Arial", 11, "bold"), pady=10, command=self._run_batch,
        )
        self.batch_run_btn.pack(fill="x", padx=20, pady=20)

        right = tk.Frame(frame, bg="#0d0d14")
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.batch_log = scrolledtext.ScrolledText(
            right, bg="#13131f", fg="#00d4aa",
            font=("Courier New", 10), relief="flat",
        )
        self.batch_log.pack(fill="both", expand=True)
        self.batch_log.tag_config("err",  foreground="#ff4d6d")
        self.batch_log.tag_config("ok",   foreground="#3ddc97")
        self.batch_log.tag_config("info", foreground="#4d9fff")

    def _tab_settings(self):
        frame = tk.Frame(self.nb, bg="#0d0d14")
        self.nb.add(frame, text=" ⚙ Settings ")

        canvas = tk.Canvas(frame, bg="#0d0d14", highlightthickness=0)
        scroll = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner  = tk.Frame(canvas, bg="#0d0d14")
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self._section(inner, "OCR (for scanned PDFs)")
        c = self._card(inner)
        self.tesseract_path = tk.StringVar(
            value=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )
        tk.Entry(c, textvariable=self.tesseract_path,
                 bg="#1a1a2c", fg="#e8e8f0").pack(fill="x", pady=5)
        tk.Label(c, text="Only needed if you want OCR on scanned PDFs.",
                 bg="#1a1a2c", fg="#6b6b8a").pack(anchor="w")

        self._section(inner, "Ollama")
        c2 = self._card(inner)
        self.ollama_status_lbl = tk.Label(c2, text="Checking…",
                                           bg="#1a1a2c", fg="#6b6b8a")
        self.ollama_status_lbl.pack(anchor="w")
        self.after(1000, self._update_ollama_status)

    # ── UI helpers ────────────────────────────────────────────────────────────
    def _section(self, parent, text):
        f = tk.Frame(parent, bg="#0d0d14")
        f.pack(fill="x", padx=10, pady=(10, 2))
        tk.Frame(f, bg="#ff4d6d", width=3, height=14).pack(side="left")
        tk.Label(f, text=f"  {text}", font=("Arial", 10, "bold"),
                 bg="#0d0d14", fg="#e8e8f0").pack(side="left")

    def _card(self, parent):
        c = tk.Frame(parent, bg="#1a1a2c", padx=10, pady=10,
                     highlightbackground="#2a2a40", highlightthickness=1)
        c.pack(fill="x", padx=10, pady=2)
        return c

    def log(self, msg, tag="info", box="single"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_queue.put((tag, f"[{ts}] {msg}\n", box))

    def _start_log_drain(self):
        try:
            while True:
                tag, msg, box = self.log_queue.get_nowait()
                target = self.log_box if box == "single" else self.batch_log
                target.insert("end", msg, tag)
                target.see("end")
        except queue.Empty:
            pass
        self.after(100, self._start_log_drain)

    def _update_ollama_status(self):
        running = check_ollama_running()
        self.ollama_status_lbl.config(
            text="✓ Ollama running" if running else "✗ Ollama not running",
            fg="#3ddc97" if running else "#ff4d6d",
        )
        self.after(5000, self._update_ollama_status)

    # ── Scrape one URL and return an index dict ────────────────────────────────
    def _scrape_url(self, i: int, url: str, title: str,
                    out_dir: Path, box: str) -> dict | None:
        try:
            html = fetch_url(url)
            text = extract_text_from_html(html)
            if not text.strip():
                self.log("  No readable text.", "err", box)
                return None

            page_file = out_dir / f"page_{i}.md"
            page_file.write_text(f"# {title}\n\nURL: {url}\n\n{text}", encoding="utf-8")

            if self.use_ollama.get() and check_ollama_running():
                summary = ollama_summarize(text, self.ollama_model.get()) or \
                          pure_python_summarize(text, self.sum_len.get())
            else:
                summary = pure_python_summarize(text, self.sum_len.get())

            keywords = (keybert_keywords(text, self.kw_count.get())
                        if self.use_keybert.get() else []) or \
                       extract_keywords(text, self.kw_count.get())

            if self.download_pdfs.get() and url.lower().endswith(".pdf"):
                pdf_path = out_dir / f"page_{i}.pdf"
                if download_file(url, pdf_path):
                    pdf_text = extract_text_from_pdf(pdf_path)
                    if pdf_text:
                        (out_dir / f"page_{i}_pdf.md").write_text(
                            f"# {title} (PDF)\n\n{pdf_text}", encoding="utf-8"
                        )
                        self.log(f"  Downloaded PDF: {pdf_path.name}", "ok", box)

            if self.follow_links.get() and self.depth.get() > 0:
                self._follow_links(html, url, out_dir, i, self.depth.get(), box)

            return {
                "title":    title,
                "url":      url,
                "summary":  summary,
                "keywords": ", ".join(keywords),
                "file":     str(page_file),
                "scraped":  datetime.now().isoformat(),
            }
        except Exception as e:
            self.log(f"  Error: {e}", "err", box)
            return None

    # ── Search & scrape thread ────────────────────────────────────────────────
    def _run_scrape(self):
        if self.is_processing:
            return
        query = self.search_query.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Enter a search query.")
            return
        if not DDGS_AVAILABLE:
            messagebox.showerror("Error",
                "DuckDuckGo library not installed.\npip install duckduckgo-search")
            return
        self.is_processing = True
        self.progress.start(10)
        self.status_label.config(text="Scraping…")
        threading.Thread(target=self._scrape_thread, args=(query,), daemon=True).start()

    def _scrape_thread(self, query: str):
        try:
            out_dir = Path(self.output_dir.get())
            out_dir.mkdir(parents=True, exist_ok=True)

            self.log(f"Searching DuckDuckGo: {query}", "info")
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_results.get()))
            self.log(f"Found {len(results)} results.", "ok")

            index_data = []
            for i, res in enumerate(results, 1):
                title = res.get("title", "")
                url   = res.get("href", "")
                self.log(f"[{i}/{len(results)}] {title}", "info")
                row = self._scrape_url(i, url, title, out_dir, "single")
                if row:
                    index_data.append(row)
                    self.log(f"  ✓ Saved page_{i}.md", "ok")

            if index_data:
                df   = pd.DataFrame(index_data)
                idx  = out_dir / "scrape_index.csv"
                df.to_csv(idx, index=False)
                self.log(f"✅ Index saved: {idx}", "ok")

            self.log("🎉 Scraping complete!", "ok")
        except Exception as e:
            self.log(f"Fatal error: {e}", "err")
        finally:
            self.is_processing = False
            self.progress.stop()
            self.status_label.config(text="Ready.")

    # ── Batch URL tab — FIXED (was `pass`) ────────────────────────────────────
    def _run_batch(self):
        batch_path = self.batch_file.get().strip()
        if not batch_path or not Path(batch_path).exists():
            messagebox.showwarning("Warning", "Select a valid URL list file.")
            return
        if self.is_processing:
            return
        self.is_processing = True
        self.progress.start(10)
        self.status_label.config(text="Batch scraping…")
        threading.Thread(target=self._batch_thread, args=(Path(batch_path),), daemon=True).start()

    def _batch_thread(self, url_file: Path):
        try:
            out_dir = Path(self.batch_out_dir.get())
            out_dir.mkdir(parents=True, exist_ok=True)

            # Read URLs — support plain .txt (one per line) and .csv (first column)
            raw_lines: list[str] = []
            if url_file.suffix.lower() == ".csv":
                import csv
                with open(url_file, newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row and row[0].strip().startswith("http"):
                            raw_lines.append(row[0].strip())
            else:
                raw_lines = [
                    l.strip() for l in url_file.read_text(encoding="utf-8").splitlines()
                    if l.strip().startswith("http")
                ]

            if not raw_lines:
                self.log("No valid URLs found in file.", "err", "batch")
                return

            self.log(f"Found {len(raw_lines)} URLs to process.", "ok", "batch")
            index_data = []

            for i, url in enumerate(raw_lines, 1):
                self.log(f"[{i}/{len(raw_lines)}] {url}", "info", "batch")
                title = f"page_{i}"
                row   = self._scrape_url(i, url, title, out_dir, "batch")
                if row:
                    index_data.append(row)
                    self.log(f"  ✓ Saved {title}.md", "ok", "batch")

            if index_data:
                df  = pd.DataFrame(index_data)
                idx = out_dir / "batch_index.csv"
                df.to_csv(idx, index=False)
                self.log(f"✅ Index saved: {idx}", "ok", "batch")

            self.log("🎉 Batch complete!", "ok", "batch")
        except Exception as e:
            self.log(f"Fatal error: {e}", "err", "batch")
        finally:
            self.is_processing = False
            self.progress.stop()
            self.status_label.config(text="Ready.")

    def _follow_links(self, html: str, base_url: str,
                      out_dir: Path, parent_id, depth: int, box: str):
        if depth <= 0:
            return
        links = extract_links(html, base_url)
        self.log(f"  Following {min(len(links), 5)} links (depth {depth})…", "info", box)
        for j, link in enumerate(links[:5]):
            try:
                html2 = fetch_url(link)
                text2 = extract_text_from_html(html2)
                if text2.strip():
                    f = out_dir / f"page_{parent_id}_link{j+1}.md"
                    f.write_text(f"# Link from {base_url}\n\nURL: {link}\n\n{text2}",
                                 encoding="utf-8")
                    self.log(f"    Saved: {f.name}", "ok", box)
                self._follow_links(html2, link, out_dir, f"{parent_id}_{j+1}", depth-1, box)
            except Exception as e:
                self.log(f"    Error following {link}: {e}", "err", box)


if __name__ == "__main__":
    app = WebScraperEngine()
    app.mainloop()
