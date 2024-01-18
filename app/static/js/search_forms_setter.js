// set values for <input>
(() => {
  function setter(val, elem_id) {
    document.getElementById(elem_id).value = val
  }
  let url = new URL(window.location.href)
  url.searchParams.forEach(setter)
})();

// set value for <input name=locations> from checkboxes
(() => {
  function on_submit() {
    function is_checked(elem) {
      return elem.children[0].children[0].checked
    }
    let locs = document.querySelectorAll("#filter-locations-block ul li")
    let vals = []
    for (let i = 0; i < locs.length; i++) {
      if (is_checked(locs[i]))
        vals.push(Number(locs[i].getAttribute("data-pnd-id")))
    }
    let res = JSON.stringify(vals)
    res = res.substring(1, res.length - 1)
    let form = document.getElementById("locations")
    form.value = res
  }
  document.getElementById("form_search").onsubmit = on_submit
})();

// set location checkboxes from <input name=locations>
(() => {
  let value_str = document.getElementById("locations").value
  value_str = `[${value_str}]`
  let vals = JSON.parse(value_str)
  for (let i = 0; i < vals.length; i++) {
    let name = "input-location-" + vals[i]
    let cbox = document.getElementById(name)
    cbox.checked = true
  }
})();