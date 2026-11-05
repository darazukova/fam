"""UI: консольные меню. Работает только через сервисы, без SQL."""
from datetime import date

from services import (
    category_service,
    expense_service,
    user_service,
)
from ui import auth


# ---------- вспомогательные функции вывода ----------

def _print_expenses(expenses):
    if not expenses:
        print("Расходов нет.")
        return
    print(f"{'ID':<4}{'Дата':<12}{'Кто':<16}{'Категория':<14}{'Сумма':>10}  Описание")
    for e in expenses:
        print(
            f"{e.expense_id:<4}{e.expense_date:<12}{e.user_name:<16}"
            f"{e.category_name:<14}{e.amount:>10.2f}  {e.description or ''}"
        )


def _print_categories(categories):
    for c in categories:
        print(f"  {c.category_id}. {c.name}")


def _read_int(prompt: str) -> int | None:
    value = input(prompt).strip()
    if not value.isdigit():
        print("Ошибка: нужно ввести целое число")
        return None
    return int(value)


def _safe(action):
    """Выполняет действие и показывает ошибку бизнес-логики пользователю."""
    try:
        action()
    except Exception as e:
        print(f"Ошибка: {e}")


# ---------- расходы ----------

def _show_expenses(user):
    _print_expenses(expense_service.get_expenses(user))
    print(f"Итого: {expense_service.get_total(user):.2f}")


def _add_expense(user):
    print("\n--- Новый расход ---")
    owner_id = None
    if user.role_id == 1:
        value = input("ID пользователя (Enter — для себя): ").strip()
        if value:
            if not value.isdigit():
                print("Ошибка: нужно ввести целое число")
                return
            owner_id = int(value)
    amount = input("Сумма: ")
    expense_date = input(f"Дата ГГГГ-ММ-ДД (Enter — {date.today()}): ").strip() \
        or str(date.today())
    print("Категории:")
    _print_categories(category_service.get_all_categories())
    category_id = _read_int("ID категории: ")
    if category_id is None:
        return
    description = input("Описание: ")

    def action():
        expense_service.create_expense(
            user, amount, expense_date, description, category_id, owner_id
        )
        print("Расход добавлен.")
    _safe(action)


def _edit_expense(user):
    _print_expenses(expense_service.get_expenses(user))
    expense_id = _read_int("ID расхода для изменения: ")
    if expense_id is None:
        return
    amount = input("Новая сумма: ")
    expense_date = input("Новая дата ГГГГ-ММ-ДД: ")
    print("Категории:")
    _print_categories(category_service.get_all_categories())
    category_id = _read_int("ID категории: ")
    if category_id is None:
        return
    description = input("Новое описание: ")

    def action():
        expense_service.update_expense(
            user, expense_id, amount, expense_date, description, category_id
        )
        print("Расход изменён.")
    _safe(action)


def _delete_expense(user):
    _print_expenses(expense_service.get_expenses(user))
    expense_id = _read_int("ID расхода для удаления: ")
    if expense_id is None:
        return

    def action():
        expense_service.delete_expense(user, expense_id)
        print("Расход удалён.")
    _safe(action)


def _show_totals(user):
    totals = category_service.get_totals_by_category(user)
    if not totals:
        print("Данных нет.")
        return
    print("\nРасходы по категориям:")
    for t in totals:
        print(f"  {t.category_name}: {t.total:.2f}")


def expenses_menu(user):
    while True:
        print("\n===== Расходы =====")
        print("1. Просмотр расходов")
        print("2. Добавить расход")
        print("3. Изменить расход")
        print("4. Удалить расход")
        print("5. Расходы по категориям")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            _show_expenses(user)
        elif choice == "2":
            _add_expense(user)
        elif choice == "3":
            _edit_expense(user)
        elif choice == "4":
            _delete_expense(user)
        elif choice == "5":
            _show_totals(user)
        elif choice == "0":
            break
        else:
            print("Неверный пункт меню")


# ---------- категории (родитель) ----------

def categories_menu(user):
    while True:
        print("\n===== Категории =====")
        print("1. Список категорий")
        print("2. Добавить категорию")
        print("3. Переименовать категорию")
        print("4. Удалить категорию")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            _print_categories(category_service.get_all_categories())
        elif choice == "2":
            name = input("Название: ")

            def action():
                category_service.create_category(user, name)
                print("Категория добавлена.")
            _safe(action)
        elif choice == "3":
            _print_categories(category_service.get_all_categories())
            category_id = _read_int("ID категории: ")
            if category_id is None:
                continue
            name = input("Новое название: ")

            def action():
                category_service.update_category(user, category_id, name)
                print("Категория изменена.")
            _safe(action)
        elif choice == "4":
            _print_categories(category_service.get_all_categories())
            category_id = _read_int("ID категории: ")
            if category_id is None:
                continue

            def action():
                category_service.delete_category(user, category_id)
                print("Категория удалена.")
            _safe(action)
        elif choice == "0":
            break
        else:
            print("Неверный пункт меню")


# ---------- пользователи (родитель) ----------

def users_menu(user):
    while True:
        print("\n===== Пользователи =====")
        print("1. Список пользователей")
        print("2. Добавить родителя")
        print("3. Изменить пользователя")
        print("4. Удалить пользователя")
        print("0. Назад")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            _safe(lambda: [
                print(f"  {u.user_id}. {u.full_name} ({u.login}) — {u.role_name}")
                for u in user_service.get_all_users(user)
            ])
        elif choice == "2":
            auth.add_parent(user)
        elif choice == "3":
            user_id = _read_int("ID пользователя: ")
            if user_id is None:
                continue
            full_name = input("Новое имя: ")
            role_id = _read_int("Роль (1 — Родитель, 2 — Ребенок): ")
            if role_id is None:
                continue

            def action():
                user_service.update_user(user, user_id, full_name, role_id)
                print("Пользователь изменён.")
            _safe(action)
        elif choice == "4":
            user_id = _read_int("ID пользователя: ")
            if user_id is None:
                continue

            def action():
                user_service.delete_user(user, user_id)
                print("Пользователь удалён.")
            _safe(action)
        elif choice == "0":
            break
        else:
            print("Неверный пункт меню")


# ---------- меню по ролям ----------

def parent_menu(user):
    while True:
        print(f"\n===== Родитель ({user.login}) =====")
        print("1. Расходы")
        print("2. Категории")
        print("3. Пользователи")
        print("0. Выход из аккаунта")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            expenses_menu(user)
        elif choice == "2":
            categories_menu(user)
        elif choice == "3":
            users_menu(user)
        elif choice == "0":
            break
        else:
            print("Неверный пункт меню")


def child_menu(user):
    while True:
        print(f"\n===== Ребенок ({user.login}) =====")
        print("1. Мои расходы")
        print("0. Выход из аккаунта")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            expenses_menu(user)
        elif choice == "0":
            break
        else:
            print("Неверный пункт меню")


def main_menu():
    while True:
        print("\n===== FamTrack: учёт семейного бюджета =====")
        print("1. Войти")
        print("2. Зарегистрироваться")
        print("0. Выход")
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            user = auth.login()
            if user:
                if user.role_id == 1:
                    parent_menu(user)
                else:
                    child_menu(user)
        elif choice == "2":
            auth.register()
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню")
