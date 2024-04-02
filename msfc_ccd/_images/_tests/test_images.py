import numpy as np
import astropy.units as u
import astropy.time
import named_arrays as na
import optika._tests.test_mixins
import msfc_ccd


class AbstractTestAbstractImageData(
    optika._tests.test_mixins.AbstractTestPrintable,
):

    def test_data(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.data
        assert result.ndim >= 2

    def test_pixel(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.pixel
        for ax in result:
            assert isinstance(ax, str)
            assert isinstance(result[ax], na.AbstractScalarArray)

    def test_axis_x(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.axis_x
        assert isinstance(result, str)
        assert result in a.data.shape

    def test_axis_y(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.axis_y
        assert isinstance(result, str)
        assert result in a.data.shape

    def test_num_x(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.num_x
        assert isinstance(result, int)

    def test_num_y(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.num_y
        assert isinstance(result, int)

    def test_time(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.time
        if not isinstance(result, astropy.time.Time):
            assert isinstance(result.ndarray, astropy.time.Time)

    def test_timedelta(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.timedelta
        assert np.all(result >= 1 * u.s)
        assert np.all(result < 1000 * u.s)

    def test_timedelta_requested(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.timedelta
        assert np.all(result >= 1 * u.s)
        assert np.all(result < 1000 * u.s)

    def test_serial_number(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.serial_number
        assert isinstance(result, (str, na.AbstractScalar))

    def test_run_mode(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.run_mode
        assert isinstance(result, (str, na.AbstractScalar))

    def test_status(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.status
        assert isinstance(result, (str, na.AbstractScalar))

    def test_voltage_fpga_vccint(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.voltage_fpga_vccint
        assert np.all(result >= 0 * u.V)
        assert np.all(result < 50 * u.V)

    def test_voltage_fpga_vccaux(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.voltage_fpga_vccaux
        assert np.all(result >= 0 * u.V)
        assert np.all(result < 50 * u.V)

    def test_voltage_fpga_vccbram(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.voltage_fpga_vccbram
        assert np.all(result >= 0 * u.V)
        assert np.all(result < 50 * u.V)

    def test_temperature_fpga(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.temperature_fpga
        assert np.all(result >= 0 * u.deg_C)
        assert np.all(result < 100 * u.deg_C)

    def test_temperature_adc_1(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.temperature_adc_1
        assert np.all(result >= 0 * u.deg_C)
        assert np.all(result < 100 * u.deg_C)

    def test_temperature_adc_2(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.temperature_adc_2
        assert np.all(result >= 0 * u.deg_C)
        assert np.all(result < 100 * u.deg_C)

    def test_temperature_adc_3(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.temperature_adc_3
        assert np.all(result >= 0 * u.deg_C)
        assert np.all(result < 100 * u.deg_C)

    def test_temperature_adc_4(self, a: msfc_ccd.abc.AbstractImageData):
        result = a.temperature_adc_4
        assert np.all(result >= 0 * u.deg_C)
        assert np.all(result < 100 * u.deg_C)
