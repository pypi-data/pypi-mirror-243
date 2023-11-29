from dataclasses import dataclass, field
from typing import List, Dict
import logging

from dftools.events import DfLoggable, StandardWarningEvent, StandardDebugEvent
from dftools.core.structure.core.structure import Structure
from dftools.core.structure.core.namespace import Namespace
from dftools.core.structure.core.structure_ref import StructureRef
from dftools.utils import DfClonable


@dataclass
class StructureCatalog(DfClonable, DfLoggable):
    structures: Dict[Namespace, Dict[str, Structure]] = field(default_factory=dict)

    def __post_init__(self):
        self.logger = logging.getLogger(__name__)

    # Namespace methods
    def add_namespace(self, namespace: Namespace) -> None:
        if not (self.has_namespace(namespace)):
            self.structures.update({namespace: {}})

    def has_namespace(self, namespace: Namespace) -> bool:
        return namespace in self.structures.keys()

    def get_namespaces(self) -> List[Namespace]:
        return list(self.structures.keys())

    # Structure methods
    def has_structure(self, namespace: Namespace, name: str) -> bool:
        if namespace is None:
            raise ValueError('Namespace is mandatory for structure search in catalog')
        if name is None:
            raise ValueError('Structure Name is mandatory for structure search in catalog')
        return name in self.get_structures(namespace).keys()

    def get_structures(self, namespace: Namespace) -> Dict[str, Structure]:
        if self.has_namespace(namespace):
            return self.structures[namespace]
        raise ValueError('No Namespace available in the structure catalog for ' + namespace.__str__())

    def get_structure(self, namespace: Namespace, name: str) -> Structure:
        if self.has_structure(namespace, name):
            return self.structures[namespace][name]
        raise ValueError('No Structure available in the structure catalog for namespace : ' + namespace.__str__() \
                         + ' and structure name : ' + name)

    def get_structure_by_name(self, name: str) -> Structure:
        for namespace in self.get_namespaces():
            if self.has_structure(namespace, name):
                return self.structures[namespace][name]
        raise ValueError('No Structure available in the structure catalog with name : ' + name)

    def add_structure(self, namespace: Namespace, structure: Structure, prevent_namespace_creation: bool = False) \
            -> None:
        self.update_structure(namespace, structure, prevent_namespace_creation, update_if_exists=False)

    def update_structure(self, namespace: Namespace, structure: Structure, prevent_namespace_creation: bool = False
                      , update_if_exists: bool = True) -> None:
        if namespace is None:
            raise ValueError('Namespace is mandatory for structure addition in catalog')
        if structure is None:
            raise ValueError('Structure is mandatory for structure addition in catalog')
        if not (self.has_namespace(namespace)):
            if prevent_namespace_creation:
                raise ValueError('No Namespace available in the structure catalog for ' + namespace.__str__())
            else:
                self.add_namespace(namespace)
        if self.has_structure(namespace, structure.name):
            if not update_if_exists:
                self.log_event(StandardWarningEvent(
                    f'Update of existing structure not applied as structure exists and update is not allowed in '
                    'structure catalog for namespace : ' + namespace.__str__() + ' and name : ' + structure.name))
                return
            else:
                self.log_event(StandardDebugEvent(
                    f'Update of existing structure in structure catalog for namespace : ' + namespace.__str__() + \
                    ' and name : ' + structure.name))
        self.structures[namespace].update({structure.name: structure})
        self.log_event(StandardDebugEvent(
            f'Update of structure catalog for namespace/structure : ' + namespace.__str__() + ' / ' + structure.name
        ))

    def get_structure_refs(self) -> List[StructureRef]:
        structure_refs = []
        for namespace, structures_dict in self.structures.items():
            for structure_name in list(structures_dict.keys()):
                structure_refs.append(
                    StructureRef(namespace.databank_name, namespace.catalog, namespace.namespace, structure_name))
        return structure_refs

    # Structure methods
    def get_number_of_structures_per_namespace(self) -> Dict[Namespace, int]:
        return {namespace: len(structure_dict) for namespace, structure_dict in self.structures.items()}

    def get_number_of_structures(self) -> int:
        return sum(self.get_number_of_structures_per_namespace().values())
