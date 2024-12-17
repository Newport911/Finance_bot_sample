from pyrogram import Client, filters
from ..database import SessionLocal
from ..models.transaction import Transaction, Category

async def start_command(client, message):
    await message.reply_text("Привет! Я бот для учета финансов. Используй /help для просмотра команд.")

async def help_command(client, message):
    help_text = """
    Доступные команды:
    /add_expense [сумма] [категория] [описание] - Добавить расход
    /add_income [сумма] [категория] [описание] - Добавить доход
    /statistics - Показать статистику
    /categories - Показать категории
    """
    await message.reply_text(help_text)

async def categories_command(client, message):
    db = SessionLocal()
    categories = db.query(Category).all()
    categories_text = "Доступные категории:\n\nРасходы:\n"
    categories_text += "\n".join([f"- {cat.name}" for cat in categories if cat.type == "expense"])
    categories_text += "\n\nДоходы:\n"
    categories_text += "\n".join([f"- {cat.name}" for cat in categories if cat.type == "income"])
    await message.reply_text(categories_text)
    db.close()