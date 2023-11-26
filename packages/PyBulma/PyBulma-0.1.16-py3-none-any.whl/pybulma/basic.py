from .base import BaseComponent
from typing import Union


class HtmlTag(BaseComponent):
    """
    Creates an HTML tag component
    """
    name = "html_tag"
    base_classes = []

    def __init__(self, tag: str, item_id: str = None, styles: dict = Union[dict, None], classes: list = None,
                 attributes: dict = Union[dict, None]) -> None:
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.tag = tag

    def _pre_template(self):
        result = [f"<{self.tag}"]
        if self.classes:
            result.append(self.classes)
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        result.append(">")
        return " ".join(result)

    def _post_template(self) -> str:
        """
        Add the ending tags to the html code

        """
        return f"</{self.tag}>"


class NoTag(BaseComponent):
    """
    NoTag component class. Adds no tags, attributes, classes, id, or styles
    """
    name = "NoTag"
    base_classes = []

    def __init__(self):
        super().__init__(item_id=None, styles=None, attributes=None, classes=None)

    def _pre_template(self):
        return ""

    def _post_template(self):
        return ""
