"""Toolbox for Japanese text."""

from ._version import __version__  # noqa: F401
from .loader import load_aozorabunko
from .textmodel import TextModel
from .wordcloud import WordCloud

__all__ = (
    "load_aozorabunko",
    "TextModel",
    "WordCloud",
)
