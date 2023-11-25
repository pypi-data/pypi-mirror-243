"""Working with pressure quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity, UnitSymbol


class PressureUnit(UnitSymbol):
    """Symbols for pressure units."""

    HECTOPASCAL = "hPa"
    HPA = "hPa"

    PASCAL = "Pa"
    PA = "Pa"

    INCHES_MERCURY = "inHg"
    INHG = "inHg"

    POUNDS_PER_SQUARE_INCH = "psi"
    PSI = "psi"


class Pressure(Quantity, ABC):
    """Base for all pressure unit types."""

    @property
    def bar(self):
        """Return the value of this quantity as bar."""
        return self.hectopascals * 0.001

    @property
    def hectopascals(self):
        """Return the value of this quantity as Hectopascals."""
        return self.pascals * 0.01

    @abstractproperty
    def pascals(self):
        """Return the value of this quantity as Pascals."""

    @abstractproperty
    def inches_mercury(self):
        """Return the value of this quantity as inches-mercury."""

    @abstractproperty
    def pounds_per_sq_in(self):
        """Return the value of this quantity as pounds-per-square-inch."""


class Pascal(Pressure):
    """A representation of Pascals."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return PressureUnit.PASCAL

    @property
    def pascals(self):
        """Return the value of this quantity as Pascals."""
        return self.value

    @property
    def inches_mercury(self):
        """Return the value of this quantity as inches-mercury."""
        return self.pascals / 3386.3886666667

    @property
    def pounds_per_sq_in(self):
        """Return the value of this quantity as pounds-per-square-inch."""
        return self.pascals / 6894.75729


class Hectopascal(Pascal):
    """A representation of Hectopascals."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return PressureUnit.HECTOPASCAL

    @property
    def pascals(self):
        """Return the value of this quantity as Pascals."""
        return self.value * 100


class InchesMercury(Pressure):
    """A representation of InchesMercury."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return PressureUnit.INCHES_MERCURY

    @property
    def pascals(self):
        """Return the value of this quantity as Pascals."""
        return self.inches_mercury * 3386.3886666667

    @property
    def inches_mercury(self):
        """Return the value of this quantity as inches-mercury."""
        return self.value

    @property
    def pounds_per_sq_in(self):
        """Return the value of this quantity as pounds-per-square-inch."""
        return self.inches_mercury * 0.4911541996322
