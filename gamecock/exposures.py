from __future__ import annotations

"""Utilities for aggregating derivative exposures."""

from pathlib import Path
from typing import List, Dict
import sqlite3

from .database import get_connection, DB_NAME


def aggregate_exposures_by_lei(db_path: Path = Path(DB_NAME)) -> List[Dict[str, float]]:
    """Return total exposure numbers grouped by LEI."""
    conn = get_connection(db_path)
    cur = conn.execute(
        "SELECT lei, SUM(value) AS val FROM nport_holding GROUP BY lei"
    )
    nport_map = {row[0]: row[1] or 0.0 for row in cur.fetchall()}

    cftc_map = {}
    try:
        cur = conn.execute(
            "SELECT lei, SUM(notional_leg1 + notional_leg2) AS val FROM cftc_swap GROUP BY lei"
        )
        for row in cur.fetchall():
            cftc_map[row[0]] = row[1] or 0.0
    except sqlite3.OperationalError:
        # table doesn't exist yet
        pass

    leis = set(nport_map) | set(cftc_map)
    exposures = []
    for lei in leis:
        nport_val = nport_map.get(lei, 0.0)
        cftc_val = cftc_map.get(lei, 0.0)
        exposures.append(
            {
                "lei": lei,
                "nport_value": nport_val,
                "cftc_notional": cftc_val,
                "total_exposure": nport_val + cftc_val,
            }
        )
    conn.close()
    return exposures


def find_exposure_triggers(threshold: float, db_path: Path = Path(DB_NAME)) -> List[Dict[str, float]]:
    """Return exposures where totals meet or exceed the given threshold."""
    exposures = aggregate_exposures_by_lei(db_path)
    return [e for e in exposures if e["total_exposure"] >= threshold]
