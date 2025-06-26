import argparse
from pathlib import Path
from datetime import datetime

from . import database, identifiers, search
from .downloader.cftc import (
    CFTCCreditDownloader,
    CFTCEquityDownloader,
    CFTCCommodityDownloader,
)
from .downloader.edgar import EdgarFilingDownloader


DEFAULT_LOOKUP = Path('cik-lookup-data.txt')


def main():
    parser = argparse.ArgumentParser(description="Gamecock CLI")
    parser.add_argument('ticker', nargs='?', help='Ticker symbol to search')
    parser.add_argument('--lookup', type=Path, default=DEFAULT_LOOKUP, help='Path to cik lookup')
    parser.add_argument('--download-cftc', action='store_true', help='Download CFTC credit archives for last day')
    parser.add_argument('--download-equity', action='store_true', help='Download CFTC equity archives for last day')
    parser.add_argument('--download-commodity', action='store_true', help='Download CFTC commodity archives for last day')
    parser.add_argument('--download-filing', nargs=2, metavar=('CIK', 'ACCESSION'), help='Download a specific EDGAR filing')
    parser.add_argument('--trace-lei', help='Search filings associated with a LEI')
    args = parser.parse_args()

    database.init_db()

    if args.ticker:
        ciks = identifiers.find_ciks_by_ticker(args.ticker, args.lookup)
        print(f'CIKs for {args.ticker}: {", ".join(ciks) if ciks else "none"}')

    if args.download_cftc:
        today = datetime.utcnow().date()
        dl = CFTCCreditDownloader(Path('cftc_credit'), today, today)
        dl.download()

    if args.download_equity:
        today = datetime.utcnow().date()
        dl = CFTCEquityDownloader(Path('cftc_equity'), today, today)
        dl.download()

    if args.download_commodity:
        today = datetime.utcnow().date()
        dl = CFTCCommodityDownloader(Path('cftc_commodity'), today, today)
        dl.download()

    if args.download_filing:
        cik, accession = args.download_filing
        dl = EdgarFilingDownloader(Path('edgar_filings'), cik, accession)
        dl.download()

    if args.trace_lei:
        for filing in search.find_filings_by_lei(args.trace_lei):
            print(filing)


if __name__ == '__main__':
    main()

