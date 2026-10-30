from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional

from app.database import get_db
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseResponse, ExpenseSummary

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    new_expense = Expense(**expense.model_dump())

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Expense)

    if category:
        query = query.filter(Expense.category == category)

    return query.order_by(Expense.date.desc()).all()


@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id
    ).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted successfully"}


@router.get("/summary", response_model=ExpenseSummary)
def get_summary(db: Session = Depends(get_db)):
    result = db.query(
        func.coalesce(func.sum(Expense.amount), 0),
        func.count(Expense.id),
        func.coalesce(func.avg(Expense.amount), 0)
    ).first()

    return {
        "total_expenses": result[0],
        "transaction_count": result[1],
        "average_expense": result[2]
    }
