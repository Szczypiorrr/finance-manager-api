from fastapi import FastAPI

from app.core.database import init_db

from app.routers.user import router as user_router
from app.routers.account import router as account_router
from app.routers.category import router as category_router
from app.routers.expense import router as expense_router
from app.routers.income import router as income_router
from app.routers.budget import router as budget_router
from app.routers.goal import router as goal_router
from app.routers.stats import router as stats_router

"""Creates the main FastAPI application."""
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
    """Initializes database on application startup."""

    init_db()

@app.get("/")
def root():
    """Returns API status message."""

    return {"message": "Personal Finance API is running"}