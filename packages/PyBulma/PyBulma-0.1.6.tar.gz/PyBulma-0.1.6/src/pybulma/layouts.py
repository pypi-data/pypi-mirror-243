from base import BaseComponent


class Section(BaseComponent):
    """Bulma Section object, used to mark a section of a page"""
    name = "section"
    base_classes = ["section"]

    def _pre_template(self):
        result = ['<section', self.classes]
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


class Level(BaseComponent):
    """Bulma level object base

    A Bulma level object is a single row object that is designed to span its given container. Inside
    the level, you add left and right had container and then item in those containers.

    https://bulma.io/documentation/layout/level/

    """
    name = "level"
    base_classes = ["level"]

    def _pre_template(self):
        result = ["<nav", self.classes]
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


class LevelLeft(BaseComponent):
    """LevelLeft component for a level component. This object must be a child of a level component"""
    name = "level-left"
    base_classes = ["level-left"]

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


class LevelRight(BaseComponent):
    """LevelRight component for a Level component. This object must be a child of a Level component"""
    name = "level-right"
    base_classes = ["level-right"]

    def __init__(self, item_id: str = None, classes: list = None, styles: dict = None, attributes: dict = None):
        if not classes:
            classes = []
        classes.append("level-right")
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

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


class LevelItem(BaseComponent):
    """LevelItem.

    A level Item is a child of either Level, LevelLeft, or LevelRight. You must place
    child items into the LevelItem to create its contents. This is just a layout structure

    """
    name = "level-item"
    base_classes = ["level-item"]

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


class Media(BaseComponent):
    """Bulma Media Object Main.

    https://bulma.io/documentation/layout/media-object/

    """
    name = "media"
    base_classes = ["media"]

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


class MediaLeft(BaseComponent):
    name = "media-left"
    base_classes = ["media-left"]

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


class MediaContent(BaseComponent):
    name = "media-content"
    base_classes = ["media-content"]

    def __init__(self, content_id=None, styles=None, attributes=None, classes=None):
        super().__init__(item_id=content_id, styles=styles, attributes=attributes)

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


class Footer(BaseComponent):
    name = "footer"
    base_classes = ["footer"]

    def _pre_template(self):
        result = ["<footer", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")

    def _post_template(self):
        return "</footer>"


class Hero(BaseComponent):
    name = "hero"
    base_classes = "hero"

    def _pre_template(self):
        result = ["<section", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")

    def _post_template(self):
        return "</section>"


class HeroBody(BaseComponent):
    name = "hero-body"
    base_classes = "hero-body"

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

