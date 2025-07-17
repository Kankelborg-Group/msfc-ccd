"""
A package for representing data gathered from imaging sensors
"""

__all__ = [
    "ImageHeader",
    "SensorData",
    "TapData",
]

from ._vectors import ImageHeader
from ._sensor_images import SensorData
from ._tap_images import TapData
