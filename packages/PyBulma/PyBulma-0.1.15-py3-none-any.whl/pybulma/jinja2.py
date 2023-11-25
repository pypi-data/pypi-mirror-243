from .base import BaseComponent


class LogicIf(BaseComponent):
    name = "if"
    base_classes = []

    def __init__(self, logic: str) -> None:
        super().__init__(item_id=None, styles=None, attributes=None, classes=None)
        self.logic = logic

    def _pre_template(self) -> str:
        start = "{% if "
        end = " %}"
        return start + self.logic + end

    def _post_template(self) -> str:
        return "{% endif %}"


class LogicFor(BaseComponent):
    name = "for"
    base_classes = []

    def __init__(self, logic: str) -> None:
        super().__init__(item_id=None, attributes=None, styles=None, classes=None)
        self.logic = logic

    def _pre_template(self) -> str:
        start = "{% for "
        end = " %}"
        return start + self.logic + end

    def _post_template(self) -> str:
        return "{% endfor %}"


class Jinja2Block(BaseComponent):
    name = "jinja2-block"
    base_classes = []

    def __init__(self, block: str) -> None:
        super().__init__(item_id=None, styles=None, attributes=None, classes=None)
        self.block = block

    def _pre_template(self) -> str:
        return "{% block " + self.block + " %}"

    def _post_template(self) -> str:
        return "{% endblock %}"


class Jinja2Adhoc(BaseComponent):
    name = "jinja2-adhoc"
    base_classes = []

    def __init__(self, template_line: str) -> None:
        super().__init__(item_id=None, styles=None, attributes=None, classes=None)
        self.template_line = template_line

    def _pre_template(self) -> str:
        return self.template_line

    def _post_template(self) -> None:
        return ""


class StaticScriptLoad(BaseComponent):
    name = "static script load"
    base_classes = []

    def __init__(self, script_type: str = "text/javascript", item_id: str = None, src: str = None) -> None:
        self.type = f'type="{script_type}"'
        static_src = "{% static '" + src + "' %}"
        self.src = f'src="{static_src}"'
        super().__init__(item_id=item_id, styles=None, attributes=None, classes=None)

    def _pre_template(self) -> str:
        result = ["<script", self.type, self.src]
        if self.id:
            result.append(self.id)
        result.append(">")
        return " ".join(result)

    def _post_template(self) -> str:
        return "</script>"


class StaticCSSLoad(BaseComponent):
    name = "static script load"
    base_classes = []

    def __init__(self, rel: str = "stylesheet", src: str = None) -> None:
        self.rel = f'rel="{rel}"'
        static_src = "{% static '" + src + "' %}"
        self.src = f'src="{static_src}"'
        super().__init__(item_id=None, styles=None, attributes=None, classes=None)

    def _pre_template(self) -> str:
        result = ["<script", self.src, self.rel, ">"]
        return " ".join(result)

    def _post_template(self) -> str:
        return ""
