from enum import Enum


class Type(Enum):
    default = 'about:blank'


class Title(Enum):
    bad_request = 'Bad Request'


class Detail(Enum):
    bad_request = 'Failed to read request'
