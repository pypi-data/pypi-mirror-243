"""
Module to collect raw content from the web and store it.
This module is only concerned with collection and storage of raw content.
To work with transformation of raw content, see the transform sub-module.
"""

__all__ = ["Collector", "CollectorConfiguration", "CollectorOptions"]

from .main import Collector
from .models import CollectorConfiguration, CollectorOptions
