import dataclasses
import importlib.resources
import typing
import warnings
from typing import Generic, Optional, Type, Union

import numpy as np
import pint
import pint.facets
import pint_pandas

from . import errors
from .data_types import (
    Array,
    Magnitude,
    PintQuantity as PintQuantityType,
    ParamDataT,
    ParamDataType,
    ParamValue,
)
from .quantity_types import QuantityType
from .unit_types import UnitsT


# Global Pint UnitRegistry, settings and classes
UNITS_DEFINITIONS_FILE = importlib.resources.files(__package__).joinpath(
    "pint_units.txt"
)
ureg = pint.UnitRegistry(
    default_as_delta=True,
    autoconvert_offset_to_baseunit=True,
    auto_reduce_dimensions=True,
    system="SI",
    cache_folder=":auto:",
)
with importlib.resources.as_file(UNITS_DEFINITIONS_FILE) as def_path:
    ureg.load_definitions(def_path)
pint_pandas.PintType.ureg = ureg  # Use global UnitsRegistry for new instances
ureg.default_format = "~"  # Short, not pretty (e.g. '1.5e-3 m ** 2')
PintQuantity = ureg.Quantity


class Quantity(Generic[UnitsT]):
    """
    A units and type-aware physical quantity
    """

    CAST_TYPE = float

    @classmethod
    def as_dataclass_field(
        cls,
        quantity_type: Type[QuantityType],
        description: str = "",
        default_magnitude: Optional[Magnitude] = None,
        default_units: Optional[UnitsT] = None,
    ):
        """
        Return a dataclasses field with a default.
        Use this instead of passing objects of this class as or initializing it in field defaults directly.
        If the normal constructor (__init__) is used for a default value inside a dataclass,
        the identical object is referred in all instances of the dataclass.
        :param quantity_type: Type of the quantity e.g., 'Power'.
        :param description: Description of the quantity.
        :param default_magnitude: Default magnitude of the quantity.
        :param default_units: Default units of the quantity. Must be always
                              applied, if default_magnitude is set.
        :return: The dataclass field
        """
        return dataclasses.field(
            default_factory=lambda: cls(
                quantity_type=quantity_type,
                description=description,
                default_magnitude=default_magnitude,
                default_units=default_units,
            )
        )

    def __init__(
        self,
        quantity_type: Type[QuantityType],
        description: str = "",
        default_magnitude: Optional[Magnitude] = None,
        default_units: Optional[UnitsT] = None,
    ):
        """
        :param quantity_type: Type of the quantity e.g., 'Power'.
        :param description: Description of the quantity.
        :param default_magnitude: Default magnitude of the quantity.
            Must be given together with default_units.
        :param default_units: Default units of the quantity.
            Must be given together with default_magnitude.
        """
        self._quantity: Optional[PintQuantityType] = None
        self.quantityType: Type[QuantityType] = quantity_type
        self.description: str = description

        # Try initializing the value with given defaults
        if (default_magnitude is not None) or (default_units is not None):
            if (default_magnitude is not None) and (default_units is not None):
                self.set(magnitude=default_magnitude, units=default_units)
            else:
                msg = (
                    f"To set a default value for Quantity, you must give"
                    f" BOTH default_magnitude and default_units."
                )
                warnings.warn(msg)

    def __repr__(self):
        return f"Quantity({self._quantity})"

    @property
    def quantity(self) -> Optional[PintQuantityType]:
        """
        Getter for the quantity
        :return: The quantity
        """
        if self._quantity is None:
            msg = (
                f"Value of this quantity is accessed before it "
                f"was set and no default value is available."
            )
            warnings.warn(msg)
        return self._quantity

    @quantity.setter
    def quantity(self, quantity_: PintQuantityType):
        """
        Set the quantity.
        Check for units compatibility.
        :param quantity_: The quantity to set
        """
        try:
            # Cast quantity's magnitude to defined data_type
            quantity_ = PintQuantity(
                self.CAST_TYPE(quantity_.magnitude), quantity_.units
            )
        except ValueError:
            if not isinstance(quantity_.magnitude, self.CAST_TYPE):
                msg = (
                    f"Type of the given quantity ({type(quantity_.magnitude)})"
                    " is not compatible with the defined data type"
                    f" ({self.CAST_TYPE})."
                )
                raise errors.QuantityValueError(msg)
            else:
                raise
        try:
            # Convert to internal unit
            self._quantity = quantity_.to(self.quantityType.internal_units)  # type: ignore[misc]
        except pint.errors.DimensionalityError as err:
            msg = (
                f"Unit of the given quantity ('{err.units1}' {err.dim1}) "
                "does not fit to the predefined quantity unit "
                f"('{err.units2}' {err.dim2})."
            )
            raise errors.QuantityUnitsError(msg)

    def set(self, magnitude: Magnitude, units: UnitsT):
        """
        Set a quantity value by declaring magnitude and units
        :param magnitude: Magnitude of the quantity
        :param units: Units of the quantity
        """
        self.quantity = PintQuantity(magnitude, units)

    def magnitude(self, units: UnitsT) -> Magnitude:
        """
        Return the magnitude of the quantity in given units
        :param units: Units in which the magnitude should be returned.
            If None, the default unit will be used.
        :return: Magnitude of the quantity
        """
        if self.quantity is not None:
            try:
                magnitude = self.quantity.m_as(units=units)
            except pint.errors.DimensionalityError as err:
                msg = (
                    f"Demanded unit ('{err.units2}'{err.dim2}) "
                    "does not fit to the predefined quantity units "
                    f"('{err.units1}'{err.dim1})."
                )
                raise errors.QuantityUnitsError(msg)
        else:
            magnitude = self.quantity
        return magnitude

    @property
    def internal_magnitude(self) -> Magnitude:
        """
        Return the magnitude of the quantity as internal units.
        """
        return self.magnitude(units=self.quantityType.internal_units)  # type: ignore[misc]

    @property
    def display_magnitude(self) -> Magnitude:
        """
        Return the magnitude of the quantity as default display units.
        If the quantity type does not define default display units,
        the magnitude is returned as internal units.
        """
        if self.quantityType.default_display_units is None:
            display_magnitude = self.internal_magnitude
        else:
            display_magnitude = self.magnitude(
                units=self.quantityType.default_display_units
            )
        return display_magnitude


