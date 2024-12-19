# Finance Tracker Bot

Telegram бот для учета личных финансов с FastAPI и PostgreSQL.

## Функциональность
- ✅ Учет доходов и расходов по категориям
- 📊 Просмотр финансовой статистики
- 🔘 Управление через кнопки
- 🌐 REST API

## Требования
- Python 3.8+
- PostgreSQL
- Telegram API credentials
- Telegram Bot Token

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Newport911/Finance_bot_sample.git
```

2. Создайте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
```
или
```bash
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```
3. Настройте .env файл:
спользуйте как пример .env.example. В нем указаны все необходимые параметры для подключения к базе данных и api бота.
4. Настройте alembic.ini сменив логин, пароль и название базы данных Postgresql.
5. Запустите докер через команды:
```bash
docker-compose build

docker-compose up
```
## Использование

### Команды бота

- /start      - Начало работы
- /help       - Список команд
- /statistics - Статистика 
- /categories - Список категорий

### Добавление транзакций

1. Нажмите кнопку:
   - 💰 Добавить доход
   - 💸 Добавить расход

2. Выберите категорию.

3. Введите сумму и описание.

## API Endpoints
1. GET  /api/v1/transactions/  # Получение списка транзакций
2. POST /api/v1/transactions/  # Создание новой транзакции

Лицензия
MIT