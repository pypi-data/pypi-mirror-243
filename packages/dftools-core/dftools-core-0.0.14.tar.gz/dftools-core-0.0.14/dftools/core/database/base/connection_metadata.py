import abc
import json

from dftools.core.structure import StructureCatalog, StructureCatalogCsv, BaseStructureDecoder
from dftools.exceptions import (
    NotImplementedMethodException,
)
from dftools.core.database.base.connection import ConnectionWrapper


class BaseConnectionMetadataService:
    """
        Database Metadata Service interface

        All connection adapters should implement this interface for metadata management
    """

    def __init__(self) -> None:
        pass

    @classmethod
    def decode_structure_metadata_result_set(cls, result_set: list) -> StructureCatalog:
        """
            Decode the specific structure result set to a structure catalog

            Parameters
            -----------
                result_set : list
                    The list of rows from a metadata result set

            Returns
            -----------
                structure_catalog : StructureCatalog
                    The structure catalog

        """
        raise NotImplementedMethodException(cls, 'decode_structure_metadata_result_set')

    @classmethod
    def get_structure_from_database(cls, conn_wrap: ConnectionWrapper, namespace: str, table_name: str, catalog: str = None) -> list:
        """
            Get a structure from the database using the local connection wrapper

            Parameters
            -----------
                conn_wrap : ConnectionWrapper
                    The connection wrapper to execute the retrieve on
                namespace : str
                    The namespace name (also named schema)
                table_name : str
                    The table name
                catalog : str, optional
                    The catalog name

            Returns
            -----------
                data_structure_result_set : a result set of the data structure dictionnary

        """
        raise NotImplementedMethodException(cls, 'get_structure_from_database')

    @classmethod
    def get_standard_structure_from_database(cls
                                             , conn_wrap: ConnectionWrapper, namespace: str, table_name: str
                                             , catalog: str = None, output_file_path: str = None) -> StructureCatalog:
        """
            Get a standard structure from the database using the local connection wrapper

            Parameters
            -----------
                conn_wrap : ConnectionWrapper
                    The connection wrapper to execute the retrieve on
                namespace : str
                    The namespace name (also named schema)
                table_name : str
                    The table name
                catalog : str, optional
                    The catalog name
                output_file_path : str, optional
                    The output file path, if a csv file to be generated

            Returns
            -----------
                structure_catalog : StructureCatalog
                    The structure catalog
        """
        current_namespace = namespace if namespace is not None else conn_wrap.get_active_schema()
        structure_catalog = cls.decode_specific_structure_result_set(
            cls.get_structure_from_database(conn_wrap=conn_wrap, namespace=current_namespace, table_name=table_name))
        if output_file_path is not None:
            StructureCatalogCsv.to_csv(output_file_path, structure_catalog)
        return structure_catalog

    @classmethod
    def get_structures_from_database(cls, conn_wrap: ConnectionWrapper, namespace: str, catalog: str = None) -> list:
        """
            Get a structure from the database using the local connection wrapper

            Parameters
            -----------
                conn_wrap : ConnectionWrapper
                    The connection wrapper to execute the retrieve on
                namespace : str
                    The namespace name (also named schema)
                catalog : str
                    The catalog name

            Returns
            -----------
                data_structure_result_set : a result set of the data structure dictionary

        """
        raise NotImplementedMethodException(cls, 'get_structures_from_database')

    @classmethod
    def get_standard_structures_from_database(cls
                                              , conn_wrap: ConnectionWrapper, namespace: str, catalog: str = None
                                              , output_file_path: str = None) -> StructureCatalog:
        """
            Get a standard structure from the database using the local connection wrapper

            Parameters
            -----------
                conn_wrap : ConnectionWrapper
                    The connection wrapper to execute the retrieve on
                namespace : str
                    The namespace name (also named schema)
                catalog : str, optional
                    The catalog name
                output_file_path : str, optional
                    The output file path, if a csv file to be generated

            Returns
            -----------
                structure_catalog : StructureCatalog
                    The structure catalog
        """
        current_namespace = namespace if namespace is not None else conn_wrap.get_active_schema()
        structure_catalog = cls.decode_specific_structure_result_set(
            cls.get_structures_from_database(conn_wrap=conn_wrap, namespace=current_namespace, catalog=catalog))
        if output_file_path is not None:
            StructureCatalogCsv.to_csv(output_file_path, structure_catalog)
        return structure_catalog


class BaseJsonConnectionMetadataService(BaseConnectionMetadataService):

    @classmethod
    @abc.abstractmethod
    def structure_decoder(cls) -> BaseStructureDecoder:
        raise NotImplementedMethodException(cls, 'structure_decoder')

    @classmethod
    def decode_specific_structure_result_set(cls, result_set: list) -> StructureCatalog:
        """
            Decode the specific structure result set to a structure catalog

            Parameters
            -----------
                result_set : list
                    The list of rows from a metadata result set

            Returns
            -----------
                structure_catalog : StructureCatalog
                    The structure catalog

        """
        structure_catalog = StructureCatalog()
        for row in result_set:
            cur_data = row[0]
            structure_meta = json.loads(cur_data)
            namespace, structure = cls.structure_decoder().decode_json(structure_meta)
            structure_catalog.add_structure(namespace=namespace, structure=structure)
        return structure_catalog
