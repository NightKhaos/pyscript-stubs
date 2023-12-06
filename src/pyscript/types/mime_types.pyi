"""
Contains the type hints for MINE classes that have certain methods (Protocols) that are supported by PyScript.
"""
from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

__all__ = [
    "MimePlain",
    "MimeHTML",
    "MimeSVG",
    "MimeJPEG",
    "MimePNG",
    "MimeJSON",
    "MimeJavaScript",
    "MimeBundle",
    "MimePDF",
    "MimeMarkdown",
    "MimeLaTeX",
    "SpecialMimeSaveFig",
    "AllSupportedMIMETypes",
]

_StrOrStrAndMeta = str | tuple[str, dict[str, Any]]
_BytesOrBytesAndMeta = bytes | str | tuple[bytes | str, dict[str, Any]]

"""
These classes represent the supported MIME classes of PyScript that prescribe to the _repr_*_ format.
"""

@runtime_checkable
class MimePlain(Protocol):
    def __repr__(self) -> str: ...

@runtime_checkable
class MimeHTML(Protocol):
    def _repr_html_(self) -> _StrOrStrAndMeta: ...

@runtime_checkable
class MimeSVG(Protocol):
    def _repr_svg_(self) -> _StrOrStrAndMeta: ...

@runtime_checkable
class MimeJPEG(Protocol):
    def _repr_jpeg_(self) -> _BytesOrBytesAndMeta: ...

@runtime_checkable
class MimePNG(Protocol):
    def _repr_png_(self) -> _BytesOrBytesAndMeta: ...

@runtime_checkable
class MimeJSON(Protocol):
    def _repr_json(self) -> _StrOrStrAndMeta: ...

@runtime_checkable
class MimeJavaScript(Protocol):
    def _repr_javascript_(self) -> _StrOrStrAndMeta: ...

@runtime_checkable
class MimeBundle(Protocol):
    def _repr_mimebundle_(
        self, include=None, exclude=None
    ) -> dict[str, Any] | tuple[dict[str, Any], dict[str, Any]]: ...

"""
These classes are special types supported by PyScript that do not prescribe to the _repr_*_ representation format
"""

@runtime_checkable
class SpecialMimeSaveFig(Protocol):
    def savefig(self) -> bytes: ...

"""
These classes are not currently implemented by PyScript, but are supported in _MIME_METHODS_. They may be supported by
PyScript in the future, so for ease of implementation they are included here.
"""

@runtime_checkable
class MimeMarkdown(Protocol):
    def _repr_markdown_(self) -> _StrOrStrAndMeta: ...

@runtime_checkable
class MimePDF(Protocol):
    def _repr_pdf_(self) -> _BytesOrBytesAndMeta: ...

@runtime_checkable
class MimeLaTeX(Protocol):
    def _repr_latex_(self) -> _BytesOrBytesAndMeta: ...

AllSupportedMIMETypes = MimePlain | MimeHTML | MimePNG | MimeJPEG | MimeSVG | MimeJSON | MimeJavaScript
