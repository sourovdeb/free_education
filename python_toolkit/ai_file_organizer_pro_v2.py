"""
╔══════════════════════════════════════════════════════╗
║          AI FILE ORGANIZER PRO  —  v2.1              ║
║   Polished PyQt6 Desktop App with Dark Theme         ║
╚══════════════════════════════════════════════════════╝

REQUIREMENTS (install once):
    pip install PyQt6 transformers torch accelerate pymupdf python-docx

SUPPORTED FILE TYPES:  .txt  .md  .pdf  .docx  .csv  .json  .log

USAGE:
    python ai_file_organizer_pro.py
"""

import sys
import os
import shutil
import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QCheckBox,
    QTextEdit, QGroupBox, QFileDialog, QTabWidget,
    QComboBox, QProgressBar, QSizePolicy, QFrame, QScrollArea
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont


# ─────────────────────────────────────────────────────────────────────────────
#  DARK THEME STYLESHEET
# ─────────────────────────────────────────────────────────────────────────────
DARK_THEME = """
QWidget {
    background-color: #12141A;
    color: #C8CDD8;
    font-family: 'Segoe UI', 'SF Pro Display', sans-serif;
    font-size: 13px;
}

QGroupBox {
    border: 1px solid #2A2D38;
    border-radius: 8px;
    margin-top: 12px;
    padding: 14px 10px 10px 10px;
    background-color: #191B24;
    font-weight: 600;
    color: #7C83A0;
    font-size: 11px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    background-color: #191B24;
}

QPushButton {
    background-color: #1E2130;
    color: #8A93B2;
    border: 1px solid #2A2D38;
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 12px;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #252840;
    color: #C8CDD8;
    border-color: #3E4460;
}

QPushButton:disabled {
    background-color: #161820;
    color: #3E4460;
    border-color: #1E2130;
}

QPushButton#run_btn {
    background-color: #2B5CE6;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 12px 28px;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

QPushButton#run_btn:hover {
    background-color: #3669F5;
}

QPushButton#run_btn:disabled {
    background-color: #1A2A5E;
    color: #4A6099;
}

QPushButton#stop_btn {
    background-color: #2A1520;
    color: #E06080;
    border: 1px solid #4A2535;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 13px;
    font-weight: 700;
}

QPushButton#stop_btn:hover {
    background-color: #3A1A28;
    border-color: #7A3550;
}

QPushButton#stop_btn:disabled {
    background-color: #161820;
    color: #3E4460;
    border-color: #1E2130;
}

QPushButton#export_btn {
    background-color: #1A2620;
    color: #5EA87A;
    border: 1px solid #2A4535;
    border-radius: 6px;
    padding: 8px 14px;
    font-size: 12px;
}

QPushButton#export_btn:hover {
    background-color: #223025;
    border-color: #4A7555;
}

QLineEdit, QTextEdit {
    background-color: #0F1018;
    color: #C8CDD8;
    border: 1px solid #2A2D38;
    border-radius: 6px;
    padding: 8px 10px;
    selection-background-color: #2B5CE6;
}

QLineEdit:focus, QTextEdit:focus {
    border-color: #3E5AC8;
    background-color: #11131C;
}

QComboBox {
    background-color: #0F1018;
    color: #C8CDD8;
    border: 1px solid #2A2D38;
    border-radius: 6px;
    padding: 8px 12px;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #5A6080;
    margin-right: 6px;
}

QComboBox QAbstractItemView {
    background-color: #1E2130;
    border: 1px solid #2A2D38;
    selection-background-color: #2B3A6E;
    color: #C8CDD8;
}

QCheckBox {
    spacing: 8px;
    color: #9098B5;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1px solid #3A3D52;
    background-color: #0F1018;
}

QCheckBox::indicator:checked {
    background-color: #2B5CE6;
    border-color: #2B5CE6;
}

QCheckBox::indicator:hover {
    border-color: #4A6AC8;
}

QProgressBar {
    background-color: #0F1018;
    border: 1px solid #2A2D38;
    border-radius: 6px;
    height: 10px;
    text-align: center;
    color: transparent;
}

QProgressBar::chunk {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #2B5CE6, stop:1 #4A8AFF
    );
    border-radius: 5px;
}

QTabWidget::pane {
    border: 1px solid #2A2D38;
    border-radius: 6px;
    background-color: #191B24;
}

QTabBar::tab {
    background-color: #12141A;
    color: #5A6080;
    border: 1px solid #2A2D38;
    border-bottom: none;
    padding: 8px 16px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-size: 12px;
}

QTabBar::tab:selected {
    background-color: #191B24;
    color: #9098B5;
    border-bottom: 1px solid #191B24;
}

QScrollBar:vertical {
    background-color: #12141A;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #2A2D38;
    border-radius: 4px;
    min-height: 20px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QLabel#path_label {
    color: #4A6099;
    font-size: 11px;
    font-style: italic;
    padding: 2px 4px;
}

QLabel#path_label[set="true"] {
    color: #5EA87A;
    font-style: normal;
}

QLabel#stat_label {
    background-color: #0F1018;
    border: 1px solid #2A2D38;
    border-radius: 6px;
    padding: 8px 14px;
    color: #7C83A0;
    font-size: 12px;
    font-weight: 600;
}

QFrame#divider {
    background-color: #2A2D38;
    max-height: 1px;
}
"""


