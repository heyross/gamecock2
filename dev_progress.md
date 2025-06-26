# Development Progress

## Initial Refactor
- Created package `gamecock` with modules for database, CLI, identifier lookup, downloaders, and parsers.
- Implemented `ArchiveDownloader` base class and CFTC/EDGAR downloaders using it.
- Added SQLite database helpers for recording downloaded files.
- Added simple NCEN parser as example dataset parser.
- Added command line interface supporting ticker lookup and a sample CFTC download action.
- Added entry script `scripts/gamecock.py`.
