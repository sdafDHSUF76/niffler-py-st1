import os

import dotenv

dotenv.load_dotenv(''.join((
    os.path.abspath(__file__).split(__name__.split('.')[0])[0],
    '.env',
)))

configs = {
    'FRONT_URL': os.getenv('FRONT_URL'),
    'GATEWAY_URL': os.getenv('GATEWAY_URL'),
    'AUTH_URL': os.getenv('AUTH_URL'),
    'TEST_USER': os.getenv('TEST_USER'),
    'TEST_PASSWORD': os.getenv('TEST_PASSWORD'),
    'DB_HOST': os.getenv('DB_HOST'),
    'DB_PORT': os.getenv('PORT_DB'),
    'DB_USER_NAME': os.getenv('DB_USER_NAME'),
    'PASSWORD_FOR_DB': os.getenv('PASSWORD_FOR_DB'),
    'DB_NAME_NIFFLER_USERDATA': os.getenv('DB_NAME_NIFFLER_USERDATA'),
    'DB_NAME_NIFFLER_SPEND': os.getenv('DB_NAME_NIFFLER_SPEND'),
    'DB_NAME_NIFFLER_CURRENCY': os.getenv('DB_NAME_NIFFLER_CURRENCY'),
    'DB_NAME_NIFFLER_AUTH': os.getenv('DB_NAME_NIFFLER_AUTH'),
}
