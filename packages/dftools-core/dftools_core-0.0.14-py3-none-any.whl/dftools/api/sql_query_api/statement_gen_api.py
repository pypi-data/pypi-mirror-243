import os

from typing import List, Dict
from jinja2 import Template

from dftools.events import log_event_default, StandardInfoEvent as StdInfoEvent
from dftools.core.structure import (
    StructureCatalog
    , StructureCatalogCsv
    , Namespace
    , StructureJinjaDictEncoder
)

"""
    Database Query Generation standard methods
"""


def create_and_output_statement_on_same_structure_from_local_files(
        metadata_folder_path: str
        , metadata_file_prefix: str
        , template_file_path: str
        , namespace: Namespace
        , structure_name: str
        , output_folder_path: str = None
        , output_file_prefix: str = None
        , output_file_suffix: str = None
        , field_characterisations_to_exclude: List[str] = None
        , structure_jinja_dict_encoder: type = StructureJinjaDictEncoder) -> str:
    """Creates a statement from the metadata

    This method requires 3 input files :
    - The template file
    - The structure metadata file, which should be named using the pattern "metadata_file_prefix + '.metadata.csv'"
    
    Parameters
    ----------
    metadata_folder_path : str
        The folder path containing all the input files
    metadata_file_prefix : str
        The prefix of the metadata file
    template_file_path : str
        The template file path
    namespace : Namespace
        The namespace
    structure_name : str
        The structure name
    output_folder_path : str, optional
        The output folder path. If not provided, no output is generated.
    output_file_prefix : str, optional
        The output file prefix.
    output_file_suffix : str, optional
        The output file suffix.
    field_characterisations_to_exclude : List[str], optional
        The list of field characterisations to exclude from the comparison
    structure_jinja_dict_encoder : StructureJinjaDictEncoder, optional
        The structure jinja dict encoder to be used for template rendering.
        If not provided, the default StructureJinjaDictEncoder will be used

    Returns
    ----------
    statement : str
        The statement of non regression rendered using the provided template
    """
    str_catalog: StructureCatalog = StructureCatalogCsv.read_csv(
        os.path.join(os.path.abspath(metadata_folder_path), metadata_file_prefix + '.metadata.csv'))
    structure = str_catalog.get_structure(namespace, structure_name)

    field_characterisations_to_exclude = \
        ['REC_DELETION_TST', 'REC_DELETION_USER_NAME', 'REC_INSERT_TST', 'REC_INSERT_USER_NAME'
            , 'REC_LAST_UPDATE_TST', 'REC_LAST_UPDATE_USER_NAME', 'REC_DATALOAD_ATTRIBUTE'] \
            if field_characterisations_to_exclude is None else field_characterisations_to_exclude
    structure_for_statement = structure.deep_copy(structure)
    structure_for_statement.remove_fields(
        [field.name for field in
         structure_for_statement.get_fields_with_characterisations(field_characterisations_to_exclude)]
    )

    with open(template_file_path, 'r') as file:
        template_file = file.read()
    template = Template(template_file)

    statement: str = structure_jinja_dict_encoder.create_statement(template, namespace, structure_for_statement)

    if output_folder_path is not None:
        os.makedirs(output_folder_path, exist_ok=True)
        output_file_name = (output_file_prefix if output_file_prefix is not None else '') \
                           + structure.name + (output_file_suffix if output_file_suffix is not None else '') + '.sql'
        output_file_path = os.path.abspath(os.path.join(output_folder_path, output_file_name))
        statement_cleaned = statement.replace('None', '')
        with open(output_file_path, "w") as fh:
            fh.write(statement_cleaned)
        log_event_default(StdInfoEvent('File generated at location : ' + output_file_path))

    return statement


def create_and_output_statements_on_same_structure_from_local_files(
        metadata_folder_path: str
        , metadata_file_prefix: str
        , template_file_path: str
        , structure_dict: Dict[Namespace, str]
        , output_folder_path: str = None
        , output_file_prefix: str = None
        , output_file_suffix: str = None
        , field_characterisations_to_exclude: List[str] = None
        , structure_jinja_dict_encoder: type = StructureJinjaDictEncoder
        , rendering_params : Dict[str, str] = {}) -> str:
    """Creates a statement from the metadata

    This method requires 3 input files :
    - The template file
    - The structure metadata file, which should be named using the pattern "metadata_file_prefix + '.metadata.csv'"
    
    Parameters
    ----------
    metadata_folder_path : str
        The folder path containing all the input files
    metadata_file_prefix : str
        The prefix of the metadata file
    template_file_path : str
        The template file path
    structure_dict : Dict[Namespace, str]
        The structure dictionary providing for each namespace, the list of structures to consist
        for the generation of statements
    output_folder_path : str, optional
        The output folder path. If not provided, no output is generated.
    output_file_prefix : str, optional
        The output file prefix.
    output_file_suffix : str, optional
        The output file suffix.
    field_characterisations_to_exclude : List[str], optional
        The list of field characterisations to exclude from the comparison
    structure_jinja_dict_encoder : StructureJinjaDictEncoder, optional
        The structure jinja dict encoder to be used for template rendering.
        If not provided, the default StructureJinjaDictEncoder will be used
    rendering_params : Dict[str, str]
        The rending parameters

    Returns
    ----------
    statement : str
        The statement of non regression rendered using the provided template
    """
    field_characterisations_to_exclude = \
        ['REC_DELETION_TST', 'REC_DELETION_USER_NAME', 'REC_INSERT_TST', 'REC_INSERT_USER_NAME'
            , 'REC_LAST_UPDATE_TST', 'REC_LAST_UPDATE_USER_NAME', 'REC_DATALOAD_ATTRIBUTE'] \
            if field_characterisations_to_exclude is None else field_characterisations_to_exclude
    str_catalog: StructureCatalog = StructureCatalogCsv.read_csv(
        os.path.join(os.path.abspath(metadata_folder_path), metadata_file_prefix + '.metadata.csv'))

    for namespace, structure_names in structure_dict.items():
        for structure_name in structure_names:
            structure = str_catalog.get_structure(namespace, structure_name)

            structure_for_statement = structure.deep_copy(structure)
            structure_for_statement.remove_fields(
                [field.name for field in
                 structure_for_statement.get_fields_with_characterisations(field_characterisations_to_exclude)]
            )

            with open(template_file_path, 'r') as file:
                template_file = file.read()
            template = Template(template_file)

            statement: str = structure_jinja_dict_encoder.create_statement(template, namespace, structure_for_statement
                                                                           , params=rendering_params)

            if output_folder_path is not None:
                os.makedirs(output_folder_path, exist_ok=True)
                output_file_name = (output_file_prefix if output_file_prefix is not None else '') \
                                   + structure.name + (
                                       output_file_suffix if output_file_suffix is not None else '') + '.sql'
                output_file_path = os.path.abspath(os.path.join(output_folder_path, output_file_name))
                statement_cleaned = statement.replace('None', '')
                with open(output_file_path, "w") as fh:
                    fh.write(statement_cleaned)
                log_event_default(StdInfoEvent('File generated at location : ' + output_file_path))

    return statement
