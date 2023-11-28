import abc
from typing import Optional, Type, Any
from dataclasses import dataclass
from strenum import StrEnum

from dftools.exceptions import NotImplementedMethodException, RequestOnClosedConnectionException
from dftools.events import DfLoggable
from dftools.events.events import ConnectionClosed
from dftools.core.structure import Namespace

@dataclass
class ConnectionCredentials(metaclass=abc.ABCMeta):
    catalog: Optional[str]
    schema: Optional[str]

    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedError('The type method is not implemented for class : ' + str(type(self)))


class ConnectionState(StrEnum):
    INIT = "init"
    OPEN = "open"
    CLOSED = "closed"
    FAIL = "fail"


@dataclass
class ConnectionWrapper(DfLoggable):
    name: str = 'DFT'
    session_id : str = None
    state: ConnectionState = ConnectionState.INIT
    credentials: Optional[Type[ConnectionCredentials]] = None
    connection: Optional[Any] = None

    def __post_init__(self):
        self._init_logger()

    @property
    @abc.abstractmethod
    def type(self) -> str:
        raise NotImplementedMethodException(self, 'type')

    # Open/Close connection methods
    @abc.abstractmethod
    def open(self):
        """
        Opens the connection based on the available credentials.
        If the connection was successfully opened, the opened connection is loaded into the connection attribute
        and the state of connection wrapper is set to OPEN

        Returns
        -------
            The connection wrapper
        """
        raise NotImplementedMethodException(self, 'open')

    def close(self):
        """
        Closes the connection

        Returns
        -------
            This connection wrapper
        """
        if self.state in {ConnectionState.CLOSED, ConnectionState.INIT}:
            return self

        connection_closed = self._close_connection()
        if connection_closed:
            self.state = ConnectionState.CLOSED
            self.log_event(ConnectionClosed(connection_name=self.name))

        return self

    def _close_connection(self) -> bool:
        """
        Close the connection

        Returns
        -------
            True if the connection was closed. False, otherwise.
        """
        """Perform the actual close operation."""
        if hasattr(self.connection, "close"):
            self.connection.close()
            return True
        return False

    # Connection status methods
    def is_opened(self) -> bool:
        """
        Checks if the connection is currently opened

        Returns
        -------
            True if the connection is opened
        """
        return self.state == ConnectionState.OPEN

    # Active connection methods
    def get_active_catalog(self) -> str:
        """
        Get the active catalog name.
        Raises a RequestOnClosedConnection exception if the connection is not opened

        Returns
        -------

        """
        if not self.is_opened():
            raise RequestOnClosedConnectionException(self.name, 'Get Active Catalog')
        return self._get_active_catalog()

    @abc.abstractmethod
    def _get_active_catalog(self) -> str:
        """
        Get the active catalog name.
        Should be called only when connection is opened

        Returns
        -------
            The currently active catalog name
        """
        raise NotImplementedMethodException(self, '_get_active_catalog')

    def get_active_schema(self) -> str:
        """
        Get the active schema name.
        Raises a RequestOnClosedConnection exception if the connection is not opened

        Returns
        -------

        """
        if not self.is_opened():
            raise RequestOnClosedConnectionException(self.name, 'Get Active Schema')
        return self._get_active_schema()

    @abc.abstractmethod
    def _get_active_schema(self) -> str:
        """
        Get the active schema name.
        Should be called only when connection is opened

        Returns
        -------
            The currently active catalog name
        """
        raise NotImplementedMethodException(self, '_get_active_schema')

    def get_active_namespace(self) -> Namespace:
        return Namespace(
            databank_name='Snowflake', catalog=self.get_active_catalog(), namespace=self.get_active_schema())
