import unittest

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.core.namespace import Namespace
from dftools.core.structure.core.structure import Structure
from dftools.core.structure.core.structure_catalog import StructureCatalog

class StructureCatalogTest(unittest.TestCase):
    DFT_STRUCTURE_DICT = {
            "name" : "df_product"
            , "desc" : "Product Table"
            , "type" : "BASE TABLE"
            , "row_count" : 320
            , "options" : {"func_domain" : "PRODUCT"}
            , "content_type" : []
            , "fields" : [
                { "name" : "id", "desc" : "ID of the product", "position" : 1, "data_type" : "NUMERIC", "length" : 10, "precision" : 0
                    , "default_value": "-1", "characterisations" : [{"name" : "TEC_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]}
                , { "name" : "code", "desc" : "Code of the product", "position" : 2, "data_type" : "STRING", "length" : 30, "precision" : 0
                    , "default_value": "'#'", "characterisations" : [{"name" : "FCT_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]}
            ]
    }
    DFT_NAMESPACE = Namespace('Snowflake', 'DF', 'DTL')
    DFT_NAMESPACE_2 = Namespace('Snowflake', 'DF', 'CDS')

    def test_namespace_methods(self):
        log_event_default(StdTestEvent("Field - Namespace Methods - Start"))
        str_catalog = StructureCatalog()
        self.assertEqual(0, len(list(str_catalog.structures.keys())))
        str_catalog.add_namespace(Namespace('Snowflake', 'DF', 'DTL'))
        self.assertEqual(1, len(list(str_catalog.structures.keys())))
        self.assertTrue(str_catalog.has_namespace(Namespace('Snowflake', 'DF', 'DTL')))
        structures = str_catalog.get_structures(Namespace('Snowflake', 'DF', 'DTL'))
        self.assertIsNotNone(structures)
        self.assertEqual(0, len(structures))
        log_event_default(StdTestEvent("Field - Namespace Methods - Succeeded"))

    def test_add_structure(self):
        log_event_default(StdTestEvent("Field - Add Structure - Start"))
        str_catalog = StructureCatalog()
        str_catalog.add_namespace(Namespace('Snowflake', 'DF', 'DTL'))
        self.assertEqual(0, len(list(str_catalog.get_structures(self.DFT_NAMESPACE))))
        self.assertEqual(False, str_catalog.has_structure(self.DFT_NAMESPACE, "df_product"))

        str_catalog.add_structure(self.DFT_NAMESPACE, Structure.from_dict(self.DFT_STRUCTURE_DICT))
        self.assertEqual(1, len(list(str_catalog.get_structures(self.DFT_NAMESPACE))))
        self.assertEqual(True, str_catalog.has_structure(self.DFT_NAMESPACE, "df_product"))
        
        log_event_default(StdTestEvent("Field - Add Structure - Succeeded"))
    
    def test_get_number_of_structures_methods(self):
        log_event_default(StdTestEvent("Field - Get Number of Structures methods - Start"))
        str_catalog = StructureCatalog()
        str_catalog.add_namespace(Namespace('Snowflake', 'DF', 'DTL'))
        self.assertEqual(0, len(list(str_catalog.get_structures(self.DFT_NAMESPACE))))
        self.assertEqual(False, str_catalog.has_structure(self.DFT_NAMESPACE, "df_product"))

        str_catalog.add_structure(self.DFT_NAMESPACE, Structure.from_dict(self.DFT_STRUCTURE_DICT))
        str_catalog.add_structure(self.DFT_NAMESPACE_2, Structure.from_dict(self.DFT_STRUCTURE_DICT))

        nb_structures = str_catalog.get_number_of_structures_per_namespace()
        self.assertIsNotNone(nb_structures)
        self.assertEqual(2, len(list(nb_structures.keys())))
        self.assertTrue(self.DFT_NAMESPACE in list(nb_structures.keys()))
        self.assertTrue(self.DFT_NAMESPACE_2 in list(nb_structures.keys()))
        self.assertEqual(1, nb_structures[self.DFT_NAMESPACE])
        self.assertEqual(1, nb_structures[self.DFT_NAMESPACE_2])

        self.assertEqual(2, str_catalog.get_number_of_structures())

        log_event_default(StdTestEvent("Field - Get Number of Structures methods - Succeeded"))

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
