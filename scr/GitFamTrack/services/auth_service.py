"""Сервис авторизации и регистрации."""
import hashlib

from models.models import User, PARENT_ROLE_ID, CHILD_ROLE_ID
from repositories import user_repository


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate(login: str, password: str) -> User | None:
    """Возвращает пользователя, если логин и пароль верны, иначе None."""
    user = user_repository.get_by_login(login.strip())
    if user and user.password_hash == hash_password(password):
        return user
    return None


def _validate(full_name: str, login: str, password: str):
    if not full_name.strip():
        raise Exception("Имя не может быть пустым")
    if not login.strip():
        raise Exception("Логин не может быть пустым")
    if len(password) < 4:
        raise Exception("Пароль должен содержать минимум 4 символа")
    if user_repository.get_by_login(login.strip()):
        raise Exception("Пользователь с таким логином уже существует")


def register_child(full_name: str, login: str, password: str):
    """Самостоятельная регистрация: создаётся пользователь с ролью «Ребенок»."""
    _validate(full_name, login, password)
    user_repository.create(
        full_name.strip(), login.strip(), hash_password(password), CHILD_ROLE_ID
    )


def add_parent(actor: User, full_name: str, login: str, password: str):
    """Добавление нового родителя (доступно только родителю)."""
    if actor.role_id != PARENT_ROLE_ID:
        raise Exception("Только родитель может добавлять родителей")
    _validate(full_name, login, password)
    user_repository.create(
        full_name.strip(), login.strip(), hash_password(password), PARENT_ROLE_ID
    )
