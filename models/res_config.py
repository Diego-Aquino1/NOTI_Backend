from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ResConfig(SQLModel, table=True):
    __tablename__ = "res_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="res_users.id")
    created_at: datetime = Field(default_factory=datetime.now)
    priority: Optional[int] = Field(default = 5)
    interval: int = Field(default = 7)