# ─────────────────────────────────────────────────────────────────────────────
#  FILE READER — supports .txt .md .pdf .docx .csv .json .log .yaml .xml
# ─────────────────────────────────────────────────────────────────────────────
def read_file_content(file_path: Path, max_chars: int = 1200) -> str | None:
    suffix = file_path.suffix.lower()

    if suffix in ('.txt', '.md', '.csv', '.json', '.log', '.yaml', '.xml'):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(max_chars)
        except Exception:
            return None

    elif suffix == '.pdf':
        try:
            import fitz
            doc = fitz.open(str(file_path))
            text = ""
            for page in doc:
                text += page.get_text()
                if len(text) >= max_chars:
                    break
            doc.close()
            return text[:max_chars] if text.strip() else None
        except ImportError:
            return f"[PDF detected: {file_path.name}. Install pymupdf to read content.]"
        except Exception:
            return None

    elif suffix == '.docx':
        try:
            from docx import Document
            doc = Document(str(file_path))
            text = "\n".join(p.text for p in doc.paragraphs)
            return text[:max_chars] if text.strip() else None
        except ImportError:
            return f"[DOCX detected: {file_path.name}. Install python-docx to read content.]"
        except Exception:
            return None

    return None


# ─────────────────────────────────────────────────────────────────────────────
#  BACKGROUND WORKER THREAD
# ─────────────────────────────────────────────────────────────────────────────
class OrganizerWorker(QThread):
    log_signal      = pyqtSignal(str)
    progress_signal = pyqtSignal(int, int)
    stats_signal    = pyqtSignal(dict)
    finished_signal = pyqtSignal()

    SUPPORTED_SUFFIXES = {'.txt', '.md', '.pdf', '.docx', '.csv', '.json', '.log', '.yaml', '.xml'}

    def __init__(self, config: dict):
        super().__init__()
        self.config = config
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True

    def run(self):
        stats = {"moved": 0, "skipped": 0, "errors": 0}

        try:
            self.log_signal.emit("⏳  Loading AI model… This may take 15–30 seconds on first run.")
            from transformers import pipeline as hf_pipeline

            pipe = hf_pipeline(
                "text-generation",
                model=self.config['model_path'],
                device_map="auto",
                torch_dtype="auto"
            )
            self.log_signal.emit("✅  AI loaded. Scanning files…\n")

            input_dir  = Path(self.config['input'])
            output_dir = Path(self.config['output'])

            all_files = [
                f for f in input_dir.rglob('*')
                if f.is_file()
                and f.suffix.lower() in self.SUPPORTED_SUFFIXES
                and not (self.config.get('ignore_hidden') and f.name.startswith('.'))
            ]

            total = len(all_files)
            if total == 0:
                self.log_signal.emit("⚠️  No supported files found in the input folder.")
                self.finished_signal.emit()
                return

            self.log_signal.emit(f"📂  Found {total} supported file(s).\n{'─'*48}")

            existing_folders: list[str] = []
            if self.config.get('use_existing') and output_dir.exists():
                existing_folders = [f.name for f in output_dir.iterdir() if f.is_dir()]

            for idx, file_path in enumerate(all_files, start=1):
                if self._stop_requested:
                    self.log_signal.emit("\n🛑  Stopped by user.")
                    break

                self.progress_signal.emit(idx, total)
                self.log_signal.emit(f"[{idx}/{total}]  Analyzing: {file_path.name}")

                content = read_file_content(file_path)
                if content is None:
                    self.log_signal.emit("       ↳ ⚠️  Skipped (unreadable)\n")
                    stats["skipped"] += 1
                    continue

                system_parts = [
                    "You are a precise file categorization assistant.",
                    self.config.get('instructions') or "Categorize files by their main topic.",
                    "Reply with EXACTLY ONE WORD (a folder name). No explanation. No punctuation.",
                    "The folder name must be suitable for a file system (letters, numbers, underscores only)."
                ]
                if existing_folders:
                    system_parts.append(
                        f"Prefer one of these existing folders if it fits: {', '.join(existing_folders[:20])}."
                    )

                prompt = [
                    {"role": "system", "content": " ".join(system_parts)},
                    {"role": "user",   "content": f"File name: {file_path.name}\n\nContent preview:\n{content}"}
                ]

                try:
                    result = pipe(
                        prompt,
                        max_new_tokens=8,
                        temperature=float(self.config.get('temperature', 0.1)),
                        do_sample=False
                    )
                    raw = result[0]['generated_text'][-1]['content'].strip().split()[0]
                    folder_name = "".join(c for c in raw if c.isalnum() or c in ('_', '-'))
                    if not folder_name:
                        folder_name = "Unsorted"
                except Exception as ai_err:
                    self.log_signal.emit(f"       ↳ ❌  AI error: {ai_err}\n")
                    stats["errors"] += 1
                    continue

                target_dir = output_dir / folder_name
                target_dir.mkdir(parents=True, exist_ok=True)

                dest = target_dir / file_path.name
                if dest.exists():
                    dest = target_dir / f"{file_path.stem}_dup{file_path.suffix}"

                try:
                    shutil.move(str(file_path), str(dest))
                except Exception as move_err:
                    self.log_signal.emit(f"       ↳ ❌  Move failed: {move_err}\n")
                    stats["errors"] += 1
                    continue

                tag_line = f"  {self.config['hashtags']}" if self.config.get('hashtags') else ""
                self.log_signal.emit(f"       ↳ ✅  → {folder_name}/{dest.name}{tag_line}\n")
                stats["moved"] += 1

        except Exception as e:
            self.log_signal.emit(f"\n❌  CRITICAL ERROR: {e}")
            stats["errors"] += 1

        self.log_signal.emit(f"\n{'═'*48}")
        self.log_signal.emit("🎉  Organization complete!")
        self.stats_signal.emit(stats)
        self.finished_signal.emit()


