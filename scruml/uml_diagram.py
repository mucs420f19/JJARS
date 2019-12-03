# ScrUML
# uml_diagram.py
# Team JJARS
from typing import Dict
from typing import FrozenSet
from typing import List
from typing import Optional
from typing import Tuple

import yaml

ClassPair = Tuple[str, str]
AttributeDict = Dict[str, str]

# ----------
# UMLDiagram class

# TODO: Change return types, they are causing issues


class UMLDiagram:
    """Interactive model representing a UML diagram containing relationships and classes with attributes."""

    # ----------
    # Constructor

    def __init__(self) -> None:
        self.__classes: Dict[str, AttributeDict] = dict()
        self.__relationships: Dict[ClassPair, AttributeDict] = dict()

    # ----------
    # Class functions

    # ----------
    # add_class

    def add_class(self, class_name: str) -> bool:
        """Adds a class with name 'class_name' to the diagram.
Fails if a class with 'class_name' is already present in the diagram.
Returns 'True' on success, or 'False' on failure."""

        if class_name in self.__classes:
            return False

        self.__classes[class_name] = dict()

        return True

    # ----------
    # remove_class

    def remove_class(self, class_name: str) -> bool:
        """Removes the class with name 'class_name' from the diagram.
Fails if a class with 'class_name' is not present in the diagram.
Returns 'True' on success, or 'False' on failure."""

        if class_name not in self.__classes:
            return False

        del self.__classes[class_name]

        # Remove any relationship that might refer to this class
        self.__relationships = {
            class_pair: attributes
            for class_pair, attributes in self.__relationships.items()
            if class_name not in class_pair
        }

        return True

    # ----------
    # get_all_class_names

    def get_all_class_names(self) -> List[str]:
        """Returns a 'List[str]' containing the name of every class in the diagram."""

        return list(self.__classes.keys())

    # ----------
    # rename_class

    def rename_class(self, old_class_name: str, new_class_name: str) -> bool:
        """Renames the class with name 'old_name' to 'new_name' in the diagram.
Fails if a class with 'old_name' is not present in the diagram or a class with 'new_name' already exists in the diagram.
Returns 'True' on success or 'False' on failure."""

        if old_class_name not in self.__classes or new_class_name in self.__classes:
            return False

        self.__classes[new_class_name] = self.__classes.pop(old_class_name)

        # Update all relationships that refer to this class
        for class_pair in self.__relationships:
            if old_class_name in class_pair:
                new_class_pair: Tuple[str, str] = (
                    class_pair[0]
                    if class_pair[0] != old_class_name
                    else new_class_name,
                    class_pair[1]
                    if class_pair[1] != old_class_name
                    else new_class_name,
                )
                self.__relationships[new_class_pair] = self.__relationships.pop(
                    class_pair
                )

        return True

    # ----------
    # Class attribute functions

    # ----------
    # set_class_attribute

    def set_class_attribute(
        self, class_name: str, attribute_name: str, attribute_value: str
    ) -> bool:
        """Sets the value of 'attribute_name' to 'attribute_value' for the class with name 'class_name' in the diagram.
If the class does not yet have an attribute with the name 'attribute_name', one will be created.
Fails if a class with 'class_name' is not present in the diagram.
Returns 'True' on success, or 'False' on failure."""

        if class_name not in self.__classes:
            return False

        self.__classes[class_name][attribute_name] = attribute_value

        return True

    # ----------
    # remove_class_attribute

    def remove_class_attribute(self, class_name: str, attribute_name: str) -> bool:
        """Removes the attribute with name 'attribute_name' from class 'class_name'.
Fails if an attribute with 'attribute_name' is not found in 'class_name'.
Fails if a class with 'class_name' is not present in the diagram.
Returns 'True' on success, or 'False' on failure."""

        if (
            class_name not in self.__classes
            or attribute_name not in self.__classes[class_name]
        ):
            return False

        del self.__classes[class_name][attribute_name]

        return True

    # ----------
    # get_class_attributes

    def get_class_attributes(self, class_name: str) -> Optional[AttributeDict]:
        """Returns a Dict[str, str] containing the attribute names and values for class 'class_name'.
Fails and returns 'None' if a class with 'class_name' is not present in the diagram."""

        if class_name not in self.__classes:
            return None

        return self.__classes[class_name]

    # ----------
    # Relationship functions

    # ----------
    # __resolve_class_pair

    def __resolve_class_pair(self, class_name_a: str, class_name_b: str) -> ClassPair:
        """Returns (class_name_b, class_name_a) if that key exists as a pair in the diagram.
Otherwise, returns (class_name_a, class_name_b)."""

        class_pair: ClassPair = (class_name_a, class_name_b)

        # If the reverse of the current pair exists already, just use that
        if (class_name_b, class_name_a) in self.__relationships:
            class_pair = (class_name_b, class_name_a)

        return class_pair

    # ----------
    # add_relationship

    def add_relationship(self, class_name_a: str, class_name_b: str) -> bool:
        """Adds a relationship between the classes 'class_name_a' and 'class_name_b' to the diagram.
Fails if a relationship between the classes 'class_name_a' and 'class_name_b' is already present in the diagram.
Returns 'True' on success, or 'False' on failure."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_name_a == class_name_b
            or class_pair in self.__relationships
        ):
            return False

        if class_pair not in self.__relationships:
            self.__relationships[class_pair] = {}

        self.__relationships[class_pair] = {}

        return True

    # ----------
    # remove_relationship

    def remove_relationship(self, class_name_a: str, class_name_b: str) -> bool:
        """Removes the relationship between the classes 'class_name_a' and 'class_name_b' from the diagram.
