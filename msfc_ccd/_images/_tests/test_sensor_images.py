import pytest
import numpy as np
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
        msfc_ccd.SensorData.from_fits(
            path=msfc_ccd.samples.path_dark_esis1,
            camera=msfc_ccd.Camera(),
        ),
        msfc_ccd.SensorData.from_fits(
            path=na.ScalarArray(
                ndarray=np.array(
                    [
                        msfc_ccd.samples.path_dark_esis1,
                        msfc_ccd.samples.path_dark_esis3,
                    ]
                ),
                axes="channel",
            ),
            camera=msfc_ccd.Camera(),
        ),
        msfc_ccd.SensorData.from_fits(
            path=na.ScalarArray(
                ndarray=np.array(
                    [
                        msfc_ccd.samples.path_dark_esis1,
                        msfc_ccd.samples.path_fe55_esis1,
                    ]
                ),
                axes="time",
            ),
            camera=msfc_ccd.Camera(),
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
        taps = result.taps()
        assert isinstance(result, msfc_ccd.SensorData)
        assert np.abs(taps.outputs[taps.where_blank()].mean()) < 1
        assert np.abs(taps.outputs[taps.where_overscan()].mean()) < 1
        assert np.abs(result.outputs.mean()) > 0

    def test_active(
        self,
        a: msfc_ccd.SensorData,
    ):
        sensor = a.camera.sensor
        num_nap = 2 * (sensor.num_blank + sensor.num_overscan)
        result = a.active
        assert isinstance(result, msfc_ccd.SensorData)
        assert result.shape[a.axis_x] == a.shape[a.axis_x] - num_nap
        assert result.shape[a.axis_y] == a.shape[a.axis_y]
