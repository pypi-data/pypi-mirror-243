import abc
import os
import csv
from typing import Dict, List, Tuple

from dftools.core.database.base.query_result import QueryExecResult, QueryExecResults
from dftools.core.database.base.query_wrapper import QueryWrapper
from dftools.core.database.base.connection import (
    ConnectionWrapper,
    ConnectionState
)
from dftools.core.database.base.connection_metadata import (
    BaseConnectionMetadataService
)
from dftools.exceptions import (
    NotImplementedMethodException,
    NoConnectionAvailableException,
    ConnectionAlreadyAvailableException,
    MissingMandatoryArgumentException,
    NoFileAtLocationException
)
from dftools.core.structure import StructureCatalog, StructureCatalogCsv
from dftools.events import DfLoggable, StandardErrorEvent, StandardWarningEvent, StandardExtendedInfoEvent
from dftools.events.events import CSVFileWriteSuccessful


class BaseConnectionAdapterManager(DfLoggable, metaclass=abc.ABCMeta):
    """
    Base Connection Manager should be inherited for a specific database type

    Multiple connections can be created and should be stored by a unique name.
    If no name is provided when adding the connection, the default connection name will be used
    """

    DEFAULT_CONNECTION_NAME = 'DFT'

    def __init__(self, metadata_service: BaseConnectionMetadataService):
        self.connections: Dict[str, ConnectionWrapper] = {}
        self._init_logger()
        self.metadata_service = metadata_service

    # Local Connection Management
    def add_connection(self, name: str, conn_wrapper: ConnectionWrapper):
        if name in self.connections.keys():
            raise ConnectionAlreadyAvailableException(name)
        self.connections.update({name: conn_wrapper})

    def get_connection(self, name: str) -> ConnectionWrapper:
        if name not in self.connections.keys():
            raise NoConnectionAvailableException(name)
        return self.connections[name]

    def open_connection(self, name: str):
        connection = self.get_connection(name)
        if connection.state in {ConnectionState.OPEN}:
            return
        connection.open()
        self.retrieve_current_session_id(name)

    # Query related methods
    @abc.abstractmethod
    def execute_query(self, conn_name: str, query_wrapper: QueryWrapper) -> QueryExecResult:
        raise NotImplementedMethodException(self, 'execute_query')

    def execute_query_for_single_output(self, conn_name: str, query_wrapper: QueryWrapper
                                        , output_file_path: str = None):
        query_exec_result = self.execute_query(conn_name=conn_name, query_wrapper=query_wrapper)

        single_output_value = None
        if query_exec_result.is_success():
            if not len(query_exec_result.result_set) > 0:
                self.log_event(StandardErrorEvent(f'Query {query_wrapper.name} retrieved O rows.'))
            else:
                if len(query_exec_result.result_set[0]) > 1:
                    self.log_event(StandardWarningEvent(f'Query {query_wrapper.name} contains more than 1 column. The '
                                                        f'first column'
                                                        f'data is used for returning the single value.'))
                single_output_value = query_exec_result.result_set[0][0]
        else:
            self.log_event(StandardErrorEvent(f'Query {query_wrapper.name} encountered an error.'))

        if output_file_path is not None:
            with open(output_file_path, 'w') as output_file:
                output_file.write(single_output_value)

        return single_output_value

    def execute_queries(self, conn_name: str, query_list: List[QueryWrapper], stop_on_error: bool = True) \
            -> QueryExecResults:
        """
        Executes a list of queries on the connection contained in the wrapper.
        Queries should be provided in dictionary with keywords : query, name and params

        An error should be raised according to the specificities of each database

        Local Variables are set to the query before the execution.
        Available variables are :
            - session_id : the current session id
            - last_query_exec_result : the last query execution result; from the previous query execution inside this method
                , thus the first query is provided an empty last_query_exec_result

        Parameters
        -----------
            conn_name : str
                The connection name
            query_list : List[dict]
                The list of sequential queries to be executed
            stop_on_error : bool, defaulted to True
                Indicates if execution should be stopped at the first error encountered

        Returns
        -----------
            The queries exec results
        """
        query_exec_results = QueryExecResults()
        last_query_exec_result = None
        for query_wrapper in query_list:
            query_wrapper.params.update({
                "session_id": self.get_connection(conn_name).session_id
                , "last_query_exec_result": last_query_exec_result
            })
            query_exec_result = self.execute_query(conn_name, query_wrapper)
            query_exec_results.append(query_exec_result)
            last_query_exec_result = query_exec_result
            if query_exec_result.is_error() & stop_on_error:
                break
        return query_exec_results

    def execute_script(self, conn_name: str, file_path: str, delimiter: str = ';') -> QueryExecResults:
        """
        Executes a script on this connection wrapper

        Parameters
        -----------
            conn_name : str
                The connection name
            file_path : str
                The file path of the script to execute
            delimiter : str
                The statements' delimiter (defaulted to ";")

        Returns
        -----------
            The queries exec results
        """
        if file_path is None:
            raise MissingMandatoryArgumentException(method_name='Execute Script', object_type=type(self),
                                                    argument_name='File Path')
        if not os.path.exists(file_path):
            raise NoFileAtLocationException(file_path=file_path)
        with open(file_path, 'r') as file:
            file_data = file.read()
        queries = file_data.split(delimiter)
        queries = [query.rstrip().lstrip() for query in queries if len(query.rstrip().lstrip()) > 0]
        self.log_event(StandardExtendedInfoEvent('Execution of SQL file : ' + os.path.basename(file_path) + ' - Start'))
        query_exec_result_list = self.execute_queries(conn_name, [QueryWrapper(query=query) for query in queries])
        self.log_event(
            StandardExtendedInfoEvent('Execution of SQL file : ' + os.path.basename(file_path) + ' - Successful'))
        return query_exec_result_list

    def execute_scripts(self, file_path_list: List[str], delimiter: str = ';') -> List[Tuple[str, QueryExecResults]]:
        """
        Executes scripts on this connection wrapper

        Parameters
        -----------
            file_path_list : List[str]
                The list of file paths of the script to execute
            delimiter : str
                The statements' delimiter (defaulted to ";")

        Returns
        -----------
            A list of tuples containing the absolute path of the script executed and the queries exec results
        """
        query_exec_result_list = []
        for file_path in file_path_list:
            try:
                query_exec_result_list.append((os.path.abspath(file_path), self.execute_script(file_path, delimiter)))
            except Exception as e:
                self.log_event(StandardErrorEvent(e.msg))
        return query_exec_result_list

    @abc.abstractmethod
    def retrieve_current_session_id(self, conn_name: str) -> str:
        """
        Retrieves the current session id and sets it on the connection

        Parameters
        ----------
        conn_name : str
            The connection name stored in the adapter

        Returns
        -------
            The current session id of the connection
        """
        raise NotImplementedMethodException(self, 'retrieve_current_session_id')

    def write_query_result_set_to_csv(self
                                      , query_result: QueryExecResult, target_file_path: str
                                      , delimiter: str = ';', newline: str = '\n', quotechar: str = '"'
                                      , header_row: bool = True):
        """
        Writes a query result set to csv.

        This method should be overriden by the child adapter for specific csv output (like data type output management,
        timestamp management)

        Parameters
        -----------
            query_result : QueryExecResult
                A query execution result
            target_file_path : str
                The target file name path
            delimiter : str
                The output file delimiter
            newline : str
                The output file newline character
            quotechar : str
                The output file quotechar
            header_row : bool
                Indicates if the header row should be generated in the output file

        """
        if query_result.is_success():
            with open(target_file_path, 'w', newline=newline) as csvfile:
                writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
                # Header row
                if header_row:
                    writer.writerow(query_result.result_set_structure.get_field_names())
                # Data row
                for row in query_result.result_set:
                    writer.writerow(row)
            self.log_event(CSVFileWriteSuccessful(file_path=target_file_path, object_type_name='SnowResultSet'))
        else:
            self.log_event(StandardExtendedInfoEvent(
                'No file generated as the query execution failed. Check query execution error message for more '
                'information.'))
        return query_result

    # Metadata Methods
    def get_structure_catalog(self
                              , conn_name: str, catalog: str = None, namespace: str = None
                              , output_file_path : str = None) \
            -> StructureCatalog:
        conn_wrap = self.get_connection(conn_name)
        current_namespace = namespace if namespace is not None else conn_wrap.get_active_schema()
        metadata_query_list = self.metadata_service.get_structures_from_database_queries(
            namespace=current_namespace, catalog=catalog)
        query_exec_results = self.execute_queries(conn_name, query_list=metadata_query_list)

        if query_exec_results.has_failed():
            raise RuntimeError('Failure on structures metadata retrieval.')

        structure_catalog = self.metadata_service.decode_specific_structure_result_set(query_exec_results[2].result_set)
        if output_file_path is not None:
            StructureCatalogCsv.to_csv(output_file_path, structure_catalog)

        return structure_catalog
