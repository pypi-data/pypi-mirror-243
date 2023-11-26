from .base import BaseComponent


class NavBar(BaseComponent):
    name = "navbar"
    base_classes = ["nav_bar"]

    def _pre_template(self):
        result = ["<nav", self.classes, 'role="navigation"', 'aria-label="main navigation"']
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</nav>"


class NavBrand(BaseComponent):
    name = "nav-brand"
    base_classes = "nav-brand"

    def __init__(self, item_id=None, styles=None, attributes=None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes)

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
        return "</div>"


class NavBurger(BaseComponent):
    name = "nav-burger"
    base_classes = ["nav-burger"]

    def _pre_template(self):
        result = ['<a role="button" aria-label="menu" aria-expanded="false"']
        if self.classes:
            result.append(self.classes)
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append('>')
        result.append('<span aria-hidden="true"></span>')
        result.append('<span aria-hidden="true"></span>')
        result.append('<span aria-hidden="true"></span>')
        return " ".join(result)

    def _post_template(self):
        return "</a>"


class NavBarMenu(BaseComponent):
    name = "navbar-menu"
    base_classes = ["navbar-menu"]

    def _pre_template(self):
        result = ['<div', self.classes]
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</div>"


class NavBarMenuStart(BaseComponent):
    name = "navbar-menu-start"
    base_classes = ["navbar-start"]

    def _pre_template(self):
        result = ['<div']
        if self.id:
            result.append(self.id)
        if self.classes:
            result.append(self.classes)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</div>"


class NavBarMenuEnd(BaseComponent):
    name = "navbar-menu-end"
    base_classes = ["navbar-end"]

    def _pre_template(self):
        result = ['<div']
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
        return "</div>"


class NavBarItem(BaseComponent):
    name = "navbar-item"
    base_classes = ["navbar-item"]

    def __init__(self, item_id=None, styles=None, attributes=None, classes=None, url=None):
        super().__init__(styles=styles, attributes=attributes, item_id=item_id, classes=classes)
        self.url = url

    def _pre_template(self):
        result = ["<a", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        if self.url:
            result.append(f'href="{self.url}"')
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</a>"


class NavBarItemDropdown(BaseComponent):
    name = "navbar-item-dropdown"
    base_classes = ["navbar-item", "has-dropdown", "is-hoverable"]

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


class NavBarLink(BaseComponent):
    name = "navbar-link"
    base_classes = ["navbar-link"]

    def _pre_template(self):
        result = ["<a", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</a>"


class NavBarDropdownDivider(BaseComponent):
    name = "navbar-dropdown-divider"
    base_classes = "navbar-divider"

    def _pre_template(self):
        result = ["<hr", self.classes]
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return ""
