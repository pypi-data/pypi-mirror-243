from .base import BaseComponent
from .icon import Icon


class Tabs(BaseComponent):
    name = "tabs"
    base_classes = ["tabs"]

    def _pre_template(self) -> str:
        result = ["<div", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append("<ul>")
        return " ".join(result)

    def _post_template(self) -> str:
        return "</ul></div>"


class TabItem(BaseComponent):
    name = "tab-item"
    base_classes = []

    def __init__(self, label: str, url: str, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None) -> None:
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.label = label
        self.url = f'href="{url}"'

    def _pre_template(self) -> str:
        result = ["<li"]
        if self.id:
            result.append(self.id)
        if self.classes:
            result.append(self.classes)
        result.append("><a")
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


class TabItemIcon(BaseComponent):
    name = "tab-item-icon"
    base_classes = []

    def __init__(self, label: str, url: str, icon: Icon, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None) -> None:
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.label = label
        self.url = f'href="{url}"'
        self.icon = icon

    def _pre_template(self) -> str:
        result = ["<li"]
        if self.id:
            result.append(self.id)
        if self.classes:
            result.append(self.classes)
        result.append("><a")
        result.append(self.url)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append("<span>")
        result.append(self.icon.compile())
        result.append("</span><span>")
        result.append(self.label)
        result.append("</span>")
        return " ".join(result)

    def _post_template(self) -> str:
        return "</a></li>"
