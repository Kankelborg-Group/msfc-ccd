import pytest
import numpy as np
import astropy.units as u
import astropy.time
import named_arrays as na
import msfc_ccd
from . import test_images


class AbstractTestAbstractSensorData(
    test_images.AbstractTestAbstractImageData,
):
    def test_taps(self, a: msfc_ccd.abc.AbstractSensorData):
        result = a.taps()
        assert isinstance(result, msfc_ccd.TapData)


@pytest.mark.parametrize(
    argnames="a",
    argvalues=[
        msfc_ccd.SensorData(
            inputs=msfc_ccd.ImageHeader(
                pixel=na.Cartesian2dVectorArray(
                    x=na.arange(0, 22, "x"),
                    y=na.arange(0, 12, "y"),
                ),
                time=astropy.time.Time("2024-03-25T20:49"),
                timedelta=9.98 * u.s,
                timedelta_requested=10 * u.s,
                serial_number="SN-001",
                run_mode="sequence",
                status="completed",
                voltage_fpga_vccint=5 * u.V,
                voltage_fpga_vccaux=6 * u.V,
                voltage_fpga_vccbram=7 * u.V,
                temperature_fpga=20 * u.deg_C,
                temperature_adc_1=21 * u.deg_C,
                temperature_adc_2=22 * u.deg_C,
                temperature_adc_3=23 * u.deg_C,
                temperature_adc_4=24 * u.deg_C,
            ),
            outputs=na.random.uniform(0, 1, shape_random=dict(x=22, y=12)),
            axis_x="x",
            axis_y="y",
            sensor=msfc_ccd.TeledyneCCD230(),
        ),
        msfc_ccd.SensorData(
            inputs=msfc_ccd.ImageHeader(
                pixel=na.Cartesian2dVectorArray(
                    x=na.arange(0, 22, "x"),
                    y=na.arange(0, 12, "y"),
                ),
                time=na.ScalarArray(
                    ndarray=np.linspace(
                        astropy.time.Time("2024-03-25T20:49"),
                        astropy.time.Time("2024-03-25T21:49"),
                        num=5,
                    ),
                    axes="t",
                ),
                timedelta=na.ScalarArray(
                    ndarray=[9.98, 9.99, 10.1, 10.06, 9.76] * u.s,
                    axes="t",
                ),
                timedelta_requested=10 * u.s,
                serial_number="SN-001",
                run_mode="sequence",
                status="completed",
                voltage_fpga_vccint=5 * u.V,
                voltage_fpga_vccaux=6 * u.V,
                voltage_fpga_vccbram=7 * u.V,
                temperature_fpga=20 * u.deg_C,
                temperature_adc_1=21 * u.deg_C,
                temperature_adc_2=22 * u.deg_C,
                temperature_adc_3=23 * u.deg_C,
                temperature_adc_4=24 * u.deg_C,
            ),
            outputs=na.random.uniform(
                low=0,
                high=1,
                shape_random=dict(t=5, x=22, y=12),
            ),
            axis_x="x",
            axis_y="y",
            sensor=msfc_ccd.TeledyneCCD230(),
        ),
        msfc_ccd.SensorData.from_fits(
            path=msfc_ccd.samples.path_dark_esis1,
            sensor=msfc_ccd.TeledyneCCD230(),
        ),
        msfc_ccd.SensorData.from_fits(
            path=na.ScalarArray(
                ndarray=np.array(
                    [
                        msfc_ccd.samples.path_dark_esis1,
                        msfc_ccd.samples.path_dark_esis3,
                    ]
                ),
                axes="time",
            ),
            sensor=msfc_ccd.TeledyneCCD230(),
        ),
    ],
)
class TestSensorData(
    AbstractTestAbstractSensorData,
):

    def test_from_taps(
        self,
        a: msfc_ccd.SensorData,
    ):
        b = a.taps("tx", "ty")
        c = a.from_taps(b)

        assert np.all(a == c)

    def test_unbiased(
        self,
        a: msfc_ccd.SensorData,
    ):
        result = a.unbiased
        assert isinstance(result, msfc_ccd.SensorData)
        assert np.abs(result.outputs.mean()) < 1
        assert np.abs(result.outputs.mean()) > 0
