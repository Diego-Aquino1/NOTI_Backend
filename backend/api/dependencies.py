from fastapi import Depends
from sqlmodel import Session
from shared.database.connection import get_session

def get_db():
    """Dependency to get database session"""
    return get_session()
