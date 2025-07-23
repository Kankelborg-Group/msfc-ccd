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
    def num_blank(self) -> int:
        """
        The number of blank columns at the start of each row of the tap image.
        """

    @property
    @abc.abstractmethod
    def num_overscan(self):
        """
        The number of overscan columns at the end of each row of the tap image.
        """



@dataclasses.dataclass(eq=False, repr=False)
class TeledyneCCD230(
    AbstractSensor,
):
    """
    The standard sensor used by the MSFC cameras.
    """

    width_pixel: u.Quantity = 15 * u.um
    """The physical size of a single pixel on the imaging sensor."""

    num_blank: int = 50
    """
    The number of blank columns at the start of each row of the tap image.
    """

    num_overscan: int = 2
    """
    The number of overscan columns at the end of each row of the tap image.
    """
