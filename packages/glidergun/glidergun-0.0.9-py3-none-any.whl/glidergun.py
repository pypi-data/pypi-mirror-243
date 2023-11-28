""" Map Algebra with NumPy and Rasterio """
import dataclasses
import IPython
import numpy
import rasterio
from base64 import b64encode
from dataclasses import dataclass
from io import BytesIO
from matplotlib import pyplot
from numpy import arctan, arctan2, cos, gradient, ndarray, pi, sin, sqrt
from numpy.lib.stride_tricks import as_strided
from rasterio.coords import BoundingBox
from rasterio.crs import CRS
from rasterio.transform import Affine
from typing import Any, Callable, Literal, Optional, Union

Cmap = Literal[
    "Accent",
    "afmhot",
    "autumn",
    "binary",
    "Blues",
    "bone",
    "BrBG",
    "brg",
    "BuGn",
    "BuPu",
    "bwr",
    "cividis",
    "CMRmap",
    "cool",
    "coolwarm",
    "copper",
    "cubehelix",
    "Dark2",
    "flag",
    "gist_earth",
    "gist_gray",
    "gist_heat",
    "gist_ncar",
    "gist_rainbow",
    "gist_stern",
    "gist_yarg",
    "GnBu",
    "gnuplot",
    "gnuplot2",
    "gray",
    "Greens",
    "Greys",
    "hot",
    "hsv",
    "inferno",
    "jet",
    "magma",
    "nipy_spectral",
    "ocean",
    "Oranges",
    "OrRd",
    "Paired",
    "Pastel1",
    "Pastel2",
    "pink",
    "PiYG",
    "plasma",
    "PRGn",
    "prism",
    "PuBu",
    "PuBuGn",
    "PuOr",
    "PuRd",
    "Purples",
    "rainbow",
    "RdBu",
    "RdGy",
    "RdPu",
    "RdYlBu",
    "RdYlGn",
    "Reds",
    "seismic",
    "Set1",
    "Set2",
    "Set3",
    "Spectral",
    "spring",
    "summer",
    "tab10",
    "tab20",
    "tab20b",
    "tab20c",
    "terrain",
    "turbo",
    "twilight",
    "twilight_shifted",
    "viridis",
    "winter",
    "Wistia",
    "YlGn",
    "YlGnBu",
    "YlOrBr",
    "YlOrRd",
]

Dtype = Literal[
    "float32",
    "float64",
    "int8",
    "int16",
    "int32",
    "int64",
    "uint8",
    "uint16",
    "uint32",
    "uint64",
]

