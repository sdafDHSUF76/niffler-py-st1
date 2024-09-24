from enum import Enum


class PathUrl(str, Enum):
    """Все пути из API niffler."""
    ADD_CATEGORY = '/api/categories/add'
    ADD_SPEND = '/api/spends/add'
    REGISTER = '/register'
    OAUTH2_AUTHORIZATION = '/oauth2/authorize'
    OAUTH2_TOKEN = '/oauth2/token'
    AUTHORIZATION = '/authorized'
    LOGIN = '/login'

    def __str__(self) -> str:
        return self.value
