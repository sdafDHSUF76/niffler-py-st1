import pytest
from configs import Configs
from utils.database import DB


@pytest.fixture
def clear_extra_users(db_niffler_auth: 'DB'):
    """Чистим созданных юзеров, кроме тестового."""
    db_niffler_auth.execute(
        'delete from authority'
        ' where user_id in (select id from "user" where username != \'%s\')'
        % Configs.TEST_USER,
    )
    db_niffler_auth.execute('delete from "user" where username != \'%s\'' % Configs.TEST_USER)
    yield
    db_niffler_auth.execute(
        'delete from authority'
        ' where user_id in (select id from "user" where username != \'%s\')'
        % Configs.TEST_USER,
    )
    db_niffler_auth.execute('delete from "user" where username != \'%s\'' % Configs.TEST_USER)


@pytest.fixture
def clear_category(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category после теста и до."""
    db_niffler_spend.execute('delete from category')
    yield
    db_niffler_spend.execute('delete from category')


@pytest.fixture
def clear_spend_and_category(db_niffler_spend: 'DB') -> None:
    """Чистим таблицу category и spend до и после теста."""
    db_niffler_spend.execute('delete from spend')
    db_niffler_spend.execute('delete from category')
    yield
    db_niffler_spend.execute('delete from spend')
    db_niffler_spend.execute('delete from category')
