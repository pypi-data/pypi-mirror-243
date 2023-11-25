from .base import BaseComponent
from .buttons import Button
from .icon import Icon


class Dropdown(BaseComponent):
    """Parent component for a Bulma Dropdown component. A dropdown trigger and dropdown menu component
    must be added a children of this component"""
    name = "dropdown"
    base_classes = ["dropdown"]
    
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


class DropdownTrigger(BaseComponent):
    """Dropdown Trigger component. This is the element that is hovered over to display the
    dropdown menu items. The icon parameter is used to define the icon used on the button. The default
    is a down arrow

    Args:
        button_text: text for the trigger button
        menu_id: html id of the dropdown menu component
        icon: Icon object representing the Icon used on the trigger. Default is fa-angle-down
    """
    name = "dropdown-trigger"
    base_classes = ["dropdown-trigger"]

    def __init__(self, button_text: str, menu_id: str, item_id: str = None, icon: Icon = None, styles: dict = None,
                 attributes: dict = None, classes: list = None) -> None:
        if not attributes:
            attributes = {}
        attributes["aria-haspopup"] = "true"
        attributes["aria-controls"] = menu_id
        if not icon:
            icon = Icon(icon_class="fas fa-angle-down")
        button = Button(item_id=item_id, button_text=button_text,
                        icon=icon, classes=classes, attributes=attributes, styles=styles)
        self.sub_components.append(button)

        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

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


class DropdownMenu(BaseComponent):
    """Dropdown menu Component. Warning. item_id is required for his object

    Args:
        item_id: required id for the menu component
    """
    name = "dropdown-menu"
    base_classes = ["dropdown-menu"]

    def _pre_template(self) -> str:
        result = ["<div", self.classes, self.id, 'role="menu"']
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self) -> str:
        return "</div>"


class DropdownContent(BaseComponent):
    """Content object that is placed inside the DropdownMenu object"""
    name = "dropdown-content"
    base_classes = "dropdown-content"

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


class DropdownItemLink(BaseComponent):
    """Dropdown Menu Link Item. This is a menu link item that is to be placed in the dropdown content object

    "url" is optional as the menu item can be linked to a script via the item_id

    Args:
        item_text: text of the menu item
        url: url for the anchor
    """
    name = "dropdown-item-link"
    base_classes = ["dropdown-item"]

    def __init__(self, item_text: str, item_id: str = None, url: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None) -> None:
        self.text = item_text
        if url:
            self.url = f'href="{url}'
        else:
            self.url = f'href="#"'
        super().__init__(item_id=item_id, styles=styles, attributes=attributes)

    def _pre_template(self) -> str:
        result = ["<a", self.classes, self.url]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append(self.text)
        return " ".join(result)

    def _post_template(self) -> str:
        return "</a>"


class DropdownItem(BaseComponent):
    """Dropdown Menu Item. This item allows you to place any content you like in
    div tags. this can be text, or icons or something else. It will not try
    to compile the content, so don't place PyBulma objects in the content, unless
    it's the compiled results

    If you wish to add PyBulma components to this, then add them as child objects and
    set contents to blank

    Args:
        content: string containing the html content for this item

    """
    name = "dropdown_item"
    base_classes = ["dropdown-item"]

    def __init__(self, content: str = "", item_id=None, classes=None, styles=None, attributes=None):
        self.content = content
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self) -> str:
        result = ["<div", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append(self.content)
        return " ".join(result)

    def _post_template(self) -> str:
        return "</div>"


class DropdownDivider(BaseComponent):
    """Dropdown menu divider item"""
    name = "dropdown-divider"
    base_classes = ["dropdown-divider"]

    def _pre_template(self) -> str:
        result = ['<hr', self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self) -> str:
        return ""
