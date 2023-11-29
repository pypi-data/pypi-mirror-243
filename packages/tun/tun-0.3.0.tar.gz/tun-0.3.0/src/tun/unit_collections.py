"""
Module with units collections for each quantity
"""

import dataclasses
import sys

from dataclasses import dataclass
from typing import Type

from . import unit_types, errors


@dataclass(frozen=True)
class UnitCollection:
    """
    Returns a collection of available units
    """
    def units_obj(self, units: str) -> unit_types.ALL:
        """
        Return the related object of a given unit in a UnitCollection.
        :param units: file
        :return:
        """
        for field in dataclasses.fields(self):
            if field.name == units:
                return getattr(self, field.name)

        msg = f"Units ({units}) not in the selected UnitCollection."
        raise errors.QuantityUnitsError(msg)


@dataclass(frozen=True)
class Acceleration(UnitCollection):
    m_per_s2: unit_types.AccelerationUnit = unit_types.AccelerationUnit("m/s²")


@dataclass(frozen=True)
class Angle(UnitCollection):
    rad: unit_types.AngleUnit = unit_types.AngleUnit("rad")
    deg: unit_types.AngleUnit = unit_types.AngleUnit("deg")
    arcmin: unit_types.AngleUnit = unit_types.AngleUnit("arcmin")
    arcsec: unit_types.AngleUnit = unit_types.AngleUnit("arcsec")


@dataclass(frozen=True)
class Area(UnitCollection):
    m2: unit_types.AreaUnit = unit_types.AreaUnit("m²")
    km2: unit_types.AreaUnit = unit_types.AreaUnit("km²")
    mm2: unit_types.AreaUnit = unit_types.AreaUnit("mm²")
    ha: unit_types.AreaUnit = unit_types.AreaUnit("ha")


@dataclass(frozen=True)
class Currency(UnitCollection):
    EUR: unit_types.CurrencyUnit = unit_types.CurrencyUnit("EUR")
    ct: unit_types.CurrencyUnit = unit_types.CurrencyUnit("ct")
    USD: unit_types.CurrencyUnit = unit_types.CurrencyUnit("USD")


@dataclass(frozen=True)
class Current(UnitCollection):
    A: unit_types.CurrentUnit = unit_types.CurrentUnit("A")
    mA: unit_types.CurrentUnit = unit_types.CurrentUnit("mA")


@dataclass(frozen=True)
class Density(UnitCollection):
    kg_per_m3: unit_types.DensityUnit = unit_types.DensityUnit("kg/m³")
    kg_per_l: unit_types.DensityUnit = unit_types.DensityUnit("kg/l")
    g_per_l: unit_types.DensityUnit = unit_types.DensityUnit("g/l")
    t_per_m3: unit_types.DensityUnit = unit_types.DensityUnit("t/m³")


@dataclass(frozen=True)
class DurationShare(UnitCollection):
    h_per_a: unit_types.NoUnit = unit_types.NoUnit("h/a")


@dataclass(frozen=True)
class DynamicViscosity(UnitCollection):
    Pa_s: unit_types.DynamicViscosityUnit = \
        unit_types.DynamicViscosityUnit("Pa·s")
    mPa_s: unit_types.DynamicViscosityUnit = \
        unit_types.DynamicViscosityUnit("mPa·s")


@dataclass(frozen=True)
class Energy(UnitCollection):
    kWh: unit_types.EnergyUnit = unit_types.EnergyUnit("kWh")
    J: unit_types.EnergyUnit = unit_types.EnergyUnit("J")
    kJ: unit_types.EnergyUnit = unit_types.EnergyUnit("kJ")
    MJ: unit_types.EnergyUnit = unit_types.EnergyUnit("MJ")
    Wh: unit_types.EnergyUnit = unit_types.EnergyUnit("Wh")
    MWh: unit_types.EnergyUnit = unit_types.EnergyUnit("MWh")


@dataclass(frozen=True)
class EnergyCosts(UnitCollection):
    EUR_per_MWh: unit_types.EnergyCostsUnit = \
        unit_types.EnergyCostsUnit("EUR/MWh")
    ct_per_kWh: unit_types.EnergyCostsUnit = \
        unit_types.EnergyCostsUnit("ct/kWh")
    EUR_per_kWh: unit_types.EnergyCostsUnit = \
        unit_types.EnergyCostsUnit("EUR/kWh")


