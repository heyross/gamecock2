from pathlib import Path
from typing import List

from .database import get_connection, DB_NAME


def find_filings_by_lei(lei: str, db_path: Path = Path(DB_NAME)) -> List[dict]:
    """Return filings associated with the given LEI."""
    conn = get_connection(db_path)
    cur = conn.execute(
        """
        SELECT f.cik, f.accession, f.form, f.filepath
        FROM filings f
        JOIN ncen_registrant n ON f.cik = n.cik
        WHERE n.lei = ?
        """,
        (lei,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def trace_liability_chain(lei: str, db_path: Path = Path(DB_NAME)) -> List[dict]:
    """Return NPORT holdings for the NCEN registrant identified by LEI."""
    conn = get_connection(db_path)
    cur = conn.execute(
        """
        SELECT n.cik, n.lei, n.name, n.accession,
               h.issuer, h.cusip, h.value
        FROM ncen_registrant n
        LEFT JOIN nport_holding h ON n.lei = h.lei
        WHERE n.lei = ?
        """,
        (lei,),
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows
