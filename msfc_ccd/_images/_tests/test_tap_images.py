import pytest
import numpy as np
import named_arrays as na
import msfc_ccd
from . import test_images


class AbstractTestAbstractTapImage(
    test_images.AbstractTestAbstractImageData,
):
    def test_axis_tap_x(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.axis_tap_x
        assert isinstance(result, str)
        assert result in a.outputs.shape

    def test_axis_tap_y(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.axis_tap_y
        assert isinstance(result, str)
        assert result in a.outputs.shape

    def test_tap(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.tap
        for ax in result:
            assert isinstance(ax, str)
            assert isinstance(result[ax], na.AbstractScalarArray)

    def test_label(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.label
        for s in result.ndarray.flat:
            assert isinstance(s, str)

    def test_where_blank(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.where_blank()
        assert result.sum() == a.sensor.num_blank

    def test_where_overscan(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.where_overscan()
        assert result.sum() == a.sensor.num_overscan

    def test_bias(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.bias()
        assert na.unit(result.outputs) == na.unit(a.outputs)
        assert result.shape[a.axis_tap_x] == a.shape[a.axis_tap_x]
        assert result.shape[a.axis_tap_y] == a.shape[a.axis_tap_y]

    def test_unbiased(self, a: msfc_ccd.abc.AbstractTapData):
        result = a.unbiased
        assert isinstance(result, msfc_ccd.TapData)
        assert na.unit(result.outputs) == na.unit(a.outputs)
        assert np.abs(result.outputs.mean()) < 1

    def test_active(self, a: msfc_ccd.abc.AbstractTapData):
        num_nap = a.sensor.num_blank + a.sensor.num_overscan
        result = a.active
        assert isinstance(result, msfc_ccd.TapData)
        assert result.shape[a.axis_x] == a.shape[a.axis_x] - num_nap
        assert result.shape[a.axis_y] == a.shape[a.axis_y]


@pytest.mark.parametrize(
    argnames="a",
    argvalues=[
        msfc_ccd.fits.open(msfc_ccd.samples.path_dark_esis1).taps(),
    ],
)
class TestTapImage(
    AbstractTestAbstractTapImage,
):
    pass
