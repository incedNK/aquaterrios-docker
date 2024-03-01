from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from utils.config import settings


DATABASE_URL = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_server}:{settings.postgres_port}/{settings.postgres_db_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

    
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()