import sqlite3
from pathlib import Path
from datetime import datetime

DB_NAME = "gamecock.db"

def get_connection(db_path: Path = Path(DB_NAME)):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: Path = Path(DB_NAME)):
    conn = get_connection(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            url TEXT UNIQUE,
            path TEXT,
            size INTEGER,
            downloaded_at TIMESTAMP
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS filings (
            cik TEXT,
            accession TEXT,
            form TEXT,
            filepath TEXT,
            downloaded_at TIMESTAMP,
            UNIQUE(cik, accession)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cik_lei (
            cik TEXT PRIMARY KEY,
            lei TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS ncen_registrant (
            cik TEXT,
            lei TEXT,
            name TEXT,
            accession TEXT,
            UNIQUE(lei, accession)
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS nport_holding (
            lei TEXT,
            issuer TEXT,
            cusip TEXT,
            value REAL,
            accession TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cftc_swap (
            dissemination_id TEXT PRIMARY KEY,
            lei TEXT,
            product TEXT,
            notional_leg1 REAL,
            notional_leg2 REAL
        )
        """
    )
    conn.commit()
    conn.close()


def record_filing(
    cik: str,
    accession: str,
    form: str,
    filepath: Path,
    db_path: Path = Path(DB_NAME),
):
    """Record a downloaded filing in the database."""
    conn = get_connection(db_path)
    conn.execute(
        "INSERT OR IGNORE INTO filings(cik, accession, form, filepath, downloaded_at)"
        " VALUES(?,?,?,?,?)",
        (cik, accession, form, str(filepath), datetime.utcnow()),
    )
    conn.commit()
    conn.close()


def record_file(url: str, path: Path, size: int, db_path: Path = Path(DB_NAME)):
    conn = get_connection(db_path)
    conn.execute(
        "INSERT OR IGNORE INTO files(url, path, size, downloaded_at) VALUES(?,?,?,?)",
        (url, str(path), size, datetime.utcnow()),
    )
    conn.commit()
    conn.close()


def file_exists(url: str, db_path: Path = Path(DB_NAME)) -> bool:
    conn = get_connection(db_path)
    cur = conn.execute("SELECT 1 FROM files WHERE url=?", (url,))
    exists = cur.fetchone() is not None
    conn.close()
    return exists


def record_cik_lei(cik: str, lei: str, db_path: Path = Path(DB_NAME)):
    conn = get_connection(db_path)
    conn.execute(
        "INSERT OR REPLACE INTO cik_lei(cik, lei) VALUES(?, ?)",
        (cik, lei),
    )
    conn.commit()
    conn.close()


def record_ncen_registrant(
    cik: str, lei: str, name: str, accession: str, db_path: Path = Path(DB_NAME)
):
    conn = get_connection(db_path)
    conn.execute(
        "INSERT OR IGNORE INTO ncen_registrant(cik, lei, name, accession) VALUES(?,?,?,?)",
        (cik, lei, name, accession),
    )
    conn.commit()
    conn.close()


def record_nport_holding(
    lei: str,
    issuer: str,
    cusip: str,
    value: float,
    accession: str,
    db_path: Path = Path(DB_NAME),
):
    conn = get_connection(db_path)
    conn.execute(
        "INSERT OR IGNORE INTO nport_holding(lei, issuer, cusip, value, accession) VALUES(?,?,?,?,?)",
        (lei, issuer, cusip, value, accession),
    )
    conn.commit()
    conn.close()


def record_cftc_swap(
    dissemination_id: str,
    lei: str,
    product: str,
    notional_leg1: float,
    notional_leg2: float,
    db_path: Path = Path(DB_NAME),
):
    conn = get_connection(db_path)
    conn.execute(
        """
        INSERT OR IGNORE INTO cftc_swap(
            dissemination_id,
            lei,
            product,
            notional_leg1,
            notional_leg2
        ) VALUES(?,?,?,?,?)
        """,
        (dissemination_id, lei, product, notional_leg1, notional_leg2),
    )
    conn.commit()
    conn.close()
