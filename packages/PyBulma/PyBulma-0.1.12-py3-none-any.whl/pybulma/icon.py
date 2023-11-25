from .base import BaseComponent


class Icon(BaseComponent):
    """Bulma Icon component

    it should be noted that the id, attributes, styles, and additionclasses are applied to the surrounding <span> tag
    and not the <i> tag.

    Args:
        icon_class: this should contain the two classes needed to identify the icon. Example "fas fa-arrow-up"

    """
    name = "icon"
    base_classes = ["icon"]

    def __init__(self, icon_class: str, item_id: str = None, styles: dict = None,
                 classes: list = None, attributes: dict = None):
        self.icon_class = icon_class
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self):
        result = ["<span", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append(f'<i {self.icon_class}></i>')
        return " ".join(result)

    def _post_template(self):
        return "</span>"


class IconText(BaseComponent):
    """Bulma Icon Text wrapper

    This object wraps a span tag around an icon object, attaching text and formatting to the text and child icon.
    An Icon object should be placed as a child of this component

    """
    name = "icon_text"
    base_classes = "icon-text"

    def __init__(self, item_text: str, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None):
        self.item_text = item_text
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self):
        result = ['<div', self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        result = ["<span>", self.item_text, "</span>", "</div>"]
        return " ".join(result)

