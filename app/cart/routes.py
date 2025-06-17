from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.cart.schemas import CartAddRequest, CartUpdateRequest, CartItemOut
from app.cart.models import CartItem
from app.products.models import Product
from app.core.database import get_db
from typing import List
from app.auth.jwt_handler import get_current_user_only 
from app.core.logger import logger
router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=CartItemOut, status_code=status.HTTP_201_CREATED)
def add_to_cart(
    request: CartAddRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_only)
):
    logger.info(f"Add to cart request by user {current_user['id']} for product {request.product_id}")

    # Validate requested quantity
    if request.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")

    # Check if product exists
    product = db.query(Product).filter(Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if product is out of stock
    if product.stock <= 0:
        raise HTTPException(status_code=400, detail="Product is out of stock")

    # Check existing cart item
    cart_item = db.query(CartItem).filter_by(
        user_id=current_user["id"],
        product_id=request.product_id
    ).first()

    # Total intended quantity (new + existing)
    existing_quantity = cart_item.quantity if cart_item else 0
    total_requested_quantity = existing_quantity + request.quantity

    # Ensure total requested does not exceed available stock
    if total_requested_quantity > product.stock:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot add {request.quantity} items to cart. Only {product.stock - existing_quantity} left in stock."
        )

    # Update or create cart item
    if cart_item:
        cart_item.quantity = total_requested_quantity
        logger.info(f"Updated cart item quantity for user {current_user['id']}")
    else:
        cart_item = CartItem(
            user_id=current_user["id"],
            product_id=request.product_id,
            quantity=request.quantity
        )
        logger.info(f"Added new item to cart for user {current_user['id']}")

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    logger.debug(f"Cart item saved: {cart_item}")
    return cart_item


@router.get("/", response_model=List[CartItemOut])
def view_cart(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user_only)):
    logger.info(f"Fetching cart items for user {current_user['id']}")
    items = db.query(CartItem).filter(CartItem.user_id == current_user["id"]).all()
    return items

@router.put("/{product_id}", response_model=CartItemOut)
def update_cart(product_id: int, request: CartUpdateRequest, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user_only)):
    logger.info(f"Update request by user {current_user['id']} for product {product_id}")
    cart_item = db.query(CartItem).filter_by(user_id=current_user["id"], product_id=product_id).first()
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

#  Quantity validation
    if request.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")


    cart_item.quantity = request.quantity
    db.commit()
    db.refresh(cart_item)
    logger.info(f"Cart item updated: {cart_item}")
    return cart_item

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_cart(product_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user_only)):
    logger.info(f"Delete request by user {current_user['id']} for product {product_id}")
    cart_item = db.query(CartItem).filter_by(user_id=current_user["id"], product_id=product_id).first()
    if not cart_item:
        logger.warning(f"Cart item not found for user {current_user['id']} and product {product_id}")
        raise HTTPException(status_code=404, detail="Item not found in cart")

    db.delete(cart_item)
    db.commit()
    logger.info(f"Cart item deleted for user {current_user['id']} and product {product_id}")