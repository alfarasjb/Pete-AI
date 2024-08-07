import logging

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from src.database.database import SessionLocal


db_router = APIRouter()
logger = logging.getLogger(__name__)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@db_router.get("/")
def db_default():
    return Response("Success", status_code=200)
