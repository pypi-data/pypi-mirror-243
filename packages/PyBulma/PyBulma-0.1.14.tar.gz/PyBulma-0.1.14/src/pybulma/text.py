from .base import BaseComponent


class TextSpan(BaseComponent):
    name = "text_span"
    base_classes = []

    def __init__(self, text, item_id=None, styles=None, classes=None, attributes=None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.text = text

    def _pre_template(self):
        result = ["<span"]
        if self.styles:
            result.append(self.styles)
        if self.classes:
            result.append(f'class="{self.classes}"')
        result.append(">")
        result.append(self.text)
        return " ".join(result)

    def _post_template(self):
        return "</span>"


class TextP(BaseComponent):
    name = "text_p"
    base_classes = []

    def __init__(self, text, item_id=None, styles=None, classes=None, attributes=None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.text = text

    def _pre_template(self):
        result = ["<p"]
        if self.styles:
            result.append(self.styles)
        if self.classes:
            result.append(f'class="{self.classes}"')
        result.append(">")
        result.append(self.text)
        return " ".join(result)

    def _post_template(self):
        return "</p>"


class TextTitle(BaseComponent):
    name = "text-title"
    base_classes = ["title"]

    def __init__(self, tag="p", text=None,  item_id=None, styles=None, attributes=None, classes=None):
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.text = text
        self.title_tag = f"<{tag}"
        self.title_end_tag = f"</{tag}>"

    def _pre_template(self):
        result = [self.title_tag, self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        if self.text:
            result.append(self.text)
        return " ".join(result)

    def _post_template(self):
        return self.title_end_tag


class TextSubtitle(BaseComponent):
    name = "text-subtitle"
    base_classes = "subtitle"

    def __init__(self, tag="p", item_id=None, text=None, styles=None, attributes=None, classes=None):
        super().__init__(item_id, styles=styles, attributes=attributes, classes=classes)
        self.text = text
        self.title_tag = f"<{tag}"
        self.title_end_tag = f"</{tag}>"

    def _pre_template(self):
        result = [self.title_tag, self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        if self.text:
            result.append(self.text)
        return " ".join(result)

    def _post_template(self):
        return self.title_end_tag


