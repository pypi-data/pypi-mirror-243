from dataclasses import dataclass
from enum import Enum

from converter.database_worker import get_type_sql_alchemy
from converter.pg_ch_converter.table_generator import PgChCreator


class ChangeEvent(Enum):
    DELETE = 1
    ADD = 2
    TYPE_UPDATE = 3


@dataclass
class ColumnChangeEvent:
    """Class for updating column"""

    change_event: ChangeEvent
    column_name: str
    column_type: str = None
    column_name_prev: str = None

    def __str__(self):
        return f"column_name: {self.column_name}, column_name_prev: {self.column_name_prev}, column_type: {self.column_type}"


class SchemaChecker(PgChCreator):

    def __init__(self, sql_credentials, table_name_pg, table_name_ch, **kwargs):
        self.events_list: list[ColumnChangeEvent] = []
        self.table_name_pg = table_name_pg
        self.table_name_ch = table_name_ch

        self.kwargs = kwargs
        self.exclude_columns_ch = self.kwargs.get("exclude_columns_ch", "").split(",")
        self.sql_credentials = sql_credentials
        super().__init__(
            self.sql_credentials,
            from_db="pg",
            to_db="ch",
            table_name_ch=self.table_name_ch,
            table_name_pg=self.table_name_pg,
            **self.kwargs,
        )

    def get_difference_events(self, exclude_function=None):
        """
        Get list
        :param exclude_function:
        :return:
        """
        columns_from = self.db_worker_from.get_table_schema(self.table_name_pg)
        columns_to = self.db_worker_to.get_table_schema(self.table_name_ch)

        if exclude_function:
            exclude_function(columns_to)

        names_from = [
            n["column_name"]
            for n in columns_from
            if n["column_name"] not in self.exclude_columns_ch
        ]
        names_to = [
            n["column_name"]
            for n in columns_to
            if n["column_name"] not in self.exclude_columns_ch
        ]

        columns_to_add = [
            c
            for c in columns_from
            if c["column_name"] in set(names_from).difference(set(names_to))
        ]

        for c in columns_to_add:
            position = names_from.index(c["column_name"])
            prev_column_pg = (
                names_from[position - 1]
                if (position > 0 and c["column_name"] in names_from)
                else None
            )
            column_type = self.update_column_type(c)
            cce = ColumnChangeEvent(
                change_event=ChangeEvent.ADD,
                column_name=c["column_name"],
                column_type=column_type,
                column_name_prev=prev_column_pg,
            )

            self.events_list.append(cce)

        columns_to_delete = [
            c
            for c in columns_to
            if c["column_name"] in set(names_to).difference(set(names_from))
        ]

        for c in columns_to_delete:
            cce = ColumnChangeEvent(
                change_event=ChangeEvent.DELETE, column_name=c["column_name"]
            )
            self.events_list.append(cce)

        columns_to_common = [
            c
            for c in columns_to
            if c["column_name"] in set(names_to).intersection(set(names_from))
        ]
        columns_from_common = [
            c
            for c in columns_from
            if c["column_name"] in set(names_to).intersection(set(names_from))
        ]

        for cf, ct in zip(columns_from_common, columns_to_common):
            if get_type_sql_alchemy(self.update_column_type(cf)) != ct["data_type"]:
                cce = ColumnChangeEvent(
                    change_event=ChangeEvent.TYPE_UPDATE,
                    column_name=cf["column_name"],
                    column_type=self.update_column_type(cf),
                )
                self.events_list.append(cce)

        return self.events_list

    def alter_statement(self, event: ChangeEvent) -> str:
        """

        :param event:
        :return:
        """
        ddl = f"ALTER TABLE {self.table_name_ch} ON CLUSTER '{{cluster}}'"

        if event.change_event == ChangeEvent.ADD:
            ddl += f" ADD COLUMN {event.column_name} {event.column_type.__name__}"
            if event.column_name_prev:
                ddl += f" AFTER  {event.column_name_prev}"

        elif event.change_event == ChangeEvent.DELETE:
            ddl += f" DROP COLUMN {event.column_name}"

        elif event.change_event == ChangeEvent.TYPE_UPDATE:
            ddl += f" MODIFY COLUMN  {event.column_name} {event.column_type.__name__}"
        else:
            return None

        return ddl
