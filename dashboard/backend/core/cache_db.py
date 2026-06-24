import hashlib
import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "cache.db"


def _ensure_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS experiment_cache (
            cache_key TEXT PRIMARY KEY,
            endpoint TEXT NOT NULL,
            params_json TEXT NOT NULL,
            result_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def make_cache_key(params: Dict[str, Any]) -> str:
    normalized = json.dumps(params, sort_keys=True)
    return hashlib.sha256(normalized.encode()).hexdigest()


def get_cached(endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    _ensure_db()
    key = make_cache_key({"endpoint": endpoint, **params})
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT result_json FROM experiment_cache WHERE cache_key = ?", (key,)
    ).fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None


def set_cached(endpoint: str, params: Dict[str, Any], result: Dict[str, Any]) -> None:
    _ensure_db()
    key = make_cache_key({"endpoint": endpoint, **params})
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        INSERT OR REPLACE INTO experiment_cache (cache_key, endpoint, params_json, result_json)
        VALUES (?, ?, ?, ?)
        """,
        (key, endpoint, json.dumps(params), json.dumps(result)),
    )
    conn.commit()
    conn.close()
