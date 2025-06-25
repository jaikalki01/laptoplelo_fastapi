from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL connection URL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:office1234@localhost/laptoplelo_schemas"

# Create the engine without the check_same_thread argument
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


class Session:
    def close(self):
        pass


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
