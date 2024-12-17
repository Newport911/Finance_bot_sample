from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_categories_keyboard():
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Продукты", callback_data="cat_products")],
        [InlineKeyboardButton("Транспорт", callback_data="cat_transport")],
        [InlineKeyboardButton("Развлечения", callback_data="cat_entertainment")],
    ])
    return keyboard
