from pydantic import BaseModel # used to Validate input data

class ProductBase(BaseModel): #Other models will inherit from this to avoid repeating fields.
    name: str
    description: str
    price: float
    stock: int
    category: str
    image_url: str

class ProductCreate(ProductBase): #For Creating Products
    pass

class ProductUpdate(ProductBase):#For Updating Products
    pass

class ProductOut(ProductBase):#Represents the product format used in API responses
    id: int

    model_config = {
        "from_attributes": True #This enables FastAPI to automatically convert SQLAlchemy objects (or similar) into this model using attribute access.
        }
