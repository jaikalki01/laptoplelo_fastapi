from typing import List, Optional
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    rental_price: float
    type: str
    brand: str
    image: Optional[str] = None
    images: List[str] = []
    specs: dict
    available: bool = True
    featured: bool = False

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
