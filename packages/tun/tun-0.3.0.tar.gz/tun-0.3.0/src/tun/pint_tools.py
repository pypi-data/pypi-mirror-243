"""
Module with interim function to compensate missing Pint functionality
"""
import typing

import pint
import warnings
import numpy as np
import pandas as pd

from scipy import interpolate  # type: ignore
from typing import Optional, Union

from . import PintQuantity


class Series:
    """
    A class with static methods for pandas.Series that
    extends the pint-pandas functionality.
    """

    @staticmethod
    def from_pint_list(pint_list: pint.Quantity) -> pd.Series:
        """
        Create a pandas series from a pint quantity list without unit stripped warning.
        :param pint_list: A list with pint quantities.
        :return: The pint list as a series.
        """
        return pd.Series(
            data=pint_list.m_as(pint_list.units),
            dtype=f"pint[{pint_list.units}]")

    @staticmethod
    def round(series: pd.Series, unit: str, decimals: int = 0) -> pd.Series:
        """
        This function is a workaround for the missing pint-series.round() functionality.
        :param series: Pint-series including the data to round.
        :param unit: String including the unit.
        :param decimals: Decimals to round.
        :return: Pint-series with rounded numbers.
        """
        series = series.pint.m_as(unit)
        series = series.round(decimals=decimals)
        return pd.Series(series, dtype=f"pint[{unit}]")


class Dataframe:
    """
    A class with static methods for pandas.Dataframe that
    extends the pint-pandas functionality.
    """

    @staticmethod
    def m_as(dataframe: pd.DataFrame, units: str):
        """
        Apply the pint 'm_as' function to a dataframe.
        :param dataframe: The dataframe.
        :param units: Pint units.
        :return: The dataframe in the given units.
        """
        dataframe_units = dataframe.astype(units)  # type: ignore[arg-type]
        with warnings.catch_warnings():
            # .pint.m_as not available for df
            warnings.simplefilter(
                action="ignore",
                category=pint.UnitStrippedWarning)
            return dataframe_units.astype("float64")


class InterpolationQuantity:
    """
    Class including an interpolation by argument in []
    """

    def __init__(self, y: pd.Series, x: Optional[pd.Series] = None, **kwargs):
        """
        :param y: Series with PintQuantities for y-axis in any unit
        :param x: Series with PintQuantities for x-axis in interpolation.
            If None, the index of y is used.
        :param kwargs: kwargs passed to interpolation function
        """
        if x is None:
            x = pd.Series(
                data=y.index,
                dtype=y.index.dtype)
        self.xUnit = x.pint.units
        self.yUnit = y.pint.units
        self.interpolationQuantity = InterpolationQuantity.\
            __quantity_interpolation(x=x.pint.magnitude, y=y.pint.magnitude,
                                     **kwargs)

    @staticmethod
    def __quantity_interpolation(x, y, **kwargs):
        """
        Internal interpolation function
        :param x: x values
        :param y: y values
        :param kwargs: kwargs passed to interp1d function
        """
        return interpolate.interp1d(
            x=x, y=y, **kwargs)

    def __getitem__(self, item: Union[pd.Series, pint.Quantity]):
        """
        :param item: X-value as PintQuantity for the interpolation
        :return: Y-value of the interpolation in PintQuantity
        """
        if isinstance(item, pd.Series):
            x = item.pint.to(self.xUnit).pint.magnitude  # type: ignore[attr-defined]
            return_series = True
        else:
            x = item.to(self.xUnit).magnitude
            return_series = False
        with np.errstate(invalid='ignore'):
            y = self.interpolationQuantity(x)
        if return_series:
            return pd.Series(data=y, dtype=f"pint[{self.yUnit}]", index=x.index)
        else:
            return PintQuantity(y, self.yUnit)


def change_unit(quantity: Union[pint.Quantity, pd.Series], unit: str):
    """
    Convert the unit of a PintQuantity or a Pint-Series
    :param quantity: PintQuantity or Series with dtype="pint[...]"
    :param unit: Target unit
    :return:
    """
    if isinstance(quantity, pd.Series):
        return quantity.pint.to(unit)  # type: ignore[attr-defined]
    else:
        return quantity.to(unit)
