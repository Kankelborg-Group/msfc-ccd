import abc
import dataclasses
import named_arrays as na
from .._sensors import AbstractSensor
from ._vectors import ImageHeader

__all__ = []


@dataclasses.dataclass(eq=False, repr=False)
class AbstractImageData(
    na.FunctionArray[
        ImageHeader,
        na.AbstractScalarArray,
    ],
):
    """
    An interface for image-like data.

    This class is useful for a single interface for data from the entire image
    sensor and for data from only a single tap on the sensor.
    """

    @property
    @abc.abstractmethod
    def axis_x(self) -> str:
        """
        The name of the logical axis representing the horizontal dimension of
        the images.
        """

    @property
    @abc.abstractmethod
    def axis_y(self) -> str:
        """
        The name of the logical axis representing the vertical dimension of
        the images.
        """

    @property
    def num_x(self) -> int:
        """
        The number of pixels along the x-axis.
        """
        return self.outputs.shape[self.axis_x]

    @property
    def num_y(self) -> int:
        """
        The number of pixels along the y-axis.
        """
        return self.outputs.shape[self.axis_y]

    @property
    @abc.abstractmethod
    def sensor(self) -> AbstractSensor:
        """
        A model of the sensor used to capture these images.
        """
