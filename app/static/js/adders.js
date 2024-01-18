const GOOD = "is-valid"
const BAD = "is-invalid"

function hide(elem)
{
  elem.setAttribute("hidden", "")
}

function show(elem)
{
  elem.removeAttribute("hidden")
}

function disable(elem)
{
  elem.setAttribute("disabled", "")
}

function enable(elem)
{
  elem.removeAttribute("disabled")
}

function is_enabled(elem)
{
  return !elem.hasAttribute("disabled")
}

function switch_add_button(button_id)
{
  let btn = document.getElementById(button_id)
  let def_label = document.querySelector(`#${button_id} .pnd-default-label`)
  let spinner = document.querySelector(`#${button_id} .pnd-wait-spinner`)
  if (is_enabled(btn))
  {
    disable(btn)
    show(spinner)
    hide(def_label)
    return
  }
  enable(btn)
  hide(spinner)
  show(def_label)
}

async function _post_add(url = "", obj_data = {})
{
  let data = new FormData()
  for (let key in obj_data)
    data.append(key, obj_data[key])
  const resp = await fetch(url, {
    method: "POST",
    body: data
  })
  return resp
}

function _add_location_client_side(id, name)
{
  LOCATION_NAMES.add(name)
  LOCATIONS.set(Number(id), name)
  const html_item_str = `
  <li class="list-group-item" data-pnd-id="${id}">
    <div id="location-${id}" class="form-check">
      <input type="checkbox" class="form-check-input" id="input-location-${id}">
      <label class="form-check-label" for="input-location-${id}">${name}</label>
    </div>
  </li>
  `
  let templ = document.createElement("template")
  templ.innerHTML = html_item_str.trim()
  let item = templ.content.firstChild
  let list = document.getElementById("filter-locations-block").children[0]
  let listfc = list.firstChild
  if (1 === listfc &&
      listfc.hasAttribute("data-pnd-id") &&
      listfc.getAttribute("data-pnd-id") === "none")
    list.removeChild(listfc)
  list.appendChild(item)
}

function _check_location_name(name)
{
  let ok = true
  let errmsg = ""
  if (0 === name.length)
    return {
      ok: false,
      errmsg: "Please choose a location name"
    }
  if (LOCATION_NAMES.has(name))
    return {
      ok: false,
      errmsg: "Location with this name is already exists"
    }
  return {
    ok: true
  }
}

function _set_input_from_check(res, input, is_valid)
{
  if (res.ok) {
    input.classList.add(GOOD)
    input.classList.remove(BAD)
    return is_valid
  }

  input.classList.add(BAD)
  input.classList.remove(GOOD)
  let fb = input.parentElement.querySelector(".invalid-feedback")
  if (null !== fb)
    fb.innerText = res.errmsg
  return false
}

async function add_location(modal_id)
{
  let is_valid = true
  let name_input = document.getElementById(`${modal_id}_input_name`)

  let resnc = _check_location_name(name_input.value)
  is_valid = _set_input_from_check(resnc, name_input, is_valid)

  if (!is_valid)
    return
  
  switch_add_button(`${modal_id}_add`)
  let resp = await _post_add("/api/location", {name: name_input.value})
  
  let modal_obj = document.getElementById(modal_id)
  let modal = bootstrap.Modal.getInstance(modal_obj)

  if (!resp.ok) {
    let msg = "Failed to add product. Server undefined error"
    if (resp.status == 400)
      msg = `Failed to add product: ${(await resp.json()).message}`
    alert(msg)
    switch_add_button(`${modal_id}_add`)
    return
  }

  let loc_id = (await resp.json()).obj_id
  let name = name_input.value
  _add_location_client_side(loc_id, name)
  modal.hide()
}

function _check_product_name(name)
{
  if (0 === name.length)
    return {
      ok: false,
      errmsg: "Please choose a product name"
    }
  if (PRODUCT_NAMES.has(name))
    return {
      ok: false,
      errmsg: "Product with this name is already exists"
    }
  return {
    ok: true
  }
}

function _check_product_desc(desc)
{
  return {
    ok: true
  }
}

