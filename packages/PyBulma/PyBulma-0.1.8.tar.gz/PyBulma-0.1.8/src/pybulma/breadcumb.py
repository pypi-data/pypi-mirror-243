from base import BaseComponent
from .icon import Icon


class Breadcrumb(BaseComponent):
    """Parent class for Breadcrumbs
    """
    name = "breadcrumb"
    base_classes = ["breadcrumb"]

    def _pre_template(self):
        result = ["<nav", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append('aria-label="breadcrumbs">')
        result.append("<ul>")
        return " ".join(result)

    def _post_template(self):
        return "</ul></nav>"


class BreadcrumbItem(BaseComponent):
    """Breadcrumb item to be added to a breadcrumb parent object.

    Args:
        label: item text
        url: link url
    """
    name = "breadcrumb-item"
    base_classes = []

    def __init__(self, label: str, url: str = None, item_id: str = None,
                 styles: dict = None, attributes: dict = None, classes: list = None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.label = label
        self.url = url

    def _pre_template(self):
        result = ["<li"]
        if self.classes:
            result.append(self.classes)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append("<a")
        if self.id:
            result.append(self.id)
        if self.url:
            result.append(f'href="{self.url}"')
        else:
            result.append('href="#"')
        result.append(">")
        result.append(self.label)
        return " ".join(result)

    def _post_template(self):
        return "</a></li>"


class BreadcrumbIconItem(BaseComponent):
    """Breadcrumb item with an Icon,  to be added to a breadcrumb parent object.

    Args:
        label: item text
        icon: text string with the classes needed for the icon
        url: link url
    """
    name = "breadcrumb-icon-icon"
    base_classes = []

    def __init__(self, label: str, icon: Icon, url: str = None, item_id: str = None,
                 styles: dict = None, attributes=None, classes: list = None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.label = label
        self.icon = icon
        self.url = url

    def _pre_template(self):
        result = ["<li"]
        if self.classes:
            result.append(self.classes)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append("<a")
        if self.id:
            result.append(self.id)
        if self.url:
            result.append(f'href="{self.url}"')
        else:
            result.append('href="#"')
        result.append(">")
        result.append(self.icon.compile())
        result.append(f"<span>{self.label}</span>")

    def _post_template(self):
        return "</a></li>"
