from pyunitsystem.unit import Unit


class ElectricCurrentSystem(Unit):
    """Unit system for electric potential SI units (volt)"""

    AMPERE = 1.0

    MILLIAMPERE = AMPERE / 1000.0

    KILOAMPERE = AMPERE * 10e3

    @classmethod
    def from_str(cls, value: str):
        assert isinstance(value, str)
        if value.lower() in ("a", "ampere"):
            return ElectricCurrentSystem.AMPERE
        elif value.lower() in ("ma", "milliampere"):
            return ElectricCurrentSystem.MILLIAMPERE
        elif value.lower() in ("ka", "kiloampere"):
            return ElectricCurrentSystem.KILOAMPERE
        else:
            raise ValueError(f"Cannot convert: {value}")

    def __str__(self):
        if self == ElectricCurrentSystem.AMPERE:
            return "A"
        elif self == ElectricCurrentSystem.MILLIAMPERE:
            return "mA"
        elif self == ElectricCurrentSystem.KILOAMPERE:
            return "kA"
        else:
            raise ValueError("Cannot convert: to voltage system")


ampere = ElectricCurrentSystem.AMPERE
