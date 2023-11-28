import unittest
import os

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.core.structure import Structure
from dftools.core.structure.check.std_structure_checks import (
    StructureCheckRuleCommentFilled
    , StructureCheckRuleFieldPresent
    , StructureCheckRulePrimaryKeyPresent
    , FieldCheckRuleCommentFilled
)
from dftools.core.structure.check.structure_checker import StructureChecker

class StructureCheckerTest(unittest.TestCase):
    DFT_STRUCTURE_DICT_1 = {
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

    DFT_STRUCTURE_DICT_2 = {
            "name" : "df_product"
            , "desc" : None
            , "type" : "BASE TABLE"
            , "row_count" : 320
            , "options" : {"func_domain" : "PRODUCT"}
            , "content_type" : []
    }

    DFT_STRUCTURE_1_RESULT_CSV_CONTENT = "Root Key;Key;Rule Name;Status;Desc\n" \
            + "df_product;df_product;Structure comment filled;VALID;\n" \
            + "df_product;df_product;Structure contains fields;VALID;\n" \
            + "df_product;df_product;Structure contains primary key;VALID;\n" \
            + "df_product;df_product.fields.id;Field comment filled;VALID;\n" \
            + "df_product;df_product.fields.code;Field comment filled;VALID;\n"
            
    DFT_STRUCTURE_2_RESULT_CSV_CONTENT = "Root Key;Key;Rule Name;Status;Desc\n" \
            + "df_product;df_product;Structure comment filled;ERROR;Structure comment is not filled\n" \
            + "df_product;df_product;Structure contains fields;ERROR;Structure should contain fields\n" \
            + "df_product;df_product;Structure contains primary key;WARN;Structure might require a primary key\n" \

    def test_structure_checker_all_valid(self):
        log_event_default(StdTestEvent("Structure Checker - All valid - Start"))

        structure_checker = StructureChecker(
            structure_check_rules=[StructureCheckRuleCommentFilled(), StructureCheckRuleFieldPresent(), StructureCheckRulePrimaryKeyPresent()]
            , field_check_rules=[FieldCheckRuleCommentFilled()]
            )
        self.assertIsNotNone(structure_checker)

        ## Use Case #1
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT_1)
        self.assertIsNotNone(structure)
        
        check_result = structure_checker.check(structure)
        self.assertIsNotNone(check_result)
        self.assertEqual(5, len(check_result.get_check_events()))
        check_keys = check_result.get_check_keys()
        self.assertIsNotNone(check_keys)
        self.assertEqual(3, len(check_keys))
        self.assertEqual(['df_product', 'df_product.fields.id', 'df_product.fields.code'], check_keys)
        check_summary_by_key = check_result.get_check_summary_by_key()
        self.assertIsNotNone(check_summary_by_key)
        self.assertEqual([{"key" : "df_product", "summary" : {"VALID" : 3, "WARN" : 0, "ERROR" : 0}}
            , {"key" : "df_product.fields.id", "summary" : {"VALID" : 1, "WARN" : 0, "ERROR" : 0}}
            , {"key" : "df_product.fields.code", "summary" : {"VALID" : 1, "WARN" : 0, "ERROR" : 0}}
            ],  check_summary_by_key)

        check_summary = check_result.get_check_summary()
        self.assertIsNotNone(check_summary)
        self.assertEqual({"VALID" : 5, "WARN" : 0, "ERROR" : 0},  check_summary)

        log_event_default(StdTestEvent("Structure Checker - All valid - Succeeded"))
    
    def test_structure_checker_missing_fields(self):
        log_event_default(StdTestEvent("Structure Checker - Missing Fields - Start"))

        structure_checker = StructureChecker(
            structure_check_rules=[StructureCheckRuleCommentFilled(), StructureCheckRuleFieldPresent(), StructureCheckRulePrimaryKeyPresent()]
            , field_check_rules=[FieldCheckRuleCommentFilled()]
            )
        self.assertIsNotNone(structure_checker)

        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT_2)
        self.assertIsNotNone(structure)
        
        check_result = structure_checker.check(structure)
        self.assertIsNotNone(check_result)
        self.assertEqual(3, len(check_result.get_check_events()))
        check_keys = check_result.get_check_keys()
        self.assertIsNotNone(check_keys)
        self.assertEqual(1, len(check_keys))
        self.assertEqual(['df_product'], check_keys)
        check_summary_by_key = check_result.get_check_summary_by_key()
        self.assertIsNotNone(check_summary_by_key)
        self.assertEqual([{"key" : "df_product", "summary" : {"VALID" : 0, "WARN" : 1, "ERROR" : 2} }],  check_summary_by_key)

        check_summary = check_result.get_check_summary()
        self.assertIsNotNone(check_summary)
        self.assertEqual({"VALID" : 0, "WARN" : 1, "ERROR" : 2},  check_summary)
        
        log_event_default(StdTestEvent("Structure Checker - Missing Fields - Succeeded"))

    def test_to_csv_all_valid(self):
        log_event_default(StdTestEvent("Structure Checker - Test to_csv - Start"))
        
        structure_checker = StructureChecker(
            structure_check_rules=[StructureCheckRuleCommentFilled(), StructureCheckRuleFieldPresent(), StructureCheckRulePrimaryKeyPresent()]
            , field_check_rules=[FieldCheckRuleCommentFilled()]
            )
        self.assertIsNotNone(structure_checker)

        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT_2)
        self.assertIsNotNone(structure)
        
        check_result = structure_checker.check(structure)
        self.assertIsNotNone(check_result)

        file_path = 'check_result_2.csv'
        abs_file_path = os.path.abspath(file_path)
        if os.path.exists(abs_file_path):
            if os.path.isfile(abs_file_path):
                os.remove(abs_file_path)
            else : 
                raise ValueError('Cannot remove object located at : ' + abs_file_path)
            
        self.assertFalse(os.path.exists(abs_file_path))

        check_result.to_csv(file_path=file_path)

        self.assertTrue(os.path.exists(abs_file_path))
        with open(abs_file_path, "r") as file :
            file_data = file.read()
            self.assertEqual(self.DFT_STRUCTURE_2_RESULT_CSV_CONTENT, file_data)

        log_event_default(StdTestEvent("Structure Checker - Test to_csv - Succeeded"))

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
