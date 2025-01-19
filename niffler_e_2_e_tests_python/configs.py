from dataclasses import dataclass


@dataclass(eq=False, repr=False, order=False)
class Configs:
    FRONT_URL: str
    GATEWAY_URL: str
    AUTH_URL: str
    TEST_USER: str
    TEST_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_USER_NAME: str
    PASSWORD_FOR_DB: str
    DB_NAME_NIFFLER_USERDATA: str
    DB_NAME_NIFFLER_SPEND: str
    DB_NAME_NIFFLER_CURRENCY: str
    DB_NAME_NIFFLER_AUTH: str
    DATABASE_NIFFLER_USERDATA_URL: str
    DATABASE_NIFFLER_SPEND_URL: str
    DATABASE_NIFFLER_CURRENCY_URL: str
    DATABASE_NIFFLER_AUTH_URL: str
    KAFKA_ADDRESS: str

    def __init__(
        self, front_url: str, gateway_url: str, auth_url: str, test_user: str, test_password: str,
        db_host: str, db_port: str, db_user_name: str, password_for_db: str,
        db_name_niffler_userdata: str, db_name_niffler_spend: str, db_name_niffler_currency: str,
        db_name_niffler_auth: str, kafka_address: str,
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
        self.KAFKA_ADDRESS = kafka_address
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
            self.DATABASE_NIFFLER_CURRENCY_URL, self.DATABASE_NIFFLER_AUTH_URL, self.KAFKA_ADDRESS,
        )

    @classmethod
    def fill_class_with_data(
        cls, front_url: str, gateway_url: str, auth_url: str, test_user: str, test_password: str,
        db_host: str, db_port: str, db_user_name: str, password_for_db: str,
        db_name_niffler_userdata: str, db_name_niffler_spend: str, db_name_niffler_currency: str,
        db_name_niffler_auth: str, database_niffler_userdata_url: str,
        database_niffler_spend_url: str, database_niffler_currency_url: str,
        database_niffler_auth_url: str, kafka_address: str,
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
        cls.KAFKA_ADDRESS = kafka_address
