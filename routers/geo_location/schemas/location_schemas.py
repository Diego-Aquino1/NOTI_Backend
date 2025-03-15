from typing import Optional
from pydantic import BaseModel


class LocationRequest(BaseModel):
    address: str