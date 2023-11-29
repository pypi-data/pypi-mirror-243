"""
Module with predefined quantity types
"""

import dataclasses

from dataclasses import dataclass
from typing import Type, Generic, Optional

from . import unit_collections, unit_types, errors
from .unit_types import UnitsT


@dataclass(frozen=True)
class QuantityType(Generic[UnitsT]):
    """
    Class for meta information of a quantity.
    Implemented as dataclass for simple definition of child-classes.
    """
    # Type of the units e.g., unit_types.EnergyUnit
    units_type: Type[UnitsT]
    # The internal units e.g., unit_collection.Energy.J
    internal_units: UnitsT
    # Collection of available units e.g., unit_collections.Energy()
    available_units: unit_collections.UnitCollection
    # Default display units e.g., unit_collection.Energy.MWh
    default_display_units: Optional[UnitsT] = None

    def __post_init__(self):
        """
        Check the compatibility of the given units
        """
        # Check if type of internal units matches the declared unit type
        if not isinstance(self.internal_units, self.units_type):
            msg = f"Type of internal_units ({type(self.internal_units)}) " \
                  f"does not match the specified unit type ({self.units_type})"
            raise errors.QuantityUnitsError(msg)

        # Check if type of display units matches the declared unit type
        if self.default_display_units is not None:
            if not isinstance(self.default_display_units, self.units_type):
                msg = f"Type of default_display_units " \
                      f"({type(self.default_display_units)}) " \
                      f"does not match the specified unit type ({self.units_type})"
                raise errors.QuantityUnitsError(msg)

        # Check if type of all fields of the units collection
        # match the declared unit type
        for units_field in dataclasses.fields(self.available_units):
            field_object = getattr(self.available_units, units_field.name)
            if not isinstance(field_object,  self.units_type):
                msg = f"The type ({type(field_object)}) " \
                      f" of the field '{units_field.name}' (and maybe others)" \
                      f" from the available_units ({self.available_units})" \
                      f" do not match the specified unit type ({self.units_type})"
                raise errors.QuantityUnitsError(msg)


@dataclass(frozen=True)
class Acceleration(QuantityType[unit_types.AccelerationUnit]):
    units_type: Type[unit_types.AccelerationUnit] = unit_types.AccelerationUnit
    internal_units: unit_types.AccelerationUnit = unit_collections.Acceleration.m_per_s2
    default_display_units: unit_types.AccelerationUnit = unit_collections.Acceleration.m_per_s2
    available_units: unit_collections.UnitCollection = unit_collections.Acceleration()
    # ToDo Q: is possible still to have a data_type as before but rename it to quantity_type?


@dataclass(frozen=True)
class Angle(QuantityType[unit_types.AngleUnit]):
    units_type: Type[unit_types.AngleUnit] = unit_types.AngleUnit
    internal_units: unit_types.AngleUnit = unit_collections.Angle.rad
    default_display_units: unit_types.AngleUnit = unit_collections.Angle.deg
    available_units: unit_collections.UnitCollection = unit_collections.Angle()


@dataclass(frozen=True)
class Area(QuantityType[unit_types.AreaUnit]):
    units_type: Type[unit_types.AreaUnit] = unit_types.AreaUnit
    internal_units: unit_types.AreaUnit = unit_collections.Area.m2
    default_display_units: unit_types.AreaUnit = unit_collections.Area.m2
    available_units: unit_collections.UnitCollection = unit_collections.Area()


@dataclass(frozen=True)
class Currency(QuantityType[unit_types.CurrencyUnit]):
    units_type: Type[unit_types.CurrencyUnit] = unit_types.CurrencyUnit
    internal_units: unit_types.CurrencyUnit = unit_collections.Currency.EUR
    default_display_units: unit_types.CurrencyUnit = unit_collections.Currency.EUR
    available_units: unit_collections.UnitCollection = unit_collections.Currency()


