from pathlib import Path
import csv
from typing import Generator, Dict


def parse(zip_path: Path) -> Generator[Dict[str, str], None, None]:
    """Yield holding records from an NPORT zip file."""
    import zipfile

    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if name.endswith("HOLDINGS.tsv"):
                with zf.open(name) as f:
                    reader = csv.DictReader(line.decode('utf-8') for line in f)
                    for row in reader:
                        yield row
