import unittest

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.adapter.field_format_adapter import FieldFormatAdaptRule, FieldFormatAdapter

class FieldFormatAdaptRuleTest(unittest.TestCase):
    def test_adapter_rule_simple(self):
        log_event_default(StdTestEvent("Field Format Adapt Rule - Simple Rule - Start"))
        input_dict = {
            "allowed_data_types" : ["STRING"], "allowed_characterisations" : []
                , "target_data_type": "STRING", "length_rule": "{length}", "precision_rule": "{precision}"
        }
        field_format_adapt_rule : FieldFormatAdaptRule = FieldFormatAdaptRule.from_dict(input_dict)
        self.assertIsNotNone(field_format_adapt_rule)
        self.assertEqual("STRING", field_format_adapt_rule.target_data_type)
        self.assertEqual("{length}", field_format_adapt_rule.length_rule)
        self.assertEqual("{precision}", field_format_adapt_rule.precision_rule)
        
        self.assertTrue(field_format_adapt_rule._is_rule_applicable(data_type='STRING', characterisations=None))
        self.assertEqual(('STRING', 40, 0), field_format_adapt_rule.get_adapted_field_format(data_type='STRING', length=40, precision=0))
        self.assertEqual(('STRING', 30, 0), field_format_adapt_rule.get_adapted_field_format(data_type='STRING', length=30, precision=0))

        self.assertFalse(field_format_adapt_rule._is_rule_applicable(data_type='NUMERIC', characterisations=None))

        log_event_default(StdTestEvent("Field Format Adapt Rule - Simple Rule - Succeeded"))
    
    def test_adapter_rule_complex(self):
        log_event_default(StdTestEvent("Field Format Adapt Rule - Complex Rule - Start"))
        input_dict = {
            "allowed_data_types" : ["STRING", "VARCHAR"], "allowed_characterisations" : ["YEAR_IN_YYYY_FORMAT", "INTEGER_VALUE"]
                , "target_data_type": "INTEGER", "length_rule": "10", "precision_rule": "{precision}"
        }
        field_format_adapt_rule : FieldFormatAdaptRule = FieldFormatAdaptRule.from_dict(input_dict)
        self.assertIsNotNone(field_format_adapt_rule)
        self.assertEqual("INTEGER", field_format_adapt_rule.target_data_type)
        self.assertEqual("10", field_format_adapt_rule.length_rule)
        self.assertEqual("{precision}", field_format_adapt_rule.precision_rule)
        
        self.assertFalse(field_format_adapt_rule._is_rule_applicable(data_type='STRING', characterisations=None))

        self.assertTrue(field_format_adapt_rule._is_rule_applicable(data_type='STRING', characterisations=['YEAR_IN_YYYY_FORMAT']))
        self.assertTrue(field_format_adapt_rule._is_rule_applicable(data_type='STRING', characterisations=['YEAR_IN_YYYY_FORMAT', 'INTEGER_VALUE']))
        self.assertTrue(field_format_adapt_rule._is_rule_applicable(data_type='STRING', characterisations=['YEAR_IN_YYYY_FORMAT', 'INTEGER_VALUE', 'TEC_ID']))
        self.assertEqual(('INTEGER', 10, 0), field_format_adapt_rule.get_adapted_field_format(data_type='STRING', length=40, precision=0))

        self.assertFalse(field_format_adapt_rule._is_rule_applicable(data_type='INTEGER', characterisations=['YEAR_IN_YYYY_FORMAT']))
        self.assertFalse(field_format_adapt_rule._is_rule_applicable(data_type='INTEGER', characterisations=['INTEGER_VALUE']))

        self.assertFalse(field_format_adapt_rule._is_rule_applicable(data_type='NUMERIC', characterisations=None))

        log_event_default(StdTestEvent("Field Format Adapt Rule - Complex Rule - Succeeded"))
    

class FieldFormatAdapterTest(unittest.TestCase):
    def test_get_adapted_field_format(self):
        log_event_default(StdTestEvent("Field Format Adapter - Get Adapted Field Format - Start"))
        input_dict = {"rules" : 
            [
                {
                    "allowed_data_types" : ["STRING", "VARCHAR"], "allowed_characterisations" : ["YEAR_IN_YYYY_FORMAT", "INTEGER_VALUE"]
                    , "target_data_type": "INTEGER", "length_rule": "10", "precision_rule": "{precision}"
                }
                , {
                    "allowed_data_types" : ["STRING"], "allowed_characterisations" : []
                    , "target_data_type": "STRING", "length_rule": "{length}", "precision_rule": "{precision}"
                }
            ]
            , "default_keep_source_format" : True
        }
        field_format_adapter : FieldFormatAdapter = FieldFormatAdapter.from_dict(input_dict)
        self.assertIsNotNone(field_format_adapter)
        self.assertEqual(2, len(field_format_adapter.rules))
        
        self.assertEqual(('STRING', 30, 0), field_format_adapter.get_adapted_field_format(data_type='STRING', length = 30, precision=0, characterisations=[]))
        self.assertEqual(('INTEGER', 10, 0), field_format_adapter.get_adapted_field_format(data_type='STRING', length = 30, precision=0, characterisations=["YEAR_IN_YYYY_FORMAT"]))
        self.assertEqual(('INTEGER', 30, 0), field_format_adapter.get_adapted_field_format(data_type='INTEGER', length = 30, precision=0, characterisations=["YEAR_IN_YYYY_FORMAT"]))
        self.assertEqual(('NUMERIC', 30, 0), field_format_adapter.get_adapted_field_format(data_type='NUMERIC', length = 30, precision=0, characterisations=[]))
        
        log_event_default(StdTestEvent("Field Format Adapter - Get Adapted Field Format - Succeeded"))
   
if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
