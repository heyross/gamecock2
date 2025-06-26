# Exposure Analysis Plan

The goal of this project is to understand derivative exposure for each party in the available filings and determine when positions or counterparties trigger notable thresholds. The following high level roadmap outlines how to build this analytic process using the existing Gamecock tools.

## 1. Data Ingestion

1. **NCEN and NPORT Filings** – Continue parsing NCEN registrant data and NPORT holdings from the SEC archives using the new parsers. Store LEI mappings, holding values, and relevant CIK/LEI relationships in `gamecock.db`.
2. **EDGAR Filings** – Collect narrative filings that reference derivatives or swaps using the EDGAR downloader. Record filing metadata in the database via `record_filing`.
3. **CFTC Swap Data** – Import swap data from the daily CFTC archives for both credit and equity instruments using the provided downloaders.

## 2. Normalization and Mapping

1. **Entity Resolution** – Map tickers to CIKs and LEIs using the identifiers module and existing `cik_lei` table.
2. **Instrument Categorization** – Normalize instrument identifiers (CUSIP, ISIN, ticker) and tag each holding or swap record with an asset class.
3. **Position Aggregation** – Summarize holdings and swap positions by party, referencing LEIs when available. Link across NCEN, NPORT and CFTC data sets.

## 3. Exposure Calculation

1. **Notional and Market Value** – For each derivative position, capture notional amounts and any reported market value from filings.
2. **Netting Rules** – Implement logic to net long and short exposures by instrument type and counterparty to arrive at a net exposure number per party.
3. **Concentration Metrics** – Calculate concentration ratios by asset class or counterparty to highlight large exposures.

## 4. Trigger Identification

1. **Regulatory Thresholds** – Flag positions that exceed thresholds from regulations (e.g., large trader reporting levels, margin requirements).
2. **Counterparty Risks** – Identify exposures to high-risk counterparties by monitoring ratings or adverse filings.
3. **Portfolio Shifts** – Track significant increases or decreases in exposure over time, raising alerts when changes breach predefined limits.

## 5. Reporting and Visualization

1. **Automated Summaries** – Extend `gamecock.summarizer` to highlight derivative sections from narrative filings and include key exposure statistics.
2. **Dashboards** – Build simple dashboards or CSV reports summarizing exposures by party with indicators for triggered thresholds.

## Next Steps

- Expand parsers to cover additional derivative forms beyond swaps.
- Refine netting and aggregation rules to match industry practice.
- Integrate external data such as ratings or default probabilities for better counterparty risk assessment.
- Improve summarization quality to capture nuanced language around derivatives in filings.
