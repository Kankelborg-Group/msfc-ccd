from typing_extensions import Self, ClassVar
import abc
import dataclasses
import astropy.units as u
import astropy.time
import named_arrays as na
from ._images import AbstractImageData
from ._sensor_images import AbstractSensorData

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

    num_tap_x: ClassVar[int] = 2
    """The number of taps along the horizontal axis of the CCD sensor."""

    num_tap_y: ClassVar[int] = 2
    """The number of taps along the vertical axis of the CCD sensor."""

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

    @classmethod
    def from_sensor_data(
        cls,
        a: AbstractSensorData,
        axis_tap_x: str = "tap_x",
        axis_tap_y: str = "tap_y",
    ) -> Self:
        """
        Creates a new instance of this class using an instance of
        :class:`msfc_ccd.SensorData`.

        Parameters
        ----------
        a
            An instance of :class:`msfc_ccd.SensorData` to convert.
        axis_tap_x
            The name of the logical axis corresponding to the horizontal
            variation of the tap index.
        axis_tap_y
            The name of the logical axis corresponding to the vertical
            variation of the tap index.
        """

        axis_x = a.axis_x
        axis_y = a.axis_y

        num_x = a.num_x
        num_y = a.num_y

        num_tap_x = cls.num_tap_x
        num_tap_y = cls.num_tap_y

        shape_img = {axis_x: num_x, axis_y: num_y}

        num_x_new = num_x // num_tap_x
        num_y_new = num_y // num_tap_y

        slice_left_x = slice(None, num_x_new)
        slice_left_y = slice(None, num_y_new)

        slice_right_x = slice(None, num_x_new - 1, -1)
        slice_right_y = slice(None, num_y_new - 1, -1)

        slices_x = [slice_left_x, slice_right_x]
        slices_y = [slice_left_y, slice_right_y]

        pixel = a.pixel

        for ax in pixel:
            p = pixel[ax].broadcast_to(shape_img)
            pixel[ax] = na.stack(
                arrays=[
                    na.stack(
                        arrays=[p[{axis_x: sx, axis_y: sy}] for sy in slices_y],
                        axis=axis_tap_y,
                    )
                    for sx in slices_x
                ],
                axis=axis_tap_x,
            )

        return cls(
            data=a.data[pixel],
            pixel=pixel,
            axis_x=a.axis_x,
            axis_y=a.axis_y,
            axis_tap_x=axis_tap_x,
            axis_tap_y=axis_tap_y,
            time=a.time,
            timedelta=a.timedelta,
            timedelta_requested=a.timedelta_requested,
            serial_number=a.serial_number,
            run_mode=a.run_mode,
            status=a.status,
            voltage_fpga_vccint=a.voltage_fpga_vccint,
            voltage_fpga_vccaux=a.voltage_fpga_vccaux,
            voltage_fpga_vccbram=a.voltage_fpga_vccbram,
            temperature_fpga=a.temperature_fpga,
            temperature_adc_1=a.temperature_adc_1,
            temperature_adc_2=a.temperature_adc_2,
            temperature_adc_3=a.temperature_adc_3,
            temperature_adc_4=a.temperature_adc_4,
        )
