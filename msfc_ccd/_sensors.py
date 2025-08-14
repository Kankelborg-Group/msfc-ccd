from typing import ClassVar, Literal
import abc
import dataclasses
import numpy as np
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

    @property
    @abc.abstractmethod
    def temperature(self):
        """The operating temperature of this sensor."""

    def dark_current(
        self,
        temperature: None | u.Quantity | na.AbstractScalar = None,
    ):
        """
        The rate of charge accumulation when the sensor is not illuminated.

        Parameters
        ----------
        temperature
            The temperature of the sensor.
            If :obj:`None`, the value of :attr:`temperature` is used.
        """


@dataclasses.dataclass
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

    num_pixel: None | na.Cartesian2dVectorArray[int, int] = None
    """
    The number of pixels along the horizontal and vertical axes.
    
    If :obj:`None`, the value ``na.Cartesian2dVectorArray(2048, 2064)`` is used.
    """

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

    temperature: u.Quantity | na.AbstractScalar = 248 * u.K
    """The operating temperature of this sensor."""

    def __post_init__(self):
        if self.num_pixel is None:
            self.num_pixel = na.Cartesian2dVectorArray(2048, 2064)

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

    @classmethod
    def _frac_Qd_Qdo(cls, temperature: u.Quantity | na.AbstractScalar):
        T = temperature
        return 122 * T * np.square(T) * np.exp(-6400 * u.K / T) / u.K**3

    def dark_current(
        self,
        temperature: None | u.Quantity | na.AbstractScalar = None,
    ):
        """
        The rate of charge accumulation when the sensor is not illuminated.

        Parameters
        ----------
        temperature
            The temperature of the sensor.
            If :obj:`None`, the value of :attr:`temperature` is used.

        Examples
        --------

        Plot the theoretical dark current of this sensor according to the
        datasheet.

        .. jupyter-execute::

            import matplotlib.pyplot as plt
            import astropy.units as u
            import astropy.visualization
            import named_arrays as na
            import msfc_ccd

            # Define a grid of temperatures to sample
            temperature = na.linspace(200, 300, axis="temperature", num=101) * u.K

            # Initialize the sensor model
            sensor = msfc_ccd.TeledyneCCD230()

            # Compute the dark current of the sensor
            # given the grid of temperatures
            dark_current = sensor.dark_current(temperature)

            # Plot the results
            with astropy.visualization.quantity_support():
                fig, ax = plt.subplots()
                ax2 = ax.twiny()
                na.plt.plot(
                    temperature,
                    dark_current,
                    ax=ax,
                )
                na.plt.plot(
                    temperature.to(u.deg_C, equivalencies=u.temperature()),
                    dark_current,
                    ax=ax2,
                )
                ax.set_yscale("log")
                ax.set_xlabel(f"temperature ({ax.get_xlabel()})")
                ax2.set_xlabel(f"temperature ({ax2.get_xlabel()})")
                ax.set_ylabel(f"dark current ({ax.get_ylabel()})")
        """
        if temperature is None:
            temperature = self.temperature
        Q_248K = 0.2 * u.electron / u.s
        f = self._frac_Qd_Qdo(248 * u.K)
        Q_do = Q_248K / f
        return Q_do * self._frac_Qd_Qdo(temperature)
