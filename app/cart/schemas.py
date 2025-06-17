from pydantic import BaseModel

class CartAddRequest(BaseModel):
    product_id: int
    quantity: int

class CartUpdateRequest(BaseModel):
    quantity: int
    
class ProductInCartOut(BaseModel):
    id: int
    name: str
    price: float

    model_config = {
        "from_attributes": True
    }
class CartItemOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    product: ProductInCartOut

    model_config = {
        "from_attributes": True
    }