class VectorQuantity(Quantity[UnitsT]):
    """
    A vector of unit-aware quantities
    """

    @classmethod
    def as_dataclass_field(
        cls,
        quantity_type: Type[QuantityType],
        description: str = "",
        default_magnitude: Optional[Magnitude] = None,
        default_units: Optional[UnitsT] = None,
    ):
        """
        Return a dataclasses field with a default.
        Use this instead of passing objects of this class as or initializing it in field defaults directly.
        If the normal constructor (__init__) is used for a default value inside a dataclass,
        the identical object is referred in all instances of the dataclass.
        :param quantity_type: Type of the quantity e.g., 'Power'.
        :param description: Description of the quantity.
        :param default_magnitude: Default list of magnitudes of the vector.
        :param default_units: Default units of the vector. Must be always
                              applied, if default_magnitude is set.
        """
        return dataclasses.field(
            default_factory=lambda: cls(
                quantity_type=quantity_type,
                description=description,
                default_magnitude=default_magnitude,
                default_units=default_units,
            )
        )

    def __init__(
        self,
        quantity_type: Type[QuantityType],
        description: str = "",
        default_magnitude: Optional[Magnitude] = None,
        default_units: Optional[UnitsT] = None,
    ):
        """
        :param quantity_type: Type of the quantity e.g., 'Power'.
        :param description: Description of the quantity.
        :param default_magnitude: Default list of magnitudes of the vector.
        :param default_units: Default units of the vector. Must be always
                              applied, if default_magnitude is set.
        """
        super().__init__(
            quantity_type=quantity_type,
            description=description,
            default_magnitude=default_magnitude,
            default_units=default_units,
        )

    def __repr__(self):
        return f"VectorQuantity({self._quantity})"

    def set(self, magnitude: Magnitude, units: UnitsT):
        """
        Set a quantity as a pint list by declaring magnitudes list and units
        :param magnitude: List of magnitudes of the vector
        :param units: Units of the vector
        """
        super().set(magnitude=magnitude, units=units)

    @property
    def quantity(self) -> Optional[PintQuantityType]:
        """
        Getter for the quantity
        :return: The quantity
        """
        return super().quantity

    @quantity.setter
    def quantity(self, quantity_: PintQuantityType):
        """
        Set the vector value.
        Check for units compatibility.
        :param quantity_: The quantity to set
        """
        try:
            # Cast value's magnitude to defined data_type
            quantity_ = PintQuantity(
                quantity_.magnitude.astype(self.CAST_TYPE), quantity_.units
            )
        except (ValueError, AttributeError):
            msg = (
                f"Type of the given value ({repr(quantity_)}) is "
                f"not compatible with the defined data type ({Array},"
                " i.e. 'an array of numbers')."
            )
            if not isinstance(quantity_.magnitude, np.ndarray):
                raise errors.QuantityValueError(msg)
            elif not isinstance(quantity_.magnitude.dtype, np.number):
                raise errors.QuantityValueError(msg)
            else:
                raise

        try:
            # Convert to internal unit
            self._quantity: PintQuantityType = quantity_.to(self.quantityType.internal_units)  # type: ignore[misc]
        except pint.errors.DimensionalityError as err:
            msg = (
                f"Unit of the given value ('{err.units1}' {err.dim1}) "
                "does not fit to the predefined quantity unit "
                f"('{err.units2}' {err.dim2})."
            )
            raise errors.QuantityUnitsError(msg)


