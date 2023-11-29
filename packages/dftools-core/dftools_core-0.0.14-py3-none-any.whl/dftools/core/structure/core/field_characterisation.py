from enum import auto
from dataclasses import dataclass
from typing import Optional, Dict
from dftools.utils import DfJsonLoadable, DictDecoderInfo
from strenum import StrEnum

class FieldConstraintType(StrEnum):
    NOT_ENFORCED='NotEnforced', 
    ENFORCED='Enforced'

class FieldCharacterisationTypeStd(StrEnum):
    IDENTIFICATION = auto()
    TECHNICAL = auto()
    DATA = auto()
    USAGE = auto()

class FieldCharacterisationSubTypeStd(StrEnum):
    ENTRY_IDENTIFICATION = auto()
    TEC_RECORD_INFO_SRC = auto()
    TEC_RECORD_INFO = auto()
    TEC_INGEST_INFO = auto()
    DATA_ENTRY = auto()

@dataclass
class FieldCharacterisation(DfJsonLoadable):
    name : str
    attributes : Optional[Dict[str, str]]
    
    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["name"], ["name", "attributes"], {})

    @classmethod
    def _default_instance(cls):
        return cls(name=None, attributes={})
    

class FieldCharacterisationStd(StrEnum):
    """ Structure General characterisations """
    TEC_ID = auto()
    FCT_ID = auto()
    UNIQUE = auto()
    MANDATORY = auto()

    """ Record Technical Characterisations - General information on structure data changes """
    REC_INSERT_TST = auto()
    REC_INSERT_USER_NAME = auto()
    REC_LAST_UPDATE_TST = auto()
    REC_LAST_UPDATE_USER_NAME = auto()
    """ Record Technical Characterisations - Logical deletion flag """
    REC_DELETION_FLAG = auto()
    REC_DELETION_TST = auto()
    REC_DELETION_USER_NAME = auto()
    """ Record Technical Characterisations - Logical archival flag """
    REC_ARCHIVE_FLAG = auto()
    REC_ARCHIVE_TST = auto()
    REC_ARCHIVE_USER_NAME = auto()

    """ Record Technical Characterisations - General Source information (insert, update, deletion 
    and archival information) """
    REC_SOURCE_INSERT_TST = auto()
    REC_SOURCE_INSERT_USER_NAME = auto()
    REC_SOURCE_LAST_UPDATE_TST = auto()
    REC_SOURCE_LAST_UPDATE_USER_NAME = auto()
    REC_SOURCE_EXTRACTION_TST = auto()
    REC_PREVIOUS_LAYER_UPDATE_TST = auto()
    REC_PREVIOUS_LAYER_UPDATE_USER_NAME = auto()
    REC_SOURCE_DELETION_FLAG = auto()
    REC_SOURCE_DELETION_TST = auto()
    REC_SOURCE_ARCHIVE_FLAG = auto()
    REC_SOURCE_ARCHIVE_TST = auto()
    """ Record Technical Characterisations - Specific Source information """
    """ Master Source characterisations define the source record information only for the master source structure 
    This is pertinent when there are multiple sources joined """
    REC_MASTER_SOURCE_INSERT_TST = auto()
    REC_MASTER_SOURCE_LAST_UPDATE_TST = auto()
    REC_MASTER_SOURCE_EXTRACTION_TST = auto()
