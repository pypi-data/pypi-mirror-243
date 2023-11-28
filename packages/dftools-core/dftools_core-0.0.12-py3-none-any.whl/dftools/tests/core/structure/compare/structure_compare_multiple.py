import unittest
import os

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.core import Namespace, Structure, StructureCatalog
from dftools.core.structure.compare import StructureComparator


class StructureCompareForMultipleTest(unittest.TestCase):
    maxDiff = 5000

    DFT_NAMESPACE = Namespace('Snowflake', 'DF', 'DTL')

    DFT_STRUCTURE_ORIG1_DICT = {
        "name": "df_product"
        , "desc": "Product Table"
        , "type": "BASE TABLE"
        , "row_count": 320
        , "options": {"func_domain": "PRODUCT"}
        , "content_type": []
        , "fields": [
            {"name": "id", "desc": "ID of the product", "position": 1, "data_type": "NUMERIC", "length": 10,
             "precision": 0
                , "default_value": "-1",
             "characterisations": [{"name": "TEC_ID"}, {"name": "MANDATORY"}, {"name": "UNIQUE"}, {"name": "UID"}]}
            , {"name": "code", "desc": "Code of the product", "position": 2, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'",
               "characterisations": [{"name": "FCT_ID"}, {"name": "UNIQUE"}, {"name": "UID"}]}
        ]
    }

    DFT_STRUCTURE_ORIG2_DICT = {
        "name": "df_customer1"
        , "desc": "MD - Customer Table"
        , "type": "BASE TABLE"
        , "row_count": 320
        , "options": {"func_domain": "CUSTOMER"}
        , "content_type": []
        , "fields": [
            {"name": "id", "desc": "ID of the customer", "position": 1, "data_type": "NUMERIC", "length": 10,
             "precision": 0
                , "default_value": "-1",
             "characterisations": [{"name": "TEC_ID"}, {"name": "MANDATORY"}, {"name": "UNIQUE"}, {"name": "UID"}]}
            , {"name": "code", "desc": "Code of the customer", "position": 2, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'",
               "characterisations": [{"name": "FCT_ID"}, {"name": "UNIQUE"}, {"name": "UID"}]}
        ]
    }

    DFT_STRUCTURE_ORIG3_DICT = {
        "name": "df_customer"
        , "desc": "MD - Product Table"
        , "type": "BASE TABLE"
        , "row_count": 320
        , "options": {"func_domain": "CUSTOMER"}
        , "content_type": []
        , "fields": [
            {"name": "id", "desc": "ID of the customer", "position": 1, "data_type": "NUMERIC", "length": 10,
             "precision": 0
                , "default_value": "-1",
             "characterisations": [{"name": "TEC_ID"}, {"name": "MANDATORY"}, {"name": "UNIQUE"}, {"name": "UID"}]}
            , {"name": "code", "desc": "Code of the customer", "position": 2, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'",
               "characterisations": [{"name": "FCT_ID"}, {"name": "UNIQUE"}, {"name": "UID"}]}
        ]
    }

    def test_compare_multiple_with_renaming_of_structure(self):
        log_event_default(StdTestEvent("Structure Compare - Test Compare Multiple with renaming of structures - Start"))

        orig_str_catalog = StructureCatalog()
        orig_str_catalog.add_structure(namespace=self.DFT_NAMESPACE
                                       , structure=Structure.from_dict(self.DFT_STRUCTURE_ORIG1_DICT))
        orig_str_catalog.add_structure(namespace=self.DFT_NAMESPACE
                                       , structure=Structure.from_dict(self.DFT_STRUCTURE_ORIG2_DICT))
        new_str_catalog = StructureCatalog()
        new_str_catalog.add_structure(namespace=self.DFT_NAMESPACE
                                       , structure=Structure.from_dict(self.DFT_STRUCTURE_ORIG1_DICT))
        new_str_catalog.add_structure(namespace=self.DFT_NAMESPACE
                                       , structure=Structure.from_dict(self.DFT_STRUCTURE_ORIG3_DICT))

        str_catalog_comparator = StructureComparator(field_characterisation_to_check=False)

        # UC #1 : Comparison without the renaming of structures
        # The comparison should detect a removal for key df_customer1 as object is missing in the new structure catalog
        # and detect a new object for key df_customer
        comparison_results = str_catalog_comparator.compare_multiple(
            orig_str_catalog.get_structures(self.DFT_NAMESPACE), new_str_catalog.get_structures(self.DFT_NAMESPACE)
        )
        self.assertIsNotNone(comparison_results)
        self.assertEqual(3, len(comparison_results))
        self.assertEqual(1, len(comparison_results.get_new()))
        self.assertEqual(1, len(comparison_results.get_removed()))
        self.assertEqual(0, len(comparison_results.get_updated()))
        self.assertEqual(1, len(comparison_results.get_identical()))

        # UC #2 : Comparison with the renaming of structures
        # The comparison should detect an update for key df_customer as object has been renamed
        comparison_results = str_catalog_comparator.compare_multiple(
            orig_str_catalog.get_structures(self.DFT_NAMESPACE), new_str_catalog.get_structures(self.DFT_NAMESPACE)
            , {'df_customer1': {'orig_key': 'df_customer'}}
        )
        self.assertIsNotNone(comparison_results)
        self.assertEqual(2, len(comparison_results))
        self.assertEqual(0, len(comparison_results.get_new()))
        self.assertEqual(0, len(comparison_results.get_removed()))
        self.assertEqual(1, len(comparison_results.get_updated()))
        self.assertEqual(1, len(comparison_results.get_identical()))

        log_event_default(StdTestEvent("Structure Compare - Test Compare Multiple with renaming of structures - "
                                       "Succeeded"))


if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
