import pytest

from pyunitsystem.energysystem import EnergySI
from pyunitsystem.metricsystem import MetricSystem
from pyunitsystem.timesystem import TimeSystem
from pyunitsystem.voltagesystem import VoltageSystem

expected_energy_conversion = {
    "eV": EnergySI.ELECTRONVOLT,
    "keV": EnergySI.KILOELECTRONVOLT,
    "meV": EnergySI.MEGAELECTRONVOLT,
    "geV": EnergySI.GIGAELECTRONVOLT,
    "J": EnergySI.JOULE,
    "kJ": EnergySI.KILOJOULE,
}


@pytest.mark.parametrize(
    "energy_as_str, energy_as_si",
    (expected_energy_conversion.items()),
)
def test_energy_conversion(energy_as_str, energy_as_si):
    assert (
        EnergySI.from_str(energy_as_str) is energy_as_si
    ), f"check {energy_as_str} == {energy_as_si}"
    assert str(energy_as_si) == energy_as_str


def test_failing_energy_conversion():
    """
    Ensure EnergySI.from_str raise a ValueErrror if cannot convert
    a string to an energy
    """
    with pytest.raises(ValueError):
        EnergySI.from_str("toto")


def test_from_value():
    assert EnergySI.from_value(EnergySI.JOULE.value) is EnergySI.JOULE


expected_metric_conversion = {
    "m": MetricSystem.METER,
    "meter": MetricSystem.METER,
    "cm": MetricSystem.CENTIMETER,
    "mm": MetricSystem.MILLIMETER,
    "um": MetricSystem.MICROMETER,
    "nm": MetricSystem.NANOMETER,
}


@pytest.mark.parametrize(
    "metric_as_str, metric_as_si", expected_metric_conversion.items()
)
def test_metric_conversion(metric_as_str, metric_as_si):
    assert (
        MetricSystem.from_str(metric_as_str) is metric_as_si
    ), f"check {metric_as_str} == {metric_as_si}"
    assert str(metric_as_si) == str(
        MetricSystem.from_str(metric_as_str)
    ), f"check {metric_as_str} == {str(metric_as_si)}"


def test_cast_metric_to_best_unit():
    """
    test the cast_metric_to_best_unit
    """
    assert MetricSystem.cast_metric_to_best_unit(value_in_m=12.3) == (12.3, "m")
    assert MetricSystem.cast_metric_to_best_unit(value_in_m=1.0) == (1.0, "m")
    assert MetricSystem.cast_metric_to_best_unit(value_in_m=0.02) == (2.0, "cm")
    assert MetricSystem.cast_metric_to_best_unit(value_in_m=3.6e-5) == (36, "um")
    assert MetricSystem.cast_metric_to_best_unit(value_in_m=6.2e-6) == (6.2, "um")


def test_failing_metric_conversion():
    """
    Ensure MetricSystem.from_str raise a ValueErrror if cannot convert
    a string to a metric
    """
    with pytest.raises(ValueError):
        MetricSystem.from_str("toto")


expected_time_conversion = {
    "second": TimeSystem.SECOND,
    "minute": TimeSystem.MINUTE,
    "hour": TimeSystem.HOUR,
    "day": TimeSystem.DAY,
    "millisecond": TimeSystem.MILLI_SECOND,
    "microsecond": TimeSystem.MICRO_SECOND,
    "nanosecond": TimeSystem.NANO_SECOND,
}


@pytest.mark.parametrize(
    "time_as_str, time_as_si", expected_time_conversion.items()
)  # noqa E501
def test_time_conversion(time_as_str, time_as_si):
    assert (
        TimeSystem.from_str(time_as_str) is time_as_si
    ), f"check {time_as_str} == {time_as_si}"
    assert str(time_as_si) == str(
        TimeSystem.from_str(time_as_str)
    ), f"check {time_as_str} == {str(time_as_si)}"


def test_failing_voltage_conversion():
    """
    Ensure VoltageSystem.from_str raise a ValueErrror if cannot convert
    a string to a voltage
    """
    with pytest.raises(ValueError):
        VoltageSystem.from_str("toto")


expected_voltage_conversion = {
    "volt": VoltageSystem.VOLT,
}


@pytest.mark.parametrize(
    "volt_as_str, volt_as_si", expected_voltage_conversion.items()
)  # noqa E501
def test_voltage_conversion(volt_as_str, volt_as_si):
    assert (
        VoltageSystem.from_str(volt_as_str) is volt_as_si
    ), f"check {volt_as_str} == {volt_as_si}"
    assert str(volt_as_si) == str(
        VoltageSystem.from_str(volt_as_str)
    ), f"check {volt_as_str} == {str(volt_as_si)}"
