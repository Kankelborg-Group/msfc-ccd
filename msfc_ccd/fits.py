"""
Utilities for working with FITS files.
"""

import pathlib
import named_arrays as na
import msfc_ccd


__all__ = [
    "open",
]


def open(
    path: str | pathlib.Path | na.AbstractScalarArray,
    axis_x: str = "detector_x",
    axis_y: str = "detector_y",
) -> msfc_ccd.SensorData:
    """
    Load an image from a given FITS file path, or an array of images from
    a given array of FITS file paths.

    This is a convenience function for :meth:`msfc_ccd.SensorData.from_fits`.

    Parameters
    ----------
    path
        Either a single path or an array of paths pointing to the FITS files
        to open.
    axis_x
        The name of the logical axis representing the horizontal dimension of
        the images.
    axis_y
        The name of the logical axis representing the vertical dimension of
        the images.

    Examples
    --------

    Load and display a single FITS file.

    .. jupyter-execute::

        import matplotlib.pyplot as plt
        import named_arrays as na
        import msfc_ccd

        # Define the x and y axes of the detector
        axis_x = "detector_x"
        axis_y = "detector_y"

        # Load the sample image
        image = msfc_ccd.fits.open(
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

    |

    Load and display an array of two FITS files.

    .. jupyter-execute::

        import numpy as np
        import named_arrays as na
        import msfc_ccd

        # Define the x and y axes of the detector
        axis_x = "detector_x"
        axis_y = "detector_y"

        # Define an arbitrary third axis representing two different exposures
        axis_time = "time"

        # Define the array of two sample FITS files
        path = na.ScalarArray(
            ndarray=np.array([
                msfc_ccd.samples.path_fe55_esis1,
                msfc_ccd.samples.path_fe55_esis3,
            ]),
            axes=axis_time,
        )

        # Load the sample images
        image = msfc_ccd.fits.open(
            path=path,
            axis_x=axis_x,
            axis_y=axis_y,
        )

        # Display the sample images
        fig, axs = na.plt.subplots(
            axis_rows=axis_time,
            nrows=image.data.shape[axis_time],
            sharex=True,
            constrained_layout=True,
        )
        im = na.plt.imshow(
            image.data,
            axis_x=axis_x,
            axis_y=axis_y,
            ax=axs,
        );
    """
    return msfc_ccd.SensorData.from_fits(
        path=path,
        axis_x=axis_x,
        axis_y=axis_y,
    )
