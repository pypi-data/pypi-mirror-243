from pyunitsystem.unit import Unit


class VoltageSystem(Unit):
    """Unit system for electric potential SI units (volt)"""

    VOLT = 1.0

    @classmethod
    def from_str(cls, value: str):
        assert isinstance(value, str)
        if value.lower() in ("v", "volt"):
            return VoltageSystem.VOLT
        else:
            raise ValueError(f"Cannot convert: {value}")

    def __str__(self):
        if self == VoltageSystem.VOLT:
            return "volt"
        else:
            raise ValueError("Cannot convert: to voltage system")


volt = VoltageSystem.VOLT
