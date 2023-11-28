from browser import document, bind


def open_modal(evt):
    try:
        target = evt.currentTarget.attrs["pybulma-target-modal"]
        modal = document[target]
        modal.classList.add("is-active")
        if "pybulma-target-focus" in evt.currentTarget.attrs:
            focus_element = evt.currentTarget.attrs["pybulma-target-focus"]
            document[focus_element].focus()
    except Exception as e:
        print(e)
        pass


def close_modal(evt):
    modals = document.select(".modal")
    for modal in modals:
        modal.classList.remove("is-active")


def set_modal_binds():
    for modal in document.select(".pybulma-modal-open"):
        modal.bind("click", open_modal)
    for modal in document.select(".pybulma-modal-close"):
        modal.bind("click", close_modal)
    for modal in document.select(".delete"):
        modal.bind("click", close_modal)
    for modal in document.select(".modal-background"):
        modal.bind("click", close_modal)


set_modal_binds()
