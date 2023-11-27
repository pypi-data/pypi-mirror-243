from .base import BaseComponent
from typing import Union


class Table(BaseComponent):
    name = "table"
    base_classes = ["table"]

    def _pre_template(self) -> str:
        result = ["<table", self.classes]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        return " ".join(result)

    def _post_template(self) -> str:
        return "</table>"


class TableHead(BaseComponent):
    name = "table_header"
    base_classes = []

    def _pre_template(self) -> str:
        result = ["<thead"]
        if self.id:
            result.append(self.id)
        if self.classes:
            result.append(self.classes)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        if self.classes:
            result.append(self.classes)
        result.append("><tr>")
        return " ".join(result)

    def _post_template(self) -> str:
        return "</tr><thead>"


class TableFoot(BaseComponent):
    name = "table_footer"
    base_classes = []

    def _pre_template(self) -> str:
        result = ["<tfoot"]
        if self.id:
            result.append(self.id)
        if self.classes:
            result.append(self.classes)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append("><tr>")
        return " ".join(result)

    def _post_template(self) -> str:
        return "</tr><tfoot>"


class HeaderCell(BaseComponent):
    name = "header_footer_cell"
    base_classes = []

    def __init__(self, cell_text: str, abbr: str = None, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None):
        super().__init__(styles=styles, attributes=attributes, item_id=item_id, classes=classes)
        self.text = cell_text
        self.abbr = abbr

    def _pre_template(self) -> str:
        result = ["<th"]
        if self.id:
            result.append(self.id)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        if self.classes:
            result.append(self.classes)
        result.append(">")
        if self.abbr:
            result.append(f'<abbr title="{self.text}">{self.abbr}</abbr>')
        else:
            result.append(self.text)
        return " ".join(result)

    def _post_template(self) -> str:
        return "</th>"


class TableBody(BaseComponent):
    name = "table_body"
    base_classes = []

    def __init__(self, data_variable: str = "table_data", row_variable: str = "row",
                 item_id: str = None, styles: dict = None, attributes: dict = None, classes: list = None) -> None:
        super().__init__(styles=styles, attributes=attributes, classes=classes, item_id=item_id)
        if not isinstance(data_variable, str):
            raise ValueError("""TableBody: data_variable must be a string representing the 
            variable that will hold the data to be rendered""")
        self.data_variable = data_variable
        if not isinstance(row_variable, str):
            raise ValueError("""TableBody: row_vaiable must be a string representing the 
            variable that will hold each row to be rendered""")
        self.row_variable = row_variable

    def _pre_template(self) -> str:
        result = ["<tbody"]
        if self.id:
            result.append(self.id)
        if self.classes:
            result.append(self.classes)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        result.append("{% for " + self.row_variable + " in " + self.data_variable + " %}")
        return " ".join(result)

    def _post_template(self) -> str:
        return "{% endfor %}</tbody>"


class TableRow(BaseComponent):
    name = "table_row"
    base_classes = []

    def _pre_template(self) -> str:
        result = ["<tr"]
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

    def _post_template(self) -> str:
        return "</tr>"


class TableCell(BaseComponent):
    name = "table_cell"
    base_classes = []

    def __init__(self, cell_content: Union[str | int] = None, item_id: str = None, styles: dict = None,
                 attributes: dict = None, classes: list = None) -> None:
        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)
        self.cell_content = cell_content

    def _pre_template(self) -> str:
        result = ["<td"]
        if self.id:
            result.append(self.id)
        if self.classes:
            result.append(self.classes)
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        if self.cell_content:
            result.append(self.cell_content)
        return " ".join(result)

    def _post_template(self) -> str:
        return "</td>"
