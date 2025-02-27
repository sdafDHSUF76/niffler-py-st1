import re
from typing import TYPE_CHECKING, Iterable

import allure
import structlog as structlog
from allure_commons.types import AttachmentType
from sqlalchemy import Connection, Engine, Row, event, text
from sqlalchemy.orm import Session

if TYPE_CHECKING:
    import cursor as cursor_
    from sqlalchemy.dialects.postgresql.psycopg2 import PGExecutionContext_psycopg2

logger = structlog.get_logger('sql')


class DB:
    """Содержит методы, для обращения в базу данных."""
    def __init__(self, connect: Engine):
        self.engine = connect
        self.conn: Connection = self.engine.connect()
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    def attach_sql(
        cursor: 'cursor_', statement: str, parameters: dict, context: 'PGExecutionContext_psycopg2',
    ):
        """Приаттачить sql query к шагу, где происходит запрос.

        *cursor обязателен, как и другие параметры,
        так как в этот метод hook передает свои параметры, и если их не
        указать, то метод будет падать, от избытка полученных параметров.
        """
        statement_with_params: str = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

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
