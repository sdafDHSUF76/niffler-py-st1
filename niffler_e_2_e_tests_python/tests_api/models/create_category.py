from datetime import datetime
from http import HTTPStatus

from pydantic import UUID4, BaseModel, ConfigDict, Extra, Field, field_validator
from tests_api.models.create_spend import UnexpectedResponseStatus


class RequestCreateCategory(BaseModel):

    model_config = ConfigDict(extra='forbid')

    category: str


class ResponseCreateCategory(BaseModel):

    model_config = ConfigDict(extra='forbid')

    id: UUID4
    category: str = Field(min_length=3)
    username: str = Field(min_length=3)


class ResponseErrorCreateCategory(BaseModel):

    model_config = ConfigDict(extra='forbid')

    timestamp: str
    status: int
    error: str
    path: str

    @field_validator('status')
    @classmethod
    def check_currency(cls, v: int) -> int:
        for value in HTTPStatus.__members__.values():
            if v == value.value:
                return v
        raise UnexpectedResponseStatus(f'Пришел неподдерживаемый http статус: {v}')


    @field_validator('timestamp')
    @classmethod
    def check_date(cls, v: str) -> str:
        try:
            datetime.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError(f'дата не в формате isoformat: {v}')
