import unittest

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.core.field import Field

class FieldTest(unittest.TestCase):
    def test_from_dict(self):
        log_event_default(StdTestEvent("Field - From Dict - Start"))
        input_dict = {
            "name" : "Field1", "desc" : "toto", "default_value": "dft_val", "characterisations" : [{"name" : "TEC_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]
        }
        field = Field.from_dict(input_dict)
        self.assertIsNotNone(field)
        self.assertEqual("Field1", field.name)
        self.assertEqual("toto", field.desc)
        self.assertEqual(0, field.position)
        self.assertEqual("dft_val", field.default_value)
        self.assertEqual(3, len(field.characterisations))
        self.assertEqual('', field.data_type)
        log_event_default(StdTestEvent("Field - From Dict - Succeeded"))
    
    def test_deep_copy(self):
        log_event_default(StdTestEvent("Field - Deep Copy - Start"))
        input_dict = {
            "name" : "Field1", "desc" : "toto", "default_value": "dft_val", "characterisations" : [{"name" : "TEC_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]
        }
        field : Field = Field.from_dict(input_dict)
        field_copy : Field = Field.deep_copy(field)
        self.assertIsNotNone(field_copy)
        self.assertEqual("Field1", field_copy.name)
        self.assertEqual("toto", field_copy.desc)
        self.assertEqual(0, field_copy.position)
        self.assertEqual('', field_copy.data_type)
        self.assertEqual(3, len(field_copy.characterisations))
        self.assertIsNone(field_copy.sourcing_info)
        log_event_default(StdTestEvent("Field - Deep Copy - Succeeded"))
    
    def test_characterisation_methods(self):
        log_event_default(StdTestEvent("Field - Characterisation Methods - Start"))
        input_dict = {
            "name" : "Field1", "desc" : "toto", "default_value": "dft_val", "characterisations" : [{"name" : "TEC_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]
        }
        field : Field = Field.from_dict(input_dict)
        self.assertEqual(3, len(field.characterisations))
        self.assertTrue(field.in_tec_key())
        self.assertFalse(field.in_func_key())
        self.assertFalse(field.is_mandatory())
        self.assertTrue(field.is_unique())
        self.assertTrue(field.has_characterisation('UID'))
        self.assertFalse(field.has_characterisation('UID2'))
        
        field.set_func_key()
        self.assertEqual(4, len(field.characterisations))
        self.assertTrue(field.in_func_key())

        field.set_func_key()
        self.assertEqual(4, len(field.characterisations))
        self.assertTrue(field.in_func_key())

        field.set_tec_key()
        self.assertEqual(4, len(field.characterisations))
        self.assertTrue(field.in_tec_key())

        log_event_default(StdTestEvent("Field - Characterisation Methods - Succeeded"))

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
