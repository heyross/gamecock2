from datetime import datetime
from pathlib import Path
from typing import List

from .base import ArchiveDownloader


class EdgarMasterDownloader(ArchiveDownloader):
    BASE_URL = "https://www.sec.gov/Archives/edgar/daily-index/"

    def __init__(self, output_dir: Path, year: int, quarter: int):
        super().__init__(output_dir)
        self.year = year
        self.quarter = quarter

    def generate_urls(self) -> List[str]:
        url = f"{self.BASE_URL}{self.year}/QTR{self.quarter}/master.zip"
        return [url]


class EdgarFilingDownloader(ArchiveDownloader):
    """Download a single EDGAR filing given CIK and accession."""

    BASE_URL = "https://www.sec.gov/Archives/"

    def __init__(self, output_dir: Path, cik: str, accession: str):
        super().__init__(output_dir)
        self.cik = cik.lstrip("0")
        self.accession = accession.replace("-", "")

    def generate_urls(self) -> List[str]:
        path = f"edgar/data/{self.cik}/{self.accession}/{self.accession}-index.html"
        return [self.BASE_URL + path]

