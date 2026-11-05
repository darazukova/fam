"""Репозиторий таблицы users (CRUD)."""
from database.database import get_connection
from models.models import User

_SELECT = """
    SELECT u.user_id, u.full_name, u.login, u.password_hash,
           u.role_id, r.name
    FROM users u
    JOIN user_roles r ON u.role_id = r.role_id
"""


def _map(row) -> User:
    return User(*row)


def create(full_name: str, login: str, password_hash: str, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO users(full_name, login, password_hash, role_id)
        VALUES (?, ?, ?, ?)
        """,
        (full_name, login, password_hash, role_id),
    )
    conn.commit()
    conn.close()


def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE u.user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE u.login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY u.user_id")
    result = [_map(r) for r in cur.fetchall()]
    conn.close()
    return result


def update(user_id: int, full_name: str, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET full_name = ?, role_id = ? WHERE user_id = ?",
        (full_name, role_id, user_id),
    )
    conn.commit()
    conn.close()


def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def count_expenses(user_id: int) -> int:
    """Сколько расходов у пользователя."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM expenses WHERE user_id = ?", (user_id,))
    count = cur.fetchone()[0]
    conn.close()
    return count
