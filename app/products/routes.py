from fastapi import APIRouter, Depends, HTTPException, status, Query #APIRouter: Used to create route groups
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import or_, asc #or_: For combining multiple filter conditions using OR, asc-ascending order
from app.core.database import get_db #Provides the database session through FastAPI's dependency system.
from app.products.models import Product
from app.products.schemas import ProductCreate, ProductOut, ProductUpdate
from app.auth.jwt_handler import get_current_admin_user #Verifies the admin user based on JWT token.
from app.orders.models import OrderItem # Model for checking if a product is part of an order before deleting.

#Tags for Swagger UI grouping.
admin_router = APIRouter(prefix="/admin/products", tags=["Admin Products"]) #Secured endpoints for admins only 
#admin can create a product.
@admin_router.post("", response_model=ProductOut, status_code=status.HTTP_201_CREATED) 
#Takes a ProductCreate body.add product to db . returns the created product with an auto-generated id.
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    #Converts Pydantic model to dictionary and unpacks to create a Product object.
    product = Product(**product_in.model_dump()) #dict() was deprecated so used model_dump()
    db.add(product)
    db.commit()
    db.refresh(product)
    #Saves the product to the database and retrieves the updated object with the generated id
    return product

@admin_router.get("", response_model=List[ProductOut])
#Returns a paginated list of products.
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    products = db.query(Product).offset(skip).limit(limit).all() #offset:Tells the database how many records to skip
    return products

@admin_router.get("/{product_id}", response_model=ProductOut)
#Get Product by ID
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user) #do admin authentication
):
    product = db.query(Product).filter(Product.id == product_id).first() #Fetches the product by ID.

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@admin_router.put("/{product_id}", response_model=ProductOut)
#updates the product by id
def update_product(
    product_id: int,
    product_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    product = db.query(Product).filter(Product.id == product_id).first() 
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    for key, value in product_in.model_dump().items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

@admin_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    #checkpoint if a product is assosiated with certain order
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if db.query(OrderItem).filter(OrderItem.product_id == product.id).first():
        raise HTTPException(
        status_code=400,
        detail="Cannot delete product that is part of an existing order."
        
    )

    db.delete(product)
    db.commit()
    return None

#public APIs 
public_router = APIRouter(tags=["Public Products"])

@public_router.get("/products", response_model=List[ProductOut])
def list_products_public(
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    sort_by: Optional[str] = Query("id"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Product)
#Supports filtering by category, price range.
    if category:
        query = query.filter(Product.category == category)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    sort_column = getattr(Product, sort_by, None)
    if not sort_column:
        sort_column = Product.id

    query = query.order_by(asc(sort_column))
    offset = (page - 1) * page_size
    products = query.offset(offset).limit(page_size).all()
    return products

@public_router.get("/products/search", response_model=List[ProductOut])
def search_products_public(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    #Searches across name, description, and category using case-insensitive matching using islike function.
    query = db.query(Product).filter(
        or_(
            Product.name.ilike(f"%{keyword}%"),
            Product.description.ilike(f"%{keyword}%"),
            Product.category.ilike(f"%{keyword}%")
        )
    ).order_by(Product.id.asc())

    offset = (page - 1) * page_size
    products = query.offset(offset).limit(page_size).all()
<<<<<<< HEAD
    #checkpoint if a product is not found with certain keywords
=======
>>>>>>> 0142af0570e43da8bccb04634ad33b1750370c08
    if not products:
        raise HTTPException(status_code=404, detail="No products found matching the keyword.")
    return products

@public_router.get("/products/{product_id}", response_model=ProductOut)
#to get product by id
def get_product_public(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    #checkpoint if a product is not found
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
