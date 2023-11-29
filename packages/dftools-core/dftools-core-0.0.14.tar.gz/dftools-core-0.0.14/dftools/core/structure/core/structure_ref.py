from dataclasses import dataclass

from dftools.utils import DfJsonLoadable, DictDecoderInfo
from dftools.core.structure.core.namespace import Namespace


@dataclass
class StructureRef(DfJsonLoadable):
    databank_name: str
    catalog: str
    namespace: str
    structure_name: str

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["databank_name", "catalog", "namespace", "structure_name"],
                               ["databank_name", "catalog", "namespace", "structure_name"])

    @classmethod
    def _default_instance(cls):
        return cls(databank_name='', catalog='', namespace='', structure_name='')

    def get_namespace(self) -> Namespace:
        return Namespace(databank_name=self.databank_name, catalog=self.catalog, namespace=self.namespace)
