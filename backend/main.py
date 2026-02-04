from fastapi import FastAPI, Header, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
import uuid

from sqlalchemy import (
    create_engine,
    Column,
    String,
    Date,
    DateTime,
    Numeric,
    text,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session


# ------------------ DB SETUP ------------------

DATABASE_URL = "sqlite:///./expenses.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# ------------------ MODEL ------------------

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True)

    amount = Column(Numeric(10, 2))
    category = Column(String)
    description = Column(String)

    date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


# ------------------ SCHEMAS ------------------

class ExpenseCreate(BaseModel):
    amount: Decimal = Field(..., gt=0)
    category: str
    description: str
    date: date


class ExpenseOut(BaseModel):
    id: str
    amount: Decimal
    category: str
    description: str
    date: date
    created_at: datetime

    class Config:
        from_attributes = True


# ------------------ APP ------------------

app = FastAPI(title="Expense Tracker API")


# ------------------ DEPENDENCY ------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------ ROUTES ------------------

@app.get("/")
def health():
    return {"status": "ok"}


# CREATE EXPENSE (IDEMPOTENT)
@app.post("/expenses", response_model=ExpenseOut)
def create_expense(
    expense: ExpenseCreate,
    x_request_id: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):

    if not x_request_id:
        raise HTTPException(
            status_code=400,
            detail="X-Request-ID header required",
        )

    # Check for duplicate request
    existing = (
        db.query(Expense)
        .filter(Expense.request_id == x_request_id)
        .first()
    )

    if existing:
        return existing

    new_expense = Expense(
        id=str(uuid.uuid4()),
        request_id=x_request_id,
        amount=expense.amount,
        category=expense.category,
        description=expense.description,
        date=expense.date,
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


# GET EXPENSES
@app.get("/expenses", response_model=List[ExpenseOut])
def get_expenses(
    category: Optional[str] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db),
):

    query = db.query(Expense)

    if category:
        query = query.filter(Expense.category == category)

    if sort == "date_desc":
        query = query.order_by(Expense.date.desc())

    return query.all()
