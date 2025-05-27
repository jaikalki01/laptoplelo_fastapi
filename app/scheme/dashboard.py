from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_users: int
    products: int
    active_rentals: int
    #sales_this_month: str