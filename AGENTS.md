# Agent Notes

## Completed
- Added downloaders for equity and commodity swaps and individual EDGAR filings.
- Expanded SQLite schema with LEI mapping and tables for NCEN registrants and NPORT holdings.
- Implemented basic search utility to find filings by LEI and exposed new CLI options.

## Next Session
- Parse NCEN and NPORT filings into the new tables.
- Build queries that walk CIK/LEI links to trace liability chains across datasets.
- Integrate local LLM summarization of narrative filings to extract derivative details.

