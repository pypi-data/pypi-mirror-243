from dataclasses import dataclass, field
from typing import List, Dict

from dftools.core.structure.core.structure import Field
from dftools.core.structure.core.namespace import Namespace

@dataclass
class FieldCatalog():
    
    fields : Dict[Namespace, Dict[str, Field]] = field(default_factory=dict)

    # Namespace methods
    def add_namespace(self, namespace : Namespace) -> None:
        if not(self.has_namespace(namespace)):
            self.fields.update({namespace : {}})

    def has_namespace(self, namespace : Namespace) -> bool:
        return namespace in self.fields.keys()
    
    def get_namespaces(self) -> List[Namespace]:
        return list(self.fields.keys())
    
    # Field methods
    def has_field(self, namespace: Namespace, name : str) -> bool:
        if namespace is None :
            raise ValueError('Namespace is mandatory for field search in catalog')
        if name is None :
            raise ValueError('Field Name is mandatory for field search in catalog')
        return name in self.get_fields(namespace).keys()

    def get_fields(self, namespace : Namespace) -> Dict[str, Field]:
        if self.has_namespace(namespace):
            return self.fields[namespace]
        raise ValueError('No Namespace available in the field catalog for ' + namespace.__str__)

    def get_field(self, namespace : Namespace, name : str) -> Field:
        if self.has_field(namespace, name):
            return self.fields[namespace][name]
        raise ValueError('No Field available in the field catalog for namespace : ' + namespace.__str__ \
                        + ' and field name : ' + name)

    def get_field_by_name(self, name : str) -> Field:
        for namespace in self.get_namespaces():
            if self.has_field(namespace, name):
                return self.fields[namespace][name]
        raise ValueError('No Field available in the field catalog with name : ' + name)

    def add_field(self, namespace : Namespace, field : Field, prevent_namespace_creation : bool = False) -> None:
        if namespace is None :
            raise ValueError('Namespace is mandatory for field addition in catalog')
        if field is None :
            raise ValueError('Field is mandatory for field addition in catalog')
        if not(self.has_namespace(namespace)):
            if prevent_namespace_creation : 
                raise ValueError('No Namespace available in the field catalog for ' + namespace.__str__)
            else :
                self.add_namespace(namespace)
        self.fields[namespace].update({field.name : field})    
