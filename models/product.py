from typing import Optional
from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None)
    original_price: Optional[float] = Field(default=None)
    liquidation_price: Optional[float] = Field(default=None)
    front_view_path: Optional[str] = Field(default=None)
    back_view_path: Optional[str] = Field(default=None)
    register_date: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default='A')
    category_fk: Optional[int] = Field(default=None, foreign_key="category.id")