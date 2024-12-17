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
git clone https://github.com/yourusername/finance-tracker-bot.git
cd finance-tracker-bot
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
Скопируйте .env.example в .env
Заполните необходимые данные
4. Настройте базу данных:
```bash
alembic upgrade head
python -m app.init_db
```
5. Запустите бота:
```bash
python run.py
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