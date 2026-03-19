#!/usr/bin/env python3
"""
Web Search + Mega Scraper Engine
- Automated search (DuckDuckGo)
- Scrape pages, PDFs, follow links
- NLP summaries & keywords
- Organise with pandas index
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import re
import time
import json
import urllib.request
from pathlib import Path
from datetime import datetime
from collections import Counter
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Optional imports (will be checked at runtime)
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

# --- NLP helpers (same as before) ---
STOPWORDS = set(["the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
                 "have", "has", "had", "do", "does", "did", "will", "would", "shall",
                 "should", "may", "might", "must", "can", "could", "to", "of", "in",
                 "on", "at", "by", "for", "with", "from", "as", "or", "and", "but",
                 "not", "this", "that", "these", "those", "it", "its", "we", "they",
                 "he", "she", "i", "you", "my", "your", "our", "their", "if", "so",
                 "about", "into", "than", "then", "when", "where", "who", "which",
                 "what", "all", "any", "each", "more", "also", "no", "up", "out"])

def extract_keywords(text: str, num: int = 5) -> list:
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    return [word for word, _ in Counter(filtered).most_common(num)]

def pure_python_summarize(text: str, sentences: int = 5) -> str:
    sents = re.split(r'(?<=[.!?])\s+', text)
    if len(sents) <= sentences:
        return text
    word_freq = Counter(re.findall(r'\b[a-z]{4,}\b', text.lower()))
    max_freq = max(word_freq.values()) if word_freq else 1
    scores = []
    for s in sents:
        s_words = re.findall(r'\b[a-z]{4,}\b', s.lower())
        score = sum(word_freq.get(w, 0) / max_freq for w in s_words if w not in STOPWORDS)
        scores.append((score, s))
    top = sorted(scores, key=lambda x: x[0], reverse=True)[:sentences]
    top = sorted(top, key=lambda x: sents.index(x[1]))
    return " ".join([s for _, s in top])

def check_ollama_running() -> bool:
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=2)
        return True
    except:
        return False

def ollama_summarize(text: str, model: str) -> str:
    prompt = "Summarize the following text in 3-5 bullet points:\n\n{text}"
    payload = json.dumps({
        "model": model,
        "prompt": prompt.replace("{text}", text[:3000]),
        "stream": False
    }).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("response", "").strip()
    except:
        return ""

def keybert_keywords(text: str, num: int = 5) -> list:
    try:
        from keybert import KeyBERT
        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1,2),
                                             stop_words='english', top_n=num)
        return [kw for kw, _ in keywords]
    except ImportError:
        return []

# --- Scraping helpers ---
def fetch_url(url: str, timeout: int = 10) -> str:
    """Fetch HTML content from a URL."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception as e:
        raise Exception(f"Failed to fetch {url}: {e}")

def extract_text_from_html(html: str) -> str:
    """Extract readable text from HTML."""
    soup = BeautifulSoup(html, 'lxml')
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator='\n')
    # Clean up lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

def extract_links(html: str, base_url: str) -> list:
    """Extract all absolute href links from HTML."""
    soup = BeautifulSoup(html, 'lxml')
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Make absolute
        if href.startswith('http'):
            links.append(href)
        elif href.startswith('/'):
            # relative to domain
            from urllib.parse import urlparse, urlunparse
            parsed = urlparse(base_url)
            base = f"{parsed.scheme}://{parsed.netloc}"
            links.append(base + href)
    return links

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text from a PDF file using pdfplumber."""
    if not PDFPLUMBER_AVAILABLE:
        return "[PDFPLUMBER NOT INSTALLED]"
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def download_file(url: str, dest: Path) -> bool:
    """Download a file from URL to destination."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, stream=True, timeout=15)
        r.raise_for_status()
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception:
        return False

