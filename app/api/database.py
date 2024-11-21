import tomli
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

def load_config():
    config_path = ".streamlit/secrets.toml"
    try:
        with open(config_path, "rb") as f:
            return tomli.load(f)
    except FileNotFoundError:
        return {
            "connections": {
                "database": os.getenv("DATABASE_URL", "sqlite:///./transactions.db")
            }
        }

config = load_config()
DATABASE_URL = config["connections"]["database"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
