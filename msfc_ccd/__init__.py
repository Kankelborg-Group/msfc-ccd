"""
A Python package for the CCD cameras developed by MSFC.
"""

__all__ = [
    "SensorData",
    "abc",
]

from . import samples
from ._images import SensorData
from . import abc
