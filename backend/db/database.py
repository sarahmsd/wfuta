from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://sd:password@localhost:5432/wfuta"
engine = create_engine(DATABASE_URL)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)



Base = declarative_base()