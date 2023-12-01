from uuid import UUID
from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError
from typing import Any, Dict, List
try:
    from mobio.libs.logging import MobioLogging

    m_log = MobioLogging()
except Exception:
    import logging as MobioLogging

    m_log = MobioLogging
import re
from sqlalchemy.sql import sqltypes
from mobio.libs.olap.mining_warehouse.datatype import _type_map, parse_sqltype


class DOUBLE(sqltypes.Float):  # pylint: disable=no-init
    __visit_name__ = "DOUBLE"


class BaseDialect:
    def __init__(self, olap_uri):
        self.olap_uri = olap_uri
        self.session_class = None

    def normalize_uuid(self, data: str) -> UUID:
        return UUID(data)

    @staticmethod
    def __check_column_valid_name__(column_name):
        """
        name của column có thể valid nếu thỏa mãn các điều kiện sau:
        1) bắt đầu bằng ký tự gạch chân (_) hoặc là chữ cái, số
        2) tiếp theo là chữ cái hoặc số (1 hoặc nhiều)
        3) tiếp theo có thể bao gồm ký tự gạch chân (_)
        4) kết thúc bằng 1 hoặc nhiều ký tự hoặc số
        :param column_name:
        :return:
        """
        return re.search("^[a-z_][A-Za-z0-9]+[A-Za-z0-9_]+[A-Za-z0-9]+$", column_name)

    @staticmethod
    def __check_contain_special_char__(data: str) -> bool:
        return True if not re.match("^[\w&\-_]+$", data) else False

    @staticmethod
    def __type_mapping__(python_data_type):

        match = re.match(
            r"^(?P<type>\w+)\s*(?:(?:\(|<)(?P<options>.*)(?:\)|>))?", python_data_type
        )
        type_name = match.group("type")
        type_opts = match.group("options")
        if type_name not in _type_map:
            raise Exception(
                {"code": -1, "detail": f"data_type: {type_name} is not support"}
            )
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
                session.execute(text(stmt))
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
                session.execute(text(stmt))
                return True
            except ProgrammingError as pe:
                # if pe.code == 'f405':
                #     return True
                m_log.warning(
                    f"fail when alter table {table}, drop column: {column_name}: {pe}"
                )
                return False

    def has_table(self, table_name: str, schema: str) -> bool:
        """
        :param table_name: tên của bảng cần kiểm tra
        :param schema: tên của database cần kiển tra
        :return: true nếu bảng đã tồn tại, else false
        """
        if self.__check_contain_special_char__(
            table_name
        ) or self.__check_contain_special_char__(schema):
            raise Exception(f"table_name {table_name} or schema {schema} is not valid")
        with self.session_class.SessionLocal() as session:
            try:
                result = session.execute(
                    text(f"DESCRIBE {schema}.{table_name}")
                ).first()
                return True if result else False
            except ProgrammingError as pe:
                # if pe.code == 'f405':
                #     return True
                m_log.warning(f"fail when check has_table {schema}.{table_name}: {pe}")
                return False

    def get_schema_names(self) -> list:
        with self.session_class.SessionLocal() as session:
            try:
                result = session.execute(text(f"SHOW schemas")).all()
                return [
                    x[0]
                    for x in result
                    if x[0] not in ["_statistics_", "information_schema", "sys"]
                ]
            except Exception as ex:
                m_log.warning("fail when get_schema_names: {}".format(ex))
                return []

    def get_table_names(self, schema):
        """Return a Unicode SHOW TABLES from a given schema."""
        if self.__check_contain_special_char__(schema):
            raise Exception(f"schema {schema} is not valid")
        with self.session_class.SessionLocal() as session:
            try:
                result = session.execute(text(f"SHOW FULL TABLES FROM {schema}")).all()
                return [row[0] for row in result if row[1] == "BASE TABLE"]
            except Exception as ex:
                m_log.warning("fail when get_table_names: {}".format(ex))
                return []

    def get_view_names(self, schema):
        if self.__check_contain_special_char__(schema):
            raise Exception(f"schema {schema} is not valid")
        with self.session_class.SessionLocal() as session:
            try:
                result = session.execute(text(f"SHOW FULL TABLES FROM {schema}")).all()
                return [row[0] for row in result if row[1] in ("VIEW", "SYSTEM VIEW")]
            except Exception as ex:
                m_log.warning("fail when get_table_names: {}".format(ex))
                return []

    def get_columns(self, table_name: str, schema: str = None) -> List[Dict[str, Any]]:
        if self.__check_contain_special_char__(
            table_name
        ) or self.__check_contain_special_char__(schema):
            raise Exception(f"table_name {table_name} or schema {schema} is not valid")
        full_name = str(table_name)
        if schema:
            full_name = "{}.{}".format(str(schema), full_name)
        with self.session_class.SessionLocal() as session:
            try:
                result = session.execute(text(f"SHOW COLUMNS FROM {full_name}")).all()
                columns = []
                for record in result:
                    column = dict(
                        name=record.Field,
                        type=parse_sqltype(record.Type),
                        nullable=record.Null == "YES",
                        default=record.Default,
                    )
                    columns.append(column)
                return columns
            except Exception as ex:
                m_log.warning("fail when get_table_names: {}".format(ex))
                return []


