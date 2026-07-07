from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import get_db_url

db_url = get_db_url()

engine = create_engine(db_url)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    """Yields database session and ensures proper closing after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes database tables based on declared SQLAlchemy models."""
    import app.models
    Base.metadata.create_all(bind=engine)