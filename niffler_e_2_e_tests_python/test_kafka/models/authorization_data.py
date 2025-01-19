import pydantic
from pydantic import BaseModel, ConfigDict


class AuthorizationDataUser(BaseModel):
    model_config = ConfigDict(extra='forbid')

    user_name: str = pydantic.Field(alias='username')
