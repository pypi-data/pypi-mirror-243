from .base import BaseComponent


class Field(BaseComponent):
    name = "field container component"
    base_classes = ["field"]

    def _pre_template(self):
        result = ["<div", self.classes]
        if self.styles:
            result.append(self.styles)
        if self.id:
            result.append(self.id)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</div>"


class Control(Field):
    name = "Control Container Component"
    base_classes = ["control"]


class Label(BaseComponent):
    name = "input_label"
    base_classes = ["label"]

    def __init__(self, text, item_id=None, styles=None, attributes=None, classes=None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.text = text

    def _pre_template(self):
        result = ["<label", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append(self.text)

    def _post_template(self):
        return "</label>"


class InputHelp(BaseComponent):
    name = "input_help"
    base_classes = ["help"]

    def __init__(self, text, item_id=None, classes=None, styles=None, attributes=None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.text = text

    def _pre_template(self):
        result = ["<p", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append(self.text)
        return " ".join(result)

    def _post_template(self):
        return "</p>"


class Input(BaseComponent):
    name = "input_element"
    base_classes = ["input"]

    def __init__(self, item_id, name, input_type, value=None,
                 placeholder=None, styles=None, classes=None, attributes=None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.name = f'name="{name}"'
        self.placeholder = placeholder
        self.input_type = f'type="{input_type}"'
        if value:
            self.value = f'value="{value}"'
        else:
            self.value = None

    def _pre_template(self):
        result = ["<input", self.id, self.classes, self.name]
        if self.value:
            result.append(self.value)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        if self.placeholder:
            result.append(self.placeholder)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return " "


class TextArea(BaseComponent):
    name = "textarea"
    base_classes = ["textarea"]

    def __init__(self, name, value=None, item_id=None, placeholder=None, classes=None, styles=None, attributes=None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.name = f'name="{name}"'
        self.placeholder = placeholder
        self.value = value

    def _pre_template(self):
        result = ["<textarea", self.name, self.classes]
        if self.placeholder:
            result.append(self.placeholder)
        if self.attributes:
            result.append(self.attributes)
        if self.styles:
            result.append(self.styles)
        if self.id:
            result.append(self.id)
        result.append(">")
        if self.value:
            result.append(self.value)
        return " ".join(result)

    def _post_template(self):
        return "</textarea>"


class SelectContainer(BaseComponent):
    name = "select container"
    base_classes = "select"

    def _pre_template(self):
        result = ["<div", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</div>"


class Select(BaseComponent):
    name = "select"
    base_classes = []

    def __init__(self, name: str, multiple: bool = False, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None):
        self.name = f'name="{name}"'
        self.multiple = multiple
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self):
        result = ["<select", self.name]
        if self.multiple:
            result.append("multiple")
        if self.classes:
            result.append(self.classes)
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</select>"


class Option(BaseComponent):
    name = "select option component"
    base_classes = []

    def __init__(self, text: str, value: str, selected: bool = False, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None):
        self.text = text
        self.value = f'value="{value}"'
        self.selected = selected
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self):
        result = ["<option", self.value]
        if self.selected:
            result.append("selected")
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        if self.classes:
            result.append(self.classes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        result = [self.text, "</option>"]
        return " ".join(result)


class CheckboxLabel(Label):
    name = "checkbox label"
    base_classes = ["checkbox"]


class CheckBox(BaseComponent):
    name = "checkbox"
    base_classes = []

    def __init__(self, name: str, value: str, checked: bool = False, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None):
        self.name = f'name="{name}"'
        self.value = f'value="{value}"'
        self.checked = checked
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self):
        result = ['<input type="checkbox"', self.name, self.value]
        if self.checked:
            result.append("checked")
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        if self.classes:
            result.append(self.classes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return ""


class RadioLabel(Label):
    name = "radio label"
    base_classes = ["radio"]


class Radio(CheckBox):
    name = "radio component"
    base_classes = []

    def _pre_template(self):
        result = ['<input type="radio"', self.name, self.value]
        if self.checked:
            result.append("checked")
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        if self.classes:
            result.append(self.classes)
        result.append(">")
        return " ".join(result)




