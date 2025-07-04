# Gamecock

This project provides tools for downloading and analyzing swap data from CFTC archives and related SEC filings. A small command line interface enables looking up CIKs by ticker symbol and downloading daily swap archives.

## Usage

Install Python 3.12 or newer and run:

```bash
python scripts/gamecock.py TICKER --download-cftc
```

Additional options allow downloading equity or commodity swap archives, EDGAR filings, and tracing LEIs:

```bash
python scripts/gamecock.py --download-equity
python scripts/gamecock.py --download-filing 0000320193 0000320193-24-000010
python scripts/gamecock.py --trace-lei XXXXXXXXXXXX
python scripts/gamecock.py --parse-ncen path/to/file.zip
python scripts/gamecock.py --parse-nport path/to/file.zip
python scripts/gamecock.py --trace-liabilities XXXXXXXXXXXX
python scripts/gamecock.py --summarize filing.txt
python scripts/gamecock.py --parse-cftc path/to/archive.zip
python scripts/gamecock.py --aggregate-exposures
python scripts/gamecock.py --exposure-threshold 1000000
```

The first run creates a `gamecock.db` SQLite database to track downloaded files. Additional modules and features will be added over time.

