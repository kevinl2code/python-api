from pypika import Table
from pypika.queries import Query, Schema


class BaseTable(Table):
    schema = Schema("public")

    def __init__(
        self, name: str, alias: str | None = None, query_cls: type[Query] | None = None
    ) -> None:
        super().__init__(name, self.schema, alias, query_cls)
