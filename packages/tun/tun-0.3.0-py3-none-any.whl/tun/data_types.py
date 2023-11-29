from typing import TypeVar, Type, Union, Any

import numpy as np
import numpy.typing as npt
import pint.facets

# Type aliases
# We explicitly narrow down pint's internal Scalar and Magnitude types
# to be typing-compatible with numpy
Scalar = Union[float, int, np.number]
Array = npt.NDArray[np.number]
Magnitude = Union[Scalar, Array]
PintQuantity = pint.facets.plain.quantity.PlainQuantity

# TypeVars
ParamDataT = TypeVar("ParamDataT", bound=npt.ArrayLike)
ParamDataType = Type[ParamDataT]
ParamValue = Union[ParamDataT, PintQuantity]
