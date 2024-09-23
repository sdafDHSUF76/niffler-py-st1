from datetime import datetime
from http import HTTPStatus

from pydantic import BaseModel, Extra, field_validator, UUID4

from tests_api.enums.currencies import Currencies


class UnexpectedResponseStatus(Exception):
    pass


class RequestCreateSpend(BaseModel, extra=Extra.forbid):
    amount: str
    description: str
    category: str
    spendDate: str
    currency: Currencies


    @field_validator('currency')
    @classmethod
    def convert_enum_to_str(cls, v: Currencies) -> str:
        return v.name


    @field_validator('spendDate')
    @classmethod
    def check_datetime(cls, v: str) -> str:
        date_time: str = v.replace('Z', '')
        try:
            date_time: datetime = datetime.fromisoformat(date_time)
        except ValueError:
            raise ValueError('Полученная дата {v}, не соответствует isoformat')
        date_time: str = date_time.replace(tzinfo=None).isoformat(timespec='milliseconds')
        return ''.join((date_time, 'Z'))


class ResponseCreateSpend(BaseModel, extra=Extra.forbid):
    id: UUID4
    spendDate: str
    category: str
    currency: str
    amount: float
    description: str
    username: str


    @field_validator('currency')
    @classmethod
    def check_currency(cls, v: str) -> str:
        try:
            return Currencies.__getitem__(v).name
        except KeyError:
            raise KeyError(f'Нету такой валюты: {v}')


    @field_validator('spendDate')
    @classmethod
    def check_date(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError(f'дата не в формате isoformat: {v}')


class ResponseErrorCreateSpend(BaseModel, extra=Extra.forbid):
    type: str
    title: str
    status: int
    detail: str
    instance: str

    @field_validator('status')
    @classmethod
    def check_currency(cls, v: int) -> int:
        for value in HTTPStatus.__members__.values():
            if v == value.value:
                return v
        raise UnexpectedResponseStatus(f'Пришел неподдерживаемый http статус: {v}')
