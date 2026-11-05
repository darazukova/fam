"""Слой данных FamTrack: подключение к базе данных SQLite."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "famtrack.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_connection():
    """Открывает соединение с базой и включает проверку внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(force: bool = False):
    """Создаёт таблицы и тестовые данные из schema.sql.

    Если база уже существует, данные не затираются (force=False).
    """
    if DB_PATH.exists() and not force:
        return
    conn = get_connection()
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.commit()
    conn.close()