function _check_product_price(price)
{
  if (0 === price.length)
    return {
      ok: false,
      errmsg: "Please set the price"
    }
  let val = Number(price)
  if (isNaN(val))
    return {
      ok: false,
      errmsg: "Not a number"
    }
  if (0 > val)
    return {
      ok: false,
      errmsg: "It cannot be a negative number"
    }
  return {
    ok: true
  }
}

function _add_product_client_side(id, name, desc, price)
{
  PRODUCT_NAMES.add(name)
  PRODUCTS.set(Number(id), name)
  const html_item_str = `
  <div id="product-${id}" class="card mb-4">
    <div class="card-body">
      <div class="float-end">
        <span class="fw-bold">${price} $</span>
      </div>
      <h4 class="card-title fw-bold">${name}</h4>
      <p class="card-text">${desc}</p>
      <div class="float-end">

        <button class="btn btn-primary"
          data-bs-toggle="modal"
          data-bs-target="#add_inventory_window"
          id="add_inventory_button"
          onclick="preprocess_inventory_add(${id})"
        >
          Add to the warehouse
        </button>
      </div>
    </div>
    <ul class="list-group list-group-flush ml-3">
    </ul>
  </div>
  `
  let templ = document.createElement("template")
  templ.innerHTML = html_item_str.trim()
  let item = templ.content.firstChild
  let list = document.getElementById("product_list")
  list.appendChild(item)
}

async function add_product(modal_id)
{
  function name(n) {
    return `${modal_id}_${n}`
  }
  let is_valid = true

  let name_input = document.getElementById(name("input_name"))
  let res_name = _check_product_name(name_input.value)
  is_valid = _set_input_from_check(res_name, name_input, is_valid)

  let desc_input = document.getElementById(name("input_desc"))
  let res_desc = _check_product_desc(desc_input.value)
  is_valid = _set_input_from_check(res_desc, desc_input, is_valid)

  let price_input = document.getElementById(name("input_price"))
  let res_price = _check_product_price(price_input.value)
  is_valid = _set_input_from_check(res_price, price_input, is_valid)

  if (!is_valid)
    return

  switch_add_button(`${modal_id}_add`)
  let resp = await _post_add("/api/product", {
    name: name_input.value,
    description: desc_input.value,
    price: price_input.value
  })

  let modal = bootstrap.Modal.getInstance(document.getElementById(modal_id))

  if (!resp.ok) {
    let msg = "Failed to add product. Server undefined error"
    if (resp.status == 400)
      msg = `Failed to add product: ${(await resp.json()).message}`
    alert(msg)
    switch_add_button(`${modal_id}_add`)
    return
  }

  {
    let id = (await resp.json()).obj_id
    let name = name_input.value
    let desc = desc_input.value
    let price = price_input.value
    _add_product_client_side(id, name, desc, price)
    modal.hide()
  }
}

function preprocess_inventory_add(product_id)
{
  function name(n) {
    return `add_inventory_window_input_${n}`
  }
  let prod = document.getElementById(name("product_id"))
  prod.value = PRODUCTS.get(product_id)
  prod.setAttribute("data-bs-id", product_id)

  let templ = document.createElement("template")
  let list = document.getElementById(name("location_id"))
  {
    templ.innerHTML = `<option selected="" value="-1"></option>`
    list.innerHTML = ""
    list.appendChild(templ.content.firstChild)
  }

  let locations = new Map(LOCATIONS)
  {
    let exist_locs = document.querySelector(
      `#product-${product_id} .list-group`).children
    for (let i = 0; i < exist_locs.length; i++) {
      let num = Number(exist_locs[i].getAttribute("data-pnd-location-id"))
      locations.delete(num)
    }
  }

  locations.forEach((name, id, map) => {
    templ.innerHTML = `<option value="${id}">${name}</option>`
    let item = templ.content.firstChild
    list.appendChild(item)
  });

  let quant = document.getElementById(name("quantity"))
  quant.value = "0"
}

function _check_inventory_location(loc)
{
  if ("-1" === loc)
    return {
      ok: false,
      errmsg: "Please select a location"
    }
  return {
    ok: true
  }
}

