from dataclasses import dataclass
from typing import Any, Dict, List

from dftools.events import log_event
from dftools.events.events import MissingMandatoryArgument
from dftools.exceptions import MissingMandatoryArgumentException
from dftools.utils import DictDecoderInfo, DfDataClassObj

@dataclass
class DataAttribute(DfDataClassObj):
    """
        Standard Data Attribute type
    """
    key : str = None
    value = None
    default_value = None
    
    def __post_init__(self):
        if self.value is None :
            self.value = self.default_value

    def set_value(self, value) -> None:
        self.value = value

    # Dictionnary methods
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(mandatory_keys=["key"], authorized_keys=["key", "value", "default_value"])
        

class HasDataAttributes():
    """
        Master Interface for all the classes with attributes
    """
    def __init__(self) -> None:
        self._attributes : Dict[str, DataAttribute] = {}

    def add_attribute(self, attribute : DataAttribute) -> None:
        """
        Adds an attribute. If an attribute with the same key already exists, it will be overriden.
        Raises a ValueError if the attribute provided is null.
        
        Parameters
        -----------
            attribute : the attribute to be added
        """
        
        if attribute is None:
            log_event(self.logger, MissingMandatoryArgument(method_name='Add Attribute', object_type=type(self), argument_name='Attribute'))
            raise MissingMandatoryArgumentException(method_name='Add Attribute', object_type=type(self), argument_name='Attribute')
        self._attributes.update({attribute.key : attribute})
    
    def add_attributes(self, att_list : List[DataAttribute]) -> None:
        """
        Add the list of attributes.
        
        Parameters
        -----------
            att_list : the list of attributes to be added
        """
        if att_list is not None : 
            for attribute in att_list:
                self.add_attribute(attribute)

    def get_attribute_keys(self) -> List[str] :
        """
        Get the list of keys available
        
        Parameters
        -----------
            None
        
        Returns
        -----------
            The list of keys available
        """
        return self._attributes.keys()

    def get_attributes(self) -> List[DataAttribute]:
        """
        Get the list of attributes
        
        Parameters
        -----------
            None
        
        Returns
        -----------
            The list of data attributes
        """
        return self._attributes.values()
    
    def get_attribute_key_value_dict(self) -> Dict[str, Any]:
        """
        Get a dictionnary with a key-value pair
        
        Parameters
        -----------
            None
        
        Returns
        -----------
            A key-value pair dictionnary
        """
        att_dict = {}
        for att in self.get_attributes():
            att_dict[att.key] = att.value
        return att_dict

    def get_attribute(self, name : str) -> DataAttribute:
        """
        Get an attribute based on its name
        
        Parameters
        -----------
            name : the attribute name to look for
        
        Returns
        -----------
            The data attribute with the name provided
        """
        return self._attributes[name] if name in self._attributes.keys() else None
    
    def has_attribute(self, name : str) -> bool:
        """
        Checks if an attribute is available
        
        Parameters
        -----------
            name : the attribute name to look for
        
        Returns
        -----------
            True if the attribute is available
            False otherwise
        """
        return name in self.get_attribute_keys()
    
    def get_attribute_value(self, name : str) -> Any:
        """
        Get an attribute value based on its name
        
        Parameters
        -----------
            name : the attribute name to look for
        
        Returns
        -----------
            The data value with the name provided
        """
        return self._attributes[name].value if name in self._attributes.keys() else None