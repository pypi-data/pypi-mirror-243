from typing import Optional, Dict
from dataclasses import dataclass, field

from dftools.exceptions import QueryExecutionException


@dataclass
class QueryWrapper:
    query: str
    interpreted_query: Optional[str] = None
    name: Optional[str] = None
    params: Dict[str, str] = field(default_factory=dict)
    runtime_exception_message: Optional[str] = None

    def update_interpreted_query(self):
        self.interpreted_query = self.query.format(**self.params)

    def raise_runtime_exception(self):
        if self.runtime_exception_message is not None:
            raise QueryExecutionException(error_message=self.runtime_exception_message.format(**self.params))

