from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base
from sqlalchemy import DateTime, func, String

#Provides all orders placed by a user
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    total_price = Column(Float, nullable=False)
    status = Column(String, default="Completed")  # default status
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

#One-to-many relationship with OrderItem.back_populates creates a two-way connection.
# cascade="all, delete" ensures all related order items are deleted when the order is deleted.

#Provides each product detail inside an order
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer)
    quantity = Column(Integer)
    price_per_unit = Column(Float)

    order = relationship("Order", back_populates="items")
