"""Working with velocity quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity, UnitSymbol


class VelocityUnit(UnitSymbol):
    """Symbols for velocity units."""

    METERS_PER_SECOND = "m/s"
    MPS = "m/s"

    KILOMETERS_PER_HOUR = "km/h"
    KPH = "km/h"

    MILES_PER_HOUR = "mph"
    MPH = "mph"

    FEET_PER_SECOND = "fps"
    FPS = "fps"

    KNOT = "knot"
    KNOTS = "knots"


class Velocity(Quantity, ABC):
    """Base for all velocity unit types."""

    @abstractproperty
    def meters_per_sec(self):
        """Return the value of this quantity as meters per second"""

    @abstractproperty
    def kilometers_per_hr(self):
        """Return the value of this quantity as kilometers per hour"""

    @abstractproperty
    def miles_per_hr(self):
        """Return the value of this quantity as miles per hour"""

    @abstractproperty
    def feet_per_sec(self):
        """Return the value of this quantity as feet per second"""

    @abstractproperty
    def knots(self):
        """Return the value of this quantity as knots"""


class MetersPerSecond(Velocity):
    """A representation of m/s."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return VelocityUnit.METERS_PER_SECOND

    @property
    def meters_per_sec(self):
        """Return the value of this quantity as meters per second"""
        return self.value

    @property
    def kilometers_per_hr(self):
        """Return the value of this quantity as kilometers per hour"""
        return self.meters_per_sec * 3.6

    @property
    def miles_per_hr(self):
        """Return the value of this quantity as miles per hour"""
        return self.meters_per_sec * 2.2369363

    @property
    def feet_per_sec(self):
        """Return the value of this quantity as feet per second"""
        return self.meters_per_sec * 3.28084

    @property
    def knots(self):
        """Return the value of this quantity as knots"""
        return self.meters_per_sec * 1.943844


class KilometersPerHour(MetersPerSecond):
    """A representation of km/h."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return VelocityUnit.KILOMETERS_PER_HOUR

    @property
    def meters_per_sec(self):
        """Return the value of this quantity as meters per second"""
        return (self.value * 1000.0) / 3600.0


class MilesPerHour(Velocity):
    """A representation of mph."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return VelocityUnit.MILES_PER_HOUR

    @property
    def meters_per_sec(self):
        """Return the value of this quantity as meters per second"""
        return self.miles_per_hr * 0.44704

    @property
    def kilometers_per_hr(self):
        """Return the value of this quantity as kilometers per hour"""
        return self.miles_per_hr * 1.609344

    @property
    def miles_per_hr(self):
        """Return the value of this quantity as miles per hour"""
        return self.value

    @property
    def feet_per_sec(self):
        """Return the value of this quantity as feet per second"""
        return (self.miles_per_hr * 5280.0) / 3600.0

    @property
    def knots(self):
        """Return the value of this quantity as knots"""
        return self.miles_per_hr * 0.86897624


class FeetPerSecond(MilesPerHour):
    """A representation of fps."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return VelocityUnit.FEET_PER_SECOND

    @property
    def miles_per_hr(self):
        """Return the value of this quantity as miles per hour"""
        return (self.value * 3600.0) / 5280.0
