DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_roles;

-- 2. Справочники
CREATE TABLE user_roles (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE
);

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL UNIQUE
);

-- 3. Основные таблицы
CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name     TEXT NOT NULL,
    login         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role_id       INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES user_roles (role_id)
);

-- 4. Таблица с несколькими внешними ключами
CREATE TABLE expenses (
    expense_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    amount       REAL NOT NULL CHECK (amount > 0),
    expense_date TEXT NOT NULL,
    description  TEXT,
    user_id      INTEGER NOT NULL,
    category_id  INTEGER NOT NULL,
    FOREIGN KEY (user_id)     REFERENCES users (user_id),
    FOREIGN KEY (category_id) REFERENCES categories (category_id)
);

-- 5. Тестовые данные
INSERT INTO user_roles (name) VALUES
    ('Родитель'),
    ('Ребенок');

INSERT INTO categories (name) VALUES
    ('Продукты'),
    ('Транспорт'),
    ('Одежда'),
    ('Развлечения'),
    ('Учеба');

-- Пароль у всех тестовых пользователей: 1234 (хранится SHA-256 хеш)
INSERT INTO users (full_name, login, password_hash, role_id) VALUES
    ('Анна Жукова',  'anna',  '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 1),
    ('Игорь Жуков',  'igor',  '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 1),
    ('Мария Жукова', 'maria', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 2),
    ('Миша Жуков',   'misha', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 2);

INSERT INTO expenses (amount, expense_date, description, user_id, category_id) VALUES
    (2500.50, '2026-10-20', 'Покупки в магазине',   1, 1),
    (1800.00, '2026-10-21', 'Бензин',               2, 2),
    (4200.00, '2026-10-21', 'Куртка',               1, 3),
    (450.00,  '2026-10-22', 'Кино',                 3, 4),
    (320.00,  '2026-10-22', 'Тетради и ручки',      4, 5),
    (150.00,  '2026-10-22', 'Проезд в автобусе',    3, 2);
