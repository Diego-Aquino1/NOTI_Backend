from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class IncIncidentType(SQLModel, table=True):
    __tablename__ = "inc_incident_types"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, nullable=False)