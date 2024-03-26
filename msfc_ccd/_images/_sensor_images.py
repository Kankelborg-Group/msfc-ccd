import dataclasses
import astropy.units as u
import astropy.time
import named_arrays as na
from ._images import AbstractImageData

__all__ = [
    "SensorData",
]


@dataclasses.dataclass(eq=False, repr=False)
class AbstractSensorData(
    AbstractImageData,
):
    """
    An interface for representing data captured by an entire image sensor.
    """


@dataclasses.dataclass(eq=False, repr=False)
class SensorData(
    AbstractSensorData,
):
    data: na.AbstractScalar = dataclasses.MISSING
    """The underlying array storing the image data."""

    axis_x: str = dataclasses.MISSING
    """
    The name of the logical axis representing the horizontal dimension of
    the images.
    """

    axis_y: str = dataclasses.MISSING
    """
    The name of the logical axis representing the vertical dimension of
    the images.
    """

    time: astropy.time.Time | na.AbstractScalar = dataclasses.MISSING
    """The time in UTC at the midpoint of the exposure."""

    timedelta: u.Quantity | na.AbstractScalar = dataclasses.MISSING
    """The measured exposure time of each image."""

    timedelta_requested: u.Quantity | na.AbstractScalar = dataclasses.MISSING
    """The requested exposure time of each image."""

    serial_number: None | str | na.AbstractScalar = None
    """The serial number of the camera that captured each image."""

    run_mode: None | str | na.AbstractScalar = None
    """The Run Mode of the camera when each image was captured."""

    status: None | str | na.AbstractScalar = None
    """The status of the camera while each image was being captured."""

    voltage_fpga_vccint: u.Quantity | na.AbstractScalar = 0
    """The VCCINT voltage of the FPGA when each image was captured."""

    voltage_fpga_vccaux: u.Quantity | na.AbstractScalar = 0
    """The VCCAUX voltage of the FPGA when each image was captured."""

    voltage_fpga_vccbram: u.Quantity | na.AbstractScalar = 0
    """The VCCBRAM voltage of the FPGA when each image was captured."""

    temperature_fpga: u.Quantity | na.AbstractScalar = 0
    """The temperature of the FPGA when each image was captured."""

    temperature_adc_1: u.Quantity | na.AbstractScalar = 0
    """Temperature 1 of the ADC when each image was captured."""

    temperature_adc_2: u.Quantity | na.AbstractScalar = 0
    """Temperature 2 of the ADC when each image was captured."""

    temperature_adc_3: u.Quantity | na.AbstractScalar = 0
    """Temperature 3 of the ADC when each image was captured."""

    temperature_adc_4: u.Quantity | na.AbstractScalar = 0
    """Temperature 4 of the ADC when each image was captured."""
