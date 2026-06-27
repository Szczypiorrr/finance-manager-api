from fastapi import FastAPI
from routers.user import router as user_router
from core.database import init_db

app = FastAPI()

app.include_router(user_router)

@app.on_event("startup")
def startup():
    init_db()