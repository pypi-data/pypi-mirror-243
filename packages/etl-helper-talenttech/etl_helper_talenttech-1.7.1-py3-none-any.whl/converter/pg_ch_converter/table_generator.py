"""
Class for automatically the creation of the table in clickhouse based on schema in python
"""
from converter.fields_converter import FieldsConverter, types_converter_dict
from sqlalchemy import Column, types, text, MetaData
from clickhouse_sqlalchemy import Table, engines
from clickhouse_sqlalchemy.drivers.base import ischema_names


class ReplicatedMergeTreeMY(engines.ReplicatedMergeTree):
    """
    Override engine for removing path and name
    """

    @property
    def name(self):
        return "ReplicatedMergeTree"

    def get_parameters(self):
        return [""]


class PgChCreator(FieldsConverter):
    """
    Class to check table in ch or create new ddl
    """

    def __init__(self, sql_credentials, table_name_pg, table_name_ch, **kwargs):
        """

        :param sql_credentials:
        :param table_name_pg: --table_name from table
        """

        self.table_name_pg = table_name_pg
        self.table_name_ch = table_name_ch
        self.kwargs = kwargs
        self._sorting_key = text(self.kwargs.get("sorting_key", "id") or "id")
        self._partition_key = text(
            self.kwargs.get("partition_key", "tuple()") or "tuple()"
        )

        self.sql_credentials = sql_credentials
        super().__init__(
            self.sql_credentials,
            from_db="pg",
            to_db="ch",
            tables=list(set([self.table_name_pg, self.table_name_ch])),
        )

    def update_column_type(self, column):
        """convert types between source and destination"""
        type_from = column["data_type"]
        types_conv = types_converter_dict[self.key]["type"]
        types_conv.update(self.kwargs.get("custom_types", {}))
        if type_from in types_conv:
            type_to = types_conv[type_from.lower()]
        else:
            type_to = type_from.lower()

        ischema_names_lower = dict((k.lower(), v) for k, v in ischema_names.items())

        return ischema_names_lower.get(type_to.lower(), types.String)

    def create_table(self, insert_func=None) -> str:
        """
        Create table by declarative way
        :param insert_func: optional function to add custom Columns
        :return:
        """
        columns_pg = self.db_worker_from.get_table_schema(self.table_name_pg)

        alchemy_columns_ch = [
            Column(name=column["column_name"], type_=self.update_column_type(column))
            for column in columns_pg
        ]
        if insert_func:
            insert_func(columns_pg, alchemy_columns_ch)

        table = Table(
            self.table_name_ch,
            MetaData(self.db_worker_to.engine),
            *alchemy_columns_ch,
            ReplicatedMergeTreeMY(
                "", "", partition_by=self.partition_key, order_by=self.sorting_key
            ),
            clickhouse_cluster="{cluster}",
            keep_existing=True
        )
        return table

    @property
    def sorting_key(self) -> str:
        """

        :return:
        """
        return self._sorting_key

    @sorting_key.setter
    def sorting_key(self, arg: str):
        """

        :param arg:
        :return:
        """
        self._sorting_key = arg

    @property
    def partition_key(self) -> str:
        """

        :return:
        """
        return self._partition_key

    @partition_key.setter
    def partition_key(self, arg: str):
        """

        :param arg:
        :return:
        """
        self._partition_key = arg
