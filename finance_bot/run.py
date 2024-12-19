"""
Finance Tracker Bot - Telegram бот для учета личных финансов.

Основной модуль, реализующий интеграцию FastAPI и Telegram бота через Pyrogram.
Обеспечивает асинхронную работу API и бота в разных потоках.

Attributes:
    app (FastAPI): Экземпляр FastAPI приложения
    user_states (Dict[int, Dict[str, Any]]): Хранилище состояний пользователей
    bot (Bot): Экземпляр бота
"""


import asyncio
from fastapi import FastAPI
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from finance_bot.app.config import settings
import uvicorn
from finance_bot.app.api.endpoints.transactions import router as transactions_router
import threading
from finance_bot.app.database import SessionLocal
from finance_bot.app.models.transaction import Category, Transaction

app = FastAPI()
app.include_router(transactions_router, prefix="/api/v1")

# Словарь для хранения состояний пользователей
user_states = {}


class Bot(Client):
    """
    Расширение базового класса Pyrogram Client.

    Добавляет функционал для управления состоянием бота и
    асинхронной обработки сообщений.

    Methods:
        start(): Запускает бота
        idle(): Поддерживает бота в активном состоянии
    """

    def __init__(self):
        """
        Инициализирует бота с настройками из конфигурации.

        Использует API_ID, API_HASH и BOT_TOKEN из settings.
        """
        super().__init__(
            "finance_bot",
            api_id=settings.API_ID,
            api_hash=settings.API_HASH,
            bot_token=settings.BOT_TOKEN
        )

    async def start(self):
        await super().start()
        print("Bot started!")

    async def idle(self):
        while True:
            try:
                while True:
                    await asyncio.sleep(1)
            except asyncio.CancelledError:
                print("Idle task cancelled.")


bot = Bot()


def get_main_keyboard():
    """
    Создает основную клавиатуру с кнопками команд.

    Returns:
        ReplyKeyboardMarkup: Клавиатура с кнопками статистики, категорий и добавления транзакций
    """
    return ReplyKeyboardMarkup([
        [KeyboardButton("📊 Статистика"), KeyboardButton("📋 Категории")],
        [KeyboardButton("💰 Добавить доход"), KeyboardButton("💸 Добавить расход")]
    ], resize_keyboard=True)


@bot.on_message(filters.command("start"))
async def start_command(client, message):
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение и показывает основную клавиатуру.
    """
    await message.reply_text(
        "Привет! Я бот для учета финансов. Используй кнопки меню или /help для просмотра команд.",
        reply_markup=get_main_keyboard()
    )


@bot.on_message(filters.command("help"))
async def help_command(client, message):
    """
    Обработчик команды /help.
    Показывает список доступных команд.
    """
    help_text = """
    Доступные команды:
    /add_expense [сумма] [категория] [описание] - Добавить расход
    /add_income [сумма] [категория] [описание] - Добавить доход
    /statistics - Показать статистику
    /categories - Показать категории
    """
    help_text = """
    Доступные команды:
    /add_expense [сумма] [категория] [описание] - Добавить расход
    /add_income [сумма] [категория] [описание] - Добавить доход
    /statistics - Показать статистику
    /categories - Показать категории
    """
    await message.reply_text(help_text, reply_markup=get_main_keyboard())


@bot.on_message(filters.regex("^📊 Статистика$") | filters.command("statistics"))
async def statistics(client, message):
    """
    Показывает финансовую статистику пользователя.

    Вычисляет и отображает:
    - Общую сумму доходов
    - Общую сумму расходов
    - Текущий баланс
    """
    db = SessionLocal()
    try:
        expenses = db.query(Transaction).join(Category).filter(
            Category.type == "expense",
            Transaction.user_id == message.from_user.id
        ).all()

        incomes = db.query(Transaction).join(Category).filter(
            Category.type == "income",
            Transaction.user_id == message.from_user.id
        ).all()

        total_expense = sum(t.amount for t in expenses)
        total_income = sum(t.amount for t in incomes)
        balance = total_income - total_expense

        stats_text = f"""
