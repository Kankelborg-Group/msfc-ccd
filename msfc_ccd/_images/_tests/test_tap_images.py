import pytest
import named_arrays as na
import msfc_ccd
from . import test_images


class AbstractTestAbstractTapImage(
    test_images.AbstractTestAbstractImageData,
):
    def test_axis_tap_x(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.axis_tap_x
        assert isinstance(result, str)
        assert result in a.data.shape

    def test_axis_tap_y(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.axis_tap_y
        assert isinstance(result, str)
        assert result in a.data.shape

    def test_tap(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.tap
        for ax in result:
            assert isinstance(ax, str)
            assert isinstance(result[ax], na.AbstractScalarArray)


@pytest.mark.parametrize(
    argnames="a",
    argvalues=[
        msfc_ccd.TapData.from_sensor_data(
            a=msfc_ccd.fits.open(msfc_ccd.samples.path_fe55_esis1)
        ),
    ],
)
class TestTapImage(
    AbstractTestAbstractTapImage,
):
    pass
