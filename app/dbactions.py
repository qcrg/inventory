from app.dbsession import \
  create_session as _create_session, \
  SessionWrapper as _SW
from app.models import Inventory, Product, Location, Base as _Base
from typing import List, Tuple, Any

class DBActions:
  def __init__(self):
    self.s = _create_session()
  
  def __del__(self):
    self.s.close()
  
  def _add(self, obj):
    try:
      self.s.add(obj)
    except Exception as e:
      self.s.rollback()
      print(e)
      return None
    self.s.commit()
    return obj
  
  def _delete(self, obj):
    try:
      self.s.delete(obj)
    except Exception as e:
      self.s.rollback()
      print(e)
      return False
    self.s.commit()
    return True

  def _get(self, Entity, entity_id):
    return self.s.get(Entity, entity_id)

  def add_product(self, name, description, price):
    prod = self.get_product_from_name(name)
    if prod is None:
      prod = Product(name = name, description = description, price = price)
      return self._add(prod)
    try:
      prod.description = description
      prod.price = price
    except:
      self.s.rollback()
      return None
    self.s.commit()
    return prod

  def get_product(self, id):
    return self._get(Product, id)

  def get_all_products(self):
    return self.s.query(Product).all()

  def get_product_from_name(self, name):
    return self.s.query(Product).filter(Product.name == name).first()

  def add_location(self, name):
    loc = self.get_location_from_name(name)
    if loc is None:
      loc = Location(name = name)
      return self._add(loc)
    return loc

  def get_location(self, id):
    return self._get(Location, id)

  def get_location_from_name(self, name):
    return self.s.query(Location).filter(Location.name == name).first()

  def get_all_locations(self):
    return self.s.query(Location).order_by(Location.id).all()

  def add_inventory(
      self,location: Location,
      product: Product,
      quantity: int):
    inv = self.get_inventory_from_loc_and_prod(location, product)
    if inv is None:
      inv = Inventory(location = location, product = product, quantity = quantity)
      return self._add(inv)

    try:
      inv.quantity = quantity
    except:
      self.s.rollback()
      return None
    self.s.commit()
    return inv

  def get_inventory(self, id: int):
    return self._get(Inventory, id)

  def get_all_inventory(self):
    return self.s.query(Inventory).all()

  def get_inventory_from_loc_and_prod(
      self,
      location: Location,
      product: Product):
    res = self.s.query(Inventory).filter(
      Inventory.location == location,
      Inventory.product == product).first()
    return res
  
  def update_inventory_from_id(self, id, quant) -> bool:
    inv = self.get_inventory(id)
    try:
      inv.quantity = quant
    except Exception as ex:
      print(ex)
      self.s.rollback()
      return False
    self.s.commit()
    return True

  def delete_inventory(self, inventory) -> bool:
    return self._delete(inventory)

  def delete_inventory_from_id(self, id) -> bool:
    return self.delete_inventory(self.get_inventory(id))