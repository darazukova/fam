"""Сервис расходов: бизнес-логика и разграничение прав."""
from datetime import datetime

from models.models import Expense, User, PARENT_ROLE_ID
from repositories import expense_repository, user_repository, category_repository


def _is_parent(user: User) -> bool:
    return user.role_id == PARENT_ROLE_ID


def _parse_amount(amount) -> float:
    try:
        value = float(str(amount).replace(",", "."))
    except ValueError:
        raise Exception("Сумма должна быть числом")
    if value <= 0:
        raise Exception("Сумма должна быть больше нуля")
    return value


def _check_date(expense_date: str) -> str:
    try:
        datetime.strptime(expense_date.strip(), "%Y-%m-%d")
    except ValueError:
        raise Exception("Дата должна быть в формате ГГГГ-ММ-ДД")
    return expense_date.strip()


def _check_access(actor: User, expense: Expense):
    """Ребёнок может работать только со своими расходами."""
    if not _is_parent(actor) and expense.user_id != actor.user_id:
        raise Exception("Нельзя изменять чужие расходы")


def get_expenses(actor: User) -> list[Expense]:
    """Родитель видит все расходы семьи, ребёнок — только свои."""
    if _is_parent(actor):
        return expense_repository.get_all()
    return expense_repository.get_by_user(actor.user_id)


def get_total(actor: User) -> float:
    if _is_parent(actor):
        return expense_repository.get_total()
    return expense_repository.get_total(actor.user_id)


def create_expense(actor: User, amount, expense_date: str,
                   description: str | None, category_id: int,
                   user_id: int | None = None):
    """Добавление расхода.

    Родитель может указать user_id любого члена семьи,
    ребёнок всегда добавляет расход себе.
    """
    value = _parse_amount(amount)
    date = _check_date(expense_date)

    owner_id = user_id if (_is_parent(actor) and user_id) else actor.user_id
    if not user_repository.get_by_id(owner_id):
        raise Exception("Пользователь не найден")
    if not category_repository.get_by_id(category_id):
        raise Exception("Категория не найдена")

    expense_repository.create(
        value, date, (description or "").strip() or None, owner_id, category_id
    )


def update_expense(actor: User, expense_id: int, amount, expense_date: str,
                   description: str | None, category_id: int):
    expense = expense_repository.get_by_id(expense_id)
    if not expense:
        raise Exception("Расход не найден")
    _check_access(actor, expense)

    value = _parse_amount(amount)
    date = _check_date(expense_date)
    if not category_repository.get_by_id(category_id):
        raise Exception("Категория не найдена")

    expense_repository.update(
        expense_id, value, date, (description or "").strip() or None, category_id
    )


def delete_expense(actor: User, expense_id: int):
    expense = expense_repository.get_by_id(expense_id)
    if not expense:
        raise Exception("Расход не найден")
    _check_access(actor, expense)
    expense_repository.delete(expense_id)
