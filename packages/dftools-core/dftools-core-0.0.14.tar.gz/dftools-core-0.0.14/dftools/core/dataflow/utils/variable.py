from dataclasses import dataclass
from typing import List

from dftools.utils import DfClonable

@dataclass
class DataVariable(DfClonable):
    name : str
    type : type

