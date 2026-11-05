"""Модели данных: по одному dataclass на каждую таблицу БД."""
from dataclasses import dataclass

# Идентификаторы ролей (соответствуют таблице user_roles)
PARENT_ROLE_ID = 1
CHILD_ROLE_ID = 2


@dataclass
class UserRole:
    role_id: int
    name: str


@dataclass
class Category:
    category_id: int
    name: str


@dataclass
class User:
    user_id: int
    full_name: str
    login: str
    password_hash: str
    role_id: int
    role_name: str | None = None  # служебное поле (из user_roles)


@dataclass
class Expense:
    expense_id: int
    amount: float
    expense_date: str
    description: str | None
    user_id: int
    category_id: int
    user_name: str | None = None      # служебное поле (из users)
    category_name: str | None = None  # служебное поле (из categories)


@dataclass
class CategoryTotal:
    """Результат агрегации: сумма расходов по категории (в БД не хранится)."""
    category_name: str
    total: float
