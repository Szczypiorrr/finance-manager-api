from fastapi import FastAPI

from core.database import init_db

from routers.user import router as user_router
from routers.account import router as account_router
from routers.category import router as category_router
from routers.expense import router as expense_router
from routers.income import router as income_router
from routers.budget import router as budget_router
from routers.goal import router as goal_router
from routers.stats import router as stats_router

app = FastAPI(
    title="Personal Finance API",
    description="A RESTful API for managing personal finances, including users, accounts, categories, expenses, incomes, budgets, goals, and statistics.",
    version="1.0.0",
)

app.include_router(user_router)
app.include_router(account_router)
app.include_router(category_router)
app.include_router(expense_router)
app.include_router(income_router)
app.include_router(budget_router)
app.include_router(goal_router)
app.include_router(stats_router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Personal Finance API is running"}