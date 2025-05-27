from pydantic import BaseModel
from typing import Optional, Dict

class Specs(BaseModel):
    processor: Optional[str] = None
    memory: Optional[str] = None
    storage: Optional[str] = None
    display: Optional[str] = None
    graphics: Optional[str] = None

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    rental_price: float
    type: str
    image: str
    brand: str
    specs: Specs
    available: bool = True
    featured: bool = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
     name: Optional[str] = None
     description: Optional[str] = None
     price: Optional[float] = None
     rental_price: Optional[float] = None
     type: Optional[str] = None
     brand: Optional[str] = None
     image: Optional[str] = None
     available: Optional[bool] = None
     featured: Optional[bool] = None
     specs: Optional[Specs] = None  # ← FIXED


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True