@dataclass(frozen=True)
class EnergyInDuration(UnitCollection):
    MWh_per_a: unit_types.PowerUnit = unit_types.PowerUnit("MWh/a")


@dataclass(frozen=True)
class Frequency(UnitCollection):
    cycle_per_s: unit_types.FrequencyUnit = unit_types.FrequencyUnit("1/s")
    Hz: unit_types.FrequencyUnit = unit_types.FrequencyUnit("Hz")
    rpm: unit_types.FrequencyUnit = unit_types.FrequencyUnit("rpm")


@dataclass(frozen=True)
class GeothermalProdIndex(UnitCollection):
    m3_per_s_Pa: unit_types.GeothermalProdIndexUnit = unit_types.GeothermalProdIndexUnit("m³/(s·Pa)")


@dataclass(frozen=True)
class HeatCapacityRate(UnitCollection):
    W_per_K: unit_types.HeatCapacityRateUnit = \
        unit_types.HeatCapacityRateUnit("W/K")


@dataclass(frozen=True)
class HeatTransferCoefficient(UnitCollection):
    W_per_m2_K: unit_types.HeatTransferCoefficientUnit = \
        unit_types.HeatTransferCoefficientUnit("W/(m²·K)")


@dataclass(frozen=True)
class HourlyCosts(UnitCollection):
    EUR_per_h: unit_types.HourlyCostsUnit = unit_types.HourlyCostsUnit("EUR/h")


@dataclass(frozen=True)
class KinematicViscosity(UnitCollection):
    m2_per_s: unit_types.KinematicViscosityUnit = \
        unit_types.KinematicViscosityUnit("m²/s")


@dataclass(frozen=True)
class Length(UnitCollection):
    m: unit_types.LengthUnit = unit_types.LengthUnit("m")
    km: unit_types.LengthUnit = unit_types.LengthUnit("km")
    dm: unit_types.LengthUnit = unit_types.LengthUnit("dm")
    cm: unit_types.LengthUnit = unit_types.LengthUnit("cm")
    mm: unit_types.LengthUnit = unit_types.LengthUnit("mm")


@dataclass(frozen=True)
class LinearPressure(UnitCollection):
    Pa_s_per_l: unit_types.PressureUnit = unit_types.PressureUnit("(Pa·s)/l")


@dataclass(frozen=True)
class Mass(UnitCollection):
    kg: unit_types.MassUnit = unit_types.MassUnit("kg")
    g: unit_types.MassUnit = unit_types.MassUnit("g")
    t: unit_types.MassUnit = unit_types.MassUnit("t")


@dataclass(frozen=True)
class NoUnit(UnitCollection):
    No: unit_types.NoUnit = unit_types.NoUnit("")


@dataclass(frozen=True)
class Power(UnitCollection):
    MW: unit_types.PowerUnit = unit_types.PowerUnit("MW")
    kW: unit_types.PowerUnit = unit_types.PowerUnit("kW")
    kVA: unit_types.PowerUnit = unit_types.PowerUnit("kVA")
    W: unit_types.PowerUnit = unit_types.PowerUnit("W")
    VA: unit_types.PowerUnit = unit_types.PowerUnit("VA")


@dataclass(frozen=True)
class PowerAreaRatio(UnitCollection):
    MW_per_m2: unit_types.PowerAreaRatioUnit = unit_types.PowerAreaRatioUnit("MW/m²")
    kW_per_m2: unit_types.PowerAreaRatioUnit = unit_types.PowerAreaRatioUnit("kW/m²")
    W_per_m2: unit_types.PowerAreaRatioUnit = unit_types.PowerAreaRatioUnit("W/m²")
    W_per_cm2: unit_types.PowerAreaRatioUnit = unit_types.PowerAreaRatioUnit("W/cm²")


@dataclass(frozen=True)
class Pressure(UnitCollection):
    bar: unit_types.PressureUnit = unit_types.PressureUnit("bar")
    mbar: unit_types.PressureUnit = unit_types.PressureUnit("mbar")
    Pa: unit_types.PressureUnit = unit_types.PressureUnit("Pa")
    kPa: unit_types.PressureUnit = unit_types.PressureUnit("kPa")
    MPa: unit_types.PressureUnit = unit_types.PressureUnit("MPa")
    psi: unit_types.PressureUnit = unit_types.PressureUnit("psi")


