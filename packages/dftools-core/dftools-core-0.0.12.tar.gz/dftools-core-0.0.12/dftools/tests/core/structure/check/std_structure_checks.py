import unittest

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.check import CheckInfo
from dftools.core.structure.core.structure import Structure
from dftools.core.structure.check.std_structure_checks import StructureCheckRuleCommentFilled, StructureCheckRuleFieldPresent

class StructureCheckRuleTest(unittest.TestCase):
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

    def test_structure_check_rule_comment_filled(self):
        log_event_default(StdTestEvent("Structure Check Rule - Comment Filled - Start"))
        structure_check_rule = StructureCheckRuleCommentFilled()
        self.assertIsNotNone(structure_check_rule)
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT_1)
        self.assertIsNotNone(structure)
        
        check_event = structure_check_rule.check(structure)
        self.assertIsNotNone(check_event)
        self.assertEqual('Structure comment filled', check_event.rule_name)
        self.assertEqual('df_product', check_event.key)
        self.assertEqual(CheckInfo.VALID, check_event.status)
        self.assertIsNone(check_event.desc)
        
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT_2)
        self.assertIsNotNone(structure)
        
        check_event = structure_check_rule.check(structure)
        self.assertIsNotNone(check_event)
        self.assertEqual('Structure comment filled', check_event.rule_name)
        self.assertEqual('df_product', check_event.key)
        self.assertEqual(CheckInfo.ERROR, check_event.status)
        self.assertEqual('Structure comment is not filled', check_event.desc)
        
        log_event_default(StdTestEvent("Structure Check Rule - Comment Filled - Succeeded"))
    
    def test_structure_check_rule_field_present(self):
        log_event_default(StdTestEvent("Structure Check Rule - Field Present - Start"))
        structure_check_rule = StructureCheckRuleFieldPresent()
        self.assertIsNotNone(structure_check_rule)
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT_1)
        self.assertIsNotNone(structure)
        
        check_event = structure_check_rule.check(structure)
        self.assertIsNotNone(check_event)
        self.assertEqual('Structure contains fields', check_event.rule_name)
        self.assertEqual('df_product', check_event.key)
        self.assertEqual(CheckInfo.VALID, check_event.status)
        self.assertIsNone(check_event.desc)
        
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT_2)
        self.assertIsNotNone(structure)
        
        check_event = structure_check_rule.check(structure)
        self.assertIsNotNone(check_event)
        self.assertEqual('Structure contains fields', check_event.rule_name)
        self.assertEqual('df_product', check_event.key)
        self.assertEqual(CheckInfo.ERROR, check_event.status)
        self.assertEqual('Structure should contain fields', check_event.desc)
        
        log_event_default(StdTestEvent("Structure Check Rule - Field Present - Succeeded"))

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
