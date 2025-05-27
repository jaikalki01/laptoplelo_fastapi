from pydantic import BaseModel

class WishlistBase(BaseModel):
    user_id: int
    product_id: int

    class Config:
        orm_mode = True
