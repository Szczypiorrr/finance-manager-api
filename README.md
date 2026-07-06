# Finance Manager API

A backend Finance Management System built with **FastAPI**, **SQLAlchemy ORM**, and **SQLite**.

The goal of this project is to demonstrate real-world backend development skills including:
- REST API design
- Database modeling and relationships
- CRUD operations
- Business logic layer (services)
- Advanced statistics & analytics queries
- Testing with pytest
- Layered architecture (routers / services / models)

---

## ⚙️ How to run

### 1. Clone repository
```bash
git clone https://github.com/Szczypiorrr/finance-manager-api.git
cd finance-manager-api
```
### 2. Create virtual environment
```bash
python -m venv venv
```
### 3. Activate virtual environment
Windows:
```bash
venv\Scripts\activate
```

Mac / Linux:
```bash
source venv/bin/activate
```
### 4. Install dependencies
```bash
pip install -r requirements.txt
```
### 6. Run application
```bash
uvicorn app.main:app --reload
```

## 📌 API Documentation
After running the project:
- Swagger UI:
```bash
http://127.0.0.1:8000/docs
```

- ReDoc:
```bash
http://127.0.0.1:8000/redoc
```

## 📌 Features

### 👤 Users
- Create, read, update and delete users
- Retrieve users by ID and username

### 🏷️ Categories
- Full CRUD operations
- Validation and duplicate prevention

### 💸 Expenses
- Create, read, update, delete expenses
- Filtering by category
- Relational linking (user, account, category)

### 📊 Statistics & Analytics
- Monthly income vs expenses summary
- Category-based spending breakdown
- Account and user balance calculations
- Top expenses ranking
- Monthly spending trends
- Aggregation queries using SQLAlchemy ORM

## 🧱 Project structure
```text
finance-manager-api/
│
├── app/
│   ├── main.py
│
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── exceptions/
│   │   ├── account_exceptions.py
│   │   ├── budget_exceptions.py
│   │   ├── category_exceptions.py
│   │   ├── common_exceptions.py
│   │   ├── expense_exceptions.py
│   │   ├── goal_exceptions.py
│   │   ├── income_exceptions.py
│   │   └── user_exceptions.py
│   │
│   ├── helpers/
│   │   ├── datetime.py
│   │   ├── rounding.py
│   │   └── validators.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── account.py
│   │   ├── base_model.py
│   │   ├── budget.py
│   │   ├── category.py
│   │   ├── expense.py
│   │   ├── goal.py
│   │   ├── income.py
│   │   └── user.py
│   │
│   ├── routers/
│   │   ├── account.py
│   │   ├── budget.py
│   │   ├── category.py
│   │   ├── expense.py
│   │   ├── goal.py
│   │   ├── income.py
│   │   ├── stats.py
│   │   └── user.py
│   │
│   ├── schemas/
│   │   ├── account.py
│   │   ├── budget.py
│   │   ├── category.py
│   │   ├── expense.py
│   │   ├── goal.py
│   │   ├── income.py
│   │   ├── stats.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── account.py
│   │   ├── budget.py
│   │   ├── category.py
│   │   ├── expense.py
│   │   ├── goal.py
│   │   ├── income.py
│   │   ├── stats.py
│   │   └── user.py
│   │
│   └── tests/
│       ├── test_user_service.py
│       ├── test_stats_service.py
│       ├── test_expense_service.py
│       └── test_category_service.py
│
├── README.md
│
└── requirements.txt
```

## 🧪 Testing

This project includes unit tests built with **pytest** covering all core service layers.

### Run tests:
```bash
python -m pytest -vv
```

### Covered areas:
- User service tests
- Category service tests
- Expense service tests
- Statistics service tests

### Tests use:
- SQLite in-memory database
- Fixtures for isolation
- Service-layer testing (no API dependency)

## 🚀 Technologies

- Python 3.12
- FastAPI
- SQLAlchemy ORM
- Pydantic
- SQLite (development database)
- Pytest
- Uvicorn
- REST API architecture
- MVC-inspired layered architecture (routers / services / models)

## 🧠 What I learned?

- Building REST APIs with FastAPI
- Structuring backend applications (services layer architecture)
- Designing relational database schemas
- SQLAlchemy ORM (queries, joins, aggregation)
- Handling business logic outside of routes
- Writing unit tests with pytest
- Testing database-driven applications
- Working with financial/statistical data
- Clean code practices in backend systems

## 🔧 Possible improvements

- Add JWT authentication (login/register system)
- Add user roles (admin / user)
- Add pagination for large datasets
- Add caching layer (Redis)
- Add Docker support
- Add frontend dashboard (React or Vue)

## 📊 Example use cases

- Personal finance tracking backend
- Expense analytics API
- Portfolio-ready backend project
- Base for full-stack finance application

# 👤 Author

Created by Szczypiorrrr  
🔗 GitHub: https://github.com/Szczypiorrr