# ----------------------------------------------------------------------
# MAIN APPLICATION
# ----------------------------------------------------------------------
class WebScraperEngine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Web Search + Mega Scraper")
        self.geometry("1200x800")
        self.configure(bg="#0d0d14")

        # Variables
        self.search_query = tk.StringVar()
        self.max_results = tk.IntVar(value=10)
        self.output_dir = tk.StringVar(value=str(Path.home() / "Documents" / "Scraper_Output"))
        self.depth = tk.IntVar(value=0)          # how many levels of links to follow
        self.download_pdfs = tk.BooleanVar(value=True)
        self.follow_links = tk.BooleanVar(value=False)
        self.use_ollama = tk.BooleanVar(value=False)
        self.use_keybert = tk.BooleanVar(value=False)
        self.ollama_model = tk.StringVar(value="gemma2:9b")
        self.kw_count = tk.IntVar(value=5)
        self.sum_len = tk.IntVar(value=5)

        self.log_queue = queue.Queue()
        self.is_processing = False
        self._build_ui()
        self._start_log_drain()

        # Check for DDGS
        if not DDGS_AVAILABLE:
            self.log("⚠️ duckduckgo-search not installed. Install with: pip install duckduckgo-search", "system")

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg="#13131f", height=60)
        hdr.pack(fill="x", side="top")
        tk.Label(hdr, text="🕸️ Web Search + Mega Scraper", font=("Arial", 14, "bold"),
                 bg="#13131f", fg="#e8e8f0").pack(side="left", padx=20)

        # Notebook
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        self._tab_scrape()
        self._tab_batch()
        self._tab_settings()

        # Status bar
        bar = tk.Frame(self, bg="#13131f", height=28)
        bar.pack(fill="x", side="bottom")
        self.status_label = tk.Label(bar, text="Ready.", font=("Arial", 9),
                                     bg="#13131f", fg="#6b6b8a", anchor="w")
        self.status_label.pack(side="left", padx=16)
        self.progress = ttk.Progressbar(bar, mode="indeterminate", length=200)
        self.progress.pack(side="right", padx=16, pady=6)

    def _tab_scrape(self):
        frame = tk.Frame(self.nb, bg="#0d0d14")
        self.nb.add(frame, text=" 🔎 Search & Scrape ")

        # Left panel (controls)
        left = tk.Frame(frame, bg="#0d0d14", width=400)
        left.pack(side="left", fill="y", padx=10, pady=10)
        left.pack_propagate(False)

        # Search query
        self._section(left, "1. Search Query")
        card_q = self._card(left)
        tk.Entry(card_q, textvariable=self.search_query, bg="#1a1a2c", fg="#e8e8f0",
                 insertbackground="#e8e8f0", font=("Arial", 10)).pack(fill="x", pady=5)
        tk.Label(card_q, text="e.g., 'artificial intelligence 2025'", font=("Arial", 8),
                 bg="#1a1a2c", fg="#6b6b8a").pack(anchor="w")

        # Max results
        self._section(left, "2. Max Results")
        card_r = self._card(left)
        tk.Spinbox(card_r, from_=1, to=100, textvariable=self.max_results,
                   bg="#1a1a2c", fg="#e8e8f0", width=10).pack(anchor="w")

        # Output folder
        self._section(left, "3. Output Folder")
        card_out = self._card(left)
        frow = tk.Frame(card_out, bg="#1a1a2c")
        frow.pack(fill="x")
        tk.Entry(frow, textvariable=self.output_dir, bg="#0d0d14", fg="#e8e8f0",
                 font=("Courier New", 9)).pack(side="left", fill="x", expand=True)
        tk.Button(frow, text="Browse", bg="#ff4d6d", fg="white", relief="flat",
                  command=lambda: self.output_dir.set(
                      filedialog.askdirectory() or self.output_dir.get())).pack(side="right")

        # Options
        self._section(left, "4. Scraping Options")
        card_opt = self._card(left)
        tk.Checkbutton(card_opt, text="Download PDFs", variable=self.download_pdfs,
                       bg="#1a1a2c", fg="#e8e8f0", selectcolor="#0d0d14").pack(anchor="w", pady=2)
        tk.Checkbutton(card_opt, text="Follow links (depth)", variable=self.follow_links,
                       bg="#1a1a2c", fg="#e8e8f0", selectcolor="#0d0d14").pack(anchor="w", pady=2)
        depth_row = tk.Frame(card_opt, bg="#1a1a2c")
        depth_row.pack(anchor="w", pady=2)
        tk.Label(depth_row, text="Depth:", bg="#1a1a2c", fg="#6b6b8a").pack(side="left")
        tk.Spinbox(depth_row, from_=0, to=3, textvariable=self.depth,
                   width=5, bg="#1a1a2c", fg="#e8e8f0").pack(side="left", padx=5)

        # NLP options
        self._section(left, "5. NLP Enhancements")
        card_nlp = self._card(left)
        tk.Checkbutton(card_nlp, text="Use Ollama for summary", variable=self.use_ollama,
                       bg="#1a1a2c", fg="#e8e8f0", selectcolor="#0d0d14").pack(anchor="w")
        mod_row = tk.Frame(card_nlp, bg="#1a1a2c")
        mod_row.pack(anchor="w", pady=2)
        tk.Label(mod_row, text="Ollama model:", bg="#1a1a2c", fg="#6b6b8a").pack(side="left")
        ttk.Combobox(mod_row, textvariable=self.ollama_model,
                     values=["gemma2:9b", "mistral-nemo", "llama3.2:3b", "phi3.5"],
                     state="readonly", width=15).pack(side="left", padx=5)

        tk.Checkbutton(card_nlp, text="Use KeyBERT for keywords", variable=self.use_keybert,
                       bg="#1a1a2c", fg="#e8e8f0", selectcolor="#0d0d14").pack(anchor="w")

        # Counts
        cnt_row = tk.Frame(card_nlp, bg="#1a1a2c")
        cnt_row.pack(anchor="w", pady=5)
        tk.Label(cnt_row, text="Keywords:", bg="#1a1a2c", fg="#6b6b8a").pack(side="left")
        tk.Spinbox(cnt_row, from_=1, to=10, textvariable=self.kw_count,
                   width=5, bg="#1a1a2c", fg="#e8e8f0").pack(side="left", padx=5)
        tk.Label(cnt_row, text="Summary sentences:", bg="#1a1a2c", fg="#6b6b8a").pack(side="left", padx=5)
        tk.Spinbox(cnt_row, from_=1, to=15, textvariable=self.sum_len,
                   width=5, bg="#1a1a2c", fg="#e8e8f0").pack(side="left")

        # Run button
        self.run_btn = tk.Button(left, text="▶ START SCRAPE", bg="#3ddc97", fg="#0d0d14",
                                 font=("Arial", 12, "bold"), pady=12,
                                 command=self._run_scrape)
        self.run_btn.pack(fill="x", padx=20, pady=20)

        # Right side (log)
        right = tk.Frame(frame, bg="#0d0d14")
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.log_box = scrolledtext.ScrolledText(right, bg="#13131f", fg="#00d4aa",
                                                  font=("Courier New", 10), relief="flat")
        self.log_box.pack(fill="both", expand=True)
        self.log_box.tag_config("err", foreground="#ff4d6d")
        self.log_box.tag_config("ok", foreground="#3ddc97")
        self.log_box.tag_config("info", foreground="#4d9fff")

    def _tab_batch(self):
        frame = tk.Frame(self.nb, bg="#0d0d14")
        self.nb.add(frame, text=" 📁 Batch URLs ")

        left = tk.Frame(frame, bg="#0d0d14", width=400)
        left.pack(side="left", fill="y", padx=10, pady=10)

        self._section(left, "URL List File")
        card = self._card(left)
        self.batch_file = tk.StringVar()
        frow = tk.Frame(card, bg="#1a1a2c")
        frow.pack(fill="x")
        tk.Entry(frow, textvariable=self.batch_file, bg="#0d0d14", fg="#e8e8f0").pack(side="left", fill="x", expand=True)
        tk.Button(frow, text="Browse", bg="#ff4d6d", fg="white", relief="flat",
                  command=lambda: self.batch_file.set(
                      filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV", "*.csv")]) or self.batch_file.get())).pack(side="right")
        tk.Label(card, text="One URL per line.", bg="#1a1a2c", fg="#6b6b8a", font=("Arial", 8)).pack(anchor="w")

        tk.Button(left, text="▶ PROCESS BATCH", bg="#ff8c42", fg="white",
                  font=("Arial", 11, "bold"), pady=10,
                  command=self._run_batch).pack(fill="x", padx=20, pady=20)

        right = tk.Frame(frame, bg="#0d0d14")
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        self.batch_log = scrolledtext.ScrolledText(right, bg="#13131f", fg="#00d4aa",
                                                    font=("Courier New", 10), relief="flat")
        self.batch_log.pack(fill="both", expand=True)

    def _tab_settings(self):
        frame = tk.Frame(self.nb, bg="#0d0d14")
        self.nb.add(frame, text=" ⚙ Settings ")

        canvas = tk.Canvas(frame, bg="#0d0d14", highlightthickness=0)
        scroll = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg="#0d0d14")
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.create_window((0,0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Tesseract path (optional)
        self._section(inner, "OCR (for scanned PDFs)")
        card = self._card(inner)
        self.tesseract_path = tk.StringVar(value=r"C:\Program Files\Tesseract-OCR\tesseract.exe")
        tk.Entry(card, textvariable=self.tesseract_path, bg="#1a1a2c", fg="#e8e8f0").pack(fill="x", pady=5)
        tk.Label(card, text="Only needed if you want OCR on scanned PDFs.", bg="#1a1a2c", fg="#6b6b8a").pack(anchor="w")

        # Ollama status
        self._section(inner, "Ollama")
        card2 = self._card(inner)
        self.ollama_status_lbl = tk.Label(card2, text="Checking...", bg="#1a1a2c", fg="#6b6b8a")
        self.ollama_status_lbl.pack(anchor="w")
        self.after(1000, self._update_ollama_status)

    # --- Helper UI methods ---
    def _section(self, parent, text):
        f = tk.Frame(parent, bg="#0d0d14")
        f.pack(fill="x", padx=10, pady=(10,2))
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
            fg="#3ddc97" if running else "#ff4d6d"
        )
        self.after(5000, self._update_ollama_status)

    def _run_scrape(self):
        if self.is_processing:
            return
        query = self.search_query.get().strip()
        if not query:
            messagebox.showwarning("Warning", "Enter a search query.")
            return
        if not DDGS_AVAILABLE:
            messagebox.showerror("Error", "DuckDuckGo search library not installed.\nRun: pip install duckduckgo-search")
            return
        self.is_processing = True
        self.progress.start(10)
        self.status_label.config(text="Scraping...")
        threading.Thread(target=self._scrape_thread, args=(query,), daemon=True).start()

    def _scrape_thread(self, query):
        try:
            out_dir = Path(self.output_dir.get())
            out_dir.mkdir(parents=True, exist_ok=True)

            self.log(f"Searching DuckDuckGo for: {query}", "info")
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_results.get()))

            self.log(f"Found {len(results)} results.", "ok")

            # Prepare a pandas DataFrame to hold index
            index_data = []

            for i, res in enumerate(results, 1):
                title = res.get('title', '')
                url = res.get('href', '')
                self.log(f"[{i}/{len(results)}] {title}", "info")

                try:
                    html = fetch_url(url)
                    text = extract_text_from_html(html)
                    if not text.strip():
                        self.log("  No readable text.", "err")
                        continue

                    # Save page content as Markdown
                    page_file = out_dir / f"page_{i}.md"
                    page_file.write_text(f"# {title}\n\nURL: {url}\n\n{text}", encoding="utf-8")

                    # Generate summary & keywords
                    summary = ""
                    if self.use_ollama.get() and check_ollama_running():
                        summary = ollama_summarize(text, self.ollama_model.get())
                    if not summary:
                        summary = pure_python_summarize(text, self.sum_len.get())

                    keywords = []
                    if self.use_keybert.get():
                        keywords = keybert_keywords(text, self.kw_count.get())
                    if not keywords:
                        keywords = extract_keywords(text, self.kw_count.get())

                    # Add to index
                    index_data.append({
                        'title': title,
                        'url': url,
                        'summary': summary,
                        'keywords': ', '.join(keywords),
                        'file': str(page_file),
                        'scraped': datetime.now().isoformat()
                    })

                    # Download PDF if link points to PDF
                    if self.download_pdfs.get() and url.lower().endswith('.pdf'):
                        pdf_path = out_dir / f"page_{i}.pdf"
                        if download_file(url, pdf_path):
                            pdf_text = extract_text_from_pdf(pdf_path)
                            if pdf_text:
                                pdf_file = out_dir / f"page_{i}_pdf.md"
                                pdf_file.write_text(f"# {title} (PDF)\n\n{pdf_text}", encoding="utf-8")
                                self.log(f"  Downloaded PDF: {pdf_path.name}", "ok")

                    # Follow links if enabled
                    if self.follow_links.get() and self.depth.get() > 0:
                        self._follow_links(html, url, out_dir, i, depth=self.depth.get())

                except Exception as e:
                    self.log(f"  Error: {e}", "err")

            # Create master index
            if index_data:
                df = pd.DataFrame(index_data)
                index_file = out_dir / "scrape_index.csv"
                df.to_csv(index_file, index=False)
                self.log(f"✅ Index saved: {index_file}", "ok")

            self.log("🎉 Scraping complete!", "ok")
        except Exception as e:
            self.log(f"Fatal error: {e}", "err")
        finally:
            self.is_processing = False
            self.progress.stop()
            self.status_label.config(text="Ready.")

    def _follow_links(self, html, base_url, out_dir, parent_id, depth):
        """Follow links from a page up to given depth."""
        if depth <= 0:
            return
        links = extract_links(html, base_url)
        self.log(f"  Found {len(links)} links, following (depth {depth})...", "info")
        for j, link in enumerate(links[:5]):  # limit to 5 per page to avoid explosion
            try:
                html2 = fetch_url(link)
                text2 = extract_text_from_html(html2)
                if text2.strip():
                    sub_file = out_dir / f"page_{parent_id}_link{j+1}.md"
                    sub_file.write_text(f"# Link from {base_url}\n\nURL: {link}\n\n{text2}", encoding="utf-8")
                    self.log(f"    Saved linked page: {sub_file.name}", "ok")
                # Recurse
                self._follow_links(html2, link, out_dir, f"{parent_id}_{j+1}", depth-1)
            except Exception as e:
                self.log(f"    Error following {link}: {e}", "err")

    def _run_batch(self):
        # Similar to scrape but reads URLs from file
        pass  # For brevity, you can implement similarly

if __name__ == "__main__":
    app = WebScraperEngine()
    app.mainloop()