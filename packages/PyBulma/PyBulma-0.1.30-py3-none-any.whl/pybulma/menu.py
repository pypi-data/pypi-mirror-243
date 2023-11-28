from .base import BaseComponent


class Menu(BaseComponent):
    name = "menu"
    base_classes = ["menu"]

    def _pre_template(self) -> str:
        result = ["<div", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self) -> str:
        return "</div>"


class MenuLabel(BaseComponent):
    name = "menu-label"
    base_classes = ["menu-label"]

    def _pre_template(self) -> str:
        result = ["<p", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append(self.label)
        return " ".join(result)

    def _post_template(self) -> str:
        return "</p>"


class MenuList(BaseComponent):
    name = "menu-list"
    base_classes = ["menu_list"]

    def _pre_template(self) -> str:
        result = ["<ul", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self) -> str:
        return "</ul>"


class MenuItem(BaseComponent):
    name = "menu-item"
    base_classes = []

    def __init__(self, label: str, item_id: str = None, url: str = None,
                 styles: dict = None, attributes: dict = None, classes: list = None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.label = label
        if url:
            self.url = f'href="{url}"'
        else:
            self.url = 'href="#"'

    def _pre_template(self) -> str:
        result = ["<li>", "<a"]
        if self.id:
            result.append(self.id)
        if self.url:
            result.append(self.url)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append(self.label)
        return " ".join(result)

    def _post_template(self) -> str:
        return "</a></li>"
