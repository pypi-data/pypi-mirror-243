from dataclasses import dataclass
from typing import Optional, List, Tuple
from datetime import datetime
import csv
import os

from dftools.events import log_event
from dftools.events.events import CSVFileWriteSuccessful


@dataclass
class QueryExecResult:
    """
    Query Execution Result
    All the queries returned by the method execute_query should return this object
    """
    query_name: str
    exec_status: str
    query: str
    query_id: str
    result_set: Optional[list]
    result_set_structure: Optional[list]
    start_tst: datetime
    end_tst: datetime

    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'

    # Status methods
    def is_success(self) -> bool:
        return self.exec_status == self.SUCCESS

    def is_error(self) -> bool:
        return self.exec_status == self.ERROR

    def get_error_message(self) -> str:
        if self.is_error():
            if self.result_set is not None:
                return self.result_set[0].replace('\n', ' ').replace('\r', ' ').strip()
        return ''

    # Dictionary methods

    def to_dict(self) -> dict:
        return {
            "query_name": self.query_name
            , "exec_status": self.exec_status
            , "query": self.query
            , "query_id": self.query_id
            , "result_set": self.result_set
            , "result_set_header": self.result_set_structure
            , "start_tst": self.start_tst.strftime("%Y%m%d%H%M%S%f")
            , "end_tst": self.end_tst.strftime("%Y%m%d%H%M%S%f")
        }


class QueryExecResults(List[QueryExecResult]):
    def __init__(self) -> None:
        super().__init__()

    def get_status(self) -> str:
        if self.has_succeeded():
            return QueryExecResult.SUCCESS
        return QueryExecResult.ERROR

    def has_succeeded(self) -> bool:
        for query_exec_result in self:
            if query_exec_result.is_error():
                return False
        return True

    def has_failed(self) -> bool:
        for query_exec_result in self:
            if query_exec_result.is_error():
                return True
        return False

    def get_number_of_results(self) -> int:
        return len(self)

    def to_str(self) -> str:
        return ', '.join([str(query_exec_result.to_dict()) for query_exec_result in self])

    def report_exec_status(self) -> str:
        return '\n'.join([(query_exec_result.query_name if query_exec_result.query_name is not None else '') + ' : '
                          + query_exec_result.exec_status + (
                              '(' + query_exec_result.get_error_message() + ')' if query_exec_result.is_error() else '')
                          for query_exec_result in self])

    def get_csv_header(self) -> List[str]:
        return ['Query Name', 'Query', 'Execution Status', 'Execution Message', 'Start Tst', 'End Tst']

    def get_csv_rows(self) -> List[list]:
        return [[query_exec_result.query_name
                    , query_exec_result.query[0:100 if len(query_exec_result.query) >= 100
            else len(query_exec_result.query)]
                        .replace('\n', ' ').replace('\r', ' ').replace(';', ' ')
                    , query_exec_result.exec_status, query_exec_result.get_error_message()
                    , query_exec_result.start_tst.strftime("%Y-%m-%d %H:%M:%S.%f"),
                 query_exec_result.end_tst.strftime("%Y-%m-%d %H:%M:%S.%f")]
                for query_exec_result in self]

    def to_csv(self, file_path: str, delimiter: str = ';', newline: str = '\n', quotechar: str = '"') -> str:
        with open(file_path, 'w', newline=newline) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
            writer.writerow(self.get_csv_header())
            for query_exec_result_csv_row in self.get_csv_rows():
                writer.writerow(query_exec_result_csv_row)
        log_event(None, CSVFileWriteSuccessful(file_path=file_path, object_type_name=QueryExecResults.__name__))


class QueryExecResultUtil:
    @classmethod
    def write_script_exec_results_to_csv(cls, script_results: List[Tuple[str, QueryExecResults]], file_path: str
                                         , delimiter: str = ';', newline: str = '\n', quotechar: str = '"') -> None:
        with open(file_path, 'w', newline=newline) as csvfile:
            writer = csv.writer(csvfile, delimiter=delimiter, quotechar=quotechar)
            writer.writerow(
                ['Script Name', 'Script Status', 'Query Name', 'Query'
                    , 'Query Status', 'Execution Message', 'Start Tst', 'End Tst'])
            for script_result in script_results:
                script_name = os.path.basename(script_result[0])
                query_exec_result = script_result[1]
                for query_exec_result_csv_row in query_exec_result.get_csv_rows():
                    csv_row = [script_name, query_exec_result.get_status()]
                    csv_row.extend(query_exec_result_csv_row)
                    writer.writerow(csv_row)
        log_event(None, CSVFileWriteSuccessful(file_path=file_path, object_type_name="ScriptExecResults"))