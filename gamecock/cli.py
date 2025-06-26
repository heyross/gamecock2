import argparse
from pathlib import Path
from datetime import datetime

from . import database, identifiers, search, exposures
from .parser import ncen as ncen_parser, nport as nport_parser, cftc as cftc_parser
from . import summarizer
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
    parser.add_argument('--parse-ncen', nargs='+', type=Path, help='Parse NCEN filing zip files')
    parser.add_argument('--parse-nport', nargs='+', type=Path, help='Parse NPORT filing zip files')
    parser.add_argument('--parse-cftc', nargs='+', type=Path, help='Parse CFTC swap archives')
    parser.add_argument('--trace-liabilities', help='Trace liability chain for a LEI')
    parser.add_argument('--summarize', type=Path, help='Summarize narrative filing text file')
    parser.add_argument('--aggregate-exposures', action='store_true', help='Aggregate exposures by LEI')
    parser.add_argument('--exposure-threshold', type=float, help='Show exposures exceeding threshold')
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

    if args.parse_ncen:
        for path in args.parse_ncen:
            accession = path.stem
            for row in ncen_parser.parse(path):
                cik = (row.get('CIK') or '').lstrip('0')
                lei = row.get('LEI') or ''
                name = row.get('FUND_NAME') or row.get('NAME') or ''
                database.record_ncen_registrant(cik, lei, name, accession)

    if args.parse_nport:
        for path in args.parse_nport:
            accession = path.stem
            for row in nport_parser.parse(path):
                lei = row.get('LEI') or ''
                issuer = row.get('ISSUER_NAME') or row.get('ISSUER') or ''
                cusip = row.get('CUSIP') or ''
                try:
                    value = float(str(row.get('VALUE') or '0').replace(',', ''))
                except ValueError:
                    value = 0.0
                database.record_nport_holding(lei, issuer, cusip, value, accession)

    if args.parse_cftc:
        for path in args.parse_cftc:
            for row in cftc_parser.parse(path):
                lei = row.get('Reporting party ID') or row.get('Lei') or ''
                d_id = row.get('Dissemination Identifier') or row.get('ID') or ''
                product = row.get('Product name') or ''
                try:
                    notional1 = float(str(row.get('Notional amount-Leg 1') or '0').replace(',', ''))
                except ValueError:
                    notional1 = 0.0
                try:
                    notional2 = float(str(row.get('Notional amount-Leg 2') or '0').replace(',', ''))
                except ValueError:
                    notional2 = 0.0
                database.record_cftc_swap(d_id, lei, product, notional1, notional2)

    if args.trace_liabilities:
        for row in search.trace_liability_chain(args.trace_liabilities):
            print(row)

    if args.summarize:
        print(summarizer.summarize_file(args.summarize))

    if args.aggregate_exposures:
        for row in exposures.aggregate_exposures_by_lei():
            print(row)

    if args.exposure_threshold is not None:
        for row in exposures.find_exposure_triggers(args.exposure_threshold):
            print(row)


if __name__ == '__main__':
    main()

