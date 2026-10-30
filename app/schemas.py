from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    category: str = Field(min_length=1, max_length=50)
    date: date


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    date: date

    model_config = ConfigDict(from_attributes=True)


class ExpenseSummary(BaseModel):
    total_expenses: float
    transaction_count: int
    average_expense: float