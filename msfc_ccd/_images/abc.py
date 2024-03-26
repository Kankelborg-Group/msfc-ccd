"""
Abstract base classes for this subpackage
"""

__all__ = [
    "AbstractImageData",
    "AbstractSensorData",
]

from ._images import AbstractImageData
from ._sensor_images import AbstractSensorData
