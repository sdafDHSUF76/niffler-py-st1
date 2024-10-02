from enum import Enum, auto, unique


@unique
class HttpMethods(Enum):
    GET = auto()
    POST = auto()
