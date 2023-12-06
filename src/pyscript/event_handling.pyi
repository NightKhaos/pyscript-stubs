"""
Contains decorators like @when for event handling in PyScript following the event_handling.py file in the stdlib.
"""
from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from pyscript.types import DOM_EVENT_TYPES
from pyweb.pydom import Element, ElementCollection

__all__ = ["when"]

EV = TypeVar("EV")  # Represents the event object
RV = TypeVar("RV")  # Represents the return value

# TODO: Determine structure of Event Object to help people know what events to expect when writing a @when and if we can
#       provide a better type rather than using a TypeVar generic.
#       -> (https://developer.mozilla.org/en-US/docs/Web/API/Event)
# TODO: Determine the expected return value of the Callable closure (None | Observable?) rather than using "TypeVar"
#       generics.

def when(event_type: DOM_EVENT_TYPES, selector: str | Element | ElementCollection) -> Callable[[EV], RV]:  # type: ignore[return]
    """
    Decorates a function and registers an event handler to pass py-* events to the decorated function.
    The events might or not be an argument of the decorated function.

    :param event_type: The event that you want to trigger
    :param selector: The selector that should be used to narrow down the event.
    :return: closure of the wrapped function as a Callable.
    """
    # Note: Without an extended runtime_checkable implementation, like beartype, it is not possible to put further
    #       constraints on something like the selector, which cannot be a set of pre-determined values (i.e. Literal
    #       type) and instead will need to be a regex.
    def decorator(func: Callable[[EV], RV] | Callable[[], RV]) -> Callable[[EV], RV]:
        """
        Inner decorator for the @when decorator

        :param func: the function that we are going to generate a closure.
        :return: closure of the wrapped function as a Callable.
        :raise ValueError: if param selector is not a valid selector (on closure call).
        """
        ...
    ...
