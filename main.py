from fastapi import FastAPI
from pydantic import BaseModel

import categorizer
import database

app = FastAPI(title="Expense Tracker AI")
database.init_db()


class ExpenseIn(BaseModel):
    description: str
    amount: float


@app.get("/")
def home():
    return {"message": "Hello, expense tracker!"}


@app.post("/expenses")
def add_expense(expense: ExpenseIn):
    category = categorizer.categorize(expense.description)
    return database.add_expense(expense.description, expense.amount, category)


@app.get("/expenses")
def list_expenses():
    return database.list_expenses()