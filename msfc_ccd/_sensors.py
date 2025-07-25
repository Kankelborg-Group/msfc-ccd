from typing import ClassVar
import abc
import dataclasses
import astropy.units as u
import optika

__all__ = [
    "TeledyneCCD230",
]


@dataclasses.dataclass(eq=False, repr=False)
class AbstractSensor(
    optika.mixins.Printable,
):
    """
    An interface for an imaging sensor or an ensemble of imaging sensors.
    """

    num_tap_x: ClassVar[int] = 2
    """The number of taps along the long axis of the CCD sensor."""

    num_tap_y: ClassVar[int] = 2
    """The number of taps along the short axis of the CCD sensor."""

    @property
    @abc.abstractmethod
    def width_pixel(self) -> u.Quantity:
        """The physical size of a single pixel on the imaging sensor."""

    @property
    @abc.abstractmethod
    def num_inactive(self) -> int:
        """
        The number of inactive pixels along the edge of each tap of the image
        sensor.
        """

    @property
    @abc.abstractmethod
    def num_overscan(self):
        """The number of overscan pixels along the inside edge of each tap."""


@dataclasses.dataclass(eq=False, repr=False)
class TeledyneCCD230(
    AbstractSensor,
):
    """
    The standard sensor used by the MSFC cameras.
    """

    width_pixel: u.Quantity = 15 * u.um
    """The physical size of a single pixel on the imaging sensor."""

    num_inactive: int = 50
    """
    The number of inactive pixels along the edge of each tap of the image
    sensor.
    """

    num_overscan: int = 2
    """The number of overscan pixels along the inside edge of each tap."""
