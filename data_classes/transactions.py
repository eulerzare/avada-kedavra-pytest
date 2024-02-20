from typing import List

from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: int
    message: str


class Transaction(BaseModel):
    number: int
    amount: float
    freezeAmount: float
    currency: str
    entity: str
    subsidiaryAccount: str
    entityType: int
    minAmount: float
    description: str


class TransactionBulk(BaseModel):
    uniqueId: str
    timestamp: int
    objectId: int
    eventType: str
    transactions: List[Transaction]
