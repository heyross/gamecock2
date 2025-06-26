# Gamecock

This project provides tools for downloading and analyzing swap data from CFTC archives and related SEC filings. A small command line interface enables looking up CIKs by ticker symbol and downloading daily swap archives.

## Usage

Install Python 3.12 or newer and run:

```bash
python scripts/gamecock.py TICKER --download-cftc
```

The first run creates a `gamecock.db` SQLite database to track downloaded files. Additional modules and features will be added over time.

