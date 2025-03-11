from typing import Optional
from pydantic import BaseModel


class RegisterRequest(BaseModel):
    email: str
    pwd: str
    name: str
    phone: Optional[str]
    address: Optional[str]
    city: Optional[str]
    country: Optional[str]

class LoginRequest(BaseModel):
    email: str
    pwd: str