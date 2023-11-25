from abc import ABC, abstractmethod
from typing import Union
from typing_extensions import Self
from pathlib import Path
import os
import bs4
from exceptions import PreTemplateError, PostTemplateError, PrettifyError


class BaseComponent(ABC):
    """
    Abstract class used for all Pybulma classes
    """

    def __init__(self, item_id: Union[str, None] = None,
                 styles: Union[dict, None] = None,
                 attributes: Union[dict, None] = None,
                 classes: Union[list, None] = None) -> None:
        """Base Abstract class for PyBulma

        Args:
            item_id: ID attribute on the html item
            styles: Dictionary of style parameters
            attributes: dictionary of html attributes

        """
        self._sub_components = []
        self._macro = ""
        if styles:
            if not isinstance(styles, dict):
                raise ValueError("ComponentClass: Styles must be a dictionary")
            self.styles = self._build_styles(styles)
        else:
            self.styles = styles
        if attributes:
            if not isinstance(attributes, dict):
                raise ValueError("ComponentClass: Attributes must be a dictionary")
            self.attributes = self._build_attributes(attributes)
        else:
            self.attributes = attributes
        if not isinstance(self.base_classes, list):
            raise ValueError("Component_class: base_classes must be a list")

        self.id = self._build_id(item_id)
        class_list = self.base_classes
        if classes:
            class_list.extend(classes)
        class_text = " ".join(class_list)
        self.classes = f'class="{class_text}"'

    @property
    def sub_components(self) -> list:
        """
        list: list of PyBulma objects to be placed inside this html item
        """
        return self._sub_components

    def add_component(self, obj: Self) -> bool:
        """
        Adds a Pybulma object to the subcomponents

        Args:
            obj: PyBulma Object

        Returns:

        """
        self._sub_components.append(obj)
        return True

    def remove_component(self, index: int) -> bool:
        """
        Removes a component object from the subcomponent list

        Args:
            index: index number of the component in the list

        Returns:

        """
        try:
            del self._sub_components[index]
            return True
        except:
            return False

    @property
    @abstractmethod
    def name(self):
        """str: Name of the component"""
        pass

    @property
    @abstractmethod
    def base_classes(self):
        """list: list of default classes for the object"""

    @staticmethod
    def _build_styles(styles) -> str:
        """
        converts the dictionary of style attributes into the html style attribute
        Args:
            styles: Dictionary of Style parameters

        Returns:

        """
        res = []
        for k, v in styles.items():
            res.append(f"{k}:{v}")
        return f'style="{";".join(res)}"'

    @staticmethod
    def _build_attributes(attributes) -> str:
        """
        converts a dictionary of attributes into a set of html attributes to be added to the html tag
        Args:
            attributes:

        Returns:

        """
        res = []
        for k, v in attributes.items():
            res.append(f'{k}="{v}"')
        return " ".join(res)

    @staticmethod
    def _build_id(item_id: str):
        """
        Create the ID parameter to be added to the html tag
        Args:
            item_id: html id value

        Returns:

        """
        if item_id:
            return f'id="{item_id}"'
        else:
            return None

    def compile(self) -> str:
        """
        Renders and returns the html for the give Pybulma object

        Returns:
           rendered html

        """
        try:
            results = [self._pre_template()]
        except Exception as e:
            raise PreTemplateError(self.name, e.__str__())
        for x in self._sub_components:
            results.append(x.compile())
        try:
            results.append(self._post_template())
        except Exception as e:
            raise PostTemplateError(self.name, e.__str__())
        try:
            res = bs4.BeautifulSoup(" ".join(results), "html.parser").prettify()
        except Exception as e:
            raise PrettifyError(self.name, e.__str__())
        return res

    @abstractmethod
    def _pre_template(self):
        pass

    @abstractmethod
    def _post_template(self):
        pass

    def save(self, filename: str):
        """
        Renders the html and saves it to a file

        Args:
            filename: name and path of the file to be created

        Returns:

        """
        with open(filename, "w") as f:
            f.writelines(self.compile())


class Compile(ABC):
    """Abstract Compile Command"""

    @property
    @abstractmethod
    def path(self):
        """directory path to where the compiled templates should be written to"""
        pass

    def __init__(self, base_dir):
        self.components = {}
        full_path = os.path.join(base_dir, self.path)
        Path(full_path).mkdir(parents=True, exist_ok=True)
        self.build()

    def add_component(self, name: str, obj: BaseComponent) -> bool:
        self.components[name] = obj.compile()
        return True

    def remove_component(self, name: str) -> bool:
        if name in self.components:
            del self.components[name]
        return True

    def compile(self):
        for k, v in self.components.items():
            filename = f"{self.path}/{k}.html.jinja"
            with open(filename, "w") as f:
                f.writelines(v)

    @abstractmethod
    def build(self):
        pass




