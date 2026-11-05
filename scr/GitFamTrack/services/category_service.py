"""Сервис категорий расходов."""
from models.models import Category, CategoryTotal, User, PARENT_ROLE_ID
from repositories import category_repository


def _require_parent(actor: User):
    if actor.role_id != PARENT_ROLE_ID:
        raise Exception("Действие доступно только родителю")


def _check_name(name: str, exclude_id: int | None = None):
    if not name.strip():
        raise Exception("Название категории не может быть пустым")
    for c in category_repository.get_all():
        if c.name.lower() == name.strip().lower() and c.category_id != exclude_id:
            raise Exception("Категория уже существует")


def get_all_categories() -> list[Category]:
    return category_repository.get_all()


def create_category(actor: User, name: str):
    _require_parent(actor)
    _check_name(name)
    category_repository.create(name.strip())


def update_category(actor: User, category_id: int, name: str):
    _require_parent(actor)
    if not category_repository.get_by_id(category_id):
        raise Exception("Категория не найдена")
    _check_name(name, exclude_id=category_id)
    category_repository.update(category_id, name.strip())


def delete_category(actor: User, category_id: int):
    _require_parent(actor)
    if not category_repository.get_by_id(category_id):
        raise Exception("Категория не найдена")
    if category_repository.count_expenses(category_id) > 0:
        raise Exception("Нельзя удалить категорию, в которой есть расходы")
    category_repository.delete(category_id)


def get_totals_by_category(actor: User) -> list[CategoryTotal]:
    """Родитель видит итоги по всей семье, ребёнок — только по себе."""
    if actor.role_id == PARENT_ROLE_ID:
        return category_repository.get_totals()
    return category_repository.get_totals(actor.user_id)
