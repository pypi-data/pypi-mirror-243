
from dataclasses import dataclass
import logging

from dftools.utils import DictDecoderInfo, DfDataClassObj

@dataclass
class DataFlowDefTemplate(DfDataClassObj):
    name : str = None
    parent_data_flow_rule : str = None
    default_step_name : str = None
    flow_name_rule : str = None
    flow_desc_rule : str = None
    default_data_flow_impl_model : str = None
    default_source_structure_template : str = None
    default_target_structure_template : str = None
    original_structure_type : str = None

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(
                mandatory_keys=["name"]
                , authorized_keys=["name", "parent_data_flow_rule", "default_step_name", "flow_name_rule"
                , "flow_desc_rule", "default_data_flow_model", "default_source_structure_template", "default_target_structure_template"
                , "original_structure_type"]
        )
    
    @classmethod
    def _default_instance(cls):
        return cls(name=None, parent_data_flow_rule=None, default_step_name=None, flow_name_rule = None
                    , flow_desc_rule = None, default_data_flow_impl_model = None, default_source_structure_template = None
                    , default_target_structure_template = None, original_structure_type = None)
    
    def __post_init__(self):
        self.logger = logging.getLogger(__name__)
