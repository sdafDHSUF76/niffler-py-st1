from typing import TYPE_CHECKING

import pytest
from allure_commons.reporter import AllureReporter
from sqlalchemy import create_engine
from utils.database import (
    DATABASE_NIFFLER_AUTH_URL,
    DATABASE_NIFFLER_CURRENCY_URL,
    DATABASE_NIFFLER_SPEND_URL,
    DATABASE_NIFFLER_USERDATA_URL,
    DB,
)

if TYPE_CHECKING:
    from _pytest.config import PytestPluginManager
    from _pytest.fixtures import SubRequest
    from pytest import FixtureDef


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


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_fixture_setup(fixturedef: 'FixtureDef', request: 'SubRequest'):
    yield
    # Очищаем из тега allure упоминание о usefixtures
    if len(request.node.own_markers):
        [
            request.node.own_markers.pop(i) for i, value in enumerate(request.node.own_markers)
            if value.name == 'usefixtures'
        ]
    # добавляем в к тексту allure обозначения scope у фикстур setup, teardown
    plugins: 'PytestPluginManager' = request.config.pluginmanager
    if plugins.has_plugin('allure_listener'):
        logger: AllureReporter = plugins.get_plugin('allure_listener').allure_logger
        item = logger.get_last_item()
        scope_letter = fixturedef.scope[0].upper()
        item.name = f"[{scope_letter}] " + " ".join(fixturedef.argname.split("_")).title()
    # TODO сделать так и для teardown, а то у них нету буквы

# TODO сделать фикстуру, что удаляет после всех тестов юзеров, что не тестовый
