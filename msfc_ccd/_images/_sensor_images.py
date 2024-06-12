from __future__ import annotations
from typing_extensions import Self
import dataclasses
import pathlib
import numpy as np
import astropy.units as u
import astropy.time
import astropy.io.fits
import named_arrays as na
import msfc_ccd
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

    @property
    def pixel(self) -> dict[str, na.AbstractScalarArray]:
        axis_x = self.axis_x
        axis_y = self.axis_y
        shape = self.data.shape
        shape_img = {
            axis_x: shape[axis_x],
            axis_y: shape[axis_y],
        }
        return na.indices(shape_img)

    def taps(
        self,
        axis_tap_x: str = "tap_x",
        axis_tap_y: str = "tap_y",
    ) -> msfc_ccd.TapData:
        """
        Split the images into separate images for each tap.

        Parameters
        ----------
        axis_tap_x
            The name of the logical axis corresponding to the horizontal
            variation of the tap index.
        axis_tap_y
            The name of the logical axis corresponding to the vertical
            variation of the tap index.
        """
        return msfc_ccd.TapData.from_sensor_data(
            a=self,
            axis_tap_x=axis_tap_x,
            axis_tap_y=axis_tap_y,
        )


@dataclasses.dataclass(eq=False, repr=False)
class SensorData(
    AbstractSensorData,
):
    """
    A class designed to represent a sequence of images captured by an
    MSFC camera.

    Examples
    --------

    Load a sample image and display it.

    .. jupyter-execute::

        import matplotlib.pyplot as plt
        import named_arrays as na
        import msfc_ccd

        # Define the x and y axes of the detector
        axis_x = "detector_x"
        axis_y = "detector_y"

        # Load the sample image
        image = msfc_ccd.SensorData.from_fits(
            path=msfc_ccd.samples.path_fe55_esis1,
            axis_x=axis_x,
            axis_y=axis_y,
        )

        # Display the sample image
        fig, ax = plt.subplots(
            constrained_layout=True,
        )
        im = na.plt.imshow(
            image.data,
            axis_x=axis_x,
            axis_y=axis_y,
            ax=ax,
        );
    """

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

    @classmethod
    def _calibrate_timedelta(cls, value: int) -> u.Quantity:
        return value * 0.000000025 * u.s

    @classmethod
    def _calibrate_voltage_fpga(cls, value: int) -> u.Quantity:
        return value * 3 / 4096 * u.V

    @classmethod
    def _calibrate_temperature_fpga(cls, value: int) -> u.Quantity:
        result = value * 503.975 / 4096 * u.K
        result = result.to(u.deg_C, equivalencies=u.temperature())
        return result

    @classmethod
    def _calibrate_temperature_adc_1(cls, value: int) -> u.Quantity:
        r = (9.814453125 * value) / (1 - (value / 4096.0))
        result = 3455.0 / np.log(r / 0.0927557) * u.K
        result = result.to(u.deg_C, equivalencies=u.temperature())
        return result

    @classmethod
    def _calibrate_temperature_adc_234(cls, value: int) -> u.Quantity:
        r = (9.814453125 * value) / (1 - (value / 4096.0))
        a = 0.0011275
        b = 0.00023441
        c = 0.000000086482
        result = 1 / (a + (b * np.log(r)) + (c * np.log(r)) ** 3) * u.K
        result = result.to(u.deg_C, equivalencies=u.temperature())
        return result

    @classmethod
    def from_fits(
        cls,
        path: str | pathlib.Path | na.AbstractScalarArray,
        axis_x: str = "detector_x",
        axis_y: str = "detector_y",
    ) -> Self:
        """
        Load an image or an array of images from a FITS file or an array of
        FITS files.

        Parameters
        ----------
        path
            Either a single path or an array of paths pointing to the FITS files
            to load.
        axis_x
            The name of the logical axis representing the horizontal dimension of
            the images.
        axis_y
            The name of the logical axis representing the vertical dimension of
            the images.
        """

        path = na.as_named_array(path)

        time = np.zeros_like(path, dtype=float)
        time.ndarray = astropy.time.Time(time.ndarray, format="jd")

        timedelta = np.empty_like(path, dtype=np.int64)
        timedelta_requested = np.empty_like(path, dtype=float) << u.s
        serial_number = np.empty_like(path, dtype=str)
        run_mode = np.empty_like(path, dtype=str)
        status = np.empty_like(path, dtype=str)
        voltage_fpga_vccint = np.empty_like(path, dtype=int)
        voltage_fpga_vccaux = np.empty_like(path, dtype=int)
        voltage_fpga_vccbram = np.empty_like(path, dtype=int)
        temperature_fpga = np.empty_like(path, dtype=int)
        temperature_adc_1 = np.empty_like(path, dtype=int)
        temperature_adc_2 = np.empty_like(path, dtype=int)
        temperature_adc_3 = np.empty_like(path, dtype=int)
        temperature_adc_4 = np.empty_like(path, dtype=int)

        for i, index in enumerate(path.ndindex()):

            hdu = astropy.io.fits.open(path[index].ndarray)[0]

            data_index = na.ScalarArray(
                ndarray=hdu.data,
                axes=(axis_y, axis_x),
            )

            if i == 0:
                data = na.ScalarArray.empty(
                    shape=na.broadcast_shapes(path.shape, data_index.shape),
                    dtype=int,
                )

            data[index] = data_index

            header = hdu.header
            time[index] = astropy.time.Time(header["IMG_TS"])
            timedelta[index] = header["MEAS_EXP"]
            timedelta_requested[index] = header["IMG_EXP"] * u.ms
            serial_number[index] = header["CAM_SN"]
            run_mode[index] = header["RUN_MODE"]
            status[index] = header["IMG_STAT"]
            voltage_fpga_vccint[index] = header["FPGAVINT"]
            voltage_fpga_vccaux[index] = header["FPGAVAUX"]
            voltage_fpga_vccbram[index] = header["FPGAVBRM"]
            temperature_fpga[index] = header["FPGATEMP"]
            temperature_adc_1[index] = header["ADCTEMP1"]
            temperature_adc_2[index] = header["ADCTEMP2"]
            temperature_adc_3[index] = header["ADCTEMP3"]
            temperature_adc_4[index] = header["ADCTEMP4"]

        timedelta = cls._calibrate_timedelta(timedelta)
        voltage_fpga_vccint = cls._calibrate_voltage_fpga(voltage_fpga_vccint)
        voltage_fpga_vccaux = cls._calibrate_voltage_fpga(voltage_fpga_vccaux)
        voltage_fpga_vccbram = cls._calibrate_voltage_fpga(voltage_fpga_vccbram)
        temperature_fpga = cls._calibrate_temperature_fpga(temperature_fpga)
        temperature_adc_1 = cls._calibrate_temperature_adc_1(temperature_adc_1)
        temperature_adc_2 = cls._calibrate_temperature_adc_234(temperature_adc_2)
        temperature_adc_3 = cls._calibrate_temperature_adc_234(temperature_adc_3)
        temperature_adc_4 = cls._calibrate_temperature_adc_234(temperature_adc_4)

        return cls(
            data=data,
            axis_x=axis_x,
            axis_y=axis_y,
            time=time,
            timedelta=timedelta,
            timedelta_requested=timedelta_requested,
            serial_number=serial_number,
            run_mode=run_mode,
            status=status,
            voltage_fpga_vccint=voltage_fpga_vccint,
            voltage_fpga_vccaux=voltage_fpga_vccaux,
            voltage_fpga_vccbram=voltage_fpga_vccbram,
            temperature_fpga=temperature_fpga,
            temperature_adc_1=temperature_adc_1,
            temperature_adc_2=temperature_adc_2,
            temperature_adc_3=temperature_adc_3,
            temperature_adc_4=temperature_adc_4,
        )
