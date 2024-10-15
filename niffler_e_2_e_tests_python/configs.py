class Configs:
    FRONT_URL: str = ''
    GATEWAY_URL: str = ''
    AUTH_URL: str = ''
    TEST_USER: str = None
    TEST_PASSWORD: str = None
    DB_HOST: str = None
    DB_PORT: str = None
    DB_USER_NAME: str = None
    PASSWORD_FOR_DB: str = None
    DB_NAME_NIFFLER_USERDATA: str = None
    DB_NAME_NIFFLER_SPEND: str = None
    DB_NAME_NIFFLER_CURRENCY: str = None
    DB_NAME_NIFFLER_AUTH: str = None
    DATABASE_NIFFLER_USERDATA_URL: str = None
    DATABASE_NIFFLER_SPEND_URL: str = None
    DATABASE_NIFFLER_CURRENCY_URL: str = None
    DATABASE_NIFFLER_AUTH_URL: str = None

    def __init__(
        self, front_url, gateway_url, auth_url, test_user, test_password, db_host, db_port,
        db_user_name, password_for_db, db_name_niffler_userdata, db_name_niffler_spend,
        db_name_niffler_currency, db_name_niffler_auth,
    ):
        self.FRONT_URL = front_url
        self.GATEWAY_URL = gateway_url
        self.AUTH_URL = auth_url
        self.TEST_USER = test_user
        self.TEST_PASSWORD = test_password
        self.DB_HOST = db_host
        self.DB_PORT = db_port
        self.DB_USER_NAME = db_user_name
        self.PASSWORD_FOR_DB = password_for_db
        self.DB_NAME_NIFFLER_USERDATA = db_name_niffler_userdata
        self.DB_NAME_NIFFLER_SPEND = db_name_niffler_spend
        self.DB_NAME_NIFFLER_CURRENCY = db_name_niffler_currency
        self.DB_NAME_NIFFLER_AUTH = db_name_niffler_auth
        self.DATABASE_NIFFLER_USERDATA_URL = (
            'postgresql+psycopg2://'
            f'{self.DB_USER_NAME}:{self.PASSWORD_FOR_DB}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME_NIFFLER_USERDATA}'
        )
        self.DATABASE_NIFFLER_SPEND_URL = (
            'postgresql+psycopg2://'
            f'{self.DB_USER_NAME}:{self.PASSWORD_FOR_DB}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME_NIFFLER_SPEND}'
        )
        self.DATABASE_NIFFLER_CURRENCY_URL = (
            'postgresql+psycopg2://'
            f'{self.DB_USER_NAME}:{self.PASSWORD_FOR_DB}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME_NIFFLER_CURRENCY}'
        )
        self.DATABASE_NIFFLER_AUTH_URL = (
            'postgresql+psycopg2://'
            f'{self.DB_USER_NAME}:{self.PASSWORD_FOR_DB}'
            f'@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME_NIFFLER_AUTH}'
        )

        self.fill_class_with_data(
            self.FRONT_URL, self.GATEWAY_URL, self.AUTH_URL, self.TEST_USER, self.TEST_PASSWORD,
            self.DB_HOST, self.DB_PORT, self.DB_USER_NAME, self.PASSWORD_FOR_DB,
            self.DB_NAME_NIFFLER_USERDATA, self.DB_NAME_NIFFLER_SPEND,
            self.DB_NAME_NIFFLER_CURRENCY, self.DB_NAME_NIFFLER_AUTH,
            self.DATABASE_NIFFLER_USERDATA_URL, self.DATABASE_NIFFLER_SPEND_URL,
            self.DATABASE_NIFFLER_CURRENCY_URL, self.DATABASE_NIFFLER_AUTH_URL,
        )

    @classmethod
    def fill_class_with_data(
        cls, front_url, gateway_url, auth_url, test_user, test_password, db_host, db_port,
        db_user_name, password_for_db, db_name_niffler_userdata, db_name_niffler_spend,
        db_name_niffler_currency, db_name_niffler_auth, database_niffler_userdata_url,
        database_niffler_spend_url, database_niffler_currency_url, database_niffler_auth_url,
    ):
        cls.FRONT_URL = front_url
        cls.GATEWAY_URL = gateway_url
        cls.AUTH_URL = auth_url
        cls.TEST_USER = test_user
        cls.TEST_PASSWORD = test_password
        cls.DB_HOST = db_host
        cls.DB_PORT = db_port
        cls.DB_USER_NAME = db_user_name
        cls.PASSWORD_FOR_DB = password_for_db
        cls.DB_NAME_NIFFLER_USERDATA = db_name_niffler_userdata
        cls.DB_NAME_NIFFLER_SPEND = db_name_niffler_spend
        cls.DB_NAME_NIFFLER_CURRENCY = db_name_niffler_currency
        cls.DB_NAME_NIFFLER_AUTH = db_name_niffler_auth
        cls.DATABASE_NIFFLER_USERDATA_URL = database_niffler_userdata_url
        cls.DATABASE_NIFFLER_SPEND_URL = database_niffler_spend_url
        cls.DATABASE_NIFFLER_CURRENCY_URL = database_niffler_currency_url
        cls.DATABASE_NIFFLER_AUTH_URL = database_niffler_auth_url
