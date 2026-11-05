"""UI: вход, регистрация и добавление родителя."""
from getpass import getpass

from services import auth_service


def _ask_password(prompt: str) -> str:
    """Ввод пароля; если терминал не поддерживает скрытый ввод — обычный input."""
    try:
        return getpass(prompt)
    except Exception:
        return input(prompt)


def login():
    login_value = input("Логин: ")
    password_value = _ask_password("Пароль: ")

    user = auth_service.authenticate(login_value, password_value)
    if not user:
        print("Неверный логин или пароль")
        return None
    return user


def register():
    print("\n--- Регистрация (роль «Ребенок») ---")
    full_name = input("Полное имя: ")
    login_value = input("Логин: ")
    password_value = _ask_password("Пароль (минимум 4 символа): ")
    try:
        auth_service.register_child(full_name, login_value, password_value)
        print("Регистрация выполнена. Теперь можно войти.")
    except Exception as e:
        print(f"Ошибка: {e}")


def add_parent(actor):
    print("\n--- Добавление родителя ---")
    full_name = input("Полное имя: ")
    login_value = input("Логин: ")
    password_value = _ask_password("Пароль (минимум 4 символа): ")
    try:
        auth_service.add_parent(actor, full_name, login_value, password_value)
        print("Родитель добавлен.")
    except Exception as e:
        print(f"Ошибка: {e}")
