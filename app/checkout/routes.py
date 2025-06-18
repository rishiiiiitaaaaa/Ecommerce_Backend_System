from fastapi import APIRouter, Depends, HTTPException,Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.utils import get_current_user
from app.auth import models as auth_models
from app.cart import models as cart_models
from app.orders import models as order_models
from app.products import models as product_models
from app.orders.schemas import CheckoutRequest
from app.core.logger import logger 

router = APIRouter(prefix="/checkout", tags=["Checkout"])

@router.post("/", status_code=201)
def dummy_checkout(
    request_data: CheckoutRequest,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    #checking the role
    if current_user["role"] != "user":
        raise HTTPException(status_code=403, detail="Only users can perform checkout")
    logger.info(f"Checkout initiated by user ID {current_user['id']}")

    #Fetching the User
    user = db.query(auth_models.User).filter(auth_models.User.id == current_user["id"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    #Fetching Cart Items
    # Fetching Cart Items (only with quantity > 0)
    cart_items = db.query(cart_models.CartItem).filter(
        cart_models.CartItem.user_id == user.id,
        cart_models.CartItem.quantity > 0
        ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty or has invalid items")

    # Log problematic items for debugging
    for item in cart_items:
        if item.quantity <= 0:
            logger.warning(f"Cart contains item with zero or negative quantity: product_id={item.product_id}")

    # Calculate Total Price
    total_price = sum(item.quantity * item.product.price for item in cart_items)

    if total_price <= 0:
        raise HTTPException(status_code=400, detail="Invalid total price. Cannot proceed with checkout.")

    logger.info(f"Total price for checkout: INR {total_price}")

    #create order
    order = order_models.Order(
        user_id=user.id,
        total_price=total_price,
        status=request_data.status

    )
    
    db.add(order)
    db.commit()
    db.refresh(order)

    logger.info(f"Order created with ID {order.id} for user ID {user.id}")
    
    for item in cart_items:
        order_item = order_models.OrderItem(
        order_id=order.id,
        product_id=item.product_id,
        quantity=item.quantity,
        price_per_unit=item.product.price
    )
    db.add(order_item)

    # Update product stock
    product = db.query(product_models.Product).filter(product_models.Product.id == item.product_id).first()
    if product:
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product '{product.name}'")
        product.stock -= item.quantity
        logger.info(f"Updated stock for product ID {product.id}: {product.stock}")
    else:
        logger.warning(f"Product ID {item.product_id} not found while updating stock")

    #Clear Cart
    db.query(cart_models.CartItem).filter(cart_models.CartItem.user_id == user.id).delete()
    db.commit()

    return {"message": " Order created.Successfully", "order_id": order.id}
