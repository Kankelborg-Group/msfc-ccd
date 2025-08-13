import pytest
import astropy.units as u
import msfc_ccd


class AbstractTestAbstractSensor:

    def test_num_tap_x(self, sensor: msfc_ccd.abc.AbstractSensor):
        result = sensor.num_tap_x
        assert result == 2

    def test_num_tap_y(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert sensor.num_tap_y == 2

    def test_manufacturer(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert isinstance(sensor.manufacturer, str)

    def test_family(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert isinstance(sensor.family, str)

    def test_serial_number(self, sensor: msfc_ccd.abc.AbstractSensor):
        if sensor.serial_number is not None:
            assert isinstance(sensor.serial_number, str)

    def test_width_pixel(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert sensor.width_pixel > 0 * u.um

    def test_num_pixels(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert sensor.num_pixel.x > 0
        assert sensor.num_pixel.y > 0

    def test_num_pixels_active(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert sensor.num_pixel_active.x > 0
        assert sensor.num_pixel_active.y > 0

    def test_num_blank(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert isinstance(sensor.num_blank, int)
        assert sensor.num_blank > 0

    def test_num_overscan(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert isinstance(sensor.num_overscan, int)
        assert sensor.num_overscan > 0

    def test_readout_noise(self, sensor: msfc_ccd.abc.AbstractSensor):
        assert sensor.readout_noise > 0 * u.electron


@pytest.mark.parametrize(
    argnames="sensor",
    argvalues=[
        msfc_ccd.TeledyneCCD230(
            serial_number="42",
        ),
    ],
)
class TestTeledyneCCD230(
    AbstractTestAbstractSensor,
):
    pass
