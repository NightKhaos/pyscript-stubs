"""
Contains methods that interact directly with the JavaScript intefaces following the magic_js.py file in the stdlib.
"""
from __future__ import annotations

__all__ = ["RUNNING_IN_WORKER", "current_target"]

RUNNING_IN_WORKER: bool
"""
Will return True if running in worker, False if running in main thread.
"""

def current_target() -> str:
    """
    Produce the current target of the current event context.

    :return: a selector string that identifies that current target
    """
    ...
