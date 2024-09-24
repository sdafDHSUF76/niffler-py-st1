from enum import Enum


class Error(str, Enum):
    """Возможные значения поля error при category запросах."""
    INTERNAL_SERVER_ERROR = 'Internal Server Error'

    def __str__(self) -> str:
        return self.value
