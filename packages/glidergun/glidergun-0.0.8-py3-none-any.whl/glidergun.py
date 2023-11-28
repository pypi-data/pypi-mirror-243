""" Map Algebra in Python with Rasterio and Numpy. """
import base64
import io
import IPython
import numpy
import rasterio
from dataclasses import dataclass
from matplotlib import pyplot
from numpy import ndarray
from numpy.lib.stride_tricks import as_strided
from rasterio.coords import BoundingBox
from rasterio.crs import CRS
from rasterio.transform import Affine
from typing import Any, Callable


@dataclass(frozen=True)
class Grid:
    dtype: str
    bounds: BoundingBox
    crs: CRS
    height: int
    width: int
    transform: Affine
    data: ndarray
    min: float
    max: float

    @classmethod
    def read(cls, file: str, band: int = 1):
        with rasterio.open(file) as dataset:
            data = dataset.read(band)
            return cls(
                dataset.dtypes[0],
                dataset.bounds,
                dataset.crs,
                dataset.height,
                dataset.width,
                dataset.transform,
                data,
                data.min(),
                data.max(),
            )

    def _create(self, data: ndarray):
        return Grid(
            data.dtype,
            self.bounds,
            self.crs,
            data.shape[0],
            data.shape[1],
            self.transform,
            data,
            data.min(),
            data.max(),
        )

    def _data(self, n):
        if isinstance(n, Grid):
            return n.data
        return n

    def __add__(self, n):
        return self._create(self.data + self._data(n))

    __radd__ = __add__

    def __sub__(self, n):
        return self._create(self.data - self._data(n))

    def __rsub__(self, n):
        return self._create(self._data(n) - self.data)

    def __mul__(self, n):
        return self._create(self.data * self._data(n))

    __rmul__ = __mul__

    def __pow__(self, n):
        return self._create(self.data ** self._data(n))

    def __rpow__(self, n):
        return self._create(self._data(n) ** self.data)

    def __truediv__(self, n):
        return self._create(self.data / self._data(n))

    def __rtruediv__(self, n):
        return self._create(self._data(n) / self.data)

    def __floordiv__(self, n):
        return self._create(self.data // self._data(n))

    def __rfloordiv__(self, n):
        return self._create(self._data(n) // self.data)

    def __mod__(self, n):
        return self._create(self.data % self._data(n))

    def __rmod__(self, n):
        return self._create(self._data(n) % self.data)

    def __lt__(self, n):
        return self._create(self.data < self._data(n))

    def __gt__(self, n):
        return self._create(self.data > self._data(n))

    __rlt__ = __gt__

    __rgt__ = __lt__

    def __lte__(self, n):
        return self._create(self.data <= self._data(n))

    def __gte__(self, n):
        return self._create(self.data >= self._data(n))

    __rlte__ = __gte__

    __rgte__ = __lte__

    def __eq__(self, n):
        return self._create(self.data == self._data(n))

    __req__ = __eq__

    def __ne__(self, n):
        return self._create(self.data != self._data(n))

    __rne__ = __ne__

    def __and__(self, n):
        return self._create(self.data & self._data(n))

    __rand__ = __and__

    def __or__(self, n):
        return self._create(self.data | self._data(n))

    __ror__ = __or__

    def __invert__(self):
        return self._create(~self.data)

    def __neg__(self):
        return self._create(-1 * self.data)

    def __pos__(self):
        return self._create(self.data)

    def __repr__(self):
        return f"{self.width} x {self.height} {self.dtype} ({self.min:.2f} ~ {self.max:.2f}) {self.crs}"

    def _base64(self):
        with io.BytesIO() as buffer:
            figure = pyplot.figure(frameon=False)
            axes = figure.add_axes((0, 0, 1, 1))
            axes.axis("off")
            pyplot.imshow(self.data, cmap="gray")
            pyplot.savefig(buffer)
            pyplot.close(figure)
            return base64.b64encode(buffer.getvalue()).decode()

    def focal(self, func: Callable[[ndarray], Any], buffer: int = 1):
        row = numpy.zeros((buffer, self.width))
        col = numpy.zeros((self.height + buffer + buffer, buffer))
        array = numpy.hstack([col, numpy.vstack([row, self.data, row]), col])
        window = (2 * buffer + 1, 2 * buffer + 1)
        shape = tuple(numpy.subtract(array.shape, window) + 1) + window
        strided = as_strided(array, shape, array.strides * 2)
        return self._create(numpy.array([list(map(func, row)) for row in strided]))


ipython = IPython.get_ipython()  # type: ignore

if ipython:

    def html(grid):
        return f'<div>{grid}</div><img src="data:image/png;base64, {grid._base64()}" />'

    # type: ignore
    formatter = ipython.display_formatter.formatters["text/html"]
    formatter.for_type(Grid, html)
    formatter.for_type(
        tuple,
        lambda grids: f"""
            <table>
                <tr style="text-align: left">
                    {"".join(f"<td>{html(grid)}</td>" for grid in grids)}
                </tr>
            </table>
        """
        if all(isinstance(grid, Grid) for grid in grids)
        else f"{grids}",
    )