function _check_inventory_quantity(quant)
{
  if (0 === quant.length)
    return {
      ok: false,
      errmsg: "Please set the quantity"
    }
  let val = Number(quant)
  if (isNaN(val))
    return {
      ok: false,
      errmsg: "Not a number"
    }
  if (0 > val)
    return {
      ok: false,
      errmsg: "It cannot be a negative number"
    }
  if (!Number.isInteger(val))
    return {
      ok: false,
      errmsg: "It can only be an integer"
    }
  return {
    ok: true
  }
}

function _add_inventory_client_side(prod_id, loc_id, inv_id, quant)
{
  const html_item_str = `
    <li class="d-flex align-items-center list-group-item ml-100"
      id="inventory_${inv_id}" 
      data-pnd-id="${inv_id}"
      data-pnd-location-id="${loc_id}"
    >
      <div class="input-group input-group-sm me-1"
        style="min-width: 150px; max-width: 150px;"
      >
        <input class="form-control pnd_inventory_quantity"
          type="text"
          value="${quant}"
          readonly=""
        />
        <span class="input-group-text">pcs</span>
      </div>
      <div class="pnd_block_inventory_change
          d-flex align-items-center
          d-none"
      >
        <div class="input-group input-group-sm me-1"
          style="min-width: 150px; max-width: 150px;"
        >
          <input class="form-control pnd_inventory_quantity_change"
            type="text"
          />
          <span class="input-group-text">pcs</span>
        </div>
        <button class="btn btn-sm btn-success me-2"
          onclick="update_inventory('${inv_id}')"
        >✔</button>
        <button class="btn btn-sm btn-danger me-2"
          onclick="switch_update_inventory_block('${inv_id}')"
        >🗙</button>
      </div>
      <span class="text-end w-100 ps-1 pe-2">
        ${LOCATIONS.get(Number(loc_id))}
      </span>
      <div class="dropend">
        <button class="btn btn-sm btn-outline-secondary
            dropdown-toggle align-items-center d-flex"
          type="button"
          data-bs-toggle="dropdown"
          aria-expanded="false"
        >
          <img src="static/images/cogwheel.svg" />
        </button>
        <ul class="dropdown-menu">
          <li><h6 class="dropdown-header">Actions</h6></li>
          <li>
            <button class="dropdown-item"
              onclick="switch_update_inventory_block('${inv_id}')"
            >
              Change
            </button>
          </li>
          <li><hr class="dropdown-divider"></li>
          <li><button class="dropdown-item text-danger" onclick="remove_inventory('${inv_id}')">Remove</button></li>
        </ul>
      </div>
    </li>
  `
  let templ = document.createElement("template")
  templ.innerHTML = html_item_str.trim()
  let item = templ.content.firstChild
  let list = document.querySelector(`#product-${prod_id} .list-group`)
  if (list.querySelector(`#inventory_${inv_id}`))
    return
  list.appendChild(item)
}

async function add_inventory(modal_id)
{
  function name(n) {
    return `${modal_id}_input_${n}`
  }
  let is_valid = true

  function check(name_, check_func) {
    let input = document.getElementById(name(name_))
    let res = check_func(input.value)
    is_valid = _set_input_from_check(res, input, is_valid)
    return input.value
  }

  let prod_id = document.getElementById(
      name("product_id")).getAttribute("data-bs-id")
  let loc_id = check("location_id", _check_inventory_location)
  let quant = check("quantity", _check_inventory_quantity)

  if (!is_valid)
    return

  switch_add_button(`${modal_id}_add`)
  let resp = await _post_add("/api/inventory", {
    product_id: prod_id,
    location_id: loc_id,
    quantity: quant
  })

  let modal = bootstrap.Modal.getInstance(document.getElementById(modal_id))

  if (!resp.ok) {
    let msg = "Failed to add inventory"
    if (resp.status == 400)
      msg += `. ${(await resp.json()).message}`
    else
      msg += ": Server undefined error"
    alert(msg)
    switch_add_button(`${modal_id}_add`)
    return
  }

  {
    let inv_id = (await resp.json()).obj_id
    _add_inventory_client_side(prod_id, loc_id, inv_id, quant)
    modal.hide()
  }
}