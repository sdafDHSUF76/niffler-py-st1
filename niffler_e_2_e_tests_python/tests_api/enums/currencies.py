from enum import Enum, auto, unique


@unique
class Currencies(Enum):
    RUB = auto()
    EUR = auto()
    KZT = auto()
    USD = auto()
