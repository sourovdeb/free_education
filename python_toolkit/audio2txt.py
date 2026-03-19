#!/usr/bin/env python3
"""
Writer & Teacher Audio/Video Transcriber Engine (v5.1)
- Intel GPU acceleration via Optimum-Intel + OpenVINO
- All previous features: YouTube, live recording, batch, NLP, Ollama, KeyBERT
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import tempfile
import re
import platform
import queue
import json
import urllib.request
from pathlib import Path
from datetime import datetime
from collections import Counter

# --- Windows DPI fix ---
if platform.system() == "Windows":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

# --- COLORS ---
BG, PANEL, CARD, BORDER = "#0d0d14", "#13131f", "#1a1a2c", "#2a2a40"
ACCENT, ACCENT2, TEXT, TEXT_DIM = "#ff4d6d", "#4d9fff", "#e8e8f0", "#6b6b8a"
SUCCESS, ERROR, RUNNING = "#3ddc97", "#ff4d6d", "#4d9fff"
WARNING = "#f5a623"

# ----------------------------------------------------------------------
#  NATIVE NLP (fallbacks)
# ----------------------------------------------------------------------
STOPWORDS = set(["the", "a", "an", "is", "are", "was", "were", "and", "but", "not", "for", "with", "that", "this", "from", "they", "them", "their", "it", "in", "on", "of", "to", "i", "you", "we"])

def get_keywords(text, n=5):
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    return [word for word, _ in Counter(filtered).most_common(n)]

def get_summary(text, count=5):
    sents = re.split(r'(?<=[.!?])\s+', text)
    if len(sents) <= count:
        return text
    freq = Counter(re.findall(r'\b[a-z]{4,}\b', text.lower()))
    max_f = max(freq.values()) if freq else 1
    scores = []
    for s in sents:
        s_words = re.findall(r'\b[a-z]{4,}\b', s.lower())
        score = sum(freq.get(w, 0) / max_f for w in s_words if w not in STOPWORDS)
        scores.append((score, s))
    top = sorted(scores, key=lambda x: x[0], reverse=True)[:count]
    return " ".join([s for _, s in sorted(top, key=lambda x: sents.index(x[1]))])

# ----------------------------------------------------------------------
#  ADVANCED NLP HELPERS (Ollama, KeyBERT)
# ----------------------------------------------------------------------
def check_ollama_running() -> bool:
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=2)
        return True
    except Exception:
        return False

def ollama_summarize(text: str, model: str, prompt: str = None) -> str:
    if not prompt:
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
    except Exception:
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

# ----------------------------------------------------------------------
#  HELPER: check if a Python package is installed
# ----------------------------------------------------------------------
def is_installed(package_name: str) -> bool:
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

# ----------------------------------------------------------------------
#  INTEL OPENVINO TRANSCRIPTION (via Optimum-Intel)
# ----------------------------------------------------------------------
def transcribe_with_openvino(audio_path: Path, model_size: str) -> str:
    """
    Transcribe using Intel Optimum with OpenVINO backend.
    Falls back to CPU if GPU unavailable.
    """
    try:
        from optimum.intel import OVModelForSpeechSeq2Seq
        from transformers import AutoProcessor, pipeline
        import torch
    except ImportError as e:
        raise ImportError("Optimum-Intel not installed. Run: pip install optimum[openvino]") from e

    # Map model names to Hugging Face IDs
    model_id = f"openai/whisper-{model_size}"
    if model_size == "large-v3":
        model_id = "openai/whisper-large-v3"

    # Load processor
    processor = AutoProcessor.from_pretrained(model_id)

    # Load model with OpenVINO (export on first use)
    # device="GPU" tries to use Intel GPU, falls back to CPU
    model = OVModelForSpeechSeq2Seq.from_pretrained(
        model_id,
        export=True,
        device="GPU",          # will use Intel GPU if available
        compile=True,
        ov_config={"PERFORMANCE_HINT": "LATENCY", "INFERENCE_PRECISION_HINT": "f32"}
    )

    # Create pipeline
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        chunk_length_s=30,
        batch_size=16,          # adjust based on your GPU memory
    )

    # Run transcription
    result = pipe(str(audio_path), return_timestamps=False)
    return result["text"]

# ----------------------------------------------------------------------
#  MAIN APP
# ----------------------------------------------------------------------
class TranscriberEngine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio/Video Transcriber Engine v5.1 (Intel GPU)")
        self.geometry("1150x800")
        self.configure(bg=BG)

        # PATH VARIABLES
        self.selected_file = tk.StringVar()
        self.batch_in_dir = tk.StringVar()
        self.master_out_dir = tk.StringVar(value=str(Path.home() / "Documents" / "Media_Pipeline_Output"))
        self.ffmpeg_path = tk.StringVar(value=r"C:\ffmpeg\bin\ffmpeg.exe")
        
        # TRANSCRIPTION ENGINE - now with Intel option
        self.transcription_engine = tk.StringVar(value="faster-whisper")
        self.whisper_model = tk.StringVar(value="base")
        self.kw_count = tk.IntVar(value=5)
        self.sum_len = tk.IntVar(value=5)

        # ADVANCED NLP
        self.use_ollama_summary = tk.BooleanVar(value=False)
        self.use_keybert_keywords = tk.BooleanVar(value=False)
        self.ollama_model = tk.StringVar(value="gemma2:9b")

        # AUDIO PREPROCESSING
        self.use_noise_reduction = tk.BooleanVar(value=False)
        self.ffmpeg_filter = tk.StringVar(value="-af afftdn=nf=-25")

        # YOUTUBE DOWNLOAD
        self.yt_url = tk.StringVar()

        # RECORDING
        self.recording = False
        self.rec_thread = None

        self.log_queue = queue.Queue()
        self.is_processing = False
        self._build_ui()
        self._start_log_drain()

    def _build_ui(self):
        # HEADER
        hdr = tk.Frame(self, bg=PANEL, height=60)
        hdr.pack(fill="x", side="top")
        tk.Label(hdr, text="🎙️ Writer & Teacher Transcriber Engine (Intel GPU)", 
                 font=("Arial", 14, "bold"), bg=PANEL, fg=TEXT).pack(side="left", padx=20)

        # NOTEBOOK
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        # --- TAB: SINGLE FILE ---
        self.tab_single = tk.Frame(self.nb, bg=BG)
        self.nb.add(self.tab_single, text=" Single File ")
        
        paned_s = tk.PanedWindow(self.tab_single, orient="horizontal", bg=BG, sashwidth=4)
        paned_s.pack(fill="both", expand=True)
        left_s = tk.Frame(paned_s, bg=BG, width=450)
        right_s = tk.Frame(paned_s, bg=BG)
        paned_s.add(left_s)
        paned_s.add(right_s)

        # --- Input methods ---
        tk.Label(left_s, text="Input Source", font=("Arial", 11, "bold"), bg=BG, fg=TEXT).pack(anchor="w", padx=20, pady=(20,5))
        card_input = tk.Frame(left_s, bg=CARD, pady=15, padx=15, highlightthickness=1, highlightbackground=BORDER)
        card_input.pack(fill="x", padx=20)

        # File selection
        tk.Label(card_input, text="Local file:", font=("Arial", 9), bg=CARD, fg=TEXT_DIM).pack(anchor="w")
        frow = tk.Frame(card_input, bg=CARD)
        frow.pack(fill="x", pady=2)
        tk.Entry(frow, textvariable=self.selected_file, bg=BG, fg=TEXT, relief="flat").pack(side="left", fill="x", expand=True)
        tk.Button(frow, text="Browse", bg=ACCENT, fg="white", relief="flat", command=self._browse_single).pack(side="right")

        # YouTube URL (if yt-dlp installed)
        if is_installed("yt_dlp"):
            tk.Label(card_input, text="YouTube URL:", font=("Arial", 9), bg=CARD, fg=TEXT_DIM).pack(anchor="w", pady=(10,0))
            yt_row = tk.Frame(card_input, bg=CARD)
            yt_row.pack(fill="x", pady=2)
            tk.Entry(yt_row, textvariable=self.yt_url, bg=BG, fg=TEXT, relief="flat").pack(side="left", fill="x", expand=True)
            tk.Button(yt_row, text="Download & Transcribe", bg=ACCENT2, fg=BG, relief="flat",
                      command=self._download_and_transcribe).pack(side="right")

        # Live recording (if sounddevice installed)
        if is_installed("sounddevice"):
            rec_row = tk.Frame(card_input, bg=CARD)
            rec_row.pack(fill="x", pady=(10,0))
            self.rec_btn = tk.Button(rec_row, text="🔴 Start Recording", bg=ERROR, fg="white", relief="flat",
                                      command=self._toggle_record)
            self.rec_btn.pack(side="left", padx=(0,10))
            tk.Label(rec_row, text="Click to record from microphone", font=("Arial", 9), bg=CARD, fg=TEXT_DIM).pack(side="left")

        # --- Transcription Options ---
        tk.Label(left_s, text="Transcription Options", font=("Arial", 11, "bold"), bg=BG, fg=TEXT).pack(anchor="w", padx=20, pady=(15,5))
        card_trans = tk.Frame(left_s, bg=CARD, pady=15, padx=15, highlightthickness=1, highlightbackground=BORDER)
        card_trans.pack(fill="x", padx=20)

        # Engine selection (now with Intel OpenVINO)
        eng_row = tk.Frame(card_trans, bg=CARD)
        eng_row.pack(fill="x", pady=2)
        tk.Label(eng_row, text="Engine:", font=("Arial", 9), bg=CARD, fg=TEXT_DIM).pack(side="left")
        self.engine_combo = ttk.Combobox(eng_row, textvariable=self.transcription_engine,
                                         values=["faster-whisper (NVIDIA)", 
                                                 "openai-whisper (CPU)",
                                                 "intel-openvino (Intel GPU/CPU)"], 
                                         state="readonly", width=25)
        self.engine_combo.pack(side="left", padx=10)

        # Whisper model
        mod_row = tk.Frame(card_trans, bg=CARD)
        mod_row.pack(fill="x", pady=2)
        tk.Label(mod_row, text="Model size:", font=("Arial", 9), bg=CARD, fg=TEXT_DIM).pack(side="left")
        self.model_combo = ttk.Combobox(mod_row, textvariable=self.whisper_model,
                                        values=["tiny", "base", "small", "medium", "large-v3"],
                                        state="readonly", width=12)
        self.model_combo.pack(side="left", padx=10)

        # Noise reduction
        nr_row = tk.Frame(card_trans, bg=CARD)
        nr_row.pack(fill="x", pady=2)
        tk.Checkbutton(nr_row, text="Enable noise reduction (ffmpeg afftdn)", variable=self.use_noise_reduction,
                       bg=CARD, fg=TEXT, selectcolor=BG).pack(side="left")

        # --- NLP Options (Basic + Advanced) ---
        tk.Label(left_s, text="NLP Options", font=("Arial", 11, "bold"), bg=BG, fg=TEXT).pack(anchor="w", padx=20, pady=(15,5))
        card_nlp = tk.Frame(left_s, bg=CARD, pady=15, padx=15, highlightthickness=1, highlightbackground=BORDER)
        card_nlp.pack(fill="x", padx=20)

        # Basic NLP counts
        cnt_row = tk.Frame(card_nlp, bg=CARD)
        cnt_row.pack(fill="x", pady=2)
        tk.Label(cnt_row, text="Keywords:", bg=CARD, fg=TEXT_DIM).pack(side="left")
        tk.Spinbox(cnt_row, from_=1, to=10, textvariable=self.kw_count, width=5).pack(side="left", padx=10)
        tk.Label(cnt_row, text="Summary sentences:", bg=CARD, fg=TEXT_DIM).pack(side="left", padx=10)
        tk.Spinbox(cnt_row, from_=1, to=15, textvariable=self.sum_len, width=5).pack(side="left")

        # Advanced NLP (Ollama, KeyBERT)
        adv_frame = tk.Frame(card_nlp, bg=CARD)
        adv_frame.pack(fill="x", pady=5)

        # Ollama
        ol_row = tk.Frame(adv_frame, bg=CARD)
        ol_row.pack(fill="x")
        self.ollama_cb = tk.Checkbutton(ol_row, text="Use Ollama for summary", variable=self.use_ollama_summary,
                                        bg=CARD, fg=TEXT, selectcolor=BG)
        self.ollama_cb.pack(side="left")
        self.ollama_status = tk.Label(ol_row, text="(checking...)", font=("Arial", 8), bg=CARD, fg=TEXT_DIM)
        self.ollama_status.pack(side="left", padx=5)

        mod_row2 = tk.Frame(adv_frame, bg=CARD)
        mod_row2.pack(fill="x")
        tk.Label(mod_row2, text="Ollama model:", bg=CARD, fg=TEXT_DIM).pack(side="left")
        self.ollama_model_combo = ttk.Combobox(mod_row2, textvariable=self.ollama_model,
                                               values=["gemma2:9b", "mistral-nemo", "llama3.2:3b", "phi3.5", "qwen2.5:7b"],
                                               state="readonly", width=15)
        self.ollama_model_combo.pack(side="left", padx=5)

        # KeyBERT
        kb_row = tk.Frame(adv_frame, bg=CARD)
        kb_row.pack(fill="x")
        self.keybert_cb = tk.Checkbutton(kb_row, text="Use KeyBERT for keywords (requires transformers)",
                                          variable=self.use_keybert_keywords, bg=CARD, fg=TEXT, selectcolor=BG)
        self.keybert_cb.pack(side="left")

        # --- Run button ---
        self.run_btn = tk.Button(left_s, text="▶ TRANSCRIBE", bg=SUCCESS, fg=BG, font=("Arial", 11, "bold"),
                                 pady=15, command=self._run_single)
        self.run_btn.pack(fill="x", padx=20, pady=20)

        # Right side: log
        self.log_box = scrolledtext.ScrolledText(right_s, bg=PANEL, fg=ACCENT2, font=("Courier New", 10), relief="flat")
        self.log_box.pack(fill="both", expand=True, padx=20, pady=20)

        # --- TAB: BATCH FOLDER ---
        self.tab_batch = tk.Frame(self.nb, bg=BG)
        self.nb.add(self.tab_batch, text=" Batch Folder ")
        
        paned_b = tk.PanedWindow(self.tab_batch, orient="horizontal", bg=BG, sashwidth=4)
        paned_b.pack(fill="both", expand=True)
        left_b = tk.Frame(paned_b, bg=BG, width=400)
        right_b = tk.Frame(paned_b, bg=BG)
        paned_b.add(left_b)
        paned_b.add(right_b)

        tk.Label(left_b, text="Batch Source Folder", font=("Arial", 11, "bold"), bg=BG, fg=TEXT).pack(anchor="w", padx=20, pady=(20,5))
        card_b = tk.Frame(left_b, bg=CARD, pady=15, padx=15, highlightthickness=1, highlightbackground=BORDER)
        card_b.pack(fill="x", padx=20)
        tk.Entry(card_b, textvariable=self.batch_in_dir, bg=BG, fg=TEXT, relief="flat").pack(fill="x", pady=5)
        tk.Button(card_b, text="Select Folder", bg=ACCENT, fg="white", relief="flat", command=self._browse_batch_in).pack(anchor="e")

        tk.Button(left_b, text="▶ RUN BATCH PROCESS", bg="#ff8c42", fg="white", font=("Arial", 11, "bold"),
                  pady=15, command=self._run_batch).pack(fill="x", padx=20, pady=20)
        self.batch_log = scrolledtext.ScrolledText(right_b, bg=PANEL, fg=ACCENT2, font=("Courier New", 10), relief="flat")
        self.batch_log.pack(fill="both", expand=True, padx=20, pady=20)

        # --- TAB: SETTINGS ---
        self.tab_set = tk.Frame(self.nb, bg=BG)
        self.nb.add(self.tab_set, text=" Settings ")
        
        canvas = tk.Canvas(self.tab_set, bg=BG, highlightthickness=0)
        scroll = tk.Scrollbar(self.tab_set, orient="vertical", command=canvas.yview)
        inner_frame = tk.Frame(canvas, bg=BG)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.create_window((0,0), window=inner_frame, anchor="nw")
        inner_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Basic Settings
        card_set = tk.Frame(inner_frame, bg=CARD, pady=30, padx=30, highlightthickness=1, highlightbackground=BORDER)
        card_set.pack(fill="x", padx=50, pady=20)

        tk.Label(card_set, text="Master Output Directory", font=("Arial", 11, "bold"), bg=CARD, fg=TEXT).pack(anchor="w")
        tk.Entry(card_set, textvariable=self.master_out_dir, bg=BG, fg=TEXT, width=80).pack(pady=5)
        tk.Button(card_set, text="Browse", bg=PANEL, fg=TEXT, command=self._browse_master_out).pack(anchor="w")

        tk.Label(card_set, text="\nFFmpeg Executable Path", font=("Arial", 11, "bold"), bg=CARD, fg=TEXT).pack(anchor="w")
        tk.Entry(card_set, textvariable=self.ffmpeg_path, bg=BG, fg=TEXT, width=80).pack(pady=5)

        tk.Label(card_set, text="\nNoise Reduction Filter", font=("Arial", 11, "bold"), bg=CARD, fg=TEXT).pack(anchor="w")
        tk.Entry(card_set, textvariable=self.ffmpeg_filter, bg=BG, fg=TEXT, width=80).pack(pady=5)

        # Intel GPU info (if optimum installed)
        tk.Label(card_set, text="\nIntel GPU Acceleration", font=("Arial", 11, "bold"), bg=CARD, fg=ACCENT2).pack(anchor="w", pady=(10,0))
        try:
            import intel_extension_for_pytorch as ipex
            tk.Label(card_set, text=f"Intel Extension for PyTorch: installed", 
                    font=("Arial", 9), bg=CARD, fg=SUCCESS).pack(anchor="w")
        except ImportError:
            tk.Label(card_set, text="Intel Extension for PyTorch not installed.", 
                    font=("Arial", 9), bg=CARD, fg=ERROR).pack(anchor="w")
            tk.Label(card_set, text="Run: pip install intel-extension-for-pytorch optimum[openvino]", 
                    font=("Arial", 8), bg=CARD, fg=TEXT_DIM).pack(anchor="w")

        # Start checking Ollama status
        self.after(1000, self._update_ollama_status)

    # --- BROWSE ACTIONS (unchanged) ---
    def _browse_single(self):
        f = filedialog.askopenfilename(filetypes=[("Media Files", "*.mp3 *.mp4 *.wav *.m4a *.mkv *.ogg *.webm *.mov *.avi *.flac")])
        if f: self.selected_file.set(f)

    def _browse_batch_in(self):
        d = filedialog.askdirectory()
        if d: self.batch_in_dir.set(d)

    def _browse_master_out(self):
        d = filedialog.askdirectory()
        if d: self.master_out_dir.set(d)

    # --- YOUTUBE DOWNLOAD (unchanged) ---
    def _download_and_transcribe(self):
        url = self.yt_url.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Enter a YouTube URL.")
            return
        threading.Thread(target=self._yt_download_thread, args=(url,), daemon=True).start()

    def _yt_download_thread(self, url):
        self.log("Downloading video from YouTube...", "single")
        try:
            import yt_dlp
        except ImportError:
            self.log("✗ yt-dlp not installed. Run: pip install yt-dlp", "single")
            return

        out_template = str(Path(tempfile.gettempdir()) / "%(title)s.%(ext)s")
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
            'outtmpl': out_template,
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                wav_file = Path(filename).with_suffix('.wav')
                if not wav_file.exists():
                    for f in Path(tempfile.gettempdir()).glob(f"{info['title']}*"):
                        if f.suffix in ['.wav', '.mp3', '.m4a']:
                            wav_file = f
                            break
                self.log(f"Downloaded: {wav_file.name}", "single")
                self.selected_file.set(str(wav_file))
                self._run_single()
        except Exception as e:
            self.log(f"✗ YouTube download error: {e}", "single")

    # --- RECORDING (unchanged) ---
    def _toggle_record(self):
        if not self.recording:
            self._start_record()
        else:
            self._stop_record()

    def _start_record(self):
        try:
            import sounddevice as sd
            import numpy as np
            import wave
        except ImportError:
            self.log("✗ sounddevice not installed. Run: pip install sounddevice numpy", "single")
            return

        self.recording = True
        self.rec_btn.config(text="⏹ Stop Recording", bg=WARNING)
        self.log("Recording started... Speak into microphone.", "single")
        self.rec_thread = threading.Thread(target=self._record_thread, daemon=True)
        self.rec_thread.start()

    def _record_thread(self):
        import sounddevice as sd
        import numpy as np
        import wave

        fs = 16000
        seconds = 3600
        recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        while self.recording:
            sd.sleep(100)
        sd.stop()
        temp_wav = Path(tempfile.gettempdir()) / f"recording_{datetime.now():%Y%m%d_%H%M%S}.wav"
        with wave.open(str(temp_wav), 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(fs)
            wf.writeframes(recording[:int(sd.portaudio.read().samples_available)].tobytes())
        self.selected_file.set(str(temp_wav))
        self.log(f"Recording saved: {temp_wav.name}", "single")
        self.rec_btn.config(text="🔴 Start Recording", bg=ERROR)

    def _stop_record(self):
        self.recording = False
        self.log("Recording stopped.", "single")

    # --- LOGIC ---
    def log(self, msg, box="single"):
        self.log_queue.put((f"[{datetime.now():%H:%M:%S}] {msg}\n", box))

    def _start_log_drain(self):
        try:
            while True:
                m, b = self.log_queue.get_nowait()
                target = self.log_box if b == "single" else self.batch_log
                target.insert("end", m)
                target.see("end")
        except queue.Empty:
            pass
        self.after(100, self._start_log_drain)

    def _update_ollama_status(self):
        def check():
            running = check_ollama_running()
            self.after(0, lambda: self.ollama_status.config(
                text="✓ running" if running else "✗ not running",
                fg=SUCCESS if running else ERROR
            ))
        threading.Thread(target=check, daemon=True).start()
        self.after(5000, self._update_ollama_status)

    def _run_single(self):
        src = self.selected_file.get()
        if not src:
            messagebox.showwarning("Warning", "Select a media file or use YouTube/record first.")
            return
        threading.Thread(target=self._process, args=(Path(src), "single"), daemon=True).start()

    def _run_batch(self):
        d = self.batch_in_dir.get()
        if not d:
            messagebox.showwarning("Warning", "Select an input folder first.")
            return
        threading.Thread(target=self._batch_thread, args=(Path(d),), daemon=True).start()

    def _batch_thread(self, in_p):
        exts = {".mp3", ".mp4", ".wav", ".m4a", ".mkv", ".ogg", ".webm", ".mov", ".avi", ".flac"}
        files = [f for f in in_p.rglob("*") if f.suffix.lower() in exts]
        self.log(f"Found {len(files)} media files.", "batch")
        for f in files:
            self._process(f, "batch")
        self.log("All batch transcriptions complete.", "batch")

    def _process(self, src: Path, box: str):
        try:
            self.log(f"Processing: {src.name}...", box)

            # Step 1: Extract/clean audio with FFmpeg
            self.log("Extracting audio with FFmpeg...", box)
            temp_wav = Path(tempfile.gettempdir()) / f"temp_{src.stem}.wav"
            ffmpeg_cmd = self.ffmpeg_path.get().strip()
            if not Path(ffmpeg_cmd).exists():
                self.log("✗ FFmpeg not found. Check path in Settings.", box)
                return

            cmd = [ffmpeg_cmd, "-y", "-i", str(src), "-ar", "16000", "-ac", "1"]
            if self.use_noise_reduction.get():
                filter_str = self.ffmpeg_filter.get().strip()
                if filter_str:
                    cmd.extend(filter_str.split())
            cmd.append(str(temp_wav))

            result = subprocess.run(cmd, capture_output=True)
            if result.returncode != 0:
                self.log(f"✗ FFmpeg error: {result.stderr.decode()[:200]}", box)
                return

            # Step 2: Transcribe with selected engine
            engine_display = self.transcription_engine.get()
            raw_text = ""

            # Map display name to internal engine
            if "intel" in engine_display.lower():
                engine = "intel-openvino"
            elif "faster" in engine_display.lower():
                engine = "faster-whisper"
            else:
                engine = "openai-whisper"

            if engine == "intel-openvino":
                self.log("Using Intel OpenVINO (Optimum) for transcription...", box)
                try:
                    raw_text = transcribe_with_openvino(temp_wav, self.whisper_model.get())
                except ImportError as e:
                    self.log(f"OpenVINO not installed: {e}. Falling back to CPU.", box)
                    engine = "openai-whisper"
                except Exception as e:
                    self.log(f"OpenVINO error: {e}, falling back to CPU.", box)
                    engine = "openai-whisper"

            if engine == "faster-whisper":
                try:
                    from faster_whisper import WhisperModel
                    model = WhisperModel(self.whisper_model.get(), device="cpu", compute_type="int8")
                    segments, info = model.transcribe(str(temp_wav))
                    self.log(f"Detected language: {info.language}", box)
                    raw_text = " ".join([s.text.strip() for s in segments])
                except ImportError:
                    self.log("faster-whisper not installed, falling back to openai-whisper.", box)
                    engine = "openai-whisper"
                except Exception as e:
                    self.log(f"faster-whisper error: {e}, falling back.", box)
                    engine = "openai-whisper"

            if engine == "openai-whisper" or (engine == "faster-whisper" and not raw_text):
                try:
                    import whisper
                    model = whisper.load_model(self.whisper_model.get())
                    result = model.transcribe(str(temp_wav))
                    raw_text = result["text"].strip()
                except ImportError:
                    self.log("✗ openai-whisper not installed.", box)
                    return
                except Exception as e:
                    self.log(f"openai-whisper error: {e}", box)
                    return

            if not raw_text:
                self.log("✗ No speech detected.", box)
                return

            # Step 3: NLP
            self.log("Generating summary & keywords...", box)

            # Summarization
            if self.use_ollama_summary.get() and check_ollama_running():
                summary = ollama_summarize(raw_text, self.ollama_model.get())
                if not summary:
                    self.log("Ollama summary failed, using native.", box)
                    summary = get_summary(raw_text, self.sum_len.get())
            else:
                summary = get_summary(raw_text, self.sum_len.get())

            # Keywords
            if self.use_keybert_keywords.get():
                try:
                    tags = keybert_keywords(raw_text, self.kw_count.get())
                    if not tags:
                        tags = get_keywords(raw_text, self.kw_count.get())
                except ImportError:
                    tags = get_keywords(raw_text, self.kw_count.get())
            else:
                tags = get_keywords(raw_text, self.kw_count.get())

            # Step 4: Write output
            out_root = Path(self.master_out_dir.get())
            out_root.mkdir(parents=True, exist_ok=True)
            final_md = out_root / f"{src.stem}_transcript.md"
            
            # Add hardware info to output
            hw_info = engine_display
            
            final_md.write_text(
                f"# {src.stem}\n\n"
                f"**Hardware:** {hw_info}\n\n"
                f"**Tags:** {tags}\n\n"
                f"**Summary:** {summary}\n\n"
                f"---\n\n"
                f"{raw_text}",
                encoding="utf-8"
            )
            self.log(f"✓ Saved: {final_md.name}", box)

            # Cleanup
            try:
                temp_wav.unlink()
            except:
                pass

        except Exception as e:
            self.log(f"✗ Error: {e}", box)

if __name__ == "__main__":
    app = TranscriberEngine()
    app.mainloop()