@dataclass(frozen=True)
class Current(QuantityType[unit_types.CurrentUnit]):
    units_type: Type[unit_types.CurrentUnit] = unit_types.CurrentUnit
    internal_units: unit_types.CurrentUnit = unit_collections.Current.A
    default_display_units: unit_types.CurrentUnit = unit_collections.Current.A
    available_units: unit_collections.UnitCollection = unit_collections.Current()


@dataclass(frozen=True)
class Density(QuantityType[unit_types.DensityUnit]):
    units_type: Type[unit_types.DensityUnit] = unit_types.DensityUnit
    internal_units: unit_types.DensityUnit = unit_collections.Density.kg_per_m3
    default_display_units: unit_types.DensityUnit = unit_collections.Density.kg_per_m3
    available_units: unit_collections.UnitCollection = unit_collections.Density()


@dataclass(frozen=True)
class DurationShare(QuantityType[unit_types.NoUnit]):
    units_type: Type[unit_types.NoUnit] = unit_types.NoUnit
    internal_units: unit_types.NoUnit = unit_collections.DurationShare.h_per_a
    default_display_units: unit_types.NoUnit = unit_collections.DurationShare.h_per_a
    available_units: unit_collections.UnitCollection = unit_collections.DurationShare()


@dataclass(frozen=True)
class DynamicViscosity(QuantityType[unit_types.DynamicViscosityUnit]):
    units_type: Type[unit_types.DynamicViscosityUnit] = unit_types.DynamicViscosityUnit
    internal_units: unit_types.DynamicViscosityUnit = unit_collections.DynamicViscosity.Pa_s
    default_display_units: unit_types.DynamicViscosityUnit = unit_collections.DynamicViscosity.Pa_s
    available_units: unit_collections.UnitCollection = unit_collections.DynamicViscosity()


@dataclass(frozen=True)
class Energy(QuantityType[unit_types.EnergyUnit]):
    units_type: Type[unit_types.EnergyUnit] = unit_types.EnergyUnit
    internal_units: unit_types.EnergyUnit = unit_collections.Energy.J
    default_display_units: unit_types.EnergyUnit = unit_collections.Energy.MWh
    available_units: unit_collections.UnitCollection = unit_collections.Energy()


@dataclass(frozen=True)
class EnergyCosts(QuantityType[unit_types.EnergyCostsUnit]):
    units_type: Type[unit_types.EnergyCostsUnit] = unit_types.EnergyCostsUnit
    internal_units: unit_types.EnergyCostsUnit = unit_collections.EnergyCosts.EUR_per_MWh
    default_display_units: unit_types.EnergyCostsUnit = unit_collections.EnergyCosts.EUR_per_MWh
    available_units: unit_collections.UnitCollection = unit_collections.EnergyCosts()


@dataclass(frozen=True)
class EnergyInDuration(QuantityType[unit_types.PowerUnit]):
    units_type: Type[unit_types.PowerUnit] = unit_types.PowerUnit
    internal_units: unit_types.PowerUnit = unit_collections.EnergyInDuration.MWh_per_a
    default_display_units: unit_types.PowerUnit = unit_collections.EnergyInDuration.MWh_per_a
    available_units: unit_collections.UnitCollection = unit_collections.EnergyInDuration()


@dataclass(frozen=True)
class Frequency(QuantityType[unit_types.FrequencyUnit]):
    units_type: Type[unit_types.FrequencyUnit] = unit_types.FrequencyUnit
    internal_units: unit_types.FrequencyUnit = unit_collections.Frequency.Hz
    default_display_units: unit_types.FrequencyUnit = unit_collections.Frequency.Hz
    available_units: unit_collections.UnitCollection = unit_collections.Frequency()


@dataclass(frozen=True)
class GeothermalProdIndex(QuantityType[unit_types.GeothermalProdIndexUnit]):
    units_type: Type[unit_types.GeothermalProdIndexUnit] = unit_types.GeothermalProdIndexUnit
    internal_units: unit_types.GeothermalProdIndexUnit = unit_collections.GeothermalProdIndex.m3_per_s_Pa
    default_display_units: unit_types.GeothermalProdIndexUnit = unit_collections.GeothermalProdIndex.m3_per_s_Pa
    available_units: unit_collections.UnitCollection = unit_collections.GeothermalProdIndex()


