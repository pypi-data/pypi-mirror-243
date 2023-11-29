
from dataclasses import dataclass
from dftools.utils import DfDataClassObj, DictDecoderInfo

@dataclass
class DataFlowNamespace(DfDataClassObj):
    project_name : str = 'default_project'

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["project_name"], ["project_name"])
    
    @classmethod
    def _default_instance(cls):
        return cls(project_name='default_project')