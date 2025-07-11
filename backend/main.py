import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from typing import Annotated, Optional

from fastapi import Depends, FastAPI
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import Session, SQLModel, create_engine
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import inspect

from sms_processing import SmsData, SMSProcessor, get_all_sms

log_file = "unprocessed_sms.log"
# Looger configuration
logging.basicConfig(
    filename=log_file,
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


DATABASE_URL = "sqlite:///./momo_dashboard.db?check_same_thread=False"

engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

@lru_cache()
def get_session():
    return Session(engine)

@asynccontextmanager
async def get_database():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

database = Annotated[Session, Depends(get_session)]


@asynccontextmanager
@lru_cache(maxsize=200)
async def lifespan(app: FastAPI):
    # Create tables at startup
    SQLModel.metadata.create_all(engine)
    
    # Check if tables exist
    with Session(engine) as session:
        inspector = inspect(engine)
        if not inspector.has_table("smsdata"):
            SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="MOMO APP API",
    description="Backend for a MOMO wallet",
    lifespan=lifespan,
    version="0.0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_headers=["Content-Type", "Authorization"],
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
)


@app.get("/", tags=["SMS Processing"])
async def main(db: database):
    """Process SMS data and return summary"""
    processor = SMSProcessor(db=db)
    result = processor.process_and_store_sms()
    return result

@app.get("/sms/all", tags=["SMS Processing"])
async def get_all_sms_data(db: database):
    """Get all SMS data from the database"""
    try:
        processor = SMSProcessor(db=db)
        data = processor.data()
        return data
    except Exception as e:
        logging.error(f"Error fetching all SMS data: {e}")
        return {"error": str(e)}


@app.get("/sms", tags=["SMS Processing"])
async def get_sms(
    db: database,
    search: Optional[str] = None,
    type: Optional[str] = None,
    date: Optional[datetime] = None,
    amount: Optional[str] = None,
):
    try:
        if amount:
            amount = float(amount)
        get_all = get_all_sms(db, search, type, date, amount)
        return get_all
    except ValueError:
        return {"error": "Invalid amount format. Please provide a valid number."}
