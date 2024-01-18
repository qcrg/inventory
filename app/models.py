from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, Text, Integer, ForeignKey, Column, Float, \
  UniqueConstraint

Base = declarative_base()

class Inventory(Base):
  __tablename__ = "inventory"

  id = Column(Integer, primary_key = True)
  product_id = Column(Integer, ForeignKey("products.id"))
  location_id = Column(Integer, ForeignKey("locations.id"))
  quantity = Column(Integer)

  __table_args__ = (UniqueConstraint(product_id, location_id), )

  product = relationship("Product", back_populates="inventory")
  location = relationship("Location", back_populates="inventory")

class Product(Base):
  __tablename__ = "products"

  id = Column(Integer, primary_key = True)
  name = Column(String(50))
  description = Column(Text)
  price = Column(Float)

  inventory = relationship("Inventory", back_populates="product")

class Location(Base):
  __tablename__ = "locations"

  id = Column(Integer, primary_key = True)
  name = Column(String(50))

  inventory = relationship("Inventory", back_populates="location")