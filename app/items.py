from app.dbsession import \
  SessionWrapper as _SessionWrapper
from app.dbactions import DBActions as _DBActions
from app.models import Product
from flask import render_template as _render_template
from typing import List

def _format_inventory(product):
  res = list()
  for inv in product.inventory:
    res.append({
      "id": inv.id,
      "location_id": inv.location.id,
      "location_name": inv.location.name,
      "quantity": inv.quantity
    })
  return res

def _format(products: List[Product]) -> List[str]:
  res = list()
  for prod in products:
    res.append(_render_template("elements/item.html.j2", item={
        "id": prod.id,
        "name": prod.name,
        "desc": prod.description,
        "price": prod.price,
        "inventory": _format_inventory(prod)
      })
    )
  return res

def get(name: str, order: str, locations: str) -> List[str]:
  from app.models import Inventory
  from sqlalchemy.sql import func
  s = _SessionWrapper()
  first_q = s.session.query(
      Inventory.product_id,
      func.sum(Inventory.quantity).label("quantity")).\
    group_by(Inventory.product_id).subquery().alias("q")

  ORDER_METHODS= {
    "0": Product.id,
    "1": Product.price.desc(),
    "2": first_q.c.quantity.desc()
  }

  prods = s.session.query(Product).\
    join(first_q, Product.id == first_q.c.product_id, isouter=True).\
    where(Product.name.like(f"%{name}%")).\
    order_by(ORDER_METHODS.get(order, Product.id)).\
    all()

  return _format(prods)