class Parameter(Generic[ParamDataT, UnitsT]):
    """
    A scalar parameter with either a unit-naive basic value or a unit-aware quantity value
    """

    def __init__(
        self,
        data_type: ParamDataType,
        quantity_type: Optional[Type[QuantityType[UnitsT]]] = None,
        description: str = "",
        default_magnitude: Optional[ParamDataT] = None,
        default_units: Optional[UnitsT] = None,
        value_comment: str = "",
    ):
        """
        :param data_type: Data type of the parameter.
        :param quantity_type: Type of the parameter's quantity e.g., 'Power'.
            A given quantity type's data type will override the given data type.
        :param description: Description of the parameter/quantity.
        :param default_magnitude: Default magnitude of the quantity.
            Must be given together with default_units.
        :param default_units: Default units of the quantity.
            Must be given together with default_magnitude.
        :param value_comment: Comment for the given default quantity value
            (e.g. a reference)
        """
        self.dataType: ParamDataType
        self.quantityType: Optional[Type[QuantityType]] = quantity_type
        # The value of a units-aware parameter
        self._quantity: Optional[Quantity[UnitsT]]
        if quantity_type is None:
            self.dataType = data_type
            self._quantity = None
        else:
            self.dataType = Quantity.CAST_TYPE
            self._quantity = Quantity(
                quantity_type=quantity_type, description=description
            )

        # The value of a units-naive parameter
        self._naive_value: Optional[ParamDataT] = None
        self.description: str = description
        self.valueComment: str = ""

        # Try initializing the value with given defaults
        if (default_magnitude is not None) or (default_units is not None):
            if (default_magnitude is not None) and (default_units is not None):
                self.set_magnitude_units(
                    magnitude=default_magnitude,
                    units=default_units,
                    value_comment=value_comment,
                )
            else:
                msg = (
                    f"To set a default value for Quantity, you must give"
                    f" BOTH default_magnitude and default_units."
                )
                warnings.warn(msg)

    @property
    def is_units_naive(self) -> bool:
        return self.quantityType is None

    @property
    def is_units_aware(self) -> bool:
        return not self.is_units_naive

    @property
    def value(self) -> Union[ParamDataT, Optional[PintQuantityType]]:
        """
        Return the parameter value, i.e.
        a units-naive value in case of a units-naive parameter or
        a pint quantity in case of a units-aware parameter
        :return: The parameter value
        """
        if self.is_units_aware:
            return self.quantity
        else:
            return self._naive_value

    @value.setter
    def value(self, value_: ParamValue):
        """
        Set the parameter value, i.e.
        a units-naive value in case of a units-naive parameter or
        a pint quantity in case of a units-aware parameter
        :param value_: The parameter value
        """
        if self.is_units_naive:
            # Allow setting to None
            if value_ is None:
                self._naive_value = value_
            else:
                if not isinstance(value_, self.dataType):
                    msg = (
                        f"Cannot set {repr(value_)} as parameter value"
                        f" as it is not an instance of {self.dataType}."
                    )
                    raise errors.ParameterValueError(msg)
                self._naive_value = self.dataType(value_)
        else:
            if not isinstance(value_, PintQuantityType):
                msg = (
                    f"Cannot set {repr(value_)} as value for units-aware"
                    " parameter. Please give a pint quantity as value."
                )
                raise errors.ParameterValueError(msg)
            self.quantity = value_

    def _raise_on_units_naive_quantity(self):
        """
        Raise an exception if a quantity of a units-naive parameter
        is being accessed
        """
        if self.is_units_naive:
            err_msg = (
                "Cannot access quantity of units-naive parameter."
                " Please use Parameter.value."
            )
            raise errors.ParameterError(err_msg)

    @property
    def quantity(self) -> Optional[PintQuantityType]:
        """
        Return the underlying quantity value (if the parameter is units-aware)
        :return: The quantity
        """
        self._raise_on_units_naive_quantity()
        assert self._quantity is not None
        return self._quantity.quantity

    @quantity.setter
    def quantity(self, quantity_: PintQuantityType):
        """
        Set the underlying quantity value (if the parameter is units-aware)
        """
        self._raise_on_units_naive_quantity()
        assert self._quantity is not None
        self._quantity.quantity = quantity_

    def set_magnitude_units(
        self,
        magnitude: ParamDataT,
        units: UnitsT,
        value_comment: Optional[str] = None,
    ):
        """
        Set the parameter's quantity value by declaring magnitude and units
        :param magnitude: Magnitude to be set
        :param units: Units for the magnitude
        :param value_comment: Comment for the quantity value (e.g. a reference)
        """
        self._raise_on_units_naive_quantity()
        assert self._quantity is not None
        magnitude_ = typing.cast(Magnitude, magnitude)
        self._quantity.set(magnitude=magnitude_, units=units)
        if value_comment is not None:
            self.valueComment = value_comment

    def _raise_on_units_naive_magnitude(self):
        """
        Raise an exception if a magnitude property of a units-naive parameter
        is being accessed
        """
        if self.is_units_naive:
            err_msg = (
                "Cannot get magnitude of units-naive parameter."
                " Please use Parameter.value."
            )
            raise errors.ParameterError(err_msg)

    def magnitude(self, units: UnitsT) -> ParamDataT:
        """
        Return the magnitude of a units-aware parameter,
        converted to given units.
        :param units: Units in which the quantity magnitude should be returned
        :return: Magnitude of the parameter
        """
        self._raise_on_units_naive_magnitude()
        assert self._quantity is not None
        magnitude = self._quantity.magnitude(units=units)
        return typing.cast(ParamDataT, magnitude)

    @property
    def internal_magnitude(self) -> ParamDataT:
        """
        Return the magnitude of a units-aware parameter,
        converted to internal units.
        """
        self._raise_on_units_naive_magnitude()
        assert self._quantity is not None
        magnitude = self._quantity.internal_magnitude
        return typing.cast(ParamDataT, magnitude)

    @property
    def display_magnitude(self) -> ParamDataT:
        """
        Return the magnitude of a units-aware parameter,
        converted to display units.
        """
        self._raise_on_units_naive_magnitude()
        assert self._quantity is not None
        magnitude = self._quantity.display_magnitude
        return typing.cast(ParamDataT, magnitude)


