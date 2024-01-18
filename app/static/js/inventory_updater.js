(() => {
  function update_quantity() {
    let url = "/api/inventory"
    fetch(url).then((resp) => {
      return resp.json()
    }).then((data) => {
      for (let i = 0; i < data.length; i++) {
        let obj = data[i]
        let out = document.querySelector(
          `#inventory_${obj.id} .pnd_inventory_quantity`)
        if (out === null)
          continue
        out.value = obj.quantity
      }
    })
  }
  setInterval(update_quantity, 1000)
})();