"""
Модели SQLAlchemy для работы с категориями и транзакциями.

Модуль определяет структуру таблиц базы данных для хранения
финансовых категорий и транзакций с использованием ORM SQLAlchemy.

Models:
    Category: Модель категории расходов/доходов
    Transaction: Модель финансовой транзакции
"""


from sqlalchemy import Column, String, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class Category(BaseModel):
    """
    Модель категории финансовой операции.

    Наследует базовые поля (id, created_at, updated_at) от BaseModel.

    Attributes:
        name (str): Название категории (уникальное, индексированное)
        type (str): Тип категории ("income" или "expense")
        transactions (List[Transaction]): Связанные транзакции

    Table Args:
        __tablename__ (str): Имя таблицы в БД
    """

    __tablename__ = "categories"

    name = Column(String, unique=True, index=True)
    type = Column(String)

    transactions = relationship("Transaction", back_populates="category")

class Transaction(BaseModel):
    """
        Модель финансовой транзакции.

        Наследует базовые поля (id, created_at, updated_at) от BaseModel.

        Attributes:
            amount (float): Сумма транзакции
            description (str): Описание транзакции
            category_id (int): ID связанной категории (внешний ключ)
            user_id (int): ID пользователя Telegram (индексированное)
            category (Category): Связанная категория

        Table Args:
            __tablename__ (str): Имя таблицы в БД

        Relationships:
            category: Связь с моделью Category (многие к одному)
        """

    __tablename__ = "transactions"

    amount = Column(Float)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, index=True)

    category = relationship("Category", back_populates="transactions")