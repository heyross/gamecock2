from datetime import datetime, timedelta
from pathlib import Path
from typing import List

from .base import ArchiveDownloader


class CFTCCreditDownloader(ArchiveDownloader):
    BASE_URL = "https://kgc0418-tdw-data-0.s3.us-gov-west-1.amazonaws.com/s3fs-public/DCIO/DCIOSwapsData/credit/"

    def __init__(self, output_dir: Path, start_date: datetime, end_date: datetime):
        super().__init__(output_dir)
        self.start_date = start_date
        self.end_date = end_date

    def generate_urls(self) -> List[str]:
        urls = []
        date = self.start_date
        while date <= self.end_date:
            name = f"{date.strftime('%Y-%m-%d')}.zip"
            urls.append(self.BASE_URL + name)
            date += timedelta(days=1)
        return urls

