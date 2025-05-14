from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class GeoLocation(SQLModel, table=True):
    __tablename__ = "geo_locations"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)
    region: Optional[str] = Field(default=None, max_length=100)
    city: Optional[str] = Field(default=None, max_length=100)
    address: Optional[str] = Field(default=None, max_length=180)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    country: Optional[str] = Field(default=None, max_length=100)
    postal_code: Optional[str] = Field(default=None, max_length=100)

class IncIncident(SQLModel, table=True):
    __tablename__ = "inc_incidents"

    id: Optional[int] = Field(default=None, primary_key=True)
    start_time: datetime = Field(nullable=False)
    end_time: datetime = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    type_id: str = Field(max_length=50, nullable=False)
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
    #title: Optional[str] = Field(default=None)
    start_time: str = Field(nullable=False)
    end_time: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    type_id: str = Field(nullable=False)
    suspendido: bool = Field(default=False)
    addresses: List[str]  = Field(sa_column = Column(JSON))  # Esto se guardará como JSON en PostgreSQL
    url: str
