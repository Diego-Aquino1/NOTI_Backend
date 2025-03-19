from sqlmodel import SQLModel, Field
from typing import Optional
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
    created_at: datetime = Field(default_factory=datetime.now)
    country: Optional[str] = Field(default = None, max_length = 100)
    postal_code: Optional[str] = Field(default = None, max_length = 100)

