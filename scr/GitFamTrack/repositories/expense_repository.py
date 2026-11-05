"""Репозиторий таблицы expenses (CRUD)."""
from database.database import get_connection
from models.models import Expense

_SELECT = """
    SELECT e.expense_id, e.amount, e.expense_date, e.description,
           e.user_id, e.category_id, u.full_name, c.name
    FROM expenses e
    JOIN users u ON e.user_id = u.user_id
    JOIN categories c ON e.category_id = c.category_id
"""


def _map(row) -> Expense:
    return Expense(*row)


def create(amount: float, expense_date: str, description: str | None,
           user_id: int, category_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO expenses(amount, expense_date, description,
                             user_id, category_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (amount, expense_date, description, user_id, category_id),
    )
    conn.commit()
    conn.close()


def get_by_id(expense_id: int) -> Expense | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE e.expense_id = ?", (expense_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Expense]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY e.expense_date, e.expense_id")
    result = [_map(r) for r in cur.fetchall()]
    conn.close()
    return result


def get_by_user(user_id: int) -> list[Expense]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        _SELECT + " WHERE e.user_id = ? ORDER BY e.expense_date, e.expense_id",
        (user_id,),
    )
    result = [_map(r) for r in cur.fetchall()]
    conn.close()
    return result


def update(expense_id: int, amount: float, expense_date: str,
           description: str | None, category_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE expenses
        SET amount = ?, expense_date = ?, description = ?, category_id = ?
        WHERE expense_id = ?
        """,
        (amount, expense_date, description, category_id, expense_id),
    )
    conn.commit()
    conn.close()


def delete(expense_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
    conn.commit()
    conn.close()


def get_total(user_id: int | None = None) -> float:
    """Общая сумма расходов (всех или одного пользователя)."""
    conn = get_connection()
    cur = conn.cursor()
    if user_id is None:
        cur.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses")
    else:
        cur.execute(
            "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id = ?",
            (user_id,),
        )
    total = cur.fetchone()[0]
    conn.close()
    return total
