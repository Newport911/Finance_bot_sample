"""
Модуль инициализации базы данных для Finance Tracker Bot.

Создает начальные категории доходов и расходов в базе данных.
Предотвращает дублирование категорий через проверку их существования.

Functions:
    init_categories(): Инициализация базовых категорий
"""


from .database import SessionLocal
from .models.transaction import Category
from sqlalchemy.exc import IntegrityError

def init_categories():
    """
        Инициализация базовых категорий доходов и расходов.

        Создает предопределенный набор категорий в базе данных.
        Проверяет существование категорий перед добавлением для
        предотвращения дублирования.

        Categories:
            Расходы:
                - Продукты
                - Транспорт
                - Развлечения
                - Коммунальные услуги
                - Здоровье

            Доходы:
                - Зарплата
                - Фриланс
                - Подарки
                - Инвестиции

        Raises:
            IntegrityError: При попытке добавить дублирующуюся категорию
        """

    db = SessionLocal()

    expense_categories = [
        {"name": "Продукты", "type": "expense"},
        {"name": "Транспорт", "type": "expense"},
        {"name": "Развлечения", "type": "expense"},
        {"name": "Коммунальные услуги", "type": "expense"},
        {"name": "Здоровье", "type": "expense"}
    ]

    income_categories = [
        {"name": "Зарплата", "type": "income"},
        {"name": "Фриланс", "type": "income"},
        {"name": "Подарки", "type": "income"},
        {"name": "Инвестиции", "type": "income"}
    ]

    for category in expense_categories + income_categories:
        # Проверяем существование категории
        existing_category = db.query(Category).filter(Category.name == category["name"]).first()
        if not existing_category:
            try:
                db_category = Category(**category)
                db.add(db_category)
                db.commit()
            except IntegrityError:
                db.rollback()
                print(f"Категория {category['name']} уже существует")
                continue
            print(f"Добавлена категория: {category['name']}")
        else:
            print(f"Категория {category['name']} уже существует")

    db.close()

if __name__ == "__main__":
    init_categories()