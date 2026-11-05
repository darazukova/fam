"""Репозиторий таблицы categories (CRUD)."""
from database.database import get_connection
from models.models import Category, CategoryTotal


def _map(row) -> Category:
    return Category(*row)


def create(name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO categories(name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


def get_by_id(category_id: int) -> Category | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT category_id, name FROM categories WHERE category_id = ?",
        (category_id,),
    )
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Category]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT category_id, name FROM categories ORDER BY category_id")
    result = [_map(r) for r in cur.fetchall()]
    conn.close()
    return result


def update(category_id: int, name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE categories SET name = ? WHERE category_id = ?",
        (name, category_id),
    )
    conn.commit()
    conn.close()


def delete(category_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM categories WHERE category_id = ?", (category_id,))
    conn.commit()
    conn.close()


def count_expenses(category_id: int) -> int:
    """Сколько расходов привязано к категории."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM expenses WHERE category_id = ?", (category_id,)
    )
    count = cur.fetchone()[0]
    conn.close()
    return count


def get_totals(user_id: int | None = None) -> list[CategoryTotal]:
    """Сумма расходов по категориям (всех или одного пользователя)."""
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        SELECT c.name, SUM(e.amount)
        FROM expenses e
        JOIN categories c ON e.category_id = c.category_id
    """
    params: tuple = ()
    if user_id is not None:
        sql += " WHERE e.user_id = ?"
        params = (user_id,)
    sql += " GROUP BY c.name ORDER BY SUM(e.amount) DESC"
    cur.execute(sql, params)
    result = [CategoryTotal(*r) for r in cur.fetchall()]
    conn.close()
    return result
