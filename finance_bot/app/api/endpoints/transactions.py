"""
API эндпоинты для работы с транзакциями.

Модуль предоставляет REST API для получения и создания финансовых транзакций.
Использует FastAPI для маршрутизации и SQLAlchemy для работы с БД.

Attributes:
    router (APIRouter): Роутер FastAPI для эндпоинтов транзакций
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...models.transaction import Transaction
from ...schemas.transaction import TransactionCreate, Transaction as TransactionSchema

router = APIRouter()

@router.get("/transactions/", response_model=List[TransactionSchema])
def get_transactions(db: Session = Depends(get_db)):
    """
    Получение списка всех транзакций.

    Args:
        db (Session): Сессия базы данных, внедряется через FastAPI Depends

    Returns:
        List[Transaction]: Список всех транзакций в базе данных

    Example:
        GET /api/v1/transactions/
        Response: [
            {
                "id": 1,
                "amount": 1000.0,
                "description": "Продукты",
                "category_id": 1,
                "user_id": 123456789,
                "created_at": "2024-01-16T12:00:00"
            },
            ...
        ]
    """
    return db.query(Transaction).all()

@router.post("/transactions/", response_model=TransactionSchema)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """
        Создание новой транзакции.

        Args:
            transaction (TransactionCreate): Данные для создания транзакции
            db (Session): Сессия базы данных, внедряется через FastAPI Depends

        Returns:
            Transaction: Созданная транзакция

        Example:
            POST /api/v1/transactions/
            Request body: {
                "amount": 1000.0,
                "description": "Продукты",
                "category_id": 1
            }
            Response: {
                "id": 1,
                "amount": 1000.0,
                "description": "Продукты",
                "category_id": 1,
                "user_id": 123456789,
                "created_at": "2024-01-16T12:00:00"
            }
        """
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction
