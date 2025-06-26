"""Simple local summarization utilities."""

import re
from pathlib import Path


def summarize_text(text: str, max_sentences: int = 5) -> str:
    """Return a crude summary focusing on derivative-related sentences."""
    sentences = re.split(r"(?<=[.!?]) +", text)
    relevant = [s.strip() for s in sentences if re.search(r"derivative|swap", s, re.I)]
    if not relevant:
        relevant = sentences[:max_sentences]
    return " ".join(relevant[:max_sentences])


def summarize_file(path: Path, max_sentences: int = 5) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return summarize_text(text, max_sentences)
