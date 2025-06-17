from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.utils import get_current_user
from app.orders.models import Order
from app.orders.schemas import OrderSummaryOut, OrderDetailOut
from app.core.logger import logger

router = APIRouter(prefix="/orders", tags=["Orders"])
#To Get Order History in summary format
@router.get("/", response_model=list[OrderSummaryOut])
def get_order_history(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="Only users can view order history")
    logger.info(f"User {current_user['id']} is retrieving order history.")
    
#Queries all orders belonging to the current user, ordered by most recent.
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user["id"])
        .order_by(Order.created_at.desc())
        .all()
    )
    logger.debug(f"Found {len(orders)} orders for user {current_user['id']}.")

    return orders

#Returns detailed information about a specific order.
@router.get("/{order_id}", response_model=OrderDetailOut)
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="Only users can view order details")
    logger.info(f"User {current_user['id']} is trying to access order {order_id}.")

    order = (
        db.query(Order)
        .filter(Order.id == order_id, Order.user_id == current_user["id"])
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
