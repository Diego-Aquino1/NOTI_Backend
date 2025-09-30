from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ResUser(SQLModel, table=True):
    __tablename__ = "res_users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=100, unique=True, nullable=False)
    pwd_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.now)