@dataclass(frozen=True)
class HeatCapacityRate(QuantityType[unit_types.HeatCapacityRateUnit]):
    units_type: Type[unit_types.HeatCapacityRateUnit] = unit_types.HeatCapacityRateUnit
    internal_units: unit_types.HeatCapacityRateUnit = unit_collections.HeatCapacityRate.W_per_K
    default_display_units: unit_types.HeatCapacityRateUnit = unit_collections.HeatCapacityRate.W_per_K
    available_units: unit_collections.UnitCollection = unit_collections.HeatCapacityRate()


@dataclass(frozen=True)
class HeatTransferCoefficient(QuantityType[unit_types.HeatTransferCoefficientUnit]):
    units_type: Type[unit_types.HeatTransferCoefficientUnit] = unit_types.HeatTransferCoefficientUnit
    internal_units: unit_types.HeatTransferCoefficientUnit = unit_collections.HeatTransferCoefficient.W_per_m2_K
    default_display_units: unit_types.HeatTransferCoefficientUnit = unit_collections.HeatTransferCoefficient.W_per_m2_K
    available_units: unit_collections.UnitCollection = unit_collections.HeatTransferCoefficient()


@dataclass(frozen=True)
class HourlyCosts(QuantityType[unit_types.HourlyCostsUnit]):
    units_type: Type[unit_types.HourlyCostsUnit] = unit_types.HourlyCostsUnit
    internal_units: unit_types.HourlyCostsUnit = unit_collections.HourlyCosts.EUR_per_h
    default_display_units: unit_types.HourlyCostsUnit = unit_collections.HourlyCosts.EUR_per_h
    available_units: unit_collections.UnitCollection = unit_collections.HourlyCosts()


@dataclass(frozen=True)
class Irradiance(QuantityType[unit_types.HeatTransferCoefficientUnit]):
    units_type: Type[unit_types.HeatTransferCoefficientUnit] = unit_types.HeatTransferCoefficientUnit
    internal_units: unit_types.HeatTransferCoefficientUnit = unit_collections.QuadraticHeatTransferCoefficient.W_per_m2_K2
    default_display_units: unit_types.HeatTransferCoefficientUnit = unit_collections.QuadraticHeatTransferCoefficient.W_per_m2_K2
    available_units: unit_collections.UnitCollection = unit_collections.QuadraticHeatTransferCoefficient()


@dataclass(frozen=True)
class KinematicViscosity(QuantityType[unit_types.KinematicViscosityUnit]):
    units_type: Type[unit_types.KinematicViscosityUnit] = unit_types.KinematicViscosityUnit
    internal_units: unit_types.KinematicViscosityUnit = unit_collections.KinematicViscosity.m2_per_s
    default_display_units: unit_types.KinematicViscosityUnit = unit_collections.KinematicViscosity.m2_per_s
    available_units: unit_collections.UnitCollection = unit_collections.KinematicViscosity()


@dataclass(frozen=True)
class Length(QuantityType[unit_types.LengthUnit]):
    units_type: Type[unit_types.LengthUnit] = unit_types.LengthUnit
    internal_units: unit_types.LengthUnit = unit_collections.Length.m
    default_display_units: unit_types.LengthUnit = unit_collections.Length.m
    available_units: unit_collections.UnitCollection = unit_collections.Length()


@dataclass(frozen=True)
class LinearPressure(QuantityType[unit_types.PressureUnit]):
    units_type: Type[unit_types.PressureUnit] = unit_types.PressureUnit
    internal_units: unit_types.PressureUnit = unit_collections.LinearPressure.Pa_s_per_l
    default_display_units: unit_types.PressureUnit = unit_collections.LinearPressure.Pa_s_per_l
    available_units: unit_collections.UnitCollection = unit_collections.LinearPressure()


