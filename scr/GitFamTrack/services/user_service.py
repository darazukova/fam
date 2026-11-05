"""Сервис управления пользователями (для роли «Родитель»)."""
from models.models import User, PARENT_ROLE_ID
from repositories import user_repository, role_repository


def _require_parent(actor: User):
    if actor.role_id != PARENT_ROLE_ID:
        raise Exception("Действие доступно только родителю")


def get_all_users(actor: User) -> list[User]:
    _require_parent(actor)
    return user_repository.get_all()


def update_user(actor: User, user_id: int, full_name: str, role_id: int):
    _require_parent(actor)
    if not user_repository.get_by_id(user_id):
        raise Exception("Пользователь не найден")
    if not full_name.strip():
        raise Exception("Имя не может быть пустым")
    if not role_repository.get_by_id(role_id):
        raise Exception("Роль не найдена")
    user_repository.update(user_id, full_name.strip(), role_id)


def delete_user(actor: User, user_id: int):
    _require_parent(actor)
    if actor.user_id == user_id:
        raise Exception("Нельзя удалить самого себя")
    if not user_repository.get_by_id(user_id):
        raise Exception("Пользователь не найден")
    if user_repository.count_expenses(user_id) > 0:
        raise Exception("Нельзя удалить пользователя, у которого есть расходы")
    user_repository.delete(user_id)
