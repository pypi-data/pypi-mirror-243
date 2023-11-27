from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
try:
    from mobio.libs.logging import MobioLogging
    m_log = MobioLogging()
except Exception:
    import logging as MobioLogging
    m_log = MobioLogging
import re
from sqlalchemy.sql import sqltypes


class DOUBLE(sqltypes.Float):  # pylint: disable=no-init
    __visit_name__ = "DOUBLE"


class BaseDialect:
    def __init__(self, olap_uri):
        self.olap_uri = olap_uri
        self.session_class = None

    def normalize_uuid(self, data: str) -> UUID:
        return UUID(data)

    def __check_column_valid_name__(self, column_name):
        return re.search('^[A-Za-z0-9]+[A-Za-z0-9_][A-Za-z0-9]$', column_name)

    def __type_mapping__(self, python_data_type):
        _type_map = {
            # === Boolean ===
            "boolean": sqltypes.BOOLEAN,
            # === Integer ===
            "tinyint": sqltypes.SMALLINT,
            "smallint": sqltypes.SMALLINT,
            "int": sqltypes.INTEGER,
            "bigint": sqltypes.BIGINT,
            "long": sqltypes.BIGINT,
            # === Floating-point ===
            "float": sqltypes.FLOAT,
            "double": DOUBLE,
            # === Fixed-precision ===
            "decimal": sqltypes.DECIMAL,
            # === String ===
            "varchar": sqltypes.VARCHAR,
            "char": sqltypes.CHAR,
            "str": sqltypes.STRINGTYPE,
            "string": sqltypes.STRINGTYPE,
            "json": sqltypes.JSON,
            # === Date and time ===
            "date": sqltypes.DATE,
            "timestamp": sqltypes.DATETIME,
            'datetime': sqltypes.DATETIME,
        }
        match = re.match(r"^(?P<type>\w+)\s*(?:(?:\(|<)(?P<options>.*)(?:\)|>))?", python_data_type)
        type_name = match.group("type")
        type_opts = match.group("options")
        if type_name not in _type_map:
            raise Exception({"code": -1, "detail": f"data_type: {type_name} is not support"})
        return f"{type_name}({type_opts})" if type_opts else f"{type_name}"

    def add_column(self, table, column_name, python_data_type):
        if not self.__check_column_valid_name__(column_name=column_name):
            raise Exception(f"add column {column_name} error. Column name not valid.")
        data_type = self.__type_mapping__(python_data_type=python_data_type)
        stmt = f"""
                alter table {table} add COLUMN {column_name} {data_type}
                """

        with self.session_class.SessionLocal() as session:
            try:
                session.execute(
                    text(stmt)
                )
                return True
            except ProgrammingError as pe:
                # if pe.code == 'f405':
                #     return True
                m_log.warning(
                    f"fail when alter table {table}, add column: {column_name} with data_type: {data_type}: {pe}"
                )
                return False

    def drop_column(self, table, column_name):
        if not self.__check_column_valid_name__(column_name=column_name):
            raise Exception(f"drop column {column_name} error. Column name not valid.")
        stmt = f"""
                alter table {table} drop COLUMN {column_name}
            """

        with self.session_class.SessionLocal() as session:
            try:
                session.execute(
                    text(stmt)
                )
                return True
            except ProgrammingError as pe:
                # if pe.code == 'f405':
                #     return True
                m_log.warning(
                    f"fail when alter table {table}, drop column: {column_name}: {pe}"
                )
                return False
