import re
from typing import Iterable

import structlog as structlog
from configs import configs
from sqlalchemy import Connection, Engine, Row, text
from sqlalchemy.orm import Session

logger = structlog.get_logger('sql')

DATABASE_NIFFLER_USERDATA_URL = (
    'postgresql+psycopg2://'
    f'{configs["DB_USER_NAME"]}:{configs["PASSWORD_FOR_DB"]}'
    f'@{configs["DB_HOST"]}:{configs["DB_PORT"]}/{configs["DB_NAME_NIFFLER_USERDATA"]}'
)
DATABASE_NIFFLER_SPEND_URL = (
    'postgresql+psycopg2://'
    f'{configs["DB_USER_NAME"]}:{configs["PASSWORD_FOR_DB"]}'
    f'@{configs["DB_HOST"]}:{configs["DB_PORT"]}/{configs["DB_NAME_NIFFLER_SPEND"]}'
)
DATABASE_NIFFLER_CURRENCY_URL = (
    'postgresql+psycopg2://'
    f'{configs["DB_USER_NAME"]}:{configs["PASSWORD_FOR_DB"]}'
    f'@{configs["DB_HOST"]}:{configs["DB_PORT"]}/{configs["DB_NAME_NIFFLER_CURRENCY"]}'
)
DATABASE_NIFFLER_AUTH_URL = (
    'postgresql+psycopg2://'
    f'{configs["DB_USER_NAME"]}:{configs["PASSWORD_FOR_DB"]}'
    f'@{configs["DB_HOST"]}:{configs["DB_PORT"]}/{configs["DB_NAME_NIFFLER_AUTH"]}'
)


class DB:
    """Содержит методы, для обращения в базу данных."""
    def __init__(self, connect: Engine):
        self.engine = connect
        self.conn: Connection = self.engine.connect()

    def get_db_name(self) -> str:
        """Get database name."""
        return self.conn.engine.url.database

    def get_value(self, query: str) -> list[Row]:
        """Получаем значения из базы данных"""

        with Session(self.conn) as session:
            result: Iterable[Row] = session.execute(text(query)).fetchall()
            logger.info('\nSQL result', database=self.get_db_name(), query=query, sql_result=result)
            return list(result)

    def get_answer_in_form_of_dictionary(self, query: str) -> list[dict]:
        """get list of dicts with column names and values from database of query."""
        result = []
        data = {}

        with Session(self.conn) as session:
            result_query: Iterable[Row] = session.execute(text(query)).fetchall()
            table_name: str = query.lower().split('from')[1].strip().split(' ')[0]
            if re.search(r'\*', query):
                columns_names: list[str] = [
                    unit[0] for unit in session.execute(text(
                        "SELECT column_name FROM information_schema.columns"
                        f" WHERE table_name = '{table_name}';"
                    )).fetchall()
                ]
            else:
                columns_names: list[str] = (
                    query.lower().split('from')[0].split('select')[1].strip().replace(' ', '')
                    .split(',')
                )
            for unit_of_data_received in result_query:
                data.update({x: y for x, y in zip(columns_names, unit_of_data_received)})
                result.append(data.copy())
                data.clear()
            logger.info('\nSQL result', database=self.get_db_name(), query=query, sql_result=result)

            return result

    def execute(self, query: str) -> None:
        """Выполнить определенный запрос, например Insert, Update,...все что кроме select."""
        with Session(self.conn) as session:
            session.execute(text(query))
            self.conn.commit()
            logger.info('\nSQL result', database=self.get_db_name(), query=query)

    def close(self) -> None:
        """Закрыть подключение к базе данных."""
        self.conn.close()
