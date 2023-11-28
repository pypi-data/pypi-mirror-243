
from typing import Dict

from dftools.core.dataflow.utils import DataVariable
from dftools.core.structure import Namespace

class DataFlowStdParameters():
    
    SRC_STRUCTURE_NAME = DataVariable('SOURCE_STRUCTURE_NAME', str )
    SRC_STRUCTURE_NAMESPACE = DataVariable('SOURCE_STRUCTURE_NAMESPACE', Namespace)
    TGT_STRUCTURE_NAMESPACE = DataVariable('TARGET_STRUCTURE_NAMESPACE', Namespace)
    FIELD_MAPPING = DataVariable('FIELD_MAPPING', Dict[str, str])

