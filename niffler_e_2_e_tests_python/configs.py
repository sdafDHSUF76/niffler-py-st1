import os

import dotenv

dotenv.load_dotenv(''.join((
    os.path.abspath(__file__).split(__name__.split('.')[1])[0],
    '.env',
)))

FRONT_URL1 = os.getenv('FRONT_URL1')
GATEWAY_URL = os.getenv('GATEWAY_URL')
AUTH_URL = os.getenv('AUTH_URL')
TEST_USER = os.getenv('TEST_USER')
TEST_PASSWORD = os.getenv('TEST_PASSWORD')
DB_HOST = os.getenv('HOST_DB_IN_DOCKER')
DB_PORT = os.getenv('PORT_DB')
DB_USER = os.getenv('USER_NAME')
DB_PASS = os.getenv('PASSWORD_FOR_DB')
DB_NAME_NIFFLER_USERDATA = os.getenv('DB_NAME_NIFFLER_USERDATA')
DB_NAME_NIFFLER_SPEND = os.getenv('DB_NAME_NIFFLER_SPEND')
DB_NAME_NIFFLER_CURRENCY = os.getenv('DB_NAME_NIFFLER_CURRENCY')
DB_NAME_NIFFLER_AUTH = os.getenv('DB_NAME_NIFFLER_AUTH')
