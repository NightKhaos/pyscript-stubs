"""
This contains the event types from the DOM, extracted from the MDM docs.

IMPORTANT: This file is generated on build of this package from a template.
"""
from __future__ import annotations

from typing import Literal

__all__ = ["DOM_EVENT_TYPES"]

DOM_EVENT_TYPES = Literal[
    {%- for event in events %}
    "{{ event }}"{% if not loop.last %},{% endif %}
    {%- endfor %}
]
"""
Events that are supported my modern browsers according to the MDN web docs.

https://developer.mozilla.org/en-US/docs/Web/Events#event_listing
"""
