from dataclasses import dataclass, field
from typing import Dict

from dftools.utils import DfClonable
from dftools.core.structure import Namespace

@dataclass
class IngestionDataFlowDef(DfClonable):

    source_databank : Namespace
    source_structure_name : str
    source_alias : str
    target_databank : Namespace
    target_structure_name : str
    target_alias : str
    data_flow_def_tmpl : str
    source_options : Dict[str, str] = field(default_factory=dict)
    tgt_field_mapping : Dict[str, str] = field(default_factory=dict)

    def _add_tgt_field_mapping(self, target_field_name : str = None, source_field_name : str = None) : 
        self.tgt_field_mapping.update({target_field_name : source_field_name})
        