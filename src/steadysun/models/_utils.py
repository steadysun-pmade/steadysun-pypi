from enum import Enum

from pydantic import BaseModel


# pylint: disable=invalid-name
class EnumIntStr(Enum):
    """Base Enum class for handling int and string conversions."""

    @classmethod
    def from_value(cls, value):
        """Convert an input value to the corresponding enum."""
        if isinstance(value, cls):
            return value
        if isinstance(value, int):
            return cls(value)
        if isinstance(value, str):
            return cls[value]
        raise ValueError(f"Invalid value '{value}' for {cls.__name__}")

    def __str__(self):
        """Return the name of the enum."""
        return self.name

    def __int__(self):
        """Return the value of the enum."""
        return self.value


class TypeCheckingBaseModel(BaseModel):
    """Base model with Pydantic configuration for validation."""

    class Config:
        """Configuration for the Pydantic model."""

        validate_assignment = True
