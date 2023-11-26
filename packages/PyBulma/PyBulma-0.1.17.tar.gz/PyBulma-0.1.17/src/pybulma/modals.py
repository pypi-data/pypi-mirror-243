from .base import BaseComponent


class Modal(BaseComponent):
    name = "modal"
    base_classes = ["modal"]

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


class ModalBackground(BaseComponent):
    name = "modal-background"
    base_classes = ["modal-background"]

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


class ModalContent(BaseComponent):
    name = "modal_content"
    base_classes = "modal-content"

    def _pre_template(self):
        result = ["<div", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")

    def _post_template(self):
        return "</div>"


class ModalCard(BaseComponent):
    name = "modal-card"
    base_classes = ["modal-card"]

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


class ModalCardHeader(BaseComponent):
    name = "modal-card-header"
    base_classes = ["modal-card-header"]

    def __init__(self, title, item_id=None, styles=None, attributes=None, classes=None):
        self.title = title
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=None)

    def _pre_template(self):
        result = ["<header", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append(self.title)
        return " ".join(result)

    def _post_template(self):
        return '<button class="delete" aria-label="close"></button></header>'


class ModalCardBody(BaseComponent):
    name = "modal-card-body"
    base_classes = ["modal-card-body"]

    def _pre_template(self):
        result = ["<section", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</section>"


class ModalCardFooter(BaseComponent):
    name = "modal-card-footer"
    base_classes = ["modal-card-footer"]

    def _pre_template(self):
        result = ["<footer", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        return " ".join(result)

    def _post_template(self):
        return "</footer>"
