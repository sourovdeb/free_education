#!/usr/bin/env python3
"""
Writer & Teacher Audio/Video Transcriber Engine (v5.2)
- Intel GPU acceleration via Optimum-Intel + OpenVINO
- YouTube download, live recording, batch processing
- NLP via shared nlp_utils.py
- FIXED: recording crash (sd.portaudio removed, InputStream callback used)
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
from pathlib import Path
from datetime import datetime

# ── Windows DPI fix ───────────────────────────────────────────────────────────
if platform.system() == "Windows":
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

# ── Shared NLP ────────────────────────────────────────────────────────────────
from nlp_utils import (
    extract_keywords, pure_python_summarize,
    check_ollama_running, ollama_summarize, keybert_keywords,
)

# ── Colors ────────────────────────────────────────────────────────────────────
BG, PANEL, CARD, BORDER   = "#0d0d14", "#13131f", "#1a1a2c", "#2a2a40"
ACCENT, ACCENT2, TEXT      = "#ff4d6d", "#4d9fff", "#e8e8f0"
TEXT_DIM, SUCCESS, ERROR   = "#6b6b8a", "#3ddc97", "#ff4d6d"
RUNNING, WARNING           = "#4d9fff", "#f5a623"


# ── Runtime package check ─────────────────────────────────────────────────────
def is_installed(package_name: str) -> bool:
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False


# ── Intel OpenVINO transcription ──────────────────────────────────────────────
def transcribe_with_openvino(audio_path: Path, model_size: str) -> str:
    try:
        from optimum.intel import OVModelForSpeechSeq2Seq
        from transformers import AutoProcessor, pipeline
    except ImportError as e:
        raise ImportError("optimum-intel not installed.") from e

    model_id = f"openai/whisper-{model_size}"
    if model_size == "large-v3":
        model_id = "openai/whisper-large-v3"

    processor = AutoProcessor.from_pretrained(model_id)
    model = OVModelForSpeechSeq2Seq.from_pretrained(
        model_id, export=True, device="GPU", compile=True,
        ov_config={"PERFORMANCE_HINT": "LATENCY", "INFERENCE_PRECISION_HINT": "f32"},
    )
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        chunk_length_s=30,
        batch_size=16,
    )
    return pipe(str(audio_path), return_timestamps=False)["text"]


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────────────────────────────────────
class TranscriberEngine(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio/Video Transcriber Engine v5.2 (Intel GPU)")
        self.geometry("1150x800")
        self.configure(bg=BG)

        # Path variables
        self.selected_file   = tk.StringVar()
        self.batch_in_dir    = tk.StringVar()
        self.master_out_dir  = tk.StringVar(
            value=str(Path.home() / "Documents" / "Media_Pipeline_Output")
        )
        self.ffmpeg_path = tk.StringVar(value=r"C:\ffmpeg\bin\ffmpeg.exe")

        # Transcription engine
        self.transcription_engine = tk.StringVar(value="faster-whisper")
        self.whisper_model        = tk.StringVar(value="base")
        self.kw_count             = tk.IntVar(value=5)
        self.sum_len              = tk.IntVar(value=5)

        # Advanced NLP
        self.use_ollama_summary   = tk.BooleanVar(value=False)
        self.use_keybert_keywords = tk.BooleanVar(value=False)
        self.ollama_model         = tk.StringVar(value="gemma2:9b")

        # Audio preprocessing
        self.use_noise_reduction = tk.BooleanVar(value=False)
        self.ffmpeg_filter       = tk.StringVar(value="-af afftdn=nf=-25")

        # YouTube
        self.yt_url = tk.StringVar()

        # Recording — FIXED: use InputStream callback instead of sd.rec()
        self.recording       = False
        self._audio_chunks   = []   # list of numpy arrays collected by callback
        self._rec_stream     = None

        self.log_queue    = queue.Queue()
        self.is_processing = False
        self._build_ui()
        self._start_log_drain()

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        hdr = tk.Frame(self, bg=PANEL, height=60)
        hdr.pack(fill="x", side="top")
        tk.Label(
            hdr, text="🎙️ Writer & Teacher Transcriber Engine v5.2 (Intel GPU)",
            font=("Arial", 14, "bold"), bg=PANEL, fg=TEXT,
        ).pack(side="left", padx=20)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        # ── Single file tab ───────────────────────────────────────────────────
        self.tab_single = tk.Frame(self.nb, bg=BG)
        self.nb.add(self.tab_single, text=" Single File ")

        paned = tk.PanedWindow(self.tab_single, orient="horizontal", bg=BG, sashwidth=4)
        paned.pack(fill="both", expand=True)
        left  = tk.Frame(paned, bg=BG, width=450)
        right = tk.Frame(paned, bg=BG)
        paned.add(left)
        paned.add(right)

        # Input source card
        tk.Label(left, text="Input Source", font=("Arial", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        card_in = self._card(left)

        tk.Label(card_in, text="Local file:", font=("Arial", 9),
                 bg=CARD, fg=TEXT_DIM).pack(anchor="w")
        frow = tk.Frame(card_in, bg=CARD)
        frow.pack(fill="x", pady=2)
        tk.Entry(frow, textvariable=self.selected_file,
                 bg=BG, fg=TEXT, relief="flat").pack(side="left", fill="x", expand=True)
        tk.Button(frow, text="Browse", bg=ACCENT, fg="white", relief="flat",
                  command=self._browse_single).pack(side="right")

        if is_installed("yt_dlp"):
            tk.Label(card_in, text="YouTube URL:", font=("Arial", 9),
                     bg=CARD, fg=TEXT_DIM).pack(anchor="w", pady=(10, 0))
            yt_row = tk.Frame(card_in, bg=CARD)
            yt_row.pack(fill="x", pady=2)
            tk.Entry(yt_row, textvariable=self.yt_url,
                     bg=BG, fg=TEXT, relief="flat").pack(side="left", fill="x", expand=True)
            tk.Button(yt_row, text="Download & Transcribe", bg=ACCENT2, fg=BG,
                      relief="flat", command=self._download_and_transcribe).pack(side="right")

        if is_installed("sounddevice"):
            rec_row = tk.Frame(card_in, bg=CARD)
            rec_row.pack(fill="x", pady=(10, 0))
            self.rec_btn = tk.Button(
                rec_row, text="🔴 Start Recording", bg=ERROR, fg="white",
                relief="flat", command=self._toggle_record,
            )
            self.rec_btn.pack(side="left", padx=(0, 10))
            tk.Label(rec_row, text="Click to record from microphone",
                     font=("Arial", 9), bg=CARD, fg=TEXT_DIM).pack(side="left")

        # Transcription options card
        tk.Label(left, text="Transcription Options", font=("Arial", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=20, pady=(15, 5))
        card_t = self._card(left)

        eng_row = tk.Frame(card_t, bg=CARD)
        eng_row.pack(fill="x", pady=2)
        tk.Label(eng_row, text="Engine:", font=("Arial", 9),
                 bg=CARD, fg=TEXT_DIM).pack(side="left")
        self.engine_combo = ttk.Combobox(
            eng_row, textvariable=self.transcription_engine,
            values=["faster-whisper (NVIDIA)", "openai-whisper (CPU)",
                    "intel-openvino (Intel GPU/CPU)"],
            state="readonly", width=25,
        )
        self.engine_combo.pack(side="left", padx=10)

        mod_row = tk.Frame(card_t, bg=CARD)
        mod_row.pack(fill="x", pady=2)
        tk.Label(mod_row, text="Model size:", font=("Arial", 9),
                 bg=CARD, fg=TEXT_DIM).pack(side="left")
        ttk.Combobox(
            mod_row, textvariable=self.whisper_model,
            values=["tiny", "base", "small", "medium", "large-v3"],
            state="readonly", width=12,
        ).pack(side="left", padx=10)

        tk.Checkbutton(
            card_t, text="Enable noise reduction (ffmpeg afftdn)",
            variable=self.use_noise_reduction, bg=CARD, fg=TEXT, selectcolor=BG,
        ).pack(anchor="w", pady=2)

        # NLP options card
        tk.Label(left, text="NLP Options", font=("Arial", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=20, pady=(15, 5))
        card_nlp = self._card(left)

        cnt = tk.Frame(card_nlp, bg=CARD)
        cnt.pack(fill="x", pady=2)
        tk.Label(cnt, text="Keywords:", bg=CARD, fg=TEXT_DIM).pack(side="left")
        tk.Spinbox(cnt, from_=1, to=10, textvariable=self.kw_count, width=5).pack(side="left", padx=10)
        tk.Label(cnt, text="Summary sentences:", bg=CARD, fg=TEXT_DIM).pack(side="left", padx=10)
        tk.Spinbox(cnt, from_=1, to=15, textvariable=self.sum_len, width=5).pack(side="left")

        ol_row = tk.Frame(card_nlp, bg=CARD)
        ol_row.pack(fill="x")
        self.ollama_cb = tk.Checkbutton(
            ol_row, text="Use Ollama for summary",
            variable=self.use_ollama_summary, bg=CARD, fg=TEXT, selectcolor=BG,
        )
        self.ollama_cb.pack(side="left")
        self.ollama_status = tk.Label(ol_row, text="(checking...)",
                                      font=("Arial", 8), bg=CARD, fg=TEXT_DIM)
        self.ollama_status.pack(side="left", padx=5)

        mod2 = tk.Frame(card_nlp, bg=CARD)
        mod2.pack(fill="x")
        tk.Label(mod2, text="Ollama model:", bg=CARD, fg=TEXT_DIM).pack(side="left")
        ttk.Combobox(
            mod2, textvariable=self.ollama_model,
            values=["gemma2:9b", "mistral-nemo", "llama3.2:3b", "phi3.5", "qwen2.5:7b"],
            state="readonly", width=15,
        ).pack(side="left", padx=5)

        tk.Checkbutton(
            card_nlp,
            text="Use KeyBERT for keywords (requires transformers)",
            variable=self.use_keybert_keywords, bg=CARD, fg=TEXT, selectcolor=BG,
        ).pack(anchor="w")

        # Run button
        self.run_btn = tk.Button(
            left, text="▶ TRANSCRIBE", bg=SUCCESS, fg=BG,
            font=("Arial", 11, "bold"), pady=15, command=self._run_single,
        )
        self.run_btn.pack(fill="x", padx=20, pady=20)

        # Log panel
        self.log_box = scrolledtext.ScrolledText(
            right, bg=PANEL, fg=ACCENT2, font=("Courier New", 10), relief="flat",
        )
        self.log_box.pack(fill="both", expand=True, padx=20, pady=20)

        # ── Batch tab ─────────────────────────────────────────────────────────
        self.tab_batch = tk.Frame(self.nb, bg=BG)
        self.nb.add(self.tab_batch, text=" Batch Folder ")

        pb = tk.PanedWindow(self.tab_batch, orient="horizontal", bg=BG, sashwidth=4)
        pb.pack(fill="both", expand=True)
        lb = tk.Frame(pb, bg=BG, width=400)
        rb = tk.Frame(pb, bg=BG)
        pb.add(lb)
        pb.add(rb)

        tk.Label(lb, text="Batch Source Folder", font=("Arial", 11, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", padx=20, pady=(20, 5))
        cb = self._card(lb)
        tk.Entry(cb, textvariable=self.batch_in_dir,
                 bg=BG, fg=TEXT, relief="flat").pack(fill="x", pady=5)
        tk.Button(cb, text="Select Folder", bg=ACCENT, fg="white",
                  relief="flat", command=self._browse_batch_in).pack(anchor="e")

        tk.Button(
            lb, text="▶ RUN BATCH PROCESS", bg="#ff8c42", fg="white",
            font=("Arial", 11, "bold"), pady=15, command=self._run_batch,
        ).pack(fill="x", padx=20, pady=20)

        self.batch_log = scrolledtext.ScrolledText(
            rb, bg=PANEL, fg=ACCENT2, font=("Courier New", 10), relief="flat",
        )
        self.batch_log.pack(fill="both", expand=True, padx=20, pady=20)

        # ── Settings tab ──────────────────────────────────────────────────────
        self.tab_set = tk.Frame(self.nb, bg=BG)
        self.nb.add(self.tab_set, text=" Settings ")

        canvas = tk.Canvas(self.tab_set, bg=BG, highlightthickness=0)
        scroll = tk.Scrollbar(self.tab_set, orient="vertical", command=canvas.yview)
        inner  = tk.Frame(canvas, bg=BG)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.create_window((0, 0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        cs = self._card(inner)
        tk.Label(cs, text="Master Output Directory", font=("Arial", 11, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w")
        tk.Entry(cs, textvariable=self.master_out_dir,
                 bg=BG, fg=TEXT, width=80).pack(pady=5)
        tk.Button(cs, text="Browse", bg=PANEL, fg=TEXT,
                  command=self._browse_master_out).pack(anchor="w")

        tk.Label(cs, text="\nFFmpeg Executable Path", font=("Arial", 11, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w")
        tk.Entry(cs, textvariable=self.ffmpeg_path,
                 bg=BG, fg=TEXT, width=80).pack(pady=5)

        tk.Label(cs, text="\nNoise Reduction Filter", font=("Arial", 11, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w")
        tk.Entry(cs, textvariable=self.ffmpeg_filter,
                 bg=BG, fg=TEXT, width=80).pack(pady=5)

        self.after(1000, self._update_ollama_status)

    # ── Helper ────────────────────────────────────────────────────────────────
    def _card(self, parent):
        c = tk.Frame(parent, bg=CARD, pady=15, padx=15,
                     highlightthickness=1, highlightbackground=BORDER)
        c.pack(fill="x", padx=20)
        return c

    # ── Browse actions ────────────────────────────────────────────────────────
    def _browse_single(self):
        f = filedialog.askopenfilename(
            filetypes=[("Media Files", "*.mp3 *.mp4 *.wav *.m4a *.mkv *.ogg *.webm *.mov *.avi *.flac")]
        )
        if f:
            self.selected_file.set(f)

    def _browse_batch_in(self):
        d = filedialog.askdirectory()
        if d:
            self.batch_in_dir.set(d)

    def _browse_master_out(self):
        d = filedialog.askdirectory()
        if d:
            self.master_out_dir.set(d)

    # ── YouTube ───────────────────────────────────────────────────────────────
    def _download_and_transcribe(self):
        url = self.yt_url.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Enter a YouTube URL.")
            return
        threading.Thread(target=self._yt_thread, args=(url,), daemon=True).start()

    def _yt_thread(self, url):
        self.log("Downloading from YouTube…", "single")
        try:
            import yt_dlp
        except ImportError:
            self.log("✗ yt-dlp not installed.", "single")
            return
        out_tpl = str(Path(tempfile.gettempdir()) / "%(title)s.%(ext)s")
        opts = {
            "format": "bestaudio/best",
            "postprocessors": [{"key": "FFmpegExtractAudio",
                                "preferredcodec": "wav", "preferredquality": "192"}],
            "outtmpl": out_tpl, "quiet": True,
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                wav = Path(ydl.prepare_filename(info)).with_suffix(".wav")
                self.log(f"Downloaded: {wav.name}", "single")
                self.selected_file.set(str(wav))
                self._run_single()
        except Exception as e:
            self.log(f"✗ YouTube error: {e}", "single")

    # ── Recording — FIXED ─────────────────────────────────────────────────────
    def _toggle_record(self):
        if not self.recording:
            self._start_record()
        else:
            self._stop_record()

    def _start_record(self):
        try:
            import sounddevice as sd
            import numpy as np
        except ImportError:
            self.log("✗ sounddevice not installed.", "single")
            return

        self.recording = True
        self._audio_chunks = []
        self.rec_btn.config(text="⏹ Stop Recording", bg=WARNING)
        self.log("Recording started… Speak into microphone.", "single")

        def _callback(indata, frames, time_info, status):
            if self.recording:
                self._audio_chunks.append(indata.copy())

        self._rec_stream = sd.InputStream(
            samplerate=16000, channels=1, dtype="int16", callback=_callback
        )
        self._rec_stream.start()

    def _stop_record(self):
        import numpy as np
        import wave

        self.recording = False
        if self._rec_stream:
            self._rec_stream.stop()
            self._rec_stream.close()
            self._rec_stream = None

        if not self._audio_chunks:
            self.log("✗ No audio captured.", "single")
            self.rec_btn.config(text="🔴 Start Recording", bg=ERROR)
            return

        audio_data = np.concatenate(self._audio_chunks, axis=0)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        wav_path = Path(tempfile.gettempdir()) / f"recording_{ts}.wav"

        with wave.open(str(wav_path), "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)          # int16 = 2 bytes
            wf.setframerate(16000)
            wf.writeframes(audio_data.tobytes())

        self.selected_file.set(str(wav_path))
        self.log(f"✓ Recording saved: {wav_path.name}", "single")
        self.rec_btn.config(text="🔴 Start Recording", bg=ERROR)

    # ── Log helpers ───────────────────────────────────────────────────────────
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
                fg=SUCCESS if running else ERROR,
            ))
        threading.Thread(target=check, daemon=True).start()
        self.after(5000, self._update_ollama_status)

    # ── Processing ────────────────────────────────────────────────────────────
    def _run_single(self):
        src = self.selected_file.get()
        if not src:
            messagebox.showwarning("Warning", "Select a media file first.")
            return
        threading.Thread(target=self._process, args=(Path(src), "single"), daemon=True).start()

    def _run_batch(self):
        d = self.batch_in_dir.get()
        if not d:
            messagebox.showwarning("Warning", "Select an input folder first.")
            return
        threading.Thread(target=self._batch_thread, args=(Path(d),), daemon=True).start()

    def _batch_thread(self, in_p: Path):
        exts  = {".mp3", ".mp4", ".wav", ".m4a", ".mkv", ".ogg", ".webm", ".mov", ".avi", ".flac"}
        files = [f for f in in_p.rglob("*") if f.suffix.lower() in exts]
        self.log(f"Found {len(files)} media files.", "batch")
        for f in files:
            self._process(f, "batch")
        self.log("All batch transcriptions complete.", "batch")

    def _process(self, src: Path, box: str):
        try:
            self.log(f"Processing: {src.name}…", box)
            temp_wav = Path(tempfile.gettempdir()) / f"temp_{src.stem}.wav"
            ffmpeg   = self.ffmpeg_path.get().strip()

            if not Path(ffmpeg).exists():
                self.log("✗ FFmpeg not found. Check Settings.", box)
                return

            cmd = [ffmpeg, "-y", "-i", str(src), "-ar", "16000", "-ac", "1"]
            if self.use_noise_reduction.get():
                flt = self.ffmpeg_filter.get().strip()
                if flt:
                    cmd.extend(flt.split())
            cmd.append(str(temp_wav))

            result = subprocess.run(cmd, capture_output=True)
            if result.returncode != 0:
                self.log(f"✗ FFmpeg error: {result.stderr.decode()[:200]}", box)
                return

            # Select engine
            engine_display = self.transcription_engine.get()
            raw_text = ""

            if "intel" in engine_display.lower():
                engine = "intel-openvino"
            elif "faster" in engine_display.lower():
                engine = "faster-whisper"
            else:
                engine = "openai-whisper"

            if engine == "intel-openvino":
                self.log("Using Intel OpenVINO…", box)
                try:
                    raw_text = transcribe_with_openvino(temp_wav, self.whisper_model.get())
                except Exception as e:
                    self.log(f"OpenVINO error: {e} — falling back.", box)
                    engine = "openai-whisper"

            if engine == "faster-whisper":
                try:
                    from faster_whisper import WhisperModel
                    model = WhisperModel(self.whisper_model.get(), device="cpu", compute_type="int8")
                    segments, info = model.transcribe(str(temp_wav))
                    self.log(f"Detected language: {info.language}", box)
                    raw_text = " ".join(s.text.strip() for s in segments)
                except ImportError:
                    self.log("faster-whisper not installed, falling back.", box)
                    engine = "openai-whisper"
                except Exception as e:
                    self.log(f"faster-whisper error: {e}", box)
                    engine = "openai-whisper"

            if engine == "openai-whisper" and not raw_text:
                try:
                    import whisper
                    model = whisper.load_model(self.whisper_model.get())
                    raw_text = model.transcribe(str(temp_wav))["text"].strip()
                except ImportError:
                    self.log("✗ openai-whisper not installed.", box)
                    return
                except Exception as e:
                    self.log(f"✗ openai-whisper error: {e}", box)
                    return

            if not raw_text:
                self.log("✗ No speech detected.", box)
                return

            # NLP
            self.log("Generating summary & keywords…", box)
            if self.use_ollama_summary.get() and check_ollama_running():
                summary = ollama_summarize(raw_text, self.ollama_model.get()) or \
                          pure_python_summarize(raw_text, self.sum_len.get())
            else:
                summary = pure_python_summarize(raw_text, self.sum_len.get())

            if self.use_keybert_keywords.get():
                tags = keybert_keywords(raw_text, self.kw_count.get()) or \
                       extract_keywords(raw_text, self.kw_count.get())
            else:
                tags = extract_keywords(raw_text, self.kw_count.get())

            # Save
            out_root = Path(self.master_out_dir.get())
            out_root.mkdir(parents=True, exist_ok=True)
            final_md = out_root / f"{src.stem}_transcript.md"
            final_md.write_text(
                f"# {src.stem}\n\n"
                f"**Engine:** {engine_display}\n\n"
                f"**Tags:** {tags}\n\n"
                f"**Summary:** {summary}\n\n"
                f"---\n\n{raw_text}",
                encoding="utf-8",
            )
            self.log(f"✓ Saved: {final_md.name}", box)

            try:
                temp_wav.unlink()
            except Exception:
                pass

        except Exception as e:
            self.log(f"✗ Error: {e}", box)


if __name__ == "__main__":
    app = TranscriberEngine()
    app.mainloop()
