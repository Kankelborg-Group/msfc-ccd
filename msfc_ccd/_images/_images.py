import abc
import dataclasses
import astropy.units as u
import astropy.time
import named_arrays as na
import optika

__all__ = []


@dataclasses.dataclass(eq=False, repr=False)
class AbstractImageData(
    optika.mixins.Printable,
):
    """
    An interface for image-like data.

    This class is useful for a single interface for data from the entire image
    sensor and for data from only a single tap on the sensor.
    """

    @property
    @abc.abstractmethod
    def data(self) -> na.AbstractScalar:
        """The underlying array storing the image data."""

    @property
    @abc.abstractmethod
    def pixel(self) -> dict[str, na.AbstractScalarArray]:
        """
        The 2-dimensional index of each pixel in the image.
        """

    @property
    @abc.abstractmethod
    def axis_x(self) -> str:
        """
        The name of the logical axis representing the horizontal dimension of
        the images.
        """

    @property
    @abc.abstractmethod
    def axis_y(self) -> str:
        """
        The name of the logical axis representing the vertical dimension of
        the images.
        """

    @property
    def num_x(self) -> int:
        """
        The number of pixels along the x-axis.
        """
        return self.data.shape[self.axis_x]

    @property
    def num_y(self) -> int:
        """
        The number of pixels along the y-axis.
        """
        return self.data.shape[self.axis_y]

    @property
    @abc.abstractmethod
    def time(self) -> astropy.time.Time | na.AbstractScalar:
        """The time in UTC at the midpoint of the exposure."""

    @property
    @abc.abstractmethod
    def timedelta(self) -> u.Quantity | na.AbstractScalar:
        """The measured exposure time of each image."""

    @property
    @abc.abstractmethod
    def timedelta_requested(self) -> u.Quantity | na.AbstractScalar:
        """The requested exposure time of each image."""

    @property
    @abc.abstractmethod
    def serial_number(self) -> str | na.AbstractScalar:
        """The serial number of the camera that captured each image."""

    @property
    @abc.abstractmethod
    def run_mode(self) -> str | na.AbstractScalar:
        """The Run Mode of the camera when each image was captured."""

    @property
    @abc.abstractmethod
    def status(self) -> str | na.AbstractScalar:
        """The status of the camera while each image was being captured."""

    @property
    @abc.abstractmethod
    def voltage_fpga_vccint(self) -> u.Quantity | na.AbstractScalar:
        """The VCCINT voltage of the FPGA when each image was captured."""

    @property
    @abc.abstractmethod
    def voltage_fpga_vccaux(self) -> u.Quantity | na.AbstractScalar:
        """The VCCAUX voltage of the FPGA when each image was captured."""

    @property
    @abc.abstractmethod
    def voltage_fpga_vccbram(self) -> u.Quantity | na.AbstractScalar:
        """The VCCBRAM voltage of the FPGA when each image was captured."""

    @property
    @abc.abstractmethod
    def temperature_fpga(self) -> u.Quantity | na.AbstractScalar:
        """The temperature of the FPGA when each image was captured."""

    @property
    @abc.abstractmethod
    def temperature_adc_1(self) -> u.Quantity | na.AbstractScalar:
        """Temperature 1 of the ADC when each image was captured."""

    @property
    @abc.abstractmethod
    def temperature_adc_2(self) -> u.Quantity | na.AbstractScalar:
        """Temperature 2 of the ADC when each image was captured."""

    @property
    @abc.abstractmethod
    def temperature_adc_3(self) -> u.Quantity | na.AbstractScalar:
        """Temperature 3 of the ADC when each image was captured."""

    @property
    @abc.abstractmethod
    def temperature_adc_4(self) -> u.Quantity | na.AbstractScalar:
        """Temperature 4 of the ADC when each image was captured."""
