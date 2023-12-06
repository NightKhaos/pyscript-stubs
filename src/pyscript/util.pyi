"""
Contains helper functions and classes following the util.py file in the stdlib.
"""
from __future__ import annotations

from typing import Any

__all__ = ["NotSupported"]

class NotSupported:
    """
    Small helper that raises exceptions if you try to get/set any attribute on it.
    """

    def __init__(self, name: str, error: str) -> None:
        """
        :param name: name of the NotSupported class.
        :param error: error message to display to the user
        """
        ...
    def __repr__(self) -> str:
        """
        :return: string representation of the NotSupported class that will include the name and error message.
        """
        ...
    def __getattr__(self, attr: str) -> Any:
        """
        :param attr: Name of attribute to get
        :return the attribute value
        :raise AttributeError
        """
        ...
    def __setattr__(self, attr: str, value: Any) -> None:
        """
        :param attr: Name of attribute to set
        :param value: Value to set the attribute too
        :raise AttributeError
        """
        ...
    def __call__(self, *args):
        """
        :raise TypeError
        """ ""
        ...
