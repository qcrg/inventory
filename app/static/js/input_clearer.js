function clear_inputs(id)
{
  let objs = document.querySelectorAll(`#${id} .form-control`)
  for (let i = 0; i < objs.length; i++) {
    objs[i].value = ""
    objs[i].classList.remove("is-valid")
    objs[i].classList.remove("is-invalid")
    const btn_id = `${id}_add`
    let btn = document.getElementById(btn_id)
    if (!is_enabled(btn))
      switch_add_button(btn_id)
  }
}

function init_modal_inputs_clearer(id)
{
  const delay = 300
  function timeout_clear() {
    setTimeout(() => {
      clear_inputs(id)
    }, delay)
  }
  let obj = document.getElementById(id)
  obj.addEventListener("hide.bs.modal", timeout_clear)
}