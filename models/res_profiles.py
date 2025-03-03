from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ResProfile(SQLModel, table=True):
    __tablename__ = "res_profiles"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(unique=True, foreign_key="res_users.id")
    name: str = Field(max_length=100, nullable=False)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None, max_length=100)
    country: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)