from base import BaseComponent


class Figure(BaseComponent):
    """Bulma figure component. This is to be used as a parent class to an image object

    Args:
        image_class: Bulma image avatar class

    Image class Options:
        * is-16x16
        * is-24x24
        * is-48x48
        * is-64x64
        * is-96x96
        * is-128x128


    """
    name = "figure"
    base_classes = ["image"]

    def __init__(self, image_class, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None):
        if not classes:
            classes = []
        classes.append(image_class)
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self):
        result = ["<figure", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</figure>"


class Image(BaseComponent):
    """Image component. This added a '<img>' tag. it should not have any child compoments

    Args:
        image_src: url end point for the image
    """
    name = "image"
    base_classes = []

    def __init__(self, image_src: str, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None):
        self.image_src = image_src
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self):
        result = ["<img"]
        if self.id:
            result.append(self.id)
        if self.classes:
            result.append(self.classes)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(f'src="{self.image_src}"')
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return ""