Operand = Union["Grid", float, int]


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
    nodata: Optional[float]
    _cmap: Cmap

    @classmethod
    def read_from(cls, file: str, band: int = 1):
        with rasterio.open(file) as dataset:
            data = dataset.read(band)

            if dataset.nodata is not None:
                data = numpy.where(data == dataset.nodata, numpy.nan, data)

            return cls(
                dataset.dtypes[0],
                dataset.bounds,
                dataset.crs,
                dataset.height,
                dataset.width,
                dataset.transform,
                data,
                numpy.nanmin(data),
                numpy.nanmax(data),
                dataset.nodata,
                "gray",
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
            numpy.nanmin(data),
            numpy.nanmax(data),
            self.nodata,
            self._cmap,
        )

    def _data(self, n: Operand):
        if isinstance(n, Grid):
            return n.data
        return n

    def __add__(self, n: Operand):
        return self._create(self.data + self._data(n))

    __radd__ = __add__

    def __sub__(self, n: Operand):
        return self._create(self.data - self._data(n))

    def __rsub__(self, n: Operand):
        return self._create(self._data(n) - self.data)

    def __mul__(self, n: Operand):
        return self._create(self.data * self._data(n))

    __rmul__ = __mul__

    def __pow__(self, n: Operand):
        return self._create(self.data ** self._data(n))

    def __rpow__(self, n: Operand):
        return self._create(self._data(n) ** self.data)

    def __truediv__(self, n: Operand):
        return self._create(self.data / self._data(n))

    def __rtruediv__(self, n: Operand):
        return self._create(self._data(n) / self.data)

    def __floordiv__(self, n: Operand):
        return self._create(self.data // self._data(n))

    def __rfloordiv__(self, n: Operand):
        return self._create(self._data(n) // self.data)

    def __mod__(self, n: Operand):
        return self._create(self.data % self._data(n))

    def __rmod__(self, n: Operand):
        return self._create(self._data(n) % self.data)

    def __lt__(self, n: Operand):
        return self._create(self.data < self._data(n))

    def __gt__(self, n: Operand):
        return self._create(self.data > self._data(n))

    __rlt__ = __gt__

    __rgt__ = __lt__

    def __le__(self, n: Operand):
        return self._create(self.data <= self._data(n))

    def __ge__(self, n: Operand):
        return self._create(self.data >= self._data(n))

    __rle__ = __ge__

    __rge__ = __le__

    def __eq__(self, n: Operand):
        return self._create(self.data == self._data(n))

    __req__ = __eq__

    def __ne__(self, n: Operand):
        return self._create(self.data != self._data(n))

    __rne__ = __ne__

    def __and__(self, n: Operand):
        return self._create(self.data & self._data(n))

    __rand__ = __and__

    def __or__(self, n: Operand):
        return self._create(self.data | self._data(n))

    __ror__ = __or__

    def __xor__(self, n: Operand):
        return self._create(self.data ^ self._data(n))

    def __rxor__(self, n: Operand):
        return self._create(self._data(n) ^ self.data)

    def __rshift__(self, n: Operand):
        return self._create(self.data >> self._data(n))

    def __lshift__(self, n: Operand):
        return self._create(self.data << self._data(n))

    __rrshift__ = __lshift__

    __rlshift__ = __rshift__

    def __neg__(self):
        return self._create(-1 * self.data)

    def __pos__(self):
        return self._create(1 * self.data)

    def __repr__(self):
        return f"{self.width} x {self.height} {self.dtype} ({self.min:.3f} ~ {self.max:.3f}) {self.crs}"

    def con(self, trueValue: Union["Grid", int, float], falseValue):
        return self.local(
            lambda data: numpy.where(
                data, self._data(trueValue), self._data(falseValue)
            )
        )

    def local(self, func: Callable[[ndarray], ndarray]):
        return self._create(func(self.data))

    def focal(self, func: Callable[[ndarray], Any], buffer: int = 1):
        row = numpy.empty((buffer, self.width))
        row[:] = numpy.nan
        col = numpy.empty((self.height + buffer + buffer, buffer))
        col[:] = numpy.nan

        array = numpy.hstack([col, numpy.vstack([row, self.data, row]), col])
        window = (2 * buffer + 1, 2 * buffer + 1)
        shape = tuple(numpy.subtract(array.shape, window) + 1) + window
        strided = as_strided(array, shape, array.strides * 2)

        return self._create(numpy.array([list(map(func, block)) for block in strided]))

    def aspect(self):
        x, y = gradient(self.data)
        return self._create(arctan2(-x, y))

    def slope(self):
        x, y = gradient(self.data)
        return self._create(pi / 2.0 - arctan(sqrt(x * x + y * y)))

    def hillshade(self, azimuth: float = 315, altitude: float = 45):
        azimuth = azimuth * pi / 180.0
        altitude = altitude * pi / 180.0

        slope = self.slope().data
        aspect = self.aspect().data

        shaded = sin(altitude) * sin(slope) + cos(altitude) * cos(slope) * cos(
            azimuth - aspect
        )

        return self._create((255 * (shaded + 1) / 2)).to_int16()

    def cmap(self, cmap: Cmap):
        return dataclasses.replace(self, _cmap=cmap)

    def change_type(self, dtype: Dtype):
        return self.local(lambda data: numpy.asanyarray(data, dtype=dtype))

    def to_int16(self):
        return self.round().change_type("int16")

    def to_int32(self):
        return self.round().change_type("int32")

    def to_int64(self):
        return self.round().change_type("int64")

    def abs(self):
        return self.local(numpy.abs)

    def round(self, decimals: int = 0):
        return self.local(lambda data: numpy.round(data, decimals))

    def write_to(self, file: str, driver: str = "GTiff", dtype: Optional[Dtype] = None):
        with rasterio.open(
            file,
            "w",
            driver=driver,
            height=self.height,
            width=self.width,
            count=1,
            crs=self.crs,
            transform=self.transform,
            dtype=dtype or self.data.dtype,
            nodata=self.nodata,
        ) as dataset:
            dataset.write(self.data, 1)
            return self


ipython = IPython.get_ipython()  # type: ignore

if ipython:

    def html(grid: Grid):
        with BytesIO() as buffer:
            figure = pyplot.figure(frameon=False)
            axes = figure.add_axes((0, 0, 1, 1))
            axes.axis("off")
            pyplot.imshow(grid.data, cmap=grid._cmap)
            pyplot.savefig(buffer)
            pyplot.close(figure)
            image = b64encode(buffer.getvalue()).decode()
            return f'<div>{grid}</div><img src="data:image/png;base64, {image}" />'

    formatter = ipython.display_formatter.formatters["text/html"]  # type: ignore
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