# ─────────────────────────────────────────────────────────────────────────────
#  MAIN UI - FIXED FOR PROPER RESIZING
# ─────────────────────────────────────────────────────────────────────────────
class AIFileOrganizerUI(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI File Organizer Pro  ·  v2.1")
        self.resize(720, 900)
        self.setMinimumSize(600, 700)  # Set minimum size to prevent cutting off
        self.setStyleSheet(DARK_THEME)
        self._console_lines: list[str] = []
        self._build_ui()

    def _build_ui(self):
        # Main layout with proper stretch factors
        root = QVBoxLayout(self)
        root.setSpacing(10)
        root.setContentsMargins(16, 16, 16, 16)

        # ·· Header ············································
        header = QHBoxLayout()
        title = QLabel("AI File Organizer Pro")
        title.setFont(QFont("Segoe UI", 17, QFont.Weight.Bold))
        title.setStyleSheet("color: #C8CDD8; letter-spacing: -0.5px;")
        title.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        
        subtitle = QLabel("v2.1")
        subtitle.setStyleSheet("color: #3E4460; font-size: 11px; padding-top: 6px;")
        subtitle.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        
        header.addWidget(title)
        header.addWidget(subtitle)
        header.addStretch()
        root.addLayout(header)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        root.addWidget(divider)

        # Create a scroll area for the main content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Create content widget for scroll area
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        # ·· 1. Target Folders ·································
        path_group = QGroupBox("1.  Target Folders")
        path_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        pl = QVBoxLayout(path_group)
        pl.setSpacing(6)

        self.input_btn   = QPushButton("📁  Select Input Folder")
        self.input_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.input_label = self._path_label()
        self.input_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        pl.addWidget(self.input_btn)
        pl.addWidget(self.input_label)

        self.output_btn   = QPushButton("📂  Select Output Destination")
        self.output_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.output_label = self._path_label()
        self.output_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        pl.addWidget(self.output_btn)
        pl.addWidget(self.output_label)

        scroll_layout.addWidget(path_group)

        # ·· 2. AI Model ·······································
        model_group = QGroupBox("2.  AI Model")
        model_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        ml = QVBoxLayout(model_group)

        self.model_combo = QComboBox()
        self.model_combo.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.model_combo.addItems([
            "Qwen/Qwen2.5-1.5B-Instruct  (lightweight, fast)",
            "Qwen/Qwen2.5-3B-Instruct  (better quality)",
            "meta-llama/Llama-3.2-1B-Instruct",
            "meta-llama/Llama-3.2-3B-Instruct",
            "Custom Local Folder…"
        ])
        ml.addWidget(QLabel("Model:"))
        ml.addWidget(self.model_combo)

        custom_row = QHBoxLayout()
        self.model_btn   = QPushButton("Browse…")
        self.model_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.model_label = self._path_label("No custom folder selected")
        self.model_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        custom_row.addWidget(self.model_btn)
        custom_row.addWidget(self.model_label, 1)
        ml.addLayout(custom_row)

        scroll_layout.addWidget(model_group)

        # ·· 3. Rules & Hashtags ·······························
        rules_group = QGroupBox("3.  Organization Rules  &  Hashtags")
        rules_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        rl = QVBoxLayout(rules_group)
        rl.setSpacing(8)

        rl.addWidget(QLabel("Custom AI Instructions:"))
        self.instruction_box = QTextEdit()
        self.instruction_box.setPlaceholderText(
            "e.g. Sort by project name. Use English. Merge receipts under Finance."
        )
        self.instruction_box.setMinimumHeight(60)
        self.instruction_box.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding
        )
        rl.addWidget(self.instruction_box, 1)

        tag_row = QHBoxLayout()
        tag_row.addWidget(QLabel("Force Hashtags:"))
        self.hashtag_input = QLineEdit()
        self.hashtag_input.setPlaceholderText("#2026  #obsidian  #sorted")
        self.hashtag_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        tag_row.addWidget(self.hashtag_input)
        rl.addLayout(tag_row)

        self.check_auto_tags = QCheckBox("Ask AI to suggest 3 hashtags per file (slower)")
        self.check_auto_tags.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        rl.addWidget(self.check_auto_tags)

        scroll_layout.addWidget(rules_group)

        # ·· 4. Advanced (Tabs) ································
        tabs = QTabWidget()
        tabs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)
        tabs.setMinimumHeight(150)

        adv_tab = QWidget()
        adv_l = QVBoxLayout(adv_tab)
        adv_l.setSpacing(8)

        self.check_existing = QCheckBox("Re-use existing destination folders when names match")
        self.check_existing.setChecked(True)
        self.check_ignore_hidden = QCheckBox("Ignore hidden files (starting with '.')")
        self.check_ignore_hidden.setChecked(True)
        adv_l.addWidget(self.check_existing)
        adv_l.addWidget(self.check_ignore_hidden)

        temp_row = QHBoxLayout()
        temp_row.addWidget(QLabel("LLM Temperature (0.1 = strict  →  1.0 = creative):"))
        self.temp_input = QLineEdit("0.1")
        self.temp_input.setMaximumWidth(70)
        self.temp_input.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        temp_row.addWidget(self.temp_input)
        temp_row.addStretch()
        adv_l.addLayout(temp_row)
        adv_l.addStretch()

        tabs.addTab(adv_tab, "⚙️  Advanced")

        filetypes_tab = QWidget()
        ft_l = QVBoxLayout(filetypes_tab)
        ft_l.addWidget(QLabel("Supported formats in this version:"))
        supported = QLabel(
            "📄  .txt  .md  .log  .csv  .json  .yaml  .xml\n"
            "📕  .pdf  (requires: pip install pymupdf)\n"
            "📘  .docx (requires: pip install python-docx)"
        )
        supported.setStyleSheet("color: #7C83A0; line-height: 1.6;")
        supported.setWordWrap(True)
        ft_l.addWidget(supported)
        ft_l.addStretch()
        tabs.addTab(filetypes_tab, "📋  File Types")

        scroll_layout.addWidget(tabs)

        # Add scroll content to scroll area
        scroll_area.setWidget(scroll_content)
        root.addWidget(scroll_area, 3)  # Give scroll area stretch factor of 3

        # ·· 5. Execute (this stays outside scroll area - always visible) ··
        exec_group = QGroupBox("4.  Execute")
        exec_group.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        el = QVBoxLayout(exec_group)
        el.setSpacing(10)

        btn_row = QHBoxLayout()
        self.run_btn = QPushButton("▶  RUN ORGANIZER")
        self.run_btn.setObjectName("run_btn")
        self.run_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.stop_btn = QPushButton("■  Stop")
        self.stop_btn.setObjectName("stop_btn")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setFixedWidth(90)

        btn_row.addWidget(self.run_btn)
        btn_row.addWidget(self.stop_btn)
        el.addLayout(btn_row)

        progress_row = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        self.file_counter = QLabel("0 / 0")
        self.file_counter.setStyleSheet("color: #3E4460; font-size: 11px; min-width: 52px;")
        self.file_counter.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        progress_row.addWidget(self.progress_bar, 1)
        progress_row.addWidget(self.file_counter)
        el.addLayout(progress_row)

        stats_row = QHBoxLayout()
        self.stat_moved   = self._stat_label("Moved",   "0")
        self.stat_skipped = self._stat_label("Skipped", "0")
        self.stat_errors  = self._stat_label("Errors",  "0")
        stats_row.addWidget(self.stat_moved)
        stats_row.addWidget(self.stat_skipped)
        stats_row.addWidget(self.stat_errors)
        el.addLayout(stats_row)

        root.addWidget(exec_group, 0)  # No stretch for exec group

        # ·· Console ··········································
        console_header = QHBoxLayout()
        console_lbl = QLabel("Console Log")
        console_lbl.setStyleSheet(
            "color: #3E4460; font-size: 11px; font-weight: 600; letter-spacing: 0.6px;"
        )
        console_lbl.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        
        self.export_btn = QPushButton("💾  Export Log")
        self.export_btn.setObjectName("export_btn")
        self.export_btn.setFixedHeight(28)
        self.export_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        console_header.addWidget(console_lbl)
        console_header.addStretch()
        console_header.addWidget(self.export_btn)
        root.addLayout(console_header)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFont(QFont("Consolas", 11))
        self.console.setStyleSheet(
            "background-color: #0A0C12; color: #8A93B2;"
            "border: 1px solid #1E2130; border-radius: 6px; padding: 8px;"
        )
        self.console.setMinimumHeight(120)
        self.console.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.MinimumExpanding
        )
        self.console.setText("System ready. Select folders and press RUN ORGANIZER.")
        root.addWidget(self.console, 2)  # Give console stretch factor of 2

        # ── Wire signals ────────────────────────────────────────────────────
        self.input_btn.clicked.connect(self.select_input)
        self.output_btn.clicked.connect(self.select_output)
        self.model_btn.clicked.connect(self.select_model)
        self.model_combo.currentIndexChanged.connect(self.toggle_model_browser)
        self.run_btn.clicked.connect(self.start_processing)
        self.stop_btn.clicked.connect(self.stop_processing)
        self.export_btn.clicked.connect(self.export_log)

        self.toggle_model_browser()

    # ── Helper widgets ─────────────────────────────────────────────────────────
    def _path_label(self, text="No folder selected…") -> QLabel:
        lbl = QLabel(text)
        lbl.setObjectName("path_label")
        lbl.setWordWrap(True)
        lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        return lbl

    def _stat_label(self, title: str, value: str) -> QLabel:
        lbl = QLabel(f"{title}\n{value}")
        lbl.setObjectName("stat_label")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setMinimumWidth(90)
        lbl.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        return lbl

    def _update_stat(self, lbl: QLabel, title: str, value: int, color: str = "#7C83A0"):
        lbl.setText(f"{title}\n{value}")
        lbl.setStyleSheet(
            f"background-color: #0F1018; border: 1px solid #2A2D38; border-radius: 6px;"
            f"padding: 8px 14px; color: {color}; font-size: 12px; font-weight: 600;"
        )

    # ── Folder / model pickers ─────────────────────────────────────────────────
    def select_input(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.input_label.setText(folder)
            self.input_label.setProperty("set", "true")
            self.input_label.setStyle(self.input_label.style())

    def select_output(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.output_label.setText(folder)
            self.output_label.setProperty("set", "true")
            self.output_label.setStyle(self.output_label.style())

    def select_model(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Local Model Folder")
        if folder:
            self.model_label.setText(folder)

    def toggle_model_browser(self):
        is_custom = "Custom" in self.model_combo.currentText()
        self.model_btn.setEnabled(is_custom)
        self.model_label.setEnabled(is_custom)

    # ── Processing ─────────────────────────────────────────────────────────────
    def start_processing(self):
        if self.input_label.text() == "No folder selected…":
            self._log("⚠️  Please select an Input folder first.")
            return
        if self.output_label.text() == "No folder selected…":
            self._log("⚠️  Please select an Output folder first.")
            return

        raw_model = self.model_combo.currentText()
        if "Custom" in raw_model:
            model_path = self.model_label.text()
            if not model_path or "No custom" in model_path:
                self._log("⚠️  Please select a custom model folder.")
                return
        else:
            model_path = raw_model.split("  ")[0].strip()

        config = {
            "input":         self.input_label.text(),
            "output":        self.output_label.text(),
            "model_path":    model_path,
            "instructions":  self.instruction_box.toPlainText().strip(),
            "hashtags":      self.hashtag_input.text().strip(),
            "temperature":   self.temp_input.text().strip() or "0.1",
            "use_existing":  self.check_existing.isChecked(),
            "ignore_hidden": self.check_ignore_hidden.isChecked(),
        }

        self.console.clear()
        self._console_lines.clear()
        self.progress_bar.setValue(0)
        self.file_counter.setText("0 / 0")
        self._update_stat(self.stat_moved,   "Moved",   0)
        self._update_stat(self.stat_skipped, "Skipped", 0)
        self._update_stat(self.stat_errors,  "Errors",  0)

        self.run_btn.setEnabled(False)
        self.run_btn.setText("⏳  ORGANIZING…")
        self.stop_btn.setEnabled(True)

        self.worker = OrganizerWorker(config)
        self.worker.log_signal.connect(self._log)
        self.worker.progress_signal.connect(self._update_progress)
        self.worker.stats_signal.connect(self._update_stats)
        self.worker.finished_signal.connect(self._on_finished)
        self.worker.start()

    def stop_processing(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.stop()
            self.stop_btn.setEnabled(False)
            self.stop_btn.setText("Stopping…")

    def _log(self, text: str):
        self.console.append(text)
        self._console_lines.append(text)
        sb = self.console.verticalScrollBar()
        sb.setValue(sb.maximum())

    def _update_progress(self, current: int, total: int):
        pct = int((current / total) * 100) if total else 0
        self.progress_bar.setValue(pct)
        self.file_counter.setText(f"{current} / {total}")

    def _update_stats(self, stats: dict):
        moved   = stats.get("moved",   0)
        skipped = stats.get("skipped", 0)
        errors  = stats.get("errors",  0)
        self._update_stat(self.stat_moved,   "Moved",   moved,   "#5EA87A" if moved   else "#7C83A0")
        self._update_stat(self.stat_skipped, "Skipped", skipped, "#B8963A" if skipped else "#7C83A0")
        self._update_stat(self.stat_errors,  "Errors",  errors,  "#C05060" if errors  else "#7C83A0")

    def _on_finished(self):
        self.run_btn.setEnabled(True)
        self.run_btn.setText("▶  RUN ORGANIZER")
        self.stop_btn.setEnabled(False)
        self.stop_btn.setText("■  Stop")
        self.progress_bar.setValue(100)

    # ── Log Export ─────────────────────────────────────────────────────────────
    def export_log(self):
        default_name = f"organizer_log_{datetime.datetime.now():%Y%m%d_%H%M%S}.txt"
        path, _ = QFileDialog.getSaveFileName(self, "Save Log", default_name, "Text files (*.txt)")
        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write("\n".join(self._console_lines))
            self._log(f"📄  Log saved → {path}")


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = AIFileOrganizerUI()
    window.show()
    sys.exit(app.exec())