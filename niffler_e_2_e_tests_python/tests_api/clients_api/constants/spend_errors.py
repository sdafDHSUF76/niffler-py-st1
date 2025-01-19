from enum import Enum


class Type(str, Enum):
    """Возможные значения поля type при spend запросах."""
    DEFAULT = 'about:blank'

    def __str__(self) -> str:
        return self.value


class Title(str, Enum):
    """Возможные значения поля title при spend запросах."""
    BAD_REQUEST = 'Bad Request'

    def __str__(self) -> str:
        return self.value


class Detail(str, Enum):
    """Возможные значения поля detail при spend запросах."""
    BAD_REQUEST = 'Failed to read request'

    def __str__(self) -> str:
        return self.value