@dataclass(frozen=True)
class Mass(QuantityType[unit_types.MassUnit]):
    units_type: Type[unit_types.MassUnit] = unit_types.MassUnit
    internal_units: unit_types.MassUnit = unit_collections.Mass.kg
    default_display_units: unit_types.MassUnit = unit_collections.Mass.kg
    available_units: unit_collections.UnitCollection = unit_collections.Mass()


@dataclass(frozen=True)
class NoUnit(QuantityType[unit_types.NoUnit]):
    units_type: Type[unit_types.NoUnit] = unit_types.NoUnit
    internal_units: unit_types.NoUnit = unit_collections.NoUnit.No
    default_display_units: unit_types.NoUnit = unit_collections.NoUnit.No
    available_units: unit_collections.UnitCollection = unit_collections.NoUnit()


@dataclass(frozen=True)
class Power(QuantityType[unit_types.PowerUnit]):
    units_type: Type[unit_types.PowerUnit] = unit_types.PowerUnit
    internal_units: unit_types.PowerUnit = unit_collections.Power.W
    default_display_units: unit_types.PowerUnit = unit_collections.Power.kW
    available_units: unit_collections.UnitCollection = unit_collections.Power()


@dataclass(frozen=True)
class PowerAreaRatio(QuantityType[unit_types.PowerAreaRatioUnit]):
    units_type: Type[unit_types.PowerAreaRatioUnit] = unit_types.PowerAreaRatioUnit
    internal_units: unit_types.PowerAreaRatioUnit = unit_collections.PowerAreaRatio.W_per_m2
    default_display_units: unit_types.PowerAreaRatioUnit = unit_collections.PowerAreaRatio.W_per_m2
    available_units: unit_collections.UnitCollection = unit_collections.PowerAreaRatio()


@dataclass(frozen=True)
class Pressure(QuantityType[unit_types.PressureUnit]):
    units_type: Type[unit_types.PressureUnit] = unit_types.PressureUnit
    internal_units: unit_types.PressureUnit = unit_collections.Pressure.Pa
    default_display_units: unit_types.PressureUnit = unit_collections.Pressure.bar
    available_units: unit_collections.UnitCollection = unit_collections.Pressure()


@dataclass(frozen=True)
class QuadraticPressure(QuantityType[unit_types.PressureUnit]):
    units_type: Type[unit_types.PressureUnit] = unit_types.PressureUnit
    internal_units: unit_types.PressureUnit = unit_collections.QuadraticPressure.Pa_s2_per_l2
    default_display_units: unit_types.PressureUnit = unit_collections.QuadraticPressure.Pa_s2_per_l2
    available_units: unit_collections.UnitCollection = unit_collections.QuadraticPressure()


@dataclass(frozen=True)
class ShareInPeriod(QuantityType[unit_types.FrequencyUnit]):
    units_type: Type[unit_types.FrequencyUnit] = unit_types.FrequencyUnit
    internal_units: unit_types.FrequencyUnit = unit_collections.ShareInPeriod.share_per_a
    default_display_units: unit_types.FrequencyUnit = unit_collections.ShareInPeriod.share_per_a
    available_units: unit_collections.UnitCollection = unit_collections.ShareInPeriod()


@dataclass(frozen=True)
class SpecificHeatCapacity(QuantityType[unit_types.SpecificHeatCapacityUnit]):
    units_type: Type[unit_types.SpecificHeatCapacityUnit] = unit_types.SpecificHeatCapacityUnit
    internal_units: unit_types.SpecificHeatCapacityUnit = unit_collections.SpecificHeatCapacity.J_per_kg_K
    default_display_units: unit_types.SpecificHeatCapacityUnit = unit_collections.SpecificHeatCapacity.J_per_kg_K
    available_units: unit_collections.UnitCollection = unit_collections.SpecificHeatCapacity()


