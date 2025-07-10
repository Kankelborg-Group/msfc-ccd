import pytest
import astropy.units as u
import msfc_ccd


class AbstractTestAbstractSensor:

    def test_num_tap_x(self, sensor: msfc_ccd.abc.AbstractSensor):
        result = sensor.num_tap_x
        print(f"{result + 1=}")
        assert result == 2

    def test_num_tap_y(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert sensor.num_tap_y == 2

    def test_width_pixel(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert sensor.width_pixel > 0 * u.um

    def test_num_inactive(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert isinstance(sensor.num_inactive, int)
        assert sensor.num_inactive > 0

    def test_num_overscan(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert isinstance(sensor.num_overscan, int)
        assert sensor.num_overscan > 0


@pytest.mark.parametrize(
    argnames="sensor",
    argvalues=[
        msfc_ccd.TeledyneCCD230,
    ],
)
class TestTeledyneCCD230(
    AbstractTestAbstractSensor,
):
    pass
