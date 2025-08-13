from typing import ClassVar
import abc
import dataclasses
import astropy.units as u

__all__ = [
    "TeledyneCCD230",
]


@dataclasses.dataclass(eq=False, repr=False)
class AbstractSensor(
    abc.ABC,
):
    """An interface for an imaging sensor or an ensemble of imaging sensors."""

    num_tap_x: ClassVar[int] = 2
    """The number of taps along the long axis of the CCD sensor."""

    num_tap_y: ClassVar[int] = 2
    """The number of taps along the short axis of the CCD sensor."""

    @property
    @abc.abstractmethod
    def manufacturer(self) -> str:
        """The company which produced the sensor."""

    @property
    @abc.abstractmethod
    def family(self) -> str:
        """The model number or product family of this sensor."""

    @property
    @abc.abstractmethod
    def serial_number(self) -> None | str:
        """A unique number which identifies this sensor."""

    @property
    @abc.abstractmethod
    def width_pixel(self) -> u.Quantity:
        """The physical size of a single pixel on the imaging sensor."""

    @property
    @abc.abstractmethod
    def num_blank(self) -> int:
        """The number of blank columns at the start of each row."""

    @property
    @abc.abstractmethod
    def num_overscan(self) -> int:
        """The number of overscan columns at the end of each row."""

    @property
    @abc.abstractmethod
    def readout_noise(self) -> u.Quantity:
        """The standard deviation of the error on each pixel value."""


@dataclasses.dataclass(eq=False, repr=False)
class TeledyneCCD230(
    AbstractSensor,
):
    """The standard sensor used by the MSFC cameras."""

    manufacturer: str = "Teledyne/e2v"
    """The company which produced the sensor."""

    family: str = "CCD230-42"
    """The model number or product family of this sensor."""

    serial_number: None | str = None
    """A unique number which identifies this sensor."""

    width_pixel: u.Quantity = 15 * u.um
    """The physical size of a single pixel on the imaging sensor."""

    num_blank: int = 50
    """The number of blank columns at the start of each row."""

    num_overscan: int = 2
    """The number of overscan columns at the end of each row."""

    readout_noise: u.Quantity = 4 * u.electron
    """The standard deviation of the error on each pixel value."""
