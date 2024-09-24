from enum import Enum


class Error(str, Enum):
    INTERNAL_SERVER_ERROR = 'Internal Server Error'

    def __str__(self) -> str:
        return self.value
