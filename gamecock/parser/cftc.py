from __future__ import annotations

"""Parser for CFTC swap CSV or zip archives."""

from pathlib import Path
from typing import Dict, Generator, IO
import csv
import zipfile
from io import TextIOWrapper


def _row_reader(f: IO[str]) -> Generator[Dict[str, str], None, None]:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        yield row


def parse(path: Path) -> Generator[Dict[str, str], None, None]:
    """Yield swap records from a CSV or zipped CSV file."""
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as zf:
            for name in zf.namelist():
                if name.endswith(".csv"):
                    with zf.open(name) as f:
                        yield from _row_reader(TextIOWrapper(f, "utf-8"))
    else:
        with path.open(encoding="utf-8") as f:
            yield from _row_reader(f)
