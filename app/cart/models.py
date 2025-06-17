from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer, nullable=False)
    # Defines a relationship with the Product table; allows access to product details from cart item
    product = relationship("Product", backref="cart_items", lazy="joined")
    
#lazy="joined" means:Load the related object in the same query using a SQL JOIN.