import argparse
from pathlib import Path
from datetime import datetime

from . import database, identifiers
from .downloader.cftc import CFTCCreditDownloader


DEFAULT_LOOKUP = Path('cik-lookup-data.txt')


def main():
    parser = argparse.ArgumentParser(description="Gamecock CLI")
    parser.add_argument('ticker', nargs='?', help='Ticker symbol to search')
    parser.add_argument('--lookup', type=Path, default=DEFAULT_LOOKUP, help='Path to cik lookup')
    parser.add_argument('--download-cftc', action='store_true', help='Download CFTC credit archives for last day')
    args = parser.parse_args()

    database.init_db()

    if args.ticker:
        ciks = identifiers.find_ciks_by_ticker(args.ticker, args.lookup)
        print(f'CIKs for {args.ticker}: {", ".join(ciks) if ciks else "none"}')

    if args.download_cftc:
        today = datetime.utcnow().date()
        dl = CFTCCreditDownloader(Path('cftc_credit'), today, today)
        dl.download()


if __name__ == '__main__':
    main()

