import unittest
import os

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.core import StructureCatalog, FieldCatalog, Structure, Field, Namespace
from dftools.core.structure.api.structure_catalog_api import StructureCatalogApi

class StructureCatalogApiTest(unittest.TestCase):
    maxDiff = 1000 # Set to 1000 due to the check of the content of the csv file generated

    DFT_NAMESPACE = Namespace('Snowflake', 'DF', 'DTL')

    DFT_STRUCTURE_DICT = {
            "name" : "df_product"
            , "desc" : "Product Table"
            , "type" : "BASE TABLE"
            , "row_count" : 320
            , "options" : {"func_domain" : "PRODUCT"}
            , "content_type" : []
            , "fields" : [
                { "name" : "id", "desc" : "ID of the product", "position" : 1, "data_type" : "NUMERIC", "length" : 10, "precision" : 0
                    , "default_value": "-1", "characterisations" : [{"name" : "TEC_ID"}, {"name" : "MANDATORY"}, {"name" : "UNIQUE"}, {"name" : "UID"}]}
                , { "name" : "code", "desc" : "Code of the product", "position" : 2, "data_type" : "STRING", "length" : 30, "precision" : 0
                    , "default_value": "'#'", "characterisations" : [{"name" : "FCT_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]}
                , { "name" : "DT_IS_INSERTED_AT", "desc" : None, "position" : 3, "data_type" : "TIMESTAMP_NTZ", "length" : 29, "precision" : 3
                    , "default_value": None, "characterisations" : [{"name" : "MANDATORY"}]}
            ]
    }

    DFT_FIELD_DICT = {
        "name" : "DT_IS_INSERTED_AT", "desc" : "Technical - The entry was created at (date and time)"
        , "position" : 0, "data_type" : "TIMESTAMP_NTZ", "length" : 29, "precision" : 9
        , "characterisations" : [{"name" : "REC_INSERT_TST"}]
        , "default_value" : None
    }

    def test_update_structure_catalog_with_known_field_standard_definitions(self):
        log_event_default(StdTestEvent("Structure Catalog API - Test Update Structure Catalog with Known Field Standard Definitions - Start"))
        str_catalog = StructureCatalog()
        str_catalog.add_namespace(self.DFT_NAMESPACE)
        str_catalog.add_structure(self.DFT_NAMESPACE, Structure.from_dict(self.DFT_STRUCTURE_DICT))

        field_catalog = FieldCatalog()
        field_catalog.add_namespace(self.DFT_NAMESPACE)
        field_catalog.add_field(self.DFT_NAMESPACE, Field.from_dict(self.DFT_FIELD_DICT))
        
        StructureCatalogApi.update_structure_catalog_with_known_field_standard_definitions(str_catalog, field_catalog
            , desc_override=True , characterisation_append = True, data_format_override = True, default_value_override = True)

        self.assertIsNotNone(str_catalog)
        self.assertIsNotNone(str_catalog.has_structure(self.DFT_NAMESPACE, 'df_product'))
        structure = str_catalog.get_structure(self.DFT_NAMESPACE, 'df_product')
        self.assertIsNotNone(structure)
        self.assertIsNotNone(structure.has_field('DT_IS_INSERTED_AT'))
        field = structure.get_field('DT_IS_INSERTED_AT')
        self.assertIsNotNone(field)
        self.assertEqual('DT_IS_INSERTED_AT', field.name)
        self.assertEqual('Technical - The entry was created at (date and time)', field.desc)
        self.assertEqual(3, field.position)
        self.assertEqual('TIMESTAMP_NTZ', field.data_type)
        self.assertEqual(29, field.length)
        self.assertEqual(9, field.precision)
        self.assertEqual(2, len(field.characterisations))
        self.assertTrue('REC_INSERT_TST' in field.get_characterisation_names())
        self.assertTrue('MANDATORY' in field.get_characterisation_names())
        self.assertIsNone(field.default_value)
        
        log_event_default(StdTestEvent("Structure Catalog API - Test Update Structure Catalog with Known Field Standard Definitions - Succeeded"))
    
if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
