from pydantic import BaseModel

class CartCreate(BaseModel):
    product_id: int
    quantity: int
    rental_duration: int
    type: str  # "rental" or "sale"
    user_id: int | None = None

class CartRemoveSchema(BaseModel):
    product_id: int
    type: str