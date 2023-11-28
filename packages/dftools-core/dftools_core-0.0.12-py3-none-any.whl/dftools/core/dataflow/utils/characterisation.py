from dataclasses import dataclass, field
from typing import Any, Dict, List

from dftools.utils import DictDecoderInfo, DfDataClassObj

@dataclass
class DataCharacterisation(DfDataClassObj):
    """
        Standard Data Attribute type
    """
    name : str = None
    add_into = Dict[str, Any] = field(default_factory=dict)
    
    # Dictionnary methods
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(mandatory_keys=["name"], authorized_keys=["name", "add_info"])
        

class HasDataCharacterisations():
    """
        Master Type for all the classes with characterisations
    """
    def __init__(self) -> None:
        self._characterisations : List[DataCharacterisation] = []

    def add_characterisation(self, char : DataCharacterisation) -> None:
        """
        Add a characterisation
        
        Parameters
        -----------
            char : the characterisation to be added
        """
        self._characterisations.append(char)
    
    def add_characterisations(self, char_list : List[DataCharacterisation]) -> None:
        """
        Add the list of characterisations to the data flow
        
        Parameters
        -----------
            char_list : the list of characterisations to be added
        """
        if char_list is not None : 
            for char in char_list:
                self.add_characterisation(char)

    def get_characterisations(self) -> List[DataCharacterisation]:
        """
        Get the list of characterisations
        
        Parameters
        -----------
            None
        
        Returns
        -----------
            The lits of data characterisation
        """
        return self._characterisations

    def get_characterisation(self, name : str) -> DataCharacterisation:
        """
        Get a characterisation based on its name
        
        Parameters
        -----------
            name : the characterisation name to look for
        
        Returns
        -----------
            The data characterisation with the name provided
        """
        for char in self._characterisations:
            if char.name == name:
                return char
        return None
    
    def has_characterisation(self, name : str) -> DataCharacterisation:
        """
        Check if a characterisation is present
        
        Parameters
        -----------
            name : the characterisation name to look for
        
        Returns
        -----------
            True if the data characterisation is available
            False otherwise
        """
        for char in self._characterisations:
            if char.name == name:
                return True
        return False