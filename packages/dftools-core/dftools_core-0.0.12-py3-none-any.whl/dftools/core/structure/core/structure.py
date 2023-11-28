from dataclasses import dataclass, field
from typing import List, Dict, Any
import logging

from dftools.events import DfLoggable, StandardWarningEvent
from dftools.utils import DictDecoderInfo, DfDataClassObj
from dftools.core.structure.core.field import Field
from dftools.core.structure.core.structure_ref import StructureRef
from dftools.events.events import MissingField, MissingMandatoryArgument, FieldAdditionInvalidPosition
from dftools.exceptions import FieldRemovalException, MissingMandatoryArgumentException, FieldAdditionException


@dataclass
class StructureSourcingInfo(DfDataClassObj):
    master_source_structure_ref: StructureRef = None
    source_structure_ref: StructureRef = None
    data_update_strategies: Dict[str, List[str]] = field(default_factory=dict)

    @classmethod
    def _get_dict_decoder_info(cls) -> DictDecoderInfo:
        return DictDecoderInfo([], ["master_source_structure_ref", "source_structure_ref", "data_update_strategies"]
                               , {"master_source_structure_ref": StructureRef, "source_structure_ref": StructureRef})

    @classmethod
    def _default_instance(cls):
        return cls(master_source_structure_ref=StructureRef._default_instance()
                   , source_structure_ref=StructureRef._default_instance()
                   , data_update_strategies={})

    def has_master_source_structure_ref(self) -> bool:
        """
        Checks if the master source structure ref is available on this field

        Returns
        -----------
            True if the master source structure ref and field name are filled
        """
        return self.master_source_structure_ref is not None

    def has_source_structure_ref(self) -> bool:
        """
        Checks if the source structure ref is available on this field

        Returns
        -----------
            True if the source structure ref and field name are filled
        """
        return self.source_structure_ref is not None