Статистика:
Всего доходов: {total_income} руб.
Всего расходов: {total_expense} руб.
Баланс: {balance} руб.
"""
        await message.reply_text(stats_text, reply_markup=get_main_keyboard())
    except Exception as e:
        await message.reply_text(f"Ошибка при получении статистики: {str(e)}")
    finally:
        db.close()


@bot.on_message(filters.regex("^📋 Категории$") | filters.command("categories"))
async def categories_command(client, message):
    db = SessionLocal()
    categories = db.query(Category).all()
    categories_text = "Доступные категории:\n\nРасходы:\n"
    categories_text += "\n".join([f"- {cat.name}" for cat in categories if cat.type == "expense"])
    categories_text += "\n\nДоходы:\n"
    categories_text += "\n".join([f"- {cat.name}" for cat in categories if cat.type == "income"])
    await message.reply_text(categories_text, reply_markup=get_main_keyboard())
    db.close()


def get_categories_keyboard(type_="expense"):
    """
        Создает inline-клавиатуру с категориями указанного типа.

        Args:
            type_ (str): Тип категорий ("expense" или "income")

        Returns:
            InlineKeyboardMarkup: Клавиатура с кнопками категорий
        """
    db = SessionLocal()
    categories = db.query(Category).filter(Category.type == type_).all()
    db.close()

    buttons = []
    for cat in categories:
        buttons.append([InlineKeyboardButton(cat.name, callback_data=f"cat_{type_}_{cat.id}")])
    return InlineKeyboardMarkup(buttons)


@bot.on_message(filters.regex("^💸 Добавить расход$"))
async def add_expense_start(client, message):
    """
    Начинает процесс добавления расхода.
    Показывает клавиатуру с категориями расходов.
    """
    await message.reply_text(
        "Выберите категорию расхода:",
        reply_markup=get_categories_keyboard("expense")
    )


@bot.on_message(filters.regex("^💰 Добавить доход$"))
async def add_income_start(client, message):
    """
    Начинает процесс добавления дохода.
    Показывает клавиатуру с категориями доходов.
    """
    await message.reply_text(
        "Выберите категорию дохода:",
        reply_markup=get_categories_keyboard("income")
    )


@bot.on_callback_query()
async def handle_callback(client, callback_query):
    """
    Обработчик нажатий на inline-кнопки категорий.

    Сохраняет выбранную категорию и запрашивает ввод суммы и описания.
    """
    data = callback_query.data
    if data.startswith("cat_"):
        _, type_, category_id = data.split("_")
        user_states[callback_query.from_user.id] = {
            'category_id': int(category_id),
            'type': type_
        }
        await callback_query.message.reply_text(
            f"Введите сумму и описание через пробел\nНапример: 1000 Описание",
            reply_markup=get_main_keyboard()
        )


@bot.on_message(filters.text & filters.regex("^(?!📊|📋|💰|💸|/).+"))
async def handle_transaction_input(client, message):
    """
    Обработчик ввода данных транзакции.

    Создает новую транзакцию на основе:
    - Выбранной ранее категории
    - Введенной суммы
    - Введенного описания
    """
    user_id = message.from_user.id

    if user_id not in user_states:
        return

    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 1:
            await message.reply_text("Пожалуйста, введите сумму и описание")
            return

        amount = float(parts[0])
        description = parts[1] if len(parts) > 1 else ""

        state = user_states[user_id]
        db = SessionLocal()

        transaction = Transaction(
            amount=amount,
            category_id=state['category_id'],
            description=description,
            user_id=user_id
        )

        db.add(transaction)
        db.commit()

        category = db.query(Category).filter(Category.id == state['category_id']).first()

        transaction_type = "Доход" if state['type'] == "income" else "Расход"
        await message.reply_text(
            f"{transaction_type} добавлен:\n"
            f"Сумма: {amount} руб.\n"
            f"Категория: {category.name}\n"
            f"Описание: {description}",
            reply_markup=get_main_keyboard()
        )

        del user_states[user_id]

    except ValueError:
        await message.reply_text("Неверный формат суммы. Пожалуйста, введите число.")
    except Exception as e:
        await message.reply_text(f"Произошла ошибка: {str(e)}")
    finally:
        db.close()


def run_api():
    uvicorn.run(app, host="0.0.0.0", port=8000)


async def main():
    """
    Основная функция приложения.

    Запускает:
    - FastAPI сервер в отдельном потоке
    - Telegram бота в асинхронном режиме
    """
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    try:
        await bot.start()
        print("Бот активен...")
        await bot.idle()
    except KeyboardInterrupt:
        print("Завершение работы...")
    finally:
        await bot.stop()


if __name__ == "__main__":
    try:
        bot.run(main())
    except KeyboardInterrupt:
        print("Завершение работы...")
    finally:
        print("Бот остановлен.")