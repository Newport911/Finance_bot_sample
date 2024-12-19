from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransactionBase(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: int


class TransactionCreate(TransactionBase):
    pass


class Transaction(TransactionBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True