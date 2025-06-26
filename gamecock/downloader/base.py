from __future__ import annotations
import logging
from pathlib import Path
from abc import ABC, abstractmethod
import requests

from .. import database

log = logging.getLogger(__name__)


class ArchiveDownloader(ABC):
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def generate_urls(self) -> list[str]:
        ...

    def download(self):
        urls = self.generate_urls()
        for url in urls:
            filename = url.split('/')[-1]
            target = self.output_dir / filename
            if database.file_exists(url) and target.exists():
                log.info("Skipping %s, already downloaded", url)
                continue
            log.info("Downloading %s", url)
            try:
                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
            except Exception as e:
                log.error("Failed %s: %s", url, e)
                continue
            target.write_bytes(resp.content)
            database.record_file(url, target, len(resp.content))

