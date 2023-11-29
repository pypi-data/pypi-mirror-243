from typing import List, Tuple

from dftools.events import log_event
from dftools.utils import CsvLoader
from dftools.core.structure.core import Field, Namespace, FieldCharacterisation, FieldCatalog
from dftools.events.events import CSVFileReadSuccessful

class FieldCatalogCsv(CsvLoader[FieldCatalog, Tuple[Namespace, Field]]):
    
    @classmethod
    def _get_csv_input_parameters(cls) -> dict:
        return {
            "first_element" : "Field"
            , "row_type_column_position" : 0
            , "row_types" : {
                "Field" : {"name" : "field", "method_rule" : "cls._create_field_from_row(row)"}
            }
        }
    
    @classmethod
    def get_header_row_list(cls) -> List[str]:
        return [ 'Row Type', 'DataBank', 'Catalog', 'Namespace', 'Name'
            , 'Description', 'Position', 'Characterisations', 'DataType', 'Length'
            , 'Precision', 'Default Value']
    
    # Object Array creation methods for csv write operations

    @classmethod
    def format_object_to_array(cls, obj : FieldCatalog) -> list:
        output_list = []
        for namespace, field_dict in obj.fields.items():
            for field in list(field_dict.values()):
                output_list.extend(cls.format_field_to_array(namespace, field))
        return cls.clean_object_arrays(obj_arrays=output_list)

    @classmethod
    def format_field_to_array(cls, namespace : Namespace, obj : Field) -> List[list]:
        """ 
        Get a description of the field as a list

        Returns
        -----------
            A list of elements
        """
        field_list=[]
        ''' Add an entry for the structure level'''
        field_list.append([
                  'Field'
                , namespace.databank_name
                , namespace.catalog
                , namespace.namespace
                , obj.name
                , obj.desc
                , obj.position
                , ','.join([char.name for char in obj.characterisations])
                , obj.data_type
                , obj.length
                , obj.precision
                , obj.default_value
            ])
        return field_list
    
    @classmethod
    def read_csv(cls, file_path : str, newline : str = '', delimiter : str = ';', quotechar : str = '"'
        , encoding : str = 'ISO 8859-1') -> FieldCatalog:
        field_catalog = FieldCatalog()
        for object_dict in cls.read_csv_to_list_from_file(file_path=file_path, newline=newline, delimiter=delimiter
            , quotechar=quotechar, encoding=encoding):
            namespace, field = cls._create_object_from_rows(**object_dict)
            field_catalog.add_field(namespace, field)
        log_event(None, CSVFileReadSuccessful(file_path=file_path, object_type_name='Field Catalog'))
        return field_catalog

    # Create objects methods from string / input array

    @classmethod
    def _create_object_from_rows(cls, **kwargs) -> Tuple[Namespace, Field]:
        namespace : Namespace = kwargs['field'][0][0]
        field : Field = kwargs['field'][0][1]
        return (namespace, field)

    @classmethod
    def _create_field_from_row(cls, row : List[str]) -> Tuple[Namespace, Field]:
        cls.clean_object_array(row)
        return (
            Namespace(row[1], row[2], row[3])
            , Field(
                name = row[4]
                , desc = row[5]
                , position = cls._get_int_from_single_cell(row[6])
                , data_type = row[8]
                , length = cls._get_int_from_single_cell(row[9])
                , precision = cls._get_int_from_single_cell(row[10])
                , default_value = row[11]
                , characterisations = [FieldCharacterisation(char, attributes={}) for char in row[7].split(',')] \
                    if (row[7] is not None) & (row[7] != '') else []
                , sourcing_info = None
            )
        )
