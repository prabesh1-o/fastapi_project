from sqlalchemy import create_engine # create_engine -> it conncets python to database
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL = "sqlite:///./task.db"
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base() 

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
