import os
from dataclasses import dataclass, field

import dotenv

dotenv.load_dotenv(''.join((os.path.abspath(__file__).split(__name__.split('.')[0])[0], '.env')))


@dataclass
class Configs:
    FRONT_URL: str = field(default=os.getenv('FRONT_URL'), init=False)
    GATEWAY_URL: str = field(default=os.getenv('GATEWAY_URL'), init=False)
    AUTH_URL: str = field(default=os.getenv('AUTH_URL'), init=False)
    TEST_USER: str = field(default=os.getenv('TEST_USER'), init=False)
    TEST_PASSWORD: str = field(default=os.getenv('TEST_PASSWORD'), init=False)
    DB_HOST: str = field(default=os.getenv('DB_HOST'), init=False)
    DB_PORT: str = field(default=os.getenv('PORT_DB'), init=False)
    DB_USER_NAME: str = field(default=os.getenv('DB_USER_NAME'), init=False)
    PASSWORD_FOR_DB: str = field(default=os.getenv('PASSWORD_FOR_DB'), init=False)
    DB_NAME_NIFFLER_USERDATA: str = field(default=os.getenv('DB_NAME_NIFFLER_USERDATA'), init=False)
    DB_NAME_NIFFLER_SPEND: str = field(default=os.getenv('DB_NAME_NIFFLER_SPEND'), init=False)
    DB_NAME_NIFFLER_CURRENCY: str = field(default=os.getenv('DB_NAME_NIFFLER_CURRENCY'), init=False)
    DB_NAME_NIFFLER_AUTH: str = field(default=os.getenv('DB_NAME_NIFFLER_AUTH'), init=False)
