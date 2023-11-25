from base import BaseComponent


class ContentContainer(BaseComponent):
    """Bulma Content Component Object"""
    name = "content_container"
    base_classes = ["content"]

    def _pre_template(self):
        result = ["</div", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " "

    def _post_template(self):
        return "</div>"


class BoxContainer(BaseComponent):
    """Bulma Box Component """
    name = "box_container"
    base_classes = ["box"]

    def _pre_template(self):
        result = ["</div", self.classes]
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


class BlockContainer(BaseComponent):
    """Bulma Block component"""
    name = "BlockContainer"
    base_classes = ["block"]

    def _pre_template(self) -> str:
        result = ["<div", self.classes]
        if self.id:
            result.append(self.id)
        if self.attributes:
            result.append(self.attributes)
        if self.styles:
            result.append(self.styles)
        result.append(">")
        return " ".join(result)

    def _post_template(self) -> str:
        return "</div>"
