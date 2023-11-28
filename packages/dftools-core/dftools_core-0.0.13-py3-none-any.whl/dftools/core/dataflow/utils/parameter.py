from dataclasses import dataclass
from typing import List

from dftools.utils import DictDecoderInfo, DfDataClassObj

@dataclass
class DataParameter(DfDataClassObj):
    
    name : str = None
    desc : str = None
    type : str = None
    input : bool = True
    variable : bool = False
    output : bool = False
    length : int = 0
    precision : int = 0
    runtime_override_enabled : bool = False
    default_value = None

    # Getter methods
    def has_default_value(self) -> bool:
        return self.default_value is not None

    # Dictionnary methods
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(
            mandatory_keys=["name", "desc", "type", "input", "output", "length"]
            , authorized_keys=["name", "desc", "type", "input", "variable", "output", "length"
                , "precision", "runtime_override_enabled", "default_value"
                ]
            )

    @classmethod
    def _default_instance(cls):
        return cls(name = None, desc = None, type = None, input = True, variable = False, output = False, length = 0, precision = 0
                   , runtime_override_enabled = False, default_value = None)

class HasDataParameters():
    """
        Master Type for all the classes with parameters
    """
    def __init__(self) -> None:
        self.parameters : List[DataParameter] = []

    def add_parameter(self, param : DataParameter) -> None:
        """
        Adds a parameter
        
        Parameters
        -----------
            param : the parameter to be added
        """
        self.parameters.append(param)
    
    def add_parameters(self, param_list : List[DataParameter]) -> None:
        """
        Adds the list of parameters
        
        Parameters
        -----------
            param_list : the list of parameters to be added
        """
        if param_list is not None : 
            for param in param_list:
                self.add_parameter(param)

    def get_parameter(self, name : str) -> DataParameter:
        """
        Get a parameter based on its name
        
        Parameters
        -----------
            name : the parameter name to look for
        
        Returns
        -----------
            The data parameter with the name provided
        """
        for param in self.parameters:
            if param.name == name:
                return param
        return None
    
    def get_parameters(self) -> List[DataParameter]:
        """
        Get the list of data parameters
        
        Parameters
        -----------
            None
        
        Returns
        -----------
            The list of data parameters
        """
        return self.parameters