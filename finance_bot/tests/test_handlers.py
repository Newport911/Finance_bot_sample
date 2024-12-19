"""
Этот модуль содержит тесты для проверки функциональности бота для учета финансов.

Тесты используют библиотеку Pytest и Pyrogram для имитации поведения клиента Telegram и сообщений.
Для асинхронного тестирования используется pytest-asyncio.

Тесты:
- test_start_command: Проверяет, что команда /start отправляет правильное приветственное сообщение.
- test_bot_initialization: Проверяет корректность инициализации бота с использованием настроек из конфигурации.
- test_help_command: Проверяет, что команда /help отправляет список доступных команд.
- test_add_expense_start: Проверяет, что функция добавления расхода отправляет сообщение с выбором категории расхода.
- test_database_connection: Проверяет, что соединение с базой данных устанавливается корректно.

Фикстуры:
- mock_client: Создает имитацию клиента Pyrogram.
- mock_message: Создает имитацию сообщения Pyrogram с возможностью асинхронного ответа.

Используемые модули:
- finance_bot.app.bot.handlers: Содержит обработчики команд бота.
- finance_bot.run: Содержит класс Bot и вспомогательные функции.
- finance_bot.app.config: Содержит настройки приложения.
- finance_bot.app.database: Содержит функции для работы с базой данных.
"""

import pytest
from pyrogram import Client, types
from unittest.mock import AsyncMock, MagicMock
from finance_bot.app.bot.handlers import start_command

from finance_bot.run import Bot, help_command, add_expense_start, get_categories_keyboard
from finance_bot.app.config import settings

from finance_bot.app.database import get_db
from sqlalchemy.orm import Session


@pytest.mark.asyncio(loop_scope="function")
async def test_start_command():
    """
    Тестирование функции start_command.

    Проверяет, что функция start_command отправляет приветственное сообщение.
    """
    client = MagicMock(spec=Client)
    message = MagicMock(spec=types.Message)
    message.reply_text = AsyncMock()

    await start_command(client, message)

    message.reply_text.assert_called_once_with(
        "Привет! Я бот для учета финансов. Используй /help для просмотра команд."
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_bot_initialization():
    """
    Тестирование инициализации бота.

    Проверяет, что при создании экземпляра класса Bot
    он корректно инициализируется с настройками из settings.
    """
    bot = Bot()
    assert bot.api_id == settings.API_ID
    assert bot.api_hash == settings.API_HASH
    assert bot.bot_token == settings.BOT_TOKEN


@pytest.mark.asyncio(loop_scope="function")
async def test_help_command():
    """
    Тестирование функции help_command.

    Проверяет, что функция help_command отправляет сообщение с
    доступными командами.
    """
    # Создаем имитацию клиента и сообщения
    client = MagicMock(spec=Client)
    message = MagicMock(spec=types.Message)
    message.reply_text = AsyncMock()

    # Вызываем тестируемую функцию
    await help_command(client, message)

    # Проверяем, что метод reply_text был вызван ровно один раз
    message.reply_text.assert_called_once()


@pytest.mark.asyncio(loop_scope="function")
async def test_add_expense_start():
    """
    Тестирование функции add_expense_start.

    Проверяет, что функция add_expense_start отправляет сообщение с выбором
    категории расхода.
    """
    client = MagicMock(spec=Client)
    message = MagicMock(spec=types.Message)
    message.reply_text = AsyncMock()

    await add_expense_start(client, message)

    message.reply_text.assert_called_once_with(
        "Выберите категорию расхода:",
        reply_markup=get_categories_keyboard("expense")
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_database_connection():
    """
    Тестирование подключения к базе данных.

    Создается сессия к БД, проверяется, что она является экземпляром класса Session,
    а затем сессия закрывается.
    """
    db = next(get_db())
    assert isinstance(db, Session)
    db.close()