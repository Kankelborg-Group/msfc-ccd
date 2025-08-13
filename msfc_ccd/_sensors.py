from typing import ClassVar, Literal
import abc
import dataclasses
import astropy.units as u
import named_arrays as na

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
    def num_pixel(self) -> na.Cartesian2dVectorArray[int, int]:
        """The number of pixels along the horizontal and vertical axes."""

    @property
    @abc.abstractmethod
    def num_pixel_active(self):
        """The number of pixels that are used to detect light."""

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

    num_pixel: na.Cartesian2dVectorArray[int, int] = na.Cartesian2dVectorArray(
        x=2048,
        y=2064,
    )
    """The number of pixels along the horizontal and vertical axes."""

    num_blank: int = 50
    """The number of blank columns at the start of each row."""

    num_overscan: int = 2
    """The number of overscan columns at the end of each row."""

    readout_noise: u.Quantity = 4 * u.electron
    """The standard deviation of the error on each pixel value."""

    readout_mode: Literal["full-frame", "transfer"] = "transfer"
    """
    The frame readout mode of the sensor.
    
    Either the entire sensor is read at the same time (``"full-frame"``),
    or half of the sensor is used for storage (``"transfer"``).
    """

    @property
    def num_pixel_active(self):
        """
        The number of pixels that are used to detect light.

        If :attr:`readout_mode` is ``"full-frame"``, then this is the same
        as :attr:`num_pixel`.
        If :attr:`readout_mode` is ``"transfer"``, then the vertical component
        of :attr:`num_pixel` is divided by 2 since half of the sensor is now used
        for charge storage.
        """
        result = self.num_pixel
        if self.readout_mode == "transfer":
            return result.replace(y=result.y / 2)
