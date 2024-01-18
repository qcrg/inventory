from app import app
import flask as _flask
from flask import \
  render_template as _render_template, \
  url_for as _url_for, \
  request as _req, \
  jsonify as _jsonify
from app.dbactions import DBActions
from app.validators import \
  IntValidator as _IntValid, \
  FloatValidator as _FloatValid, \
  StringValidator as _StringValid, \
  NotNoneValidator as _NotNoneValid
import json as _json

def _create_fail_resp(message) -> (_flask.Response, 400):
  return (_jsonify(message=message), 400)

def _db_add_fail_resp() -> (_flask.Response, 500):
  return (_jsonify(message="Failed to add in database"), 500)

def _create_db_add_ok_resp(obj_id: int) -> (_flask.Response, 200):
  return (_jsonify(obj_id=obj_id), 200)

@app.route("/")
def index():
  import app.items as utils
  dbacts = DBActions()
  arg_name = _req.args.get("name", "")
  arg_order = _req.args.get("order", "")
  arg_locs = _req.args.get("locations", "")
  items = utils.get(arg_name, arg_order, arg_locs)
  locations = [
    {"id": loc.id, "name": loc.name}
    for loc in dbacts.get_all_locations()
  ]
  products = [
    {"id": prod.id, "name": prod.name}
    for prod in dbacts.get_all_products()
  ]
  return _render_template(
    "index.html.j2",
    items=items,
    products=products,
    locations=locations)

@app.post("/api/product")
def add_product():
  name = _req.form.get("name", None)
  name_checker = _StringValid("Product Name", 1, 50)
  if not name_checker.check(name):
    return name_checker.response()
  
  desc = _req.form.get("description", None)
  # if desc is None:
  #   return _jsonify(status=1,
  #                   message="Description is undefined"), 400

  price = _req.form.get("price", None)
  price_checker = _FloatValid("Product Price", 0)
  if not price_checker.check(price):
    return price_checker.response()

  dbacts = DBActions()
  product = dbacts.add_product(name, desc, price)
  if product is None:
    return _db_add_fail_resp()
  return _create_db_add_ok_resp(product.id)

@app.post("/api/location")
def add_location():
  dbacts = DBActions()
  name = _req.form.get("name", None)
  name_checker = _StringValid("Location Name", 1, 50)
  if not name_checker.check(name):
    return name_checker.response()
  loc = dbacts.add_location(name)
  if loc is None:
    return _db_add_fail_resp()
  return _create_db_add_ok_resp(loc.id)

@app.post("/api/inventory")
def add_inventory():
  dbacts = DBActions()

  loc_id = _req.form.get("location_id", None)
  loc_id_checker = _NotNoneValid("location_id")
  if not loc_id_checker.check(loc_id):
    return loc_id_checker.response()
  
  loc = dbacts.get_location(loc_id)
  if loc is None:
    return _create_fail_resp(
      f"Location with ID[{loc_id}] not found in database")

  prod_id = _req.form.get("product_id", None)
  prod_id_checker = _NotNoneValid("product_id")
  if not prod_id_checker.check(prod_id):
    return prod_id_checker.response()
  prod = dbacts.get_product(prod_id)
  if prod is None:
    return _create_fail_resp(
      f"Product with ID[{prod_id}] not found in database")

  count = _req.form.get("quantity", None)
  count_cheker = _IntValid("Quantity", 0)
  if not count_cheker.check(count):
    return count_cheker.resp

  inv = dbacts.add_inventory(loc, prod, count)
  if inv is None:
    return _db_add_fail_resp()
  return _create_db_add_ok_resp(inv.id)

@app.patch("/api/inventory_<int:id>")
def update_inventory(id):
  dbacts = DBActions()

  id_checker = _IntValid("Inventory ID", 1)
  if not id_checker.check(id):
    return id_checker.response()

  quant = _req.form.get("quantity", None)
  quant_cheker = _IntValid("Quantity", 0)
  if not quant_cheker.check(quant):
    return quant_cheker.resp

  if dbacts.update_inventory_from_id(id, quant):
    return ("", 204)
  return ("", 500)

@app.delete("/api/inventory_<int:id>")
def delete_inventory(id):
  dbacts = DBActions()
  id_checker = _IntValid("Inventory ID", 1)
  if not id_checker.check(id):
    return id_checker.response()
  if dbacts.delete_inventory_from_id(id):
    return ("", 204)
  return ("", 500)


@app.get("/api/inventory")
def get_inventory():
  dbacts = DBActions()
  res = list()
  # data = _json.loads(_req.get_data().decode())
  ids_str = _req.args.get("ids", str)
  tmpdata = ids_str.split(',')
  ids = set()
  for id_obj in tmpdata:
    try:
      inv_id = int(id_obj)
    except:
      continue
    else:
      ids.add(inv_id)
  if len(ids) == 0:
    invs = dbacts.get_all_inventory()
    for inv in invs:
      res.append({
        "id": inv.id,
        "quantity": inv.quantity
      })
  else:
    for inv_id in ids:
      inv = dbacts.get_inventory(inv_id)
      res.append({
        "id": inv_id,
        "quantity": inv.quantity if inv else 0
      })
  return (_jsonify(res), 200)

@app.route("/test_<string:name>")
def test(name):
  for key, value in _req.args.items():
    print(key, "=", value)
  return f"""
  <form method="post" action="/api/{name}">
    <input id="name" name="name" type="text" maxlength=50 />
    <label for="name">Name</label>
    <br/>

    <textarea id="desc" name="description"></textarea>
    <label for="desc">Description</label>
    <br/>

    <input id="price" name="price" type="number"
        value=0.0 min=0.0 max=999999.0 />
    <label for="price">Price</label>
    <br/>
    <br/>
    <br/>

    <input id="product_id" name="product_id" type="number"
        min=1 max=999999 />
    <label for="product_id">Product ID</label>
    <br/>

    <input id="location_id" name="location_id" type="number"
        min=1 max=999999 />
    <label for="location_id">Location ID</label>
    <br/>

    <input id="quantity" name="quantity" type="number"
        value=1 min=1 max=999999 />
    <label for="quantity">Quantity</label>
    <br/>

    <input type="submit" value="Submit Test" />
  </form>
"""