# ToDo @Olessya adjust comments
class VectorParameter(Parameter[ParamDataT, UnitsT]):
    """
    A vector parameter with either a unit-naive basic value or a unit-aware quantity value
    """

    CAST_TYPE = float

    def __init__(
        self,
        data_type: ParamDataType,
        quantity_type: Optional[Type[QuantityType[UnitsT]]] = None,
        description: str = "",
        default_magnitude: Optional[ParamDataT] = None,
        default_units: Optional[UnitsT] = None,
        value_comment: str = "",
    ):
        """
        :param data_type: Data type of the parameter.
        :param quantity_type: Type of the parameter's quantity e.g., 'Power'.
            A given quantity type's data type will override the given data type.
        :param description: Description of the parameter/quantity.
        :param default_magnitude: Default magnitude of the quantity.
            Must be given together with default_units.
        :param default_units: Default units of the quantity.
            Must be given together with default_magnitude.
        :param value_comment: Comment for the given default quantity value
            (e.g. a reference)
        """
        super().__init__(
            data_type=data_type,
            quantity_type=quantity_type,
            description=description,
            default_magnitude=default_magnitude,
            default_units=default_units,
            value_comment=value_comment,
        )

        # The value of a units-aware vector parameter
        if quantity_type is not None:
            self._quantity = VectorQuantity(
                quantity_type=quantity_type, description=description
            )
