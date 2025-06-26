from pathlib import Path
import csv

CACHED_LOOKUP = {}


def load_cik_lookup(path: Path) -> dict:
    if path in CACHED_LOOKUP:
        return CACHED_LOOKUP[path]
    lookup = {}
    with path.open('r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f, delimiter='|')
        for line in reader:
            if len(line) >= 2:
                ticker = line[0].strip().upper()
                cik = line[1].lstrip('0')
                lookup.setdefault(ticker, set()).add(cik)
    CACHED_LOOKUP[path] = lookup
    return lookup


def find_ciks_by_ticker(ticker: str, lookup_path: Path) -> list[str]:
    lookup = load_cik_lookup(lookup_path)
    return sorted(list(lookup.get(ticker.upper(), [])))
