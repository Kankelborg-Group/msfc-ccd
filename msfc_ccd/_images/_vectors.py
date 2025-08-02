from typing import Type
from typing_extensions import Self
import dataclasses
import astropy.units as u
import astropy.time
import named_arrays as na

__all__ = [
    "ImageHeader",
]


@dataclasses.dataclass(eq=False, repr=False)
class ImageHeader(
    na.AbstractExplicitCartesianVectorArray,
):
    """A singe FITS header or a sequence of FITS headers saved by MSFC camera."""

    pixel: na.AbstractCartesian2dVectorArray = dataclasses.MISSING
    """The indices of each pixel in the image."""

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

    @property
    def type_abstract(self: Self) -> Type[Self]:  # pragma: nocover
        return ImageHeader

    @property
    def type_explicit(self: Self) -> Type[Self]:  # pragma: nocover
        return ImageHeader

    @property
    def type_matrix(self) -> Type[na.AbstractCartesianMatrixArray]:  # pragma: nocover
        raise NotImplementedError

    @classmethod
    def from_scalar(
        cls: Type[Self],
        scalar: na.AbstractScalar,
        like: None | na.AbstractExplicitVectorArray = None,
    ) -> Self:
        return cls(
            pixel=scalar,
            time=scalar,
            timedelta=scalar,
            timedelta_requested=scalar,
            serial_number=scalar,
            run_mode=scalar,
            status=scalar,
            voltage_fpga_vccint=scalar,
            voltage_fpga_vccaux=scalar,
            voltage_fpga_vccbram=scalar,
            temperature_fpga=scalar,
            temperature_adc_1=scalar,
            temperature_adc_2=scalar,
            temperature_adc_3=scalar,
            temperature_adc_4=scalar,
        )
