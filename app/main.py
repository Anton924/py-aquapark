from __future__ import annotations
from abc import ABC, abstractmethod


class IntegerRange:
    def __init__(self, min_amount: int, max_amount: int) -> None:
        self.min_amount = min_amount
        self.max_amount = max_amount

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> str | int | object:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int) -> None:
        if isinstance(value, int):
            if not self.min_amount <= value <= self.max_amount:
                raise ValueError
            else:
                setattr(instance, self.protected_name, value)
        else:
            raise TypeError


class Visitor:
    def __init__(self, name: str, age: int, weight: int, height: int) -> None:
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height


class SlideLimitationValidator(ABC):
    @abstractmethod
    def __init__(self, age: int, weight: int, height: int) -> None:
        self.age = age
        self.weight = weight
        self.height = height


class ChildrenSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)

    age = IntegerRange(4, 14)
    weight = IntegerRange(20, 50)
    height = IntegerRange(80, 120)


class AdultSlideLimitationValidator(SlideLimitationValidator):
    def __init__(self, age: int, weight: int, height: int) -> None:
        super().__init__(age, weight, height)
    age = IntegerRange(14, 60)
    weight = IntegerRange(50, 120)
    height = IntegerRange(120, 220)


class Slide:
    def __init__(
            self, name: str,
            limitation_class:
            type[ChildrenSlideLimitationValidator
                 | AdultSlideLimitationValidator]) -> None:
        self.name = name
        self.limitation_class = limitation_class

    def can_access(self, visitor: Visitor) -> bool:
        try:
            self.limitation_class(visitor.age, visitor.weight, visitor.height)
            return True
        except TypeError:
            return False
        except ValueError:
            return False
