from base import BaseComponent
from icon import Icon


class FileContainer(BaseComponent):
    name = "file container"
    base_classes = ["file"]

    def _pre_template(self):
        result = ["<div", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        if self.classes:
            result.append(self.classes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</div>"


class FileLabel(BaseComponent):
    name = "file label"
    base_classes = ["file-label"]

    def _pre_template(self):
        result = ["<label", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        if self.classes:
            result.append(self.classes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</label>"


class FileInput(BaseComponent):
    name = "file input"
    base_classes = ["file-input"]

    def __init__(self, name: str, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None):
        self.name = f'name="{name}"'
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    def _pre_template(self):
        result = ["<input", self.name, self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return ""


class FileCTA(BaseComponent):
    name = "file cta"
    base_classes = ["file-cta"]

    def _pre_template(self):
        result = ["<span", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</span>"


class FileIcon(Icon):
    name = "fileIcon"
    base_classes = ["file-icon"]


class FileLabelSpan(FileLabel):

    def _pre_template(self):
        result = ["<span", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        if self.classes:
            result.append(self.classes)
        result.append(">")
        return " ".join(result)

    def _post_template(self):
        return "</span>"


class FileName(FileLabelSpan):
    name = "file name"
    base_classes = ["file-name"]
