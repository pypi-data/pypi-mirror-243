import enum


class _Enum(enum.Enum):
    """Enum with additional class methods."""

    @classmethod
    def from_value(cls, value):
        """Convert a value to corresponding Enum member

        :param value: The value to compare to Enum members
           If it is already a member of Enum, it is returned directly.
        :return: The corresponding enum member
        :rtype: Enum
        :raise ValueError: In case the conversion is not possible
        """
        if isinstance(value, cls):
            return value
        for member in cls:
            if value == member.value:
                return member
        raise ValueError("Cannot convert: %s" % value)

    @classmethod
    def members(cls):
        """Returns a tuple of all members.

        :rtype: Tuple[Enum]
        """
        return tuple(member for member in cls)

    @classmethod
    def names(cls):
        """Returns a tuple of all member names.

        :rtype: Tuple[str]
        """
        return tuple(member.name for member in cls)

    @classmethod
    def values(cls):
        """Returns a tuple of all member values.

        :rtype: Tuple
        """
        return tuple(member.value for member in cls)


class Unit(_Enum):
    """
    Base class for all Unit.
    Children class are also expected to inherit from silx Enum class
    """

    @classmethod
    def from_str(cls, value: str):
        raise NotImplementedError("Base class")

    @classmethod
    def from_value(cls, value):
        if isinstance(value, str):
            return cls.from_str(value=value)
        else:
            return super().from_value(value=value)
