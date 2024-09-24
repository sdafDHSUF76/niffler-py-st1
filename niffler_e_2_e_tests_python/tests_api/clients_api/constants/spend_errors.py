from enum import Enum


class Type(str, Enum):
    DEFAULT = 'about:blank'

    def __str__(self) -> str:
        return self.value


class Title(str, Enum):
    BAD_REQUEST = 'Bad Request'

    def __str__(self) -> str:
        return self.value


class Detail(str, Enum):
    BAD_REQUEST = 'Failed to read request'

    def __str__(self) -> str:
        return self.value
