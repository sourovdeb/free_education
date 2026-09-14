"""
nlp_utils.py — Shared NLP helpers for the 4-script toolkit.
Import this in any script instead of copy-pasting the same code.

    from nlp_utils import extract_keywords, pure_python_summarize, \
                          check_ollama_running, ollama_summarize, keybert_keywords
"""

import re
import json
import urllib.request
from collections import Counter

# ── Stopwords ─────────────────────────────────────────────────────────────────
STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "to", "of", "in",
    "on", "at", "by", "for", "with", "from", "as", "or", "and", "but",
    "not", "this", "that", "these", "those", "it", "its", "we", "they",
    "he", "she", "i", "you", "my", "your", "our", "their", "if", "so",
    "about", "into", "than", "then", "when", "where", "who", "which",
    "what", "all", "any", "each", "more", "also", "no", "up", "out",
}


# ── Keyword extraction ────────────────────────────────────────────────────────
def extract_keywords(text: str, num: int = 5) -> list[str]:
    """Return the top `num` keywords using simple word-frequency scoring."""
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    return [word for word, _ in Counter(filtered).most_common(num)]


# ── Extractive summariser ─────────────────────────────────────────────────────
def pure_python_summarize(text: str, sentences: int = 5) -> str:
    """Return an extractive summary of `sentences` sentences."""
    sents = re.split(r'(?<=[.!?])\s+', text)
    if len(sents) <= sentences:
        return text
    word_freq = Counter(
        w for w in re.findall(r'\b[a-z]{4,}\b', text.lower())
        if w not in STOPWORDS
    )
    max_freq = max(word_freq.values()) if word_freq else 1

    def score(s):
        return sum(
            word_freq.get(w, 0) / max_freq
            for w in re.findall(r'\b[a-z]{4,}\b', s.lower())
            if w not in STOPWORDS
        )

    top = sorted(sents, key=score, reverse=True)[:sentences]
    # Restore original order
    ordered = sorted(top, key=lambda s: sents.index(s))
    return " ".join(ordered)


# ── Spell-check / grammar clean ───────────────────────────────────────────────
def clean_grammar(text: str) -> str:
    """Basic spell-correction using pyspellchecker (falls back silently)."""
    try:
        from spellchecker import SpellChecker
        spell = SpellChecker()
        text = re.sub(r'\s+([.,!?])', r'\1', text)
        corrected = []
        for word in text.split():
            bare = re.sub(r'[^\w]', '', word)
            if len(bare) > 4 and bare.isalpha() and bare.lower() not in spell:
                fix = spell.correction(bare)
                if fix:
                    word = word.replace(bare, fix)
            corrected.append(word)
        return " ".join(corrected)
    except ImportError:
        return text


# ── Ollama helpers ────────────────────────────────────────────────────────────
def check_ollama_running() -> bool:
    """Return True if the local Ollama server responds."""
    try:
        urllib.request.urlopen("http://localhost:11434", timeout=2)
        return True
    except Exception:
        return False


def ollama_summarize(text: str, model: str, prompt: str | None = None) -> str:
    """Send text to Ollama and return the summary string (empty on failure)."""
    if not prompt:
        prompt = "Summarize the following text in 3-5 bullet points:\n\n{text}"
    payload = json.dumps({
        "model": model,
        "prompt": prompt.replace("{text}", text[:3000]),
        "stream": False,
    }).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode()).get("response", "").strip()
    except Exception:
        return ""


def get_ollama_models() -> list[str]:
    """Return list of model names installed in Ollama (empty on failure)."""
    import subprocess
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, check=True
        )
        lines = result.stdout.strip().splitlines()
        return [line.split()[0] for line in lines[1:] if line.split()]
    except Exception:
        return []


# ── KeyBERT helper ────────────────────────────────────────────────────────────
def keybert_keywords(text: str, num: int = 5) -> list[str]:
    """Extract keywords with KeyBERT; returns [] if not installed."""
    try:
        from keybert import KeyBERT
        kw_model = KeyBERT()
        kws = kw_model.extract_keywords(
            text, keyphrase_ngram_range=(1, 2), stop_words="english", top_n=num
        )
        return [kw for kw, _ in kws]
    except ImportError:
        return []
