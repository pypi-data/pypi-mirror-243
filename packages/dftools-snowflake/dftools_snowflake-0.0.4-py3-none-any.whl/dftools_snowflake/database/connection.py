from typing import Optional
from dataclasses import dataclass

import snowflake.connector

from dftools.events.events import ConnectionOpened
from dftools.core.database.base import ConnectionCredentials, ConnectionWrapper, ConnectionState


@dataclass
class SnowflakeCredentials(ConnectionCredentials):
    account: str
    user: str
    password: Optional[str] = None
    authenticator: Optional[str] = None
    role: Optional[str] = None
    warehouse: Optional[str] = None

    @property
    def type(self) -> str:
        return "snowflake"


@dataclass
class SnowflakeConnectionWrapper(ConnectionWrapper):

    @property
    def type(self) -> str:
        return "snowflake"

    def open(self):
        if self.credentials is not None :
            self.connection = snowflake.connector.connect(
                account=self.credentials.account
                , user=self.credentials.user
                , authenticator=self.credentials.authenticator
                , password=self.credentials.password
            )
            self.state = ConnectionState.OPEN
            self.log_event(ConnectionOpened(connection_name=self.name))
        return self

    def _get_active_catalog(self) -> str:
        return self.credentials.catalog

    def _get_active_schema(self) -> str:
        return self.credentials.schema
