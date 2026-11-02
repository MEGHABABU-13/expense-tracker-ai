from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Expense Tracker AI")


class ExpenseIn(BaseModel):
    description: str
    amount: float


expenses = []


@app.get("/")
def home():
    return {"message": "Hello, expense tracker!"}


@app.post("/expenses")
def add_expense(expense: ExpenseIn):
    new_expense = {
        "id": len(expenses) + 1,
        "description": expense.description,
        "amount": expense.amount,
    }
    expenses.append(new_expense)
    return new_expense


@app.get("/expenses")
def list_expenses():
    return expenses