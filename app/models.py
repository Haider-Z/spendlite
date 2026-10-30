
from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)