@dataclass(frozen=True)
class QuadraticHeatTransferCoefficient(UnitCollection):
    W_per_m2_K2: unit_types.HeatTransferCoefficientUnit = \
        unit_types.HeatTransferCoefficientUnit("W/(m²·K²)")


@dataclass(frozen=True)
class QuadraticPressure(UnitCollection):
    Pa_s2_per_l2: unit_types.PressureUnit = unit_types.PressureUnit("(Pa·s²)/l²")


@dataclass(frozen=True)
class ShareInPeriod(UnitCollection):
    share_per_a: unit_types.FrequencyUnit = \
        unit_types.FrequencyUnit("1/a")


@dataclass(frozen=True)
class SpecificHeatCapacity(UnitCollection):
    J_per_kg_K: unit_types.SpecificHeatCapacityUnit = \
        unit_types.SpecificHeatCapacityUnit("J/(kg·K)")
    kJ_per_kg_K: unit_types.SpecificHeatCapacityUnit = \
        unit_types.SpecificHeatCapacityUnit("kJ/(kg·K)")


@dataclass(frozen=True)
class Temperature(UnitCollection):
    K: unit_types.TemperatureUnit = unit_types.TemperatureUnit("K")
    deg_C: unit_types.TemperatureUnit = unit_types.TemperatureUnit("°C")


@dataclass(frozen=True)
class TemperatureCorrection(UnitCollection):
    inverse_K: unit_types.TemperatureCorrectionUnit = unit_types.TemperatureCorrectionUnit("1/K")


@dataclass(frozen=True)
class TemperatureDifference(UnitCollection):
    delta_deg_C: unit_types.TemperatureDifferenceUnit = unit_types.TemperatureDifferenceUnit("delta_degC")


@dataclass(frozen=True)
class ThermalConductivity(UnitCollection):
    W_per_m_K: unit_types.ThermalConductivityUnit = \
        unit_types.ThermalConductivityUnit("W/(m·K)")


@dataclass(frozen=True)
class Time(UnitCollection):
    s: unit_types.TimeUnit = unit_types.TimeUnit("s")
    min: unit_types.TimeUnit = unit_types.TimeUnit("min")
    h: unit_types.TimeUnit = unit_types.TimeUnit("h")
    d: unit_types.TimeUnit = unit_types.TimeUnit("d")
    week: unit_types.TimeUnit = unit_types.TimeUnit("week")
    a: unit_types.TimeUnit = unit_types.TimeUnit("a")
    month: unit_types.TimeUnit = unit_types.TimeUnit("month")


@dataclass(frozen=True)
class Velocity(UnitCollection):
    m_per_s: unit_types.VelocityUnit = unit_types.VelocityUnit("m/s")
    km_per_h: unit_types.VelocityUnit = unit_types.VelocityUnit("km/h")


@dataclass(frozen=True)
class Volume(UnitCollection):
    m3: unit_types.VolumeUnit = unit_types.VolumeUnit("m³")
    dm3: unit_types.VolumeUnit = unit_types.VolumeUnit("dm³")
    l: unit_types.VolumeUnit = unit_types.VolumeUnit("l")
    cm3: unit_types.VolumeUnit = unit_types.VolumeUnit("cm³")


@dataclass(frozen=True)
class VolumeFlow(UnitCollection):
    m3_per_h: unit_types.VolumeFlowUnit = unit_types.VolumeFlowUnit("m³/h")
    l_per_min: unit_types.VolumeFlowUnit = unit_types.VolumeFlowUnit("l/min")
    m3_per_s: unit_types.VolumeFlowUnit = unit_types.VolumeFlowUnit("m³/s")
    l_per_s: unit_types.VolumeFlowUnit = unit_types.VolumeFlowUnit("l/s")


def from_str(quantity_type: str, units: str) -> unit_types.ALL:
    """
    Return a unit object of the given quantity type and unit
    :param quantity_type: String of the given quantity (e.g., 'Power')
    :param units: String of the required unit (e.g., 'kW')
    :return: an object of the unit of the corresponding unit type
    """
    units_collection: Type[UnitCollection] = getattr(
        sys.modules[__name__], quantity_type)
    return units_collection().units_obj(units=units)
