"""
This module provides classes for the unit types.
The implementation uses full class definitions, since their type can be used in
the code directly via type(unit_obj).
"""
from typing import Union, TypeVar


class BaseUnitType(str):
    """
    Base class for all the unit types
    """
    pass


class AccelerationUnit(BaseUnitType):
    pass


class AngleUnit(BaseUnitType):
    pass


class AreaUnit(BaseUnitType):
    pass


class CurrencyUnit(BaseUnitType):
    pass


class CurrentUnit(BaseUnitType):
    pass


class DensityUnit(BaseUnitType):
    pass


class DynamicViscosityUnit(BaseUnitType):
    pass


class EnergyCostsUnit(BaseUnitType):
    pass


class EnergyUnit(BaseUnitType):
    pass


class FrequencyUnit(BaseUnitType):
    pass


class GeothermalProdIndexUnit(BaseUnitType):
    pass


class HeatCapacityRateUnit(BaseUnitType):
    pass


class HeatTransferCoefficientUnit(BaseUnitType):
    pass


class HourlyCostsUnit(BaseUnitType):
    pass


class KinematicViscosityUnit(BaseUnitType):
    pass


class LengthUnit(BaseUnitType):
    pass


class MassUnit(BaseUnitType):
    pass


class NoUnit(BaseUnitType):
    pass


class PowerAreaRatioUnit(BaseUnitType):
    pass


class PowerUnit(BaseUnitType):
    pass


class PressureUnit(BaseUnitType):
    pass


class SpecificHeatCapacityUnit(BaseUnitType):
    pass


class TemperatureCorrectionUnit(BaseUnitType):
    pass


class TemperatureDifferenceUnit(BaseUnitType):
    pass


class TemperatureUnit(BaseUnitType):
    pass


class ThermalConductivityUnit(BaseUnitType):
    pass


class TimeUnit(BaseUnitType):
    pass


class VelocityUnit(BaseUnitType):
    pass


class VolumeFlowUnit(BaseUnitType):
    pass


class VolumeUnit(BaseUnitType):
    pass


ALL = Union[AccelerationUnit, AngleUnit, AreaUnit, CurrencyUnit, CurrentUnit,
            DensityUnit, DynamicViscosityUnit, EnergyCostsUnit, EnergyUnit,
            FrequencyUnit, GeothermalProdIndexUnit, HeatCapacityRateUnit,
            HeatTransferCoefficientUnit, HourlyCostsUnit, KinematicViscosityUnit,
            LengthUnit, MassUnit, NoUnit, PowerAreaRatioUnit, PowerUnit, PressureUnit,
            SpecificHeatCapacityUnit, TemperatureCorrectionUnit, TemperatureDifferenceUnit,
            TemperatureUnit, ThermalConductivityUnit, TimeUnit, VelocityUnit, VolumeFlowUnit,
            VolumeUnit]
UnitsT = TypeVar("UnitsT", bound=BaseUnitType)
