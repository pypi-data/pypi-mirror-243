"""
Module to collect raw content from the web and store it.
This module is only concerned with collection and storage of raw content.
To work with transformation of raw content, see the transform sub-module.
"""

__all__ = ["URLCollector", "URLConfig"]

from .main import URLCollector, URLConfig
