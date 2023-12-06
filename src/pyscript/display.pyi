"""
Contains methods to render text and HTML in PyScript following the display.py file in the stdlib.
"""
from __future__ import annotations

from pyscript.types.mime_types import AllSupportedMIMETypes

__all__ = ["HTML", "display"]

class HTML:
    """
    Basic wrapper of a string so that display() can render it as plain HTML.

    This is included as a stub implementation for display() for HTML objects. In more complex applications you should
    look to use objects that output supported MIME types with the required _repr_*_ method implemented.

    WARNING: This class can be dangerous as it allows you to produce raw HTML that has not been validated.
    """

    def __init__(self, html: str) -> None:
        """
        :param html: The raw HTML representation of this object.
        """
        ...
    def _repr_html_(self) -> str:
        """
        Returns raw HTML representation of this object.
        """
        ...

def display(*values: AllSupportedMIMETypes, target: str | None = None, append: bool = True) -> None:
    """
    Quickly write objects to the current view based upon the current target or a specified target.

    :param values: objects to replace the target's children with or append to the target.
    :param target: ID of element which should be written/appended to (Default: current target).
    :param append: determines replacement or append behaviour.
    :raise ValueError: if param target is not a valid selector.
    """
    # Note: Without an extended runtime_checkable implementation, like beartype, it is not possible to put further
    #       constraints on something like the target, which cannot be a set of pre-determined values (i.e. Literal
    #       type) and instead will need to be a regex.
    ...