@dataclass(frozen=True)
class Temperature(QuantityType[unit_types.TemperatureUnit]):
    units_type: Type[unit_types.TemperatureUnit] = unit_types.TemperatureUnit
    internal_units: unit_types.TemperatureUnit = unit_collections.Temperature.K
    default_display_units: unit_types.TemperatureUnit = unit_collections.Temperature.deg_C
    available_units: unit_collections.UnitCollection = unit_collections.Temperature()


@dataclass(frozen=True)
class TemperatureCorrection(QuantityType[unit_types.TemperatureCorrectionUnit]):
    units_type: Type[unit_types.TemperatureCorrectionUnit] = unit_types.TemperatureCorrectionUnit
    internal_units: unit_types.TemperatureCorrectionUnit = unit_collections.TemperatureCorrection.inverse_K
    default_display_units: unit_types.TemperatureCorrectionUnit = unit_collections.TemperatureCorrection.inverse_K
    available_units: unit_collections.UnitCollection = unit_collections.TemperatureCorrection()


@dataclass(frozen=True)
class TemperatureDifference(QuantityType[unit_types.TemperatureDifferenceUnit]):
    units_type: Type[unit_types.TemperatureDifferenceUnit] = unit_types.TemperatureDifferenceUnit
    internal_units: unit_types.TemperatureDifferenceUnit = unit_collections.TemperatureDifference.delta_deg_C
    default_display_units: unit_types.TemperatureDifferenceUnit = unit_collections.TemperatureDifference.delta_deg_C
    available_units: unit_collections.UnitCollection = unit_collections.TemperatureDifference()


@dataclass(frozen=True)
class ThermalConductivity(QuantityType[unit_types.ThermalConductivityUnit]):
    units_type: Type[unit_types.ThermalConductivityUnit] = unit_types.ThermalConductivityUnit
    internal_units: unit_types.ThermalConductivityUnit = unit_collections.ThermalConductivity.W_per_m_K
    default_display_units: unit_types.ThermalConductivityUnit = unit_collections.ThermalConductivity.W_per_m_K
    available_units: unit_collections.UnitCollection = unit_collections.ThermalConductivity()


@dataclass(frozen=True)
class Time(QuantityType[unit_types.TimeUnit]):
    units_type: Type[unit_types.TimeUnit] = unit_types.TimeUnit
    internal_units: unit_types.TimeUnit = unit_collections.Time.s
    default_display_units: unit_types.TimeUnit = unit_collections.Time.h
    available_units: unit_collections.UnitCollection = unit_collections.Time()


@dataclass(frozen=True)
class Velocity(QuantityType[unit_types.VelocityUnit]):
    units_type: Type[unit_types.VelocityUnit] = unit_types.VelocityUnit
    internal_units: unit_types.VelocityUnit = unit_collections.Velocity.m_per_s
    default_display_units: unit_types.VelocityUnit = unit_collections.Velocity.m_per_s
    available_units: unit_collections.UnitCollection = unit_collections.Velocity()


@dataclass(frozen=True)
class Volume(QuantityType[unit_types.VolumeUnit]):
    units_type: Type[unit_types.VolumeUnit] = unit_types.VolumeUnit
    internal_units: unit_types.VolumeUnit = unit_collections.Volume.m3
    default_display_units: unit_types.VolumeUnit = unit_collections.Volume.m3
    available_units: unit_collections.UnitCollection = unit_collections.Volume()


@dataclass(frozen=True)
class VolumeFlow(QuantityType[unit_types.VolumeFlowUnit]):
    units_type: Type[unit_types.VolumeFlowUnit] = unit_types.VolumeFlowUnit
    internal_units: unit_types.VolumeFlowUnit = unit_collections.VolumeFlow.m3_per_h
    default_display_units: unit_types.VolumeFlowUnit = unit_collections.VolumeFlow.l_per_min
    available_units: unit_collections.UnitCollection = unit_collections.VolumeFlow()
