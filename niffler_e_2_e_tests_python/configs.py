import os
from dataclasses import dataclass

import dotenv

dotenv.load_dotenv(''.join((
    os.path.abspath(__file__).split(__name__.split('.')[0])[0],
    '.env',
)))


@dataclass
class Configs:
    FRONT_URL: str = os.getenv('FRONT_URL')
    GATEWAY_URL: str = os.getenv('GATEWAY_URL')
    AUTH_URL: str = os.getenv('AUTH_URL')
    TEST_USER: str = os.getenv('TEST_USER')
    TEST_PASSWORD: str = os.getenv('TEST_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: str = os.getenv('PORT_DB')
    DB_USER_NAME: str = os.getenv('DB_USER_NAME')
    PASSWORD_FOR_DB: str = os.getenv('PASSWORD_FOR_DB')
    DB_NAME_NIFFLER_USERDATA: str = os.getenv('DB_NAME_NIFFLER_USERDATA')
    DB_NAME_NIFFLER_SPEND: str = os.getenv('DB_NAME_NIFFLER_SPEND')
    DB_NAME_NIFFLER_CURRENCY: str = os.getenv('DB_NAME_NIFFLER_CURRENCY')
    DB_NAME_NIFFLER_AUTH: str = os.getenv('DB_NAME_NIFFLER_AUTH')
