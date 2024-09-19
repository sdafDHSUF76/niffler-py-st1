import pytest
from playwright.sync_api import Browser, Page, sync_playwright
from sqlalchemy import create_engine
from utils.database import (
    DATABASE_NIFFLER_AUTH_URL,
    DATABASE_NIFFLER_CURRENCY_URL,
    DATABASE_NIFFLER_SPEND_URL,
    DATABASE_NIFFLER_USERDATA_URL,
    DB,
)


@pytest.fixture(scope='session')
def db_niffler_auth() -> DB:
    """Получаем доступ к базе данных niffler_auth, чтобы делать в ней запросы."""
    mydb: DB = DB(
        create_engine(
            DATABASE_NIFFLER_AUTH_URL,
            # pool_size=os.getenv("DATABASE_POOL_SIZE", 10)
        ),
    )
    yield mydb
    mydb.close()


@pytest.fixture(scope='session')
def db_niffler_currency() -> DB:
    """Получаем доступ к базе данных niffler_currency, чтобы делать в ней запросы."""
    mydb: DB = DB(
        create_engine(
            DATABASE_NIFFLER_CURRENCY_URL,
            # pool_size=os.getenv("DATABASE_POOL_SIZE", 10)
        ),
    )
    yield mydb
    mydb.close()


@pytest.fixture(scope='session')
def db_niffler_spend() -> DB:
    """Получаем доступ к базе данных niffler_spend, чтобы делать в ней запросы."""
    mydb: DB = DB(
        create_engine(
            DATABASE_NIFFLER_SPEND_URL,
            # pool_size=os.getenv("DATABASE_POOL_SIZE", 10)
        ),
    )
    yield mydb
    mydb.close()


@pytest.fixture(scope='session')
def db_niffler_userdata() -> DB:
    """Получаем доступ к базе данных niffler_userdata, чтобы делать в ней запросы."""
    mydb: DB = DB(
        create_engine(
            DATABASE_NIFFLER_USERDATA_URL,
            # pool_size=os.getenv("DATABASE_POOL_SIZE", 10)
        ),
    )
    yield mydb
    mydb.close()


@pytest.fixture(scope='session')
def driver() -> Page:
    """Получить WebDriver."""
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(channel="chrome", headless=False)
        page: Page = browser.new_page()
        yield page
        page.close()
        browser.close()
