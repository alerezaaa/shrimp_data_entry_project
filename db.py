import sqlite3

def init_db(db_path: str) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT,
            daily_feed REAL,
            feed_percentage REAL,
            avg_weight REAL,
            current_count INTEGER,
            larve_count INTEGER,
            survival_rate REAL,
            biomass REAL,
            daily_feeding_rate REAL
        )
        """)
        conn.commit()

def insert_record(db_path: str, r: dict) -> None:
    if r != {}:
        with sqlite3.connect(db_path) as conn:
            conn.execute("""
            INSERT INTO records
            (created_at, daily_feed, feed_percentage, avg_weight, current_count, larve_count,
            survival_rate, biomass, daily_feeding_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                r.get("created_at"),
                r.get("daily_feed"),
                r.get("feed_percentage"),
                r.get("avg_weight"),
                r.get("current_count"),
                r.get("larve_count"),
                r.get("survival_rate"),
                r.get("biomass"),
                r.get("daily_feeding_rate"),
            ))
            conn.commit()
            

def count_records(db_path: str) -> int:
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute("SELECT COUNT(*) FROM records")
        return cur.fetchone()[0]

def fetch_latest_record(db_path: str) -> dict | None:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM records ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        return dict(row) if row else None


def fetch_records(db_path: str, limit: int = 50) -> list[dict]:
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(
            "SELECT * FROM records ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cur.fetchall()
        return [dict(r) for r in rows]
    
    
def delete_record(db_path: str, record_id: int) -> None:
    with sqlite3.connect(db_path) as conn:
        print(f"Count records before deletion: {count_records(db_path)}")
        conn.execute("DELETE FROM records WHERE id = ?", (record_id,))
        print(f"Count records after deletion: {count_records(db_path)}")
        conn.commit()

