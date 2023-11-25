from .base import BaseComponent


class Page(BaseComponent):
    name = "html page"
    base_classes = []

    def __init__(self, load_static: bool = True, attributes: dict = None):
        self.load_static = load_static
        super().__init__(attributes=attributes)

    def _pre_template(self):
        if self.load_static:
            result = ["{% load static %}", "<!DOCTYPE html>", "<html"]
        else:
            result = ["<!DOCTYPE html>", "<html"]
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</html>"


class Head(BaseComponent):
    name = "html head"
    base_classes = []

    def _pre_template(self):
        return "<head>"

    def _post_template(self):
        return "</head>"


class Meta(BaseComponent):
    name = "html meta"
    base_classes = []

    def _pre_template(self):
        result = ["<meta"]
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return ""


class Title(BaseComponent):
    name = "html title"
    base_classes = []

    def __init__(self, title_text):
        self.title_text = title_text
        super().__init__()

    def _pre_template(self):
        return f"<title>{self.title_text}"

    def _post_template(self):
        return "</title>"


class Body(BaseComponent):
    name = "html body"
    base_classes = []

    def _pre_template(self):
        result = ["<body"]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</body>"
