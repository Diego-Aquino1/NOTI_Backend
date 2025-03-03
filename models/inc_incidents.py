from sqlmodel import SQLModel, Field
from typing import Optional
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