@dataclass
class Structure(DfDataClassObj, DfLoggable):
    name: str
    desc: str
    type: str
    row_count: int = 0
    options: Dict[str, str] = field(default_factory=dict)
    content_type: List[str] = field(default_factory=list)
    fields: List[Field] = field(default_factory=list)
    characterisations: List[str] = field(default_factory=list)
    sourcing_info: StructureSourcingInfo = None

    @classmethod
    def _get_dict_decoder_info(cls) -> DictDecoderInfo:
        return DictDecoderInfo(["name"]
                               , ["name", "desc", "type", "row_count", "options", "content_type", "fields",
                                  "characterisations", "sourcing_info"]
                               , {"fields": Field, "sourcing_info": StructureSourcingInfo})

    @classmethod
    def _default_instance(cls):
        return cls(name=None, desc=None, type=None, row_count=0, options={}, content_type=[], fields=[],
                   characterisations=[], sourcing_info=None)

    def __post_init__(self):
        self.logger = logging.getLogger(__name__)

        if isinstance(self.sourcing_info, dict):
            self.sourcing_info = StructureSourcingInfo.from_dict(input_dict=self.sourcing_info)

    # Structure-level methods
    def is_table(self) -> bool:
        """
        Checks if the structure is a table.
        Accepted values for structure type are : BASE TABLE and TABLE
        
        Returns
        -----------
            True, if the structure is a table
            False, otherwise
        """
        return self.type.upper() in ['BASE TABLE', 'TABLE'] if self.type is not None else False

    def is_view(self) -> bool:
        """
        Checks if the structure is a view.
        Accepted values for structure type are : VIEW
        
        Returns
        -----------
            True, if the structure is a view
            False, otherwise
        """
        return self.type.upper() in ['VIEW'] if self.type is not None else False

    # Field-level methods
    def get_field_names(self) -> List[str]:
        """
        Get the list of field names by ordinal position
        
        Returns
        -----------
            The list of the field names
        """
        self.sort_fields_by_ordinal_position()
        return [field.name for field in self.fields]

    def get_field(self, name: str) -> Field:
        """
        Get a field based on its name
        
        Parameters
        -----------
            The field name to look for

        Returns
        -----------
            The field structure with the provided field name
        """
        for field in self.fields:
            if field.name == name:
                return field
        return None

    def has_field(self, name: str) -> bool:
        """
        Checks if a field with the provided name is available in the structure
        
        Parameters
        -----------
            The field name to look for

        Returns
        -----------
            True, if a field with the provided name exists
        """
        return self.get_field(name=name) is not None

    def get_fields_with_characterisation(self, characterisation: str) -> List[Field]:
        """
        Get the list of field with the provided characterisation
        
        Parameters
        -----------
            characterisation : The characterisation to look for

        Returns
        -----------
            The list of field with the provided characterisation
        """
        return [field for field in self.fields if characterisation in [char.name for char in field.characterisations]]

    def get_fields_with_characterisations(self, characterisations: List[str]) -> List[Field]:
        """
        Get the list of field with any of the provided characterisations
        
        Parameters
        -----------
            characterisations : The list of characterisations to look for

        Returns
        -----------
            The list of field with the provided characterisation
        """
        return [field for field in self.fields if
                any(char in characterisations for char in [char.name for char in field.characterisations])]

    def get_fields_wo_characterisations(self, characterisations: List[str]) -> List[Field]:
        """
        Get the list of field without any of the provided characterisations
        
        Parameters
        -----------
            characterisations : The list of characterisations to look for

        Returns
        -----------
            The list of field with the provided characterisation
        """
        return [field for field in self.fields if
                field not in self.get_fields_with_characterisations(characterisations)]

    def get_field_names_with_characterisation(self, characterisation: str) -> List[str]:
        """
        Get the list of field names with the provided characterisation
        
        Parameters
        -----------
            characterisation : The characterisation to look for

        Returns
        -----------
            The list of field names with the provided characterisation
        """
        return [field.name for field in self.get_fields_with_characterisation(characterisation)]

    def get_field_names_with_characterisations(self, characterisations: list) -> List[str]:
        """
        Get the list of field names with any of the provided characterisations
        
        Parameters
        -----------
            characterisations : The list of characterisations to look for

        Returns
        -----------
            The list of field names with the provided characterisation
        """
        return [field.name for field in self.get_fields_with_characterisations(characterisations)]

    def get_field_names_wo_characterisations(self, characterisations: list) -> List[str]:
        """
        Get the list of field names without any of the provided characterisations
        
        Parameters
        -----------
            characterisations : The list of characterisations to look for

        Returns
        -----------
            The list of field names without the provided characterisations
        """
        return [field.name for field in self.get_fields_wo_characterisations(characterisations)]

    def add_field(self
                  , new_field: Field
                  , force_position: bool = False
                  , prevent_position_check: bool = False
                  , previous_field_name: str = None
                  , next_field_name: str = None
                  ) -> None:
        """
        Adds the provided field to this structure

        The field can be provided with a predefined position, or without a position.
        If the field has a predefined position, this value is checked to be equal to the current number of fields plus 1
        , as this field is by default added as the last field of the structure

        Parameters
        -----------
            new_field : The new field to be added
            force_position : Flag to force the position stored in the new field to be taken into account
                The force_position takes priority over prevent_position_check argument and over the 
                previous_field_name and next_field_name arguments, e.g. if force_position is True
                , the position of the field is forced based on the position valued in the field provided
                and all the fields in the structure are modified accordingly and all other parameters are 
                not used.
            prevent_position_check: Flag to prevent any position check while adding the fields
            previous_field_name : The previous field name, when field is to be added after a specific field
            next_field_name : The next field name, when field is to be added before a specific field

        """
        if new_field is None:
            self.log_event(MissingMandatoryArgument(method_name='Add Field'
                , object_type=type(self), argument_name='New Field'))
            raise MissingMandatoryArgumentException(method_name='Add Field'
                , object_type=type(self), argument_name='New Field')

        if force_position:
            pos_to_add_new_field = new_field.position

            for field in self.fields:
                if field.position >= pos_to_add_new_field:
                    field.position = field.position + 1
            self.fields.append(new_field)

        elif (previous_field_name is None) & (next_field_name is None):

            if not prevent_position_check:
                if (new_field.position is None) | (new_field.position == 0):
                    new_field.position = len(self.fields) + 1
                elif new_field.position != (len(self.fields) + 1):
                    self.log_event(FieldAdditionInvalidPosition(
                        field_name=new_field.name, structure_name=self.name
                        , position=str(new_field.position), expected_last_position=str(len(self.fields) + 1)))
                    raise FieldAdditionException(field_name=new_field.name, structure_name=self.name)

            self.fields.append(new_field)

        else:
            pos_to_add_new_field = None
            if previous_field_name is not None:
                field = self.get_field(previous_field_name)
                if field is None:
                    self.log_event(MissingField(field_name=previous_field_name, structure_name=self.name))
                    raise FieldAdditionException(field_name=new_field.name, structure_name=self.name)

                pos_to_add_new_field = field.position + 1
            elif next_field_name is not None:
                field = self.get_field(next_field_name)
                if field is None:
                    self.log_event(MissingField(field_name=next_field_name, structure_name=self.name))
                    raise FieldAdditionException(field_name=new_field.name, structure_name=self.name)
                pos_to_add_new_field = field.position

            for field in self.fields:
                if field.position >= pos_to_add_new_field:
                    field.position += 1
            new_field.position = pos_to_add_new_field
            self.fields.append(new_field)

    def remove_field(self, name: str):
        """
        Removes the field with the provided name and updates all the position values of the fields contained in this structure

        Parameters
        -----------
            name : The new field to be removed
            
        """
        field_to_remove = self.get_field(name)
        if field_to_remove is None:
            self.log_event(MissingField(field_name=name, structure_name=self.name))
            raise FieldRemovalException(field_name=name, structure_name=self.name)
        base_position = field_to_remove.position
        self.fields.remove(field_to_remove)
        for field in self.fields:
            if field.position > base_position:
                field.position -= 1

    def remove_fields(self, names: List[str]) -> None:
        """
        Removes the fields with the provided names and updates all the position values of the fields contained in this structure.

        Parameters
        -----------
            names : The list of fields to be removed
            
        """
        for name in names:
            self.remove_field(name)

    def sort_fields_by_ordinal_position(self) -> None:
        """
        Sort the Fields by Ordinal Position
        """
        self.fields = sorted(self.fields, key=lambda field: field.position)

    def get_number_of_fields(self) -> int:
        """ 
        Get the number of fields contained in the data structure definition

        Returns
        -----------
            The number of fields
        """
        return len(self.fields)

    def get_tec_key_fields(self) -> List[Field]:
        """ 
        Get the list of fields contained in the structure technical key

        Returns
        -----------
            The fields contained in the structure technical key
        """
        return [field for field in self.fields if field.in_tec_key()]

    def get_func_key_fields(self) -> List[Field]:
        """ 
        Get the list of fields contained in the structure functional key

        Returns
        -----------
            The fields contained in the structure functional key
        """
        return [field for field in self.fields if field.in_func_key()]

    def get_last_update_tst_field(self) -> Field:
        """
        Get the last update timestamp field.
        If there are multiple last update timestamp fields in this structure, a warning message is logged and one of
        the fields is returned (randomly)

        Returns
        -----------
            The last update timestamp field.
        """
        last_update_tst_fields = [field for field in self.fields if field.is_last_update_tst()]
        if len(last_update_tst_fields) == 0:
            return None
        if len(last_update_tst_fields) > 1:
            self.log_event(StandardWarningEvent(
                f'Multiple last update timestamp fields in structure {self.name} : {", ".join(last_update_tst_fields)}'))
            return last_update_tst_fields[0]
        return last_update_tst_fields[0]

    def get_insert_tst_field(self) -> Field:
        """
        Get the insert timestamp field.
        If there are multiple insert timestamp fields in this structure, a warning message is logged and one of
        the fields is returned (randomly)

        Returns
        -----------
            The last update timestamp field.
        """
        insert_tst_fields = [field for field in self.fields if field.is_insert_tst()]
        if len(insert_tst_fields) == 0:
            return None
        if len(insert_tst_fields) > 1:
            self.log_event(StandardWarningEvent(
                f'Multiple insert timestamp fields in structure {self.name} : {", ".join(insert_tst_fields)}'))
            return insert_tst_fields[0]
        return insert_tst_fields[0]

    def get_source_last_update_tst_field(self) -> Field:
        """
        Get the source last update timestamp field.
        If there are multiple source last update timestamp fields in this structure, a warning message is logged and
        one of the fields is returned (randomly)

        Returns
        -----------
            The last update timestamp field.
        """
        source_last_update_tst_fields = [field for field in self.fields if field.is_source_last_update_tst()]
        if len(source_last_update_tst_fields) == 0:
            return None
        if len(source_last_update_tst_fields) > 1:
            self.log_event(StandardWarningEvent(
                f'Multiple source last update timestamp fields in structure {self.name} : {", ".join(source_last_update_tst_fields)}'))
            return source_last_update_tst_fields[0]
        return source_last_update_tst_fields[0]

    # Options methods
    def get_options(self) -> Dict[str, Any]:
        """
        Get the options dictionary

        Returns
        -------
            The options dictionary
        """
        return self.options

    def get_option_keys(self) -> List[str]:
        """
        Get the available option keys

        Returns
        -------
            The list of options keys
        """
        return list(self.options.keys())

    def has_option(self, key: str):
        """
        Checks if this structure has the provided option key

        Parameters
        ----------
        key : str
            The option key

        Returns
        -------
            True if an option with this key is available
        """
        return key in self.get_option_keys()

    def get_option_value(self, key: str):
        """
        Get the option value for the provided key

        Parameters
        ----------
        key : str
            The option key

        Returns
        -------
            The option value
        """
        return self.options.get(key)

    # Characterisation methods
    def get_characterisations(self) -> List[str]:
        return self.characterisations

    def has_characterisations(self) -> bool:
        """
        Checks if this structure has any characterisations

        Returns
        -----------
            True if this structure has any characterisations

        """
        return len(self.characterisations) > 0

    def has_characterisation(self, char: str) -> bool:
        """
        Checks if this structure has the requested characterisation

        Parameters
        -----------
            char : the characterisation to look for

        Returns
        -----------
            True if this structure has the characterisation searched
        """
        return char in self.characterisations

    def has_any_characterisation(self, char_list: List[str]) -> bool:
        """
        Checks if this structure has any of the requested characterisations

        Parameters
        -----------
            char_list : the list of characterisations to look for

        Returns
        -----------
            True if this structure has at least one of the characterisation searched
        """
        return any(char in self.characterisations for char in char_list)

    def get_matching_characterisations(self, char_list : List[str]) -> List[str]:
        """
        Checks all the matching characterisations from the provided list with this structure charactersations

        Parameters
        -----------
            char_list : the list of characterisations to look for

        Returns
        -----------
            A list of the matching characterisations
        """
        return [char for char in char_list if self.has_characterisation(char)]

    def add_characterisation(self, new_char: str) -> None:
        """
        Adds the characterisation provided in the characterisations of the structure, if it does not already exist.

        Parameters
        -----------
            new_char : the characterisation to be added
        """
        if new_char is not None:
            if new_char not in self.get_characterisations():
                self.characterisations.append(new_char)

    def remove_characterisation(self, char: str) -> None:
        """
        Removes the characterisation provided in the characterisations of the structure, if it already exists

        Parameters
        -----------
            char : the characterisation to be removed
        """
        if char is not None:
            self.characterisations.remove(char)
