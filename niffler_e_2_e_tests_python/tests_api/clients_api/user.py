from typing import TYPE_CHECKING

from tests_api.clients_api.authorization import Authorization
from tests_api.clients_api.constants.api_paths import PathUrl
from tests_api.enums.http_methods import HttpMethods

if TYPE_CHECKING:
    from requests import Response


class User(Authorization):

    def create_user(self, user_name: str, password: str) -> 'Response':
        """Создать пользователя."""
        cookie: str = '; '.join((
            self.request(HttpMethods.GET, '/').history[0].headers['Set-Cookie'].replace(
                ', ', ''
            ).split('; Path=/')[:2]
        ))
        return self.request(
            HttpMethods.POST,
            PathUrl.REGISTER,
            data=dict(
                _csrf=cookie.split('; ')[0].split('XSRF-TOKEN=')[1],
                username=user_name,
                password=password,
                passwordSubmit=password,
            ),
            headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': cookie},
        )
