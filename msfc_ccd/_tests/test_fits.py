import pytest
import pathlib
import numpy as np
import named_arrays as na
import msfc_ccd


@pytest.mark.parametrize(
    argnames="path",
    argvalues=[
        msfc_ccd.samples.path_fe55_esis1,
        na.ScalarArray(
            ndarray=np.array(
                [
                    msfc_ccd.samples.path_fe55_esis1,
                    msfc_ccd.samples.path_fe55_esis3,
                ]
            ),
            axes="time",
        ),
    ],
)
def test_open(path: str | pathlib.Path | na.AbstractScalarArray):
    result = msfc_ccd.fits.open(path)
    assert isinstance(result, msfc_ccd.SensorData)
    assert result.data.sum() != 0
