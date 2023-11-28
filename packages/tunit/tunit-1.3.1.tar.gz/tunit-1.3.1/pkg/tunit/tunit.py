#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright by: P.J. Grochowski

from __future__ import annotations  # TODO: Remove when support dropped for: Python < 3.10

import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from functools import total_ordering
from typing import Any, Callable, Generic, Optional, Tuple, Type, TypeVar, Union, cast

if sys.version_info >= (3, 8):  # TODO: Remove when support dropped for: Python < 3.8
    from typing import get_args
else:
    def get_args(union: Any) -> Tuple[Any, ...]:
        return cast(Tuple[Any, ...], getattr(union, '__args__'))

C = TypeVar('C')
T = TypeVar('T')


class TimeUnitTypeError(TypeError):
    pass


class ClassProperty(Generic[C, T]):

    def __init__(self, callback: Callable[[Type[C]], T]) -> None:
        self._callback = callback

    def __get__(self, instance: C, owner: Type[C]) -> T:
        return self._callback(owner)


class ITimeUnit(ABC):

    @dataclass(frozen=True)
    class UnitInfo:
        name: str
        symbol: str
        conversionFactor: int

    @abstractmethod
    def __int__(self) -> int:
        pass

    @abstractmethod
    def __float__(self) -> float:
        pass

    @property
    @abstractmethod
    def value(self) -> int:
        pass

    @staticmethod
    @abstractmethod
    def unitInfo() -> UnitInfo:
        pass

    @abstractmethod
    def toRawUnit(self, unit: Type[ITimeUnit]) -> float:
        pass


@total_ordering
class TimeUnit(ITimeUnit, ABC):

    class _ArithmeticOperation(Enum):
        Addition = auto()
        Subtraction = auto()
        Multiplication = auto()
        Division = auto()

    @dataclass(frozen=True)
    class _ArithmeticDetails:
        symbol: str
        name: str
        operation: Callable[[int, float], float]

    _ARITHMETIC = {
        _ArithmeticOperation.Addition: _ArithmeticDetails(symbol='+', name='addition', operation=lambda value, otherValue: value + otherValue),
        _ArithmeticOperation.Subtraction: _ArithmeticDetails(symbol='-', name='subtraction', operation=lambda value, otherValue: value - otherValue),
        _ArithmeticOperation.Multiplication: _ArithmeticDetails(symbol='*', name='multiplication', operation=lambda value, otherValue: value * otherValue),
        _ArithmeticOperation.Division: _ArithmeticDetails(symbol='/', name='division', operation=lambda value, otherValue: value / otherValue),
    }

    SupportedValue = Union[int, float, ITimeUnit]

    name: Union[ClassProperty, str] = ClassProperty[ITimeUnit, str](lambda cls: cls.unitInfo().name)
    symbol: Union[ClassProperty, str] = ClassProperty[ITimeUnit, str](lambda cls: cls.unitInfo().symbol)
    conversionFactor: Union[ClassProperty, int] = ClassProperty[ITimeUnit, int](lambda cls: cls.unitInfo().conversionFactor)

    @classmethod
    def fromRawUnit(cls, unit: Type[TimeUnit], value: Union[int, float]) -> TimeUnit:
        unitInfo = cls.unitInfo()
        otherUnitInfo = unit.unitInfo()
        if otherUnitInfo.conversionFactor <= unitInfo.conversionFactor:
            return cls(value=unit(value=value))

        multiplier = otherUnitInfo.conversionFactor / unitInfo.conversionFactor
        return cls(value=(multiplier * value))

    def __init__(self, value: Optional[SupportedValue] = None) -> None:
        value = value if value is not None else 0

        self._value: int = self._convertValue(value)

    def __str__(self) -> str:
        return f"{self._value}[{self.symbol}]"

    def __repr__(self) -> str:
        return f"{self.name}({self._value})"

    def __int__(self) -> int:
        return self._value

    def __float__(self) -> float:
        return float(self._value)

    def __add__(self, other: object) -> TimeUnit:
        return self._arithmetic(operation=TimeUnit._ArithmeticOperation.Addition, other=other)

    def __sub__(self, other: object) -> TimeUnit:
        return self._arithmetic(operation=TimeUnit._ArithmeticOperation.Subtraction, other=other)

    def __mul__(self, other: object) -> TimeUnit:
        return self._arithmetic(operation=TimeUnit._ArithmeticOperation.Multiplication, other=other)

    def __truediv__(self, other: object) -> TimeUnit:
        return self._arithmetic(operation=TimeUnit._ArithmeticOperation.Division, other=other)

    def __neg__(self) -> TimeUnit:
        return self.__class__(value=(-self._value))

    def __eq__(self, other: object) -> bool:
        return self._value == self._convertValue(other)

    def __gt__(self, other: object) -> bool:
        return self._value > self._convertValue(other)

    @property
    def value(self) -> int:
        return self._value

    def toRawUnit(self, unit: Type[ITimeUnit]) -> float:
        unitInfo = self.unitInfo()
        otherUnitInfo = unit.unitInfo()
        if otherUnitInfo.conversionFactor <= unitInfo.conversionFactor:
            return float(cast(Type[TimeUnit], unit)(self))
        divider = otherUnitInfo.conversionFactor / unitInfo.conversionFactor
        return self._value / divider

    def _arithmetic(self, operation: _ArithmeticOperation, other: object) -> TimeUnit:
        operationDetails = TimeUnit._ARITHMETIC[operation]

        if not self._isSupportedValueType(other=other):
            raise TimeUnitTypeError(f"Cannot perform {operationDetails.name} of types '{self.name}' and '{type(other).__name__}'!")

        if isinstance(other, TimeUnit) and self.unitInfo() != other.unitInfo():
            raise TimeUnitTypeError(f"Cannot perform {operationDetails.name} between different time units! ({self.name} {operationDetails.symbol} {other.name})")

        otherValue = self._calculateValue(cast(TimeUnit.SupportedValue, other))
        return self.__class__(value=operationDetails.operation(self._value, otherValue))

    def _convertValue(self, other: object) -> int:
        if not self._isSupportedValueType(other=other):
            raise TimeUnitTypeError(f"Cannot create '{self.name}' from '{type(other).__name__}'!")
        return self._calculateValue(other=cast(TimeUnit.SupportedValue, other))

    def _calculateValue(self, other: SupportedValue) -> int:
        rawValue = other._value * other.conversionFactor / self.conversionFactor if isinstance(other, TimeUnit) \
            else other
        return int(rawValue)

    @staticmethod
    def _isSupportedValueType(other: object) -> bool:
        return isinstance(other, get_args(TimeUnit.SupportedValue))
