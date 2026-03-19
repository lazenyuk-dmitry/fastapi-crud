# User Service API (FastAPI)

Backend-сервис на базе FastAPI и SQLAlchemy 2.0 для управления пользователями с разделением ролей (Admin/User).

DEMO: https://fastapi-crud-p9i6.onrender.com/docs

## 🚀 Стек технологий

- Framework: FastAPI
- Database: SQLite (SQLAlchemy + Alembic)
- Auth: JWT (Passlib + Python-Jose)
- Validation: Pydantic v2
- Environment: Python 3.12+

## 🏗 Архитектура

Проект построен по принципу Separation of Concerns:

- api — Маршруты (Routes) и логика обработки HTTP.
- services — Бизнес-логика (Service Layer).
- schemas — Pydantic модели для валидации данных.
- models — SQLAlchemy модели (Database Layer).

## 🛠 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/lazenyuk-dmitry/fastapi-crud.git
cd fastapi-crud
```

### 2. Настройка окружения

```bash
uv sync
```

### 3. Настройте переменные окружения (скопируйте и переименуйте .env.example -> .env)

Можно создать копию командой в терминале

```bash
# Linux / macOS / Git Bash
cp .env.example .env
# В Windows (PowerShell)
copy .env.example .env
```

Заполните своими данными

```bash
DATABASE_URL = "sqlite+aiosqlite:///./data/database.db"
SECRET_KEY = "super-secret-key"
```

### 4. Запуск сервера

```bash
# for production mode
make run
# or for development
make dev
```

## 🔐 Обработка ошибок

В проекте реализована централизованная система обработки исключений. Все бизнес-ошибки наследуются от AppError.

- 404 Not Found — Пользователь не найден.
- 400 Bad Request — Email уже занят или неверные данные.
- 403 Forbidden — Доступ запрещен (не админ или аккаунт деактивирован).

| Метод  | Путь               | Описание                            | Доступ           |
| ------ | ------------------ | ----------------------------------- | ---------------- |
| POST   | /login             | Получение JWT токена (авторизация)  | Публичный        |
| POST   | /users             | Регистрация нового пользователя     | Публичный        |
| GET    | /users             | Получение списка всех пользователей | Admin            |
| GET    | /users/{id}        | Получение данных конкретного юзера  | Admin / Владелец |
| PUT    | /users/{id}        | Полное обновление данных профиля    | Admin / Владелец |
| PATCH  | /users/{id}/status | Активация или деактивация (бан)     | Admin            |
| DELETE | /users/{id}        | Удаление аккаунта из системы        | Admin / Владелец |
