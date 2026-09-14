#!/usr/bin/env python3
"""
Writer & Teacher Document Engine (v5.1)
Extracts text from PDFs, Images, Scans → Markdown with NLP.
- Ollama summaries, KeyBERT keywords, Surya OCR, marker-pdf
- FIXED: missing imports (subprocess, tempfile, PIL.Image)
- NLP via shared nlp_utils.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess          # ← was missing
import tempfile            # ← was missing
import os
import re
import platform
import queue
import time
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

# ── Windows DPI fix ───────────────────────────────────────────────────────────
if platform.system() == "Windows":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

# ── Shared NLP ────────────────────────────────────────────────────────────────
from nlp_utils import (
    extract_keywords, pure_python_summarize, clean_grammar,
    check_ollama_running, ollama_summarize, keybert_keywords,
    get_ollama_models,
)

# ── Colors & fonts ────────────────────────────────────────────────────────────
BG       = "#0d0d14"
PANEL    = "#13131f"
CARD     = "#1a1a2c"
BORDER   = "#2a2a40"
ACCENT   = "#7c5cfc"
ACCENT2  = "#00d4aa"
TEXT     = "#e8e8f0"
TEXT_DIM = "#6b6b8a"
SUCCESS  = "#3ddc97"
ERROR    = "#ff4d6d"
RUNNING  = "#4d9fff"

_FF       = "Arial" if platform.system() == "Windows" else "Helvetica"
FONT_MAIN  = (_FF, 11)
FONT_MONO  = ("Courier New" if platform.system() == "Windows" else "Courier", 10)
FONT_HEAD  = (_FF, 11, "bold")
FONT_SMALL = (_FF, 9)


# ── OCR helpers ───────────────────────────────────────────────────────────────
def ocr_with_tesseract(image_path: Path, tesseract_cmd: str, lang: str = "eng") -> str:
    import pytesseract
    from PIL import Image              # ← was missing at module level
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    img = Image.open(image_path)
    return pytesseract.image_to_string(img, lang=lang)


def ocr_with_surya(image_path: Path) -> str | None:
    try:
        from surya.ocr import run_ocr
        from surya.model.detection.model  import load_model as load_det
        from surya.model.recognition.model     import load_model as load_rec
        from surya.model.recognition.processor import load_processor as load_proc
        from PIL import Image

        img         = Image.open(image_path)
        det_model   = load_det()
        det_proc    = load_det()
        rec_model   = load_rec()
        rec_proc    = load_proc()
        predictions = run_ocr([img], [["en"]], det_model, det_proc, rec_model, rec_proc)
        return "\n".join(line.text for page in predictions for line in page.text_lines)
    except ImportError:
        return None
    except Exception as e:
        return f"[Surya OCR error: {e}]"


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APPLICATION
# ─────────────────────────────────────────────────────────────────────────────
class DocumentEngine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Document & OCR Engine v5.1")
        self.geometry("1100x750")
        self.configure(bg=BG)

        self.log_queue    = queue.Queue()
        self.is_processing = False

        # Variables
        self.selected_file   = tk.StringVar()
        self.batch_in_dir    = tk.StringVar()
        self.batch_out_dir   = tk.StringVar(
            value=str(Path.home() / "Documents" / "OCR_Output")
        )
        self.single_out_dir  = tk.StringVar()
        self.tesseract_path  = tk.StringVar(
            value=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        # Basic NLP
        self.do_grammar   = tk.BooleanVar(value=True)
        self.do_summary   = tk.BooleanVar(value=True)
        self.do_keywords  = tk.BooleanVar(value=True)

        # Advanced NLP
        self.use_ollama_summary   = tk.BooleanVar(value=False)
        self.use_keybert_keywords = tk.BooleanVar(value=False)
        self.ollama_model         = tk.StringVar(value="gemma2:9b")

        # OCR
        self.ocr_engine    = tk.StringVar(value="tesseract")
        self.ocr_lang      = tk.StringVar(value="eng")
        self.use_marker_pdf = tk.BooleanVar(value=False)

        self._build_ui()
        self._start_log_drain()
        self._refresh_ollama_models()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        hdr = tk.Frame(self, bg=PANEL, height=60)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="📄", font=(_FF, 22), bg=PANEL, fg=ACCENT).pack(side="left", padx=(20, 10))
        info = tk.Frame(hdr, bg=PANEL)
        info.pack(side="left")
        tk.Label(info, text="Document & OCR Engine", font=(_FF, 14, "bold"),
                 bg=PANEL, fg=TEXT).pack(anchor="w")
        tk.Label(info, text="PDF · Images · Scans → Markdown  |  Ollama · KeyBERT · Surya · marker-pdf",
                 font=FONT_SMALL, bg=PANEL, fg=TEXT_DIM).pack(anchor="w")

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)
        s = ttk.Style(self)
        s.theme_use("default")
        s.configure("TNotebook", background=BG, borderwidth=0, tabmargins=0)
        s.configure("TNotebook.Tab", background=PANEL, foreground=TEXT_DIM,
                    padding=[16, 9], font=FONT_HEAD, borderwidth=0)
        s.map("TNotebook.Tab", background=[("selected", CARD)],
              foreground=[("selected", TEXT)])

        self._tab_single()
        self._tab_batch()
        self._tab_settings()

        bar = tk.Frame(self, bg=PANEL, height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self.status_label = tk.Label(bar, text="Ready.", font=FONT_SMALL,
                                     bg=PANEL, fg=TEXT_DIM, anchor="w")
        self.status_label.pack(side="left", padx=16)
        self.progress = ttk.Progressbar(bar, mode="indeterminate", length=200)
        self.progress.pack(side="right", padx=16, pady=6)

    def _section(self, parent, text):
        f = tk.Frame(parent, bg=BG)
        f.pack(fill="x", padx=16, pady=(14, 3))
        tk.Frame(f, bg=ACCENT, width=3, height=16).pack(side="left")
        tk.Label(f, text=f"  {text}", font=FONT_HEAD, bg=BG, fg=TEXT).pack(side="left")

    def _card(self, parent):
        c = tk.Frame(parent, bg=CARD, padx=16, pady=12,
                     highlightbackground=BORDER, highlightthickness=1)
        c.pack(fill="x", padx=16, pady=3)
        return c

    def _dir_row(self, parent, label, var):
        row = tk.Frame(parent, bg=CARD)
        row.pack(fill="x", pady=3)
        tk.Label(row, text=label, font=FONT_SMALL, bg=CARD,
                 fg=TEXT_DIM, width=16, anchor="w").pack(side="left")
        tk.Entry(row, textvariable=var, bg=BG, fg=TEXT,
                 insertbackground=TEXT, relief="flat", font=FONT_MONO).pack(
            side="left", fill="x", expand=True)
        tk.Button(
            row, text="Browse", font=FONT_SMALL, bg=PANEL, fg=TEXT_DIM,
            relief="flat", cursor="hand2", padx=8,
            command=lambda: var.set(filedialog.askdirectory(title="Choose folder") or var.get()),
        ).pack(side="right")

    def _tab_single(self):
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text="  📄  Single File  ")

        left = tk.Frame(frame, bg=BG, width=430)
        left.pack(side="left", fill="y", padx=(18, 0), pady=16)
        left.pack_propagate(False)

        self._section(left, "1  ·  Select Document")
        src = self._card(left)
        tk.Label(src, text="Accepts: .pdf  .png  .jpg  .jpeg",
                 font=FONT_SMALL, bg=CARD, fg=TEXT_DIM).pack(anchor="w", pady=(0, 5))
        frow = tk.Frame(src, bg=CARD)
        frow.pack(fill="x")
        tk.Entry(frow, textvariable=self.selected_file,
                 bg=BG, fg=TEXT, font=FONT_MONO, relief="flat").pack(
            side="left", fill="x", expand=True, padx=(0, 6))
        tk.Button(
            frow, text="Browse", bg=ACCENT, fg="white", relief="flat",
            cursor="hand2", padx=10,
            command=lambda: self.selected_file.set(
                filedialog.askopenfilename(
                    filetypes=[("Documents", "*.pdf *.png *.jpg *.jpeg")]
                )
            ),
        ).pack(side="right")

        self._section(left, "2  ·  Basic NLP Options")
        opt = self._card(left)
        for txt, var in [
            ("📚 Clean Grammar (PySpellChecker)", self.do_grammar),
            ("🧠 Generate Summary (Extractive)", self.do_summary),
            ("🏷️ Extract Keywords (Frequency)", self.do_keywords),
        ]:
            tk.Checkbutton(opt, text=txt, variable=var, bg=CARD, fg=TEXT,
                           selectcolor=BG, font=FONT_SMALL, anchor="w",
                           cursor="hand2").pack(fill="x", pady=2)

        self._section(left, "3  ·  Advanced AI Options")
        adv = self._card(left)

        ol_row = tk.Frame(adv, bg=CARD)
        ol_row.pack(fill="x", pady=2)
        tk.Checkbutton(ol_row, text="Use Ollama for summary",
                       variable=self.use_ollama_summary, bg=CARD, fg=TEXT,
                       selectcolor=BG, font=FONT_SMALL).pack(side="left")
        self.ollama_status = tk.Label(ol_row, text="(checking…)",
                                      font=FONT_SMALL, bg=CARD, fg=TEXT_DIM)
        self.ollama_status.pack(side="left", padx=5)

        mod_row = tk.Frame(adv, bg=CARD)
        mod_row.pack(fill="x", pady=2)
        tk.Label(mod_row, text="Ollama model:",
                 font=FONT_SMALL, bg=CARD, fg=TEXT_DIM).pack(side="left")
        self.ollama_model_combo = ttk.Combobox(
            mod_row, textvariable=self.ollama_model, values=[],
            state="readonly", width=18,
        )
        self.ollama_model_combo.pack(side="left", padx=5)

        tk.Checkbutton(
            adv, text="Use KeyBERT for keywords (requires transformers)",
            variable=self.use_keybert_keywords, bg=CARD, fg=TEXT,
            selectcolor=BG, font=FONT_SMALL,
        ).pack(anchor="w", pady=2)

        self.after(100, self._update_ollama_status)

        self._section(left, "4  ·  Output Folder (optional)")
        out = self._card(left)
        self._dir_row(out, "Save to:", self.single_out_dir)
        tk.Label(out, text="If empty, saves next to input file.",
                 font=FONT_SMALL, bg=CARD, fg=TEXT_DIM).pack(anchor="w", pady=(0, 5))

        tk.Frame(left, bg=BG, height=12).pack()
        self.run_btn = tk.Button(
            left, text="  ▶   Process Document  ",
            font=(_FF, 13, "bold"), bg=SUCCESS, fg=BG, relief="flat",
            cursor="hand2", pady=14, command=self._run_single,
        )
        self.run_btn.pack(fill="x")

        right = tk.Frame(frame, bg=BG)
        right.pack(side="right", fill="both", expand=True, padx=16, pady=16)
        self._section(right, "Live Log")
        self.log_box = scrolledtext.ScrolledText(
            right, bg=PANEL, fg=ACCENT2, font=FONT_MONO, relief="flat",
            padx=14, pady=10,
        )
        self.log_box.pack(fill="both", expand=True, padx=16)
        for tag, col in [("err", ERROR), ("ok", SUCCESS), ("info", RUNNING), ("dim", TEXT_DIM)]:
            self.log_box.tag_config(tag, foreground=col)

    def _tab_batch(self):
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text="  📚  Batch Folder  ")

        left = tk.Frame(frame, bg=BG, width=450)
        left.pack(side="left", fill="y", padx=(18, 0), pady=16)
        left.pack_propagate(False)

        self._section(left, "Batch Process PDFs & Images")
        card = self._card(left)
        self._dir_row(card, "Input Folder:", self.batch_in_dir)
        self._dir_row(card, "Output Folder:", self.batch_out_dir)
        tk.Label(card, text="NLP options from Single File tab will be applied.",
                 font=FONT_SMALL, bg=CARD, fg=TEXT_DIM).pack(anchor="w", pady=10)

        self.batch_btn = tk.Button(
            left, text="  ▶   Process Entire Folder  ",
            font=(_FF, 13, "bold"), bg="#ff8c42", fg="white",
            relief="flat", cursor="hand2", pady=14, command=self._run_batch,
        )
        self.batch_btn.pack(fill="x")

        right = tk.Frame(frame, bg=BG)
        right.pack(side="right", fill="both", expand=True, padx=16, pady=16)
        self._section(right, "Batch Log")
        self.batch_log = scrolledtext.ScrolledText(
            right, bg=PANEL, fg=ACCENT2, font=FONT_MONO,
            relief="flat", padx=14, pady=10,
        )
        self.batch_log.pack(fill="both", expand=True, padx=16)
        for tag, col in [("err", ERROR), ("ok", SUCCESS), ("info", RUNNING)]:
            self.batch_log.tag_config(tag, foreground=col)

    def _tab_settings(self):
        frame = tk.Frame(self.nb, bg=BG)
        self.nb.add(frame, text="  ⚙  Settings  ")

        canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        scroll = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner  = tk.Frame(canvas, bg=BG)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self._section(inner, "Tesseract OCR Path")
        c1 = self._card(inner)
        tk.Entry(c1, textvariable=self.tesseract_path,
                 bg=BG, fg=TEXT, font=FONT_MONO, relief="flat").pack(fill="x", pady=5)
        tk.Label(c1, text="Required for Tesseract OCR.",
                 font=FONT_SMALL, bg=CARD, fg=TEXT_DIM).pack(anchor="w")

        self._section(inner, "OCR Engine")
        c2 = self._card(inner)
        ocr_fr = tk.Frame(c2, bg=CARD)
        ocr_fr.pack(fill="x", pady=5)
        tk.Label(ocr_fr, text="Engine:", font=FONT_SMALL,
                 bg=CARD, fg=TEXT_DIM).pack(side="left")
        ttk.Combobox(
            ocr_fr, textvariable=self.ocr_engine,
            values=["tesseract", "surya", "tesseract (fallback to surya)"],
            state="readonly", width=28,
        ).pack(side="left", padx=10)
        tk.Label(c2, text="Language code (Tesseract):",
                 font=FONT_SMALL, bg=CARD, fg=TEXT_DIM).pack(anchor="w", pady=(5, 0))
        tk.Entry(c2, textvariable=self.ocr_lang, bg=BG, fg=TEXT, width=10).pack(anchor="w")

        self._section(inner, "Advanced PDF Extraction")
        c3 = self._card(inner)
        tk.Checkbutton(
            c3, text="Use marker-pdf for PDFs (AI-powered, requires marker-pdf)",
            variable=self.use_marker_pdf, bg=CARD, fg=TEXT, selectcolor=BG,
        ).pack(anchor="w")
        tk.Label(
            c3, text="If enabled, PDFs are processed with marker-pdf instead of pdfplumber.",
            font=FONT_SMALL, bg=CARD, fg=TEXT_DIM, wraplength=400, justify="left",
        ).pack(anchor="w", pady=5)

        self._section(inner, "Ollama Models")
        c4 = self._card(inner)
        tk.Button(
            c4, text="Refresh Ollama Model List",
            command=self._refresh_ollama_models,
            bg=PANEL, fg=TEXT, relief="flat", padx=10,
        ).pack(anchor="w")

        tk.Frame(inner, bg=BG, height=20).pack()

    # ── Logic ─────────────────────────────────────────────────────────────────
    def log(self, tag, msg, box="single"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_queue.put((tag, f"[{ts}]  {msg}\n", box))

    def _start_log_drain(self):
        def drain():
            try:
                while True:
                    tag, msg, box = self.log_queue.get_nowait()
                    target = self.log_box if box == "single" else self.batch_log
                    target.insert("end", msg, tag)
                    target.see("end")
            except queue.Empty:
                pass
            self.after(80, drain)
        self.after(80, drain)

    def _refresh_ollama_models(self):
        def fetch():
            models = get_ollama_models()
            if models:
                self.after(0, lambda: self.ollama_model_combo.configure(values=models))
                if self.ollama_model.get() not in models:
                    self.after(0, lambda: self.ollama_model.set(models[0]))
        threading.Thread(target=fetch, daemon=True).start()

    def _update_ollama_status(self):
        def check():
            running = check_ollama_running()
            self.after(0, lambda: self.ollama_status.config(
                text="✓ running" if running else "✗ not running",
                fg=SUCCESS if running else ERROR,
            ))
            if running:
                self._refresh_ollama_models()
        threading.Thread(target=check, daemon=True).start()
        self.after(5000, self._update_ollama_status)

    def _run_single(self):
        src = self.selected_file.get().strip()
        if not src or not Path(src).exists():
            return messagebox.showerror("Error", "Invalid file.")
        if self.is_processing:
            return
        self.is_processing = True
        self.progress.start(12)
        self.status_label.config(text="Processing Document…")

        out_dir = self.single_out_dir.get().strip() or str(Path(src).parent)
        Path(out_dir).mkdir(parents=True, exist_ok=True)

        threading.Thread(
            target=self._process_doc, args=(Path(src), out_dir, "single"), daemon=True
        ).start()

    def _run_batch(self):
        in_dir  = self.batch_in_dir.get().strip()
        out_dir = self.batch_out_dir.get().strip()
        if not in_dir or not Path(in_dir).exists():
            return messagebox.showerror("Error", "Invalid input folder.")
        if self.is_processing:
            return
        self.is_processing = True
        self.progress.start(12)
        self.status_label.config(text="Running Batch OCR…")
        threading.Thread(
            target=self._batch_thread, args=(Path(in_dir), Path(out_dir)), daemon=True
        ).start()

    def _batch_thread(self, in_path: Path, out_path: Path):
        out_path.mkdir(parents=True, exist_ok=True)
        files = [f for f in in_path.rglob("*")
                 if f.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg"}]
        self.log("info", f"Found {len(files)} files to process.\n", "batch")
        for i, file in enumerate(files, 1):
            self.log("dim", f"[{i}/{len(files)}] Processing {file.name}…", "batch")
            self._process_doc(file, str(out_path), "batch")
        self.is_processing = False
        self.progress.stop()
        self.status_label.config(text="Batch Complete.")
        self.log("ok", "\n✅ Batch Processing Complete!", "batch")

    def _process_doc(self, src: Path, out_dir: str, log_box: str):
        try:
            raw_text = ""
            ext = src.suffix.lower()

            if ext == ".pdf":
                if self.use_marker_pdf.get():
                    try:
                        from marker.convert import convert_single_pdf
                        from marker.models  import load_all_models
                        self.log("info", "Using marker-pdf…", log_box)
                        raw_text, _, _ = convert_single_pdf(str(src), load_all_models())
                    except ImportError:
                        self.log("err", "marker-pdf not installed. Run: pip install marker-pdf", log_box)
                        return
                    except Exception as e:
                        self.log("err", f"marker-pdf error: {e} — falling back.", log_box)
                        raw_text = ""

                if not raw_text:
                    self.log("dim", "Reading PDF with pdfplumber…", log_box)
                    import pdfplumber
                    with pdfplumber.open(src) as pdf:
                        for page in pdf.pages:
                            t = page.extract_text()
                            if t:
                                raw_text += t + "\n"

                    if len(raw_text.strip()) < 50:
                        self.log("info", "PDF appears scanned — running OCR…", log_box)
                        try:
                            import fitz                        # PyMuPDF
                            from PIL import Image              # ← now properly available
                            doc = fitz.open(src)
                            for page in doc:
                                pix  = page.get_pixmap()
                                img  = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                                tmp  = Path(tempfile.gettempdir()) / f"tmp_page_{page.number}.png"
                                img.save(tmp)
                                raw_text += (self._ocr_image(tmp, log_box) or "") + "\n"
                                tmp.unlink(missing_ok=True)
                        except ImportError:
                            self.log("err", "pymupdf required for scanned PDFs.", log_box)
                            return
            else:
                self.log("dim", "Running OCR on image…", log_box)
                raw_text = self._ocr_image(src, log_box) or ""

            if not raw_text.strip():
                self.log("err", f"No text extracted from {src.name}", log_box)
                return

            if self.do_grammar.get():
                self.log("dim", "Cleaning grammar…", log_box)
                raw_text = clean_grammar(raw_text)

            summary = ""
            if self.do_summary.get():
                if self.use_ollama_summary.get() and check_ollama_running():
                    self.log("info", f"Ollama summary ({self.ollama_model.get()})…", log_box)
                    summary = ollama_summarize(raw_text, self.ollama_model.get()) or \
                              pure_python_summarize(raw_text)
                else:
                    summary = pure_python_summarize(raw_text)

            keywords = []
            if self.do_keywords.get():
                if self.use_keybert_keywords.get():
                    keywords = keybert_keywords(raw_text) or extract_keywords(raw_text)
                else:
                    keywords = extract_keywords(raw_text)

            final_file = Path(out_dir) / f"{src.stem}_formatted.md"
            content  = f"# {src.stem}\n\n"
            if keywords:
                content += f"## Tags\n`{'` `'.join(keywords)}`\n\n"
            if summary:
                content += f"## Summary\n{summary}\n\n---\n"
            content += f"## Full Text\n\n{raw_text}"
            final_file.write_text(content, encoding="utf-8")
            self.log("ok", f"✓ Saved: {final_file.name}", log_box)

        except Exception as e:
            self.log("err", f"✗ Error processing {src.name}: {e}", log_box)
        finally:
            if log_box == "single":
                self.is_processing = False
                self.progress.stop()
                self.status_label.config(text="Done.")

    def _ocr_image(self, image_path: Path, log_box: str) -> str:
        engine = self.ocr_engine.get()
        tess   = self.tesseract_path.get().strip()
        lang   = self.ocr_lang.get().strip() or "eng"

        if engine == "tesseract":
            try:
                return ocr_with_tesseract(image_path, tess, lang)
            except Exception as e:
                self.log("err", f"Tesseract error: {e}", log_box)
                return ""

        elif engine == "surya":
            result = ocr_with_surya(image_path)
            if result is None:
                self.log("err", "Surya OCR failed (not installed?).", log_box)
                return ""
            return result

        else:   # tesseract with surya fallback
            try:
                text = ocr_with_tesseract(image_path, tess, lang)
                if text.strip():
                    return text
                self.log("info", "Tesseract returned nothing — trying Surya…", log_box)
            except Exception as e:
                self.log("err", f"Tesseract error: {e} — trying Surya…", log_box)
            result = ocr_with_surya(image_path)
            if result is None:
                self.log("err", "Surya also failed.", log_box)
                return ""
            return result


if __name__ == "__main__":
    app = DocumentEngine()
    app.mainloop()
