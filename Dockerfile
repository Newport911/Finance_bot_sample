FROM python:3.9-slim

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода проекта
COPY . /app

# Установка рабочей директории
WORKDIR /app/finance_bot

# Выполнение команды запуска приложения
CMD ["sh", "-c", "alembic upgrade head && python -c 'from app.init_db import init_categories; init_categories()' && python run.py"]