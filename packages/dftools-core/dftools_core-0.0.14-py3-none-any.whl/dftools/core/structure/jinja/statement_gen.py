from jinja2 import Template
from typing import Dict
from dataclasses import asdict
from datetime import datetime

from dftools.core.structure.core import Structure, Namespace
from dftools.core.structure.compare import StructureComparisonResult

"""
    Statement Generation methods
"""


class StructureJinjaDictEncoder:
    """
    Structure Jinja Dictionary Encoder

    Provides method to convert a structure to a dictionary interpretable by jinja.
    This class can be inherited to provide a different method of dictionary interpretations
    """
    def __init__(self):
        pass

    @classmethod
    def get_structure_jinja_dict(cls, structure: Structure) -> dict:
        """
            Get a structure dictionary for jinja rendering

            Output Dictionary contains :
            - All the structure attributes and field attributes, with all
                the field characterisation stored as {characterisation name : []}
            - tec_key : List of the technical key fields
            - func_key : List of the functional key fields
            - last_update_tst_field : The last update timestamp field, if available
            - source_last_update_tst_field : The source last update timestamp field, if available
            - insert_tst_field : The insert timestamp field, if available

        Parameters
        -----------
            structure : Structure
                A structure

        Returns
        -----------
            The structure dictionary for jinja rendering
        """
        structure_dict = asdict(structure)
        structure_dict['tec_key'] = [tec_key_field.name for tec_key_field in structure.get_tec_key_fields()]
        structure_dict['func_key'] = [func_key_field.name for func_key_field in structure.get_func_key_fields()] \
            if len(structure.get_func_key_fields()) > 0 else structure_dict['tec_key']
        for field in structure_dict['fields']:
            field: dict
            characterisations = {}
            for characterisation in field['characterisations']:
                characterisations.update({characterisation['name']: []})
            field.pop('characterisations')
            field.update({'characterisations': characterisations})
        structure_dict['last_update_tst_field'] = structure.get_last_update_tst_field()
        structure_dict['source_last_update_tst_field'] = structure.get_source_last_update_tst_field()
        structure_dict['insert_tst_field'] = structure.get_insert_tst_field()
        return structure_dict

    @classmethod
    def get_generic_param_dict(cls) -> Dict[str, str]:
        """
        Get the generic parameter dictionary.

        Output Dictionary contains :
            - cur_date_str : the current date formatted as %d-%m-Y

        Returns
        -------
            A dictionary, which all generic parameters (not specific to the input information)
        """
        return {
            "cur_date_str": datetime.now().strftime("%d-%m-%Y")
        }

    @classmethod
    def get_template_input_dict(cls, namespace : Namespace, structure : Structure, params : Dict[str, str]) -> dict:
        """
        Get the input dictionary for template rendering based on all input parameters

        The created dictionary contains :
            - str_namespace : A dictionary of the namespace attributes
            - structure : A dictionary of the structure attributes, created using the get_structure_jinja_dict method
            - gen_params : A dictionary of the general parameters, including the class generic parameters
                and the parameters provided as input

        Parameters
        ----------
        namespace : Namespace
            The namespace
        structure : Structure
            The structure
        params : Dict[str, str]
            The specific parameters for the generation

        Returns
        -------
            The Dictionary for template rendering
        """
        gen_param_dict = cls.get_generic_param_dict()
        gen_param_dict.update(params)
        return {
            "str_namespace": asdict(namespace) if namespace is not None else {}
            , "structure": cls.get_structure_jinja_dict(structure)
            , "gen_params" : gen_param_dict
        }

    @classmethod
    def create_statement(cls, template: Template, namespace: Namespace, structure: Structure,
                         params: Dict[str, str] = {}) -> str:
        """
        Create a statement (stored in a string) using the provided template for the input namespace
        , structure and parameters

        Parameters
        ----------
        template : Template
            The template used for statement rendering
        namespace : Namespace
            The structure namespace
        structure : Structure
            The structure
        params : Dict, optional
            A dictionary of parameters, which can be used by the template

        Returns
        -------
            The rendered statement
        """
        return template.render(cls.get_template_input_dict(namespace=namespace, structure=structure, params=params))


class StructureComparedJinjaDictEncoder(StructureJinjaDictEncoder):
    """
    Structure Compared Jinja Dictionary Encoder

    Provides method to convert a structure to a dictionary interpretable by jinja.
    This class can be inherited to provide a different method of dictionary interpretations
    """
    def __init__(self):
        pass

    @classmethod
    def get_template_input_dict(cls, namespace: Namespace, structure: Structure
                                ,structure_comparison: StructureComparisonResult, params: Dict[str, str]) -> dict:
        """
        Get the input dictionary for template rendering based on all input parameters

        The created dictionary contains :
            - str_namespace : A dictionary of the namespace attributes
            - structure : A dictionary of the structure attributes, created using the get_structure_jinja_dict method
            - gen_params : A dictionary of the general parameters, including the class generic parameters
                and the parameters provided as input
            - structure_comparison : A dictionary of the structure comparison
                , created using the create_structure_comparison_dict method

        Parameters
        ----------
        namespace : Namespace
            The namespace
        structure : Structure
            The structure (the new structure from the comparison, or the baseline if structure is removed)
        structure_comparison : StructureComparisonResult
            The structure comparison result
        params : Dict[str, str]
            The specific parameters for the generation

        Returns
        -------
            The Dictionary for template rendering
        """
        gen_param_dict = cls.get_generic_param_dict()
        gen_param_dict.update(params)
        return {
            "str_namespace": asdict(namespace) if namespace is not None else {}
            , "structure": cls.get_structure_jinja_dict(structure)
            , "gen_params": gen_param_dict
            , "structure_comparison": cls.get_structure_comparison_dict(structure_comparison)
        }

    @classmethod
    def get_structure_comparison_dict(cls, structure_comparison: StructureComparisonResult) -> dict:
        """
        Get the structure comparison dictionary.

        Output Dictionary contains :
            - root_key : The root key value
            - events : Dictionary of the events recorded as changed (new, removed or updated)
            - removed_fields : Dictionary of the removed fields stored with field names as keys
            - new_fields : Dictionary of the new fields stored with field names as keys

        Parameters
        ----------
        structure_comparison : StructureComparisonResult
            The structure comparison result

        Returns
        -------
            The Structure Comparison Dictionary for template rendering
        """
        structure_comparison_dict = structure_comparison.get_event_dict()
        structure_comparison_dict.update({
            "removed_fields":
                {field_dict['name']: field_dict for field_dict in structure_comparison.get_removed_fields()}}
        )
        structure_comparison_dict.update({
            "new_fields":
                {field_dict['name']: field_dict for field_dict in structure_comparison.get_new_fields()}}
        )
        return structure_comparison_dict

    @classmethod
    def create_statement(cls, template: Template, namespace: Namespace, structure: Structure,
                         structure_comparison: StructureComparisonResult,
                         params: Dict[str, str] = {}) -> str:
        """
        Create a statement (stored in a string) using the provided template for the input namespace
        , structure and parameters

        Parameters
        ----------
        template : Template
            The template used for statement rendering
        namespace : Namespace
            The structure namespace
        structure : Structure
            The structure
        structure_comparison :StructureComparisonResult
            The structure comparison result
        params : Dict, optional
            A dictionary of parameters, which can be used by the template

        Returns
        -------
            The rendered statement
        """
        return template.render(
            cls.get_template_input_dict(namespace=namespace, structure=structure
                                        , structure_comparison=structure_comparison, params=params))
