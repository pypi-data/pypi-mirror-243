from pyunitsystem.energysystem import (
    EnergySI,
)  # noqa F401  kept for bacward compatibility
from pyunitsystem.unit import Unit

# Default units:
#  - lenght: meter (m)
#  - energy: kilo Electronvolt (keV)
_meter = 1.0
_kev = 1.0


class MetricSystem(Unit):
    """Util enum to retrieve metric"""

    METER = _meter
    m = _meter
    CENTIMETER = _meter / 100.0
    MILLIMETER = _meter / 1000.0
    MICROMETER = _meter * 1e-6
    NANOMETER = _meter * 1e-9

    KILOELECTRONVOLT = _kev
    ELECTRONVOLT = _kev * 1e-3
    JOULE = _kev / EnergySI.KILOELECTRONVOLT.value
    KILOJOULE = _kev / EnergySI.KILOELECTRONVOLT.value * 1e3

    @classmethod
    def from_str(cls, value: str):
        assert isinstance(value, str)
        if value.lower() in ("m", "meter"):
            return MetricSystem.METER
        elif value.lower() in ("cm", "centimeter"):
            return MetricSystem.CENTIMETER
        elif value.lower() in ("mm", "millimeter"):
            return MetricSystem.MILLIMETER
        elif value.lower() in ("um", "micrometer", "microns"):
            return MetricSystem.MICROMETER
        elif value.lower() in ("nm", "nanometer"):
            return MetricSystem.NANOMETER
        else:
            raise ValueError(f"Cannot convert: {value}")

    def __str__(self):
        if self == MetricSystem.METER:
            return "m"
        elif self == MetricSystem.CENTIMETER:
            return "cm"
        elif self == MetricSystem.MILLIMETER:
            return "mm"
        elif self == MetricSystem.MICROMETER:
            return "um"
        elif self == MetricSystem.NANOMETER:
            return "nm"
        else:
            raise ValueError(f"Cannot convert: {self}")

    @staticmethod
    def cast_metric_to_best_unit(value_in_m):
        """
        cast a value to the 'most appropriate' unit.
        The goal is that the user can easily get an accurate value with a 'short' representation
        """
        if value_in_m < MetricSystem.MICROMETER.value:
            return value_in_m / MetricSystem.NANOMETER.value, str(
                MetricSystem.NANOMETER
            )
        elif value_in_m < (MetricSystem.MILLIMETER.value / 10.0):  # prefer mm to um
            return value_in_m / MetricSystem.MICROMETER.value, str(
                MetricSystem.MICROMETER
            )
        elif value_in_m < (MetricSystem.CENTIMETER.value):
            return value_in_m / MetricSystem.MILLIMETER.value, str(
                MetricSystem.MILLIMETER
            )
        elif value_in_m < (MetricSystem.METER.value):
            return value_in_m / MetricSystem.CENTIMETER.value, str(
                MetricSystem.CENTIMETER
            )
        else:
            return value_in_m, str(MetricSystem.METER)


m = MetricSystem.METER
meter = MetricSystem.METER

centimeter = MetricSystem.CENTIMETER
cm = centimeter

millimeter = MetricSystem.MILLIMETER
mm = MetricSystem.MILLIMETER

micrometer = MetricSystem.MICROMETER

nanometer = MetricSystem.NANOMETER
