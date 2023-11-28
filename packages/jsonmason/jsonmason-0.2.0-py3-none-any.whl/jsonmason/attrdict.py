"""
Attrdict
--------
A dictionary that allows to get and set items, attribute style.

Example:
^^^^^^^^

>>> my_attrdict = AttrDict.from_container({"swallows": {"laden": 1, "unladen": 9000}})
>>> my_attrdict.swallows.unladen
9000
>>> my_attrdict.swallows.unladen += 111
>>> my_attrdict.swallows.unladen
9111
"""

from typing import Union, List, Dict, Any

from . import deconstruct, reconstruct


class AttrDict(dict):

    def __getattribute__(self, name: str):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return super().__getitem__(name)

    def __setattribute__(self, name: str, value: Any):
        if hasattr(self, name):
            setattr(self, name, value)
        super().__setitem__(name, value)

    @classmethod
    def from_container(cls, container: Union[dict | list]):
        return reconstruct(deconstruct(container), container_mapping={List: list, Dict: cls})
