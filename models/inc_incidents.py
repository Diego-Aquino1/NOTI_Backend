from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from models.geo_locations import GeoLocation

class IncIncident(SQLModel, table=True):
    __tablename__ = "inc_incidents"

    id: Optional[int] = Field(default=None, primary_key=True)
    start_time: datetime = Field(nullable=False)
    end_time: datetime = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    type_id: str = Field(max_length=100, nullable=False)  # Ajustado a max_length=100
    suspendido: bool = Field(default=False)
    url: str = Field(nullable=False)
    
    addresses: List["IncIncidentAddress"] = Relationship(back_populates="incident")

class IncIncidentAddress(SQLModel, table=True):
    __tablename__ = "inc_incident_addresses"

    id: Optional[int] = Field(default=None, primary_key=True)
    incident_id: int = Field(foreign_key="inc_incidents.id", nullable=False)
    location_id: int = Field(foreign_key="geo_locations.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    incident: IncIncident = Relationship(back_populates="addresses")
    location: GeoLocation = Relationship()