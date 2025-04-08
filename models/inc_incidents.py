from sqlmodel import SQLModel, Field, Column
from typing import Optional, List
from sqlalchemy import JSON
from datetime import datetime

class IncIncident(SQLModel, table=True):
    __tablename__ = "inc_incidents"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    location_id: int = Field(foreign_key="geo_locations.id")
    start_time: datetime = Field(nullable=False)
    end_time: datetime = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    type_id: int = Field(foreign_key="inc_incident_types.id")
    created_at: datetime = Field(default_factory=datetime.now)

class CorteEnergia(SQLModel, table=True):
    __tablename__ = "cortes"

    id: Optional[int] = Field(default=None, primary_key=True)
    start_time: str = Field(nullable=False)
    end_time: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    type_id: str = Field(nullable=False)
    addresses: List[str]  = Field(sa_column = Column(JSON))  # Esto se guardará como JSON en PostgreSQL
    url: str