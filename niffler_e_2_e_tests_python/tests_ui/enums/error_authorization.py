from enum import Enum


class ErrorAuthorization(str, Enum):
    INVALID_USER_CREDENTIALS = 'Неверные учетные данные пользователя'