Fails if a relationship between the classes 'class_name_a' and 'class_name_b' is not present in the diagram.
Returns 'True' on success, or 'False' on failure."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
        ):
            return False

        del self.__relationships[class_pair]

        return True

    # ----------
    # get_relationship_between

    def get_relationship_between(
        self, class_name_a: str, class_name_b: str
    ) -> Optional[AttributeDict]:
        """Returns a Dict[str, str] containing all relationship attributes between 'class_name_a' and 'class_name_b'.
Fails if class 'class_name_a' or class 'class_name_b' is not present in the diagram.
Fails if a relationship between 'class_name_a' and 'class_name_b' does not exist.
Returns 'None' on failure."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
        ):
            return None

        return self.__relationships[class_pair]

    # ----------
    # get_all_relationship_pairs

    def get_all_relationship_pairs(self) -> List[ClassPair]:
        """Returns a 'List[Tuple[str, str]]' containing every pair of related classes in the diagram."""

        return list(self.__relationships.keys())

    # ----------
    # Relationship attribute functions

    # ----------
    # set_relationship_attribute

    def set_relationship_attribute(
        self,
        class_name_a: str,
        class_name_b: str,
        attribute_name: str,
        attribute_value: str,
    ) -> bool:
        """Sets the value of 'attribute_name' to 'attribute_value' for the relationship between 'class_name_a' and 'class_name_b'.
If the relationship does not yet have an attribute with the name 'attribute_name', one will be created.
Fails if a relationship between 'class_name_a' and 'class_name_b' is not present in the diagram.
Returns 'True' on success, or 'False' on failure."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
        ):
            return False

        self.__relationships[class_pair][attribute_name] = attribute_value

        return True

    # ----------
    # remove_relationship_attribute

    def remove_relationship_attribute(
        self, class_name_a: str, class_name_b: str, attribute_name: str
    ) -> bool:
        """Removes the attribute with name 'attribute_name' from the relationship between 'class_name_a' and 'class_name_b'
Fails if an attribute with 'attribute_name' is not found in the relationship.
Fails if a relationship between 'class_name_a' and 'class_name_b' is not present in the diagram.
Returns 'True' on success, or 'False' on failure."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
            or attribute_name not in self.__relationships[class_pair]
        ):
            return False

        del self.__relationships[class_pair][attribute_name]

        return True

    # ----------
    # get_relationship_attributes

    def get_relationship_attributes(
        self, class_name_a: str, class_name_b: str
    ) -> Optional[AttributeDict]:
        """Returns a Dict[str, str] containing the attribute names and values for the relationship between 'class_name_a' and 'class_name_b'
Fails and returns 'None' if a relationship between 'class_name_a' and 'class_name_b' is not present in the diagram."""

        class_pair: ClassPair = self.__resolve_class_pair(class_name_a, class_name_b)

        if (
            class_name_a not in self.__classes
            or class_name_b not in self.__classes
            or class_pair not in self.__relationships
        ):
            return None

        return self.__relationships[class_pair]
