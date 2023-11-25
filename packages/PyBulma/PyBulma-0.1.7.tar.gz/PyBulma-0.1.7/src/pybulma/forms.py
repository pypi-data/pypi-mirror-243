from base import BaseComponent


class Form(BaseComponent):
    name = "form"
    base_classes = []

    def __init__(self, item_id, action=None, method=None, styles=None, classes=None, attributes=None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.method = method
        self.action = action

    def _pre_template(self):
        result = [f'<form', self.id]
        if self.method:
            result.append(f'method="{self.method}"')
        if self.action:
            result.append(f'action="{self.action}"')
        if self.attributes:
            result.append(self.attributes)
        if self.styles:
            result.append(self.styles)
        if self.classes:
            result.append(self.classes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</form>"


class InputControl(BaseComponent):
    name = "input_control"
    base_classes = ["control"]

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


class Field(BaseComponent):
    name = "input_field"
    base_classes = ["field"]

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


class FieldAddons(BaseComponent):
    name = "input_field_addons"
    base_classes = ["field", "has-addons"]

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


class FieldGrouped(BaseComponent):
    name = "input_field_grouped"
    base_classes = ["field", "is-grouped"]

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
