from datetime import datetime
from enum import Enum
from pydantic import BaseModel, field_validator
from typing import Literal , List #Literal restricts a value to exactly one of the given strings.

class OrderStatus(str, Enum): #status according to srs
    paid = "paid"
    pending = "pending"
    cancelled = "cancelled"

#request model for checking out an order
class CheckoutRequest(BaseModel):
    status: Literal["paid", "pending", "cancelled"]

    @field_validator("status")
    @classmethod
    def to_lower(cls, v: str) -> str:
        return v.lower() #Ensures the status value is always lowercase

#Represents a single item in an order
class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price_per_unit: float

#Represents a full order for output.
class OrderOut(BaseModel):
    id: int
    user_id: int
    total_price: float
    items: List[OrderItemOut]

    model_config = {
        "from_attributes": True
    }

# Represents a brief view of an order(used in order history)
class OrderSummaryOut(BaseModel):
    id: int
    total_price: float
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class OrderItemDetailOut(BaseModel):
    product_id: int
    quantity: int
    price_per_unit: float

    model_config = {
        "from_attributes": True
    }

#used when showing full details of an order.
class OrderDetailOut(BaseModel):
    id: int
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemDetailOut]

    model_config = {
        "from_attributes": True
    }
