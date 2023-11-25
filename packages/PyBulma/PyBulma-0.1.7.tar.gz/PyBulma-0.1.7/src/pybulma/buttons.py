from base import BaseComponent
from abc import abstractmethod
from .icon import Icon


class ButtonBase(BaseComponent):
    """Base Abstract class for Buttons

    Args:
        button_text: text to be placed on the button
        icon: icon Object to be placed on the button
    """

    def __init__(self, item_id: str, button_text: str = None, classes: list = None, icon: Icon = None,
                 styles=None, attributes=None, disabled=False):
        self.button_text = button_text
        self.icon = icon
        self.disabled = disabled

        super().__init__(item_id=item_id, styles=styles, attributes=attributes, classes=classes)

    @abstractmethod
    def _pre_template(self):
        pass

    @abstractmethod
    def _post_template(self):
        pass


class ButtonLink(ButtonBase):
    """Button made from an anchor tag

    Args:
        url: link url
        item_id: html id
        button_text: text placed on the button
        icon: Icon Component Object
        classes: optional classes for the button
        styles: dictionary of styles
        attributes: dictionary of additional attributes

    Optional Classes:
        * is-primary
        * is-link
        * is-info
        * is-success
        * is-warning
        * is-danger
        * is-white
        * is-light
        * is-dark
        * is-black
        * is-text
        * is-ghost
        * is-small
        * is-medium
        * is-normal
        * is-large
        * is-responsive
        * is-fullwidth
        * is-outlined
        * is-inverted
        * is rounded
        * is-hovered
        * is-focused
        * is-active
        * is-loading
        * is-static


    """
    name = "button_link"
    base_classes = ["button"]

    def __init__(self, url: str, item_id: str, button_text: str = None, disabled=False,
                 classes: list = None, styles: str = None, icon: Icon = None, attributes: dict = None):
        super().__init__(item_id=item_id, button_text=button_text, classes=classes,
                         styles=styles, icon=icon, attributes=attributes, disabled=disabled)
        self.url = f'href="{url}"'

    def _pre_template(self):
        result = ['<a', self.classes, self.url]
        if self.disabled:
            result.append('disabled="disabled"')
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        if self.icon:
            result.append(self.icon.compile())
        if self.button_text and self.icon:
            result.append(f'</span>{self.button_text}</span>')
        elif self.button_text and not self.icon:
            result.append(self.button_text)
        return " ".join(result)

    def _post_template(self):
        return "</a>"


class ButtonInput(ButtonBase):
    """Button made from an input tag

    Args:
        icon: Icon Object
        button_type: submit/cancel etc
        disabled: boolean value to set the disabled attribute

    """
    name = "button-input"
    base_classes = ["button"]

    def __init__(self, item_id: str, button_type: str, button_text: str = None, disabled: bool = False,
                 classes: list = None, styles: dict = None, icon: Icon = None, attributes: dict = None):
        super().__init__(item_id=item_id, button_text=button_text, disabled=disabled,
                         classes=classes, styles=styles, icon=icon, attributes=attributes)

        self.type = f'type="{button_type}"'

    def _pre_template(self):
        result = ["<input ", self.type, self.classes]
        if self.disabled:
            result.append('disabled="disabled"')
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(f'value="{self.button_text}">')
        return " ".join(result)

    def _post_template(self):
        return ""


class Button(ButtonBase):
    """Button made from a button tag

    Args:
        url: link url
        button_text: text placed on the button
        icon: icon classes

    """
    name = "button"
    base_classes = ["button"]

    def _pre_template(self):
        result = ['<button', self.classes]
        if self.disabled:
            result.append('disabled="disabled"')
        if self.styles:
            result.append(self.styles)
        if self.attributes:
            result.append(self.attributes)
        result.append(">")
        if self.icon:
            result.append(self.icon.compile())
        if self.button_text and self.icon:
            result.append(f'</span>{self.button_text}</span>')
        elif self.button_text and not self.icon:
            result.append(self.button_text)
        return " ".join(result)

    def _post_template(self):
        return "</button>"


class ButtonGroup(BaseComponent):
    """A wrapper class for one or more button objects using the 'is-grouped' class.

    ButtonGroup and Buttons are very similar in nature. This component however wraps all child objects
    in a control object

    """
    name = "button_group"
    base_classes = ["field", "is-grouped"]

    def compile(self):
        results = [self._pre_template()]
        for x in self._sub_components:
            results.append(f'<p class="control">')
            results.append(x.compile())
            results.append("</control>")
        results.append(self._post_template())

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


class ButtonAddon(BaseComponent):
    """A wrapper class for one or more button objects using the 'has-addons' class. This
    works the same as a ButtonGroup object, wrapping reach button in a control object,
    but the buttons are formatted differently

    """
    name = "button_addon"
    base_classes = ["field", "has-addons"]

    def compile(self):
        results = [self._pre_template()]
        for x in self._sub_components:
            results.append(f'<p class="control">')
            results.append(x.compile())
            results.append("</control>")
        results.append(self._post_template())

    def _pre_template(self):
        result = ['<div class="field has-addons"']
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


class Buttons(BaseComponent):
    """Buttons component. Wrapper for multiple button objects. This looks similar to a button group
    but it allows wrapping and does not have control objects wrapping the buttons. Adding 'has-addons'
    as a class, make this duplicate the ButtonAddons object

    Optional Classes:
        * are-small
        * are-medium
        * are-large


    """
    name = "buttons"
    base_classes = ["buttons"]

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
