async function remove_inventory(id)
{
  let item = document.getElementById(`inventory_${id}`)
  let resp = await fetch(`/api/inventory_${id}`, {method: "DELETE"})
  if (!resp.ok) {
    let msg = "Failed to remove inventory"
    if (resp.status == 400)
      msg += `: ${(await resp.json()).message}`
    else
      msg += ". Server undefined error"
    alert(msg)
    return
  }
  item.parentElement.removeChild(item)
}

let disabled_inventory = -1

function switch_update_inventory_block(id)
{
  let elem = document.getElementById(`inventory_${id}`)
  let block = elem.querySelector(".pnd_block_inventory_change")
  let input = elem.querySelector(".pnd_inventory_quantity_change")
  let non_input = elem.querySelector(".pnd_inventory_quantity")

  const block_is_hiden = () => block.classList.contains("d-none")
  const show_block = () => {
    block.classList.remove("d-none")
    disable(non_input)
  }
  const hide_block = () => {
    block.classList.add("d-none")
    enable(non_input)
  }

  if (block_is_hiden()) {
    if (disabled_inventory !== -1)
      switch_update_inventory_block(disabled_inventory)
    show_block()
    disabled_inventory = id
  } else {
    hide_block()
    disabled_inventory = -1
  }

  input.classList.remove(GOOD)
  input.classList.remove(BAD)
  input.value = Number(non_input.value) + 1
}

async function update_inventory(id)
{
  let elem = document.getElementById(`inventory_${id}`)
  let input = elem.querySelector(".pnd_inventory_quantity_change")
  let non_input = elem.querySelector(".pnd_inventory_quantity")
  
  let is_valid = true
  let resc = _check_inventory_quantity(input.value)

  is_valid = _set_input_from_check(resc, input, is_valid)

  if (!is_valid)
    return
  
  let data = new FormData()
  data.append("quantity", Number(input.value))

  let resp = await fetch(`/api/inventory_${id}`, {
    method: "PATCH",
    body: data
  })

  if (!resp.ok) {
    let msg = "Failed to update inventory"
    if (resp.status == 400)
      msg += `: ${(await resp.json()).message}`
    else
      msg += ". Server undefined error"
    alert(msg)
    return
  }
  non_input.value = Number(input.value)
  switch_update_inventory_block(id)
}