
from typing import Dict, List
import json

from dftools.utils.dict_decoder import DictDecoderInfo, DictDecoder, create_dict_decoder

class DfJsonLoadable():
    """
        Standard Interface for a json-loadable object.
        The underlying object should extend this class and implement the method __get_dict_decoder_info()
    """
    
    def __init__(self) -> None:
        pass
    
    def __get_dict_decoder_info() -> DictDecoderInfo:
        """
        Provides the DictDecoderInfo specific to the class
        This method should be overridden in each object extending
        
        Parameters
        -----------
            None

        Returns
        -----------
            The DictDecoderInfo specific to the class 
        """
        return NotImplementedError('The __get_dict_decoder_info method is not implemented')
    
    @classmethod
    def __get_dict_decoder(cls) -> DictDecoder:
        """
        Provides the DictDecoder specific to this class
        The DictDecoder is generated based on the DictDecoder provided for each object
        
        Parameters
        -----------
            None

        Returns
        -----------
            The dictionnary decoder
        """
        return create_dict_decoder(cls.__get_dict_decoder_info())

    @classmethod
    def load_dict(cls, input_dict : dict):
        return cls.__get_dict_decoder().__load_dict(cls, input_dict)

    @classmethod
    def read_json(cls, file_path : str):
        with open(file_path, 'r') as f:
            data_dict = json.load(f)
        return cls.load_dict(data_dict)
    