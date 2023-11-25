from base import BaseComponent


class Card(BaseComponent):
    """Card component card

    """
    name = "card"
    base_classes = ["card"]

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
    

class CardHeader(BaseComponent):
    """Header component for a card. Must be inside a Card object

    """
    name = "card-header"
    base_classes = ["card-header"]
    
    def _pre_template(self):
        result = ['<header', self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</header>"


class CardHeaderTitle(BaseComponent):
    """Card header title component. Must be placed inside a CardHeader object

    Args:
        title: title text
    """
    name = "card-header-title"
    base_classes = ["card-header-title"]

    def __init__(self, title: str, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.title = title

    def _pre_template(self):
        result = ["<p", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(self.title)
        return " ".join(result)

    def _post_template(self):
        return "</p>"


class CardHeaderIcon(BaseComponent):
    """Adds a header icon object to the Card Header. Must be a child of the
    CardHeader.

    Args:
        icon: string of space delimited icon classes

    """
    name = "card-header-icon"
    base_classes = ["card-header-icon"]

    def __init__(self, icon: str, item_id: str = None, classes: list = None,
                 styles: dict = None, attributes: dict = None):
        self.icon = icon
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self):
        result = ["<button", self.classes]
        if self.id:
            result.append([self.id])
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append('<span class="icon">')
        result.append(f'<i class="{self.icon}"></i>')
        result.append("</span>")
        return " ".join(result)

    def _post_template(self):
        return "</button>"


class CardImage(BaseComponent):
    """adds a card Image object to a card. Must be a child of a Card object

    """
    name = "card-image"
    base_classes = ["card_image"]

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
        return '</div>'


class CardContent(BaseComponent):
    """Content object for a Card. Must be a child of a Card Object"""
    name = "card-content"
    base_classes = ["card-content"]

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


class CardFooter(BaseComponent):
    """Footer object for a Card. Must be a child of a Card object"""
    name = "card-footer"
    base_classes = ["card-footer"]

    def _pre_template(self):
        result = ["<footer", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</footer>"


class CardFooterItem(BaseComponent):
    """Card Footer Item. Must be a child of a CardFooter Object

    Args:
        item_text: Text for the item link
        item_url: url for the link
    """
    name = "card-footer-item"
    base_classes = ["card-footer-item"]

    def __init__(self, item_id: str = None, item_text: str = None, item_url: str = None,
                 styles: dict = None, attributes: dict = None, classes: list = None):
        self.item_text = item_text
        if item_url:
            self.url = f'href="{item_url}"'
        else:
            self.url = 'href="#"'
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self):
        result = ["<a", self.classes, self.url]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        if self.item_text:
            result.append(str(self.item_text))
        return " ".join(result)

    def _post_template(self):
        return "</a>"
