from pypika import Field

from .base_table import BaseTable


class Users(BaseTable):
    def __init__(self) -> None:
        super().__init__("users")
        self.firstName = Field("firstName", table=self)
        self.lastName = Field("lastName", table=self)
        self.email = Field("email", table=self)
        self.type = Field("type", table=self)
        self.conversation = Field("conversation", table=self)
        self.location = Field("location", table=self)
