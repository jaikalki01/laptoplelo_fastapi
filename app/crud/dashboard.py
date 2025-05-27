from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.user import User
from app.models.product import Product

def get_dashboard_stats(db: Session):
    total_users = db.query(func.count(User.id)).scalar()
    products = db.query(func.count(Product.id)).scalar()

    # Placeholder logic
    active_rentals = db.query(func.count(Product.id)).filter(Product.type == "rent").scalar()  # Replace when you add rental table
    #sales_this_month = "₹0"  # Replace when you add invoice/sales table

    return {
        "total_users": total_users,
        "products": products,
        "active_rentals": active_rentals,
        #"sales_this_month": sales_this_month
    }
