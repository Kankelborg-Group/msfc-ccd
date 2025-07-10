import abc
import dataclasses
import astropy.units as u
import astropy.time
import named_arrays as na
from .._sensors import AbstractSensor
from ._images import AbstractImageData

__all__ = [
    "TapData",
]


@dataclasses.dataclass(eq=False, repr=False)
class AbstractTapData(
    AbstractImageData,
):
    """
    An interface for representing data gathered by a single tap on an image
    sensor.
    """

    @property
    @abc.abstractmethod
    def axis_tap_x(self):
        """
        The name of the logical axis corresponding to the horizontal
        variation of the tap index.
        """

    @property
    @abc.abstractmethod
    def axis_tap_y(self):
        """
        The name of the logical axis corresponding to the vertical
        variation of the tap index.
        """

    @property
    def tap(self) -> dict[str, na.AbstractScalarArray]:
        """
        The 2-dimensional index of the tap corresponding to each image.
        """
        axis_tap_x = self.axis_tap_x
        axis_tap_y = self.axis_tap_y
        shape = self.data.shape
        shape_img = {
            axis_tap_x: shape[axis_tap_x],
            axis_tap_y: shape[axis_tap_y],
        }
        return na.indices(shape_img)


@dataclasses.dataclass(eq=False, repr=False)
class TapData(
    AbstractTapData,
):
    """
    A class designed to represent a sequence of images from each tap of an
    MSFC camera.

    Examples
    --------

    Load a sample image and split it into the four tap images.

    .. jupyter-execute::

        import named_arrays as na
        import msfc_ccd

        # Define the x and y axes of the detector
        axis_x = "detector_x"
        axis_y = "detector_y"

        # Define the x and y axes of the taps
        axis_tap_x = "tap_x"
        axis_tap_y = "tap_y"

        # Load the sample image
        image = msfc_ccd.fits.open(
            path=msfc_ccd.samples.path_fe55_esis1,
            axis_x=axis_x,
            axis_y=axis_y,
        )

        # Split the sample image into four separate images for each tap
        taps = image.taps(axis_tap_x, axis_tap_y)

        # Display the four images
        fig, axs = na.plt.subplots(
            axis_rows=axis_tap_y,
            nrows=taps.data.shape[axis_tap_y],
            axis_cols=axis_tap_x,
            ncols=taps.data.shape[axis_tap_x],
            sharex=True,
            sharey=True,
            constrained_layout=True,
        );
        axs = axs[{axis_tap_y: slice(None, None, -1)}]
        na.plt.pcolormesh(
            *taps.pixel.values(),
            C=taps.data,
            ax=axs,
        );

    """

    data: na.AbstractScalar = dataclasses.MISSING
    """The underlying array storing the image data."""

    pixel: dict[str, na.AbstractScalarArray] = dataclasses.MISSING
    """The 2-dimensional index of each pixel in the image"""

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

    axis_tap_x: str = dataclasses.MISSING
    """
    The name of the logical axis corresponding to the horizontal
    variation of the tap index.
    """

    axis_tap_y: str = dataclasses.MISSING
    """
    The name of the logical axis corresponding to the vertical
    variation of the tap index.
    """

    time: astropy.time.Time | na.AbstractScalar = dataclasses.MISSING
    """The time in UTC at the midpoint of the exposure."""

    timedelta: u.Quantity | na.AbstractScalar = dataclasses.MISSING
    """The measured exposure time of each image."""

    timedelta_requested: u.Quantity | na.AbstractScalar = dataclasses.MISSING
    """The requested exposure time of each image."""

    sensor: AbstractSensor = dataclasses.MISSING
    """A model of the sensor used to capture these images."""

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
