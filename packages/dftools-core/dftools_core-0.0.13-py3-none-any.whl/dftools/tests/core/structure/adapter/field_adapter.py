import unittest

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.adapter.field_adapter import FieldAdapter
from dftools.core.structure.core import Field

class FieldAdapterTest(unittest.TestCase):
    FLD_ADAPTER_DICT_KEEP_SOURCE_FORMAT = {
        "name_rule" : "original_field.name"
        , "desc_rule" : "original_field.desc"
        , "all_fields_optional" : False
        , "keep_tec_key" : True
        , "keep_func_key" : True
        , "orig_to_new_characterisation_mapping" : {}
        , "field_format_adapter":
            {
            "rules" : 
                [
                    {
                        "allowed_data_types" : ["STRING", "VARCHAR"], "allowed_characterisations" : ["YEAR_IN_YYYY_FORMAT", "INTEGER_VALUE"]
                        , "target_data_type": "INTEGER", "length_rule": "10", "precision_rule": "{precision}"
                    }
                    , {
                        "allowed_data_types" : ["STRING"], "allowed_characterisations" : []
                        , "target_data_type": "STRING", "length_rule": "{length}", "precision_rule": "{precision}"
                    }
                    , {
                        "allowed_data_types" : ["TIMESTAMP"], "allowed_characterisations" : []
                        , "target_data_type": "TIMESTAMP_NTZ", "length_rule": "29", "precision_rule": "9"
                    }
                ]
                , "default_keep_source_format" : True
            }
    }

    FLD_ADAPTER_DICT_DEFAULT_FORMAT_AND_STAGING_CONFIG = {
        "name_rule" : "original_field.name"
        , "desc_rule" : "original_field.desc"
        , "all_fields_optional" : True
        , "keep_tec_key" : False
        , "keep_func_key" : True
        , "orig_to_new_characterisation_mapping" : {}
        , "field_format_adapter":
            {
            "rules" : 
                [
                    {
                        "allowed_data_types" : ["STRING", "VARCHAR"], "allowed_characterisations" : ["YEAR_IN_YYYY_FORMAT", "INTEGER_VALUE"]
                        , "target_data_type": "INTEGER", "length_rule": "10", "precision_rule": "{precision}"
                    }
                    , {
                        "allowed_data_types" : ["STRING"], "allowed_characterisations" : []
                        , "target_data_type": "STRING", "length_rule": "{length}", "precision_rule": "{precision}"
                    }
                    , {
                        "allowed_data_types" : ["TIMESTAMP"], "allowed_characterisations" : []
                        , "target_data_type": "TIMESTAMP_NTZ", "length_rule": "29", "precision_rule": "9"
                    }
                ]
                , "default_keep_source_format" : False
            }
    }

    FLD_ADAPTER_DICT_DEFAULT_CURATED_FROM_SRC = {
        "name_rule" : "override_params['field_name'] if 'field_name' in override_params.keys() else original_field.name"
        , "desc_rule" : "original_field.desc"
        , "all_fields_optional" : False
        , "keep_tec_key" : True
        , "keep_func_key" : True
        , "orig_to_new_characterisation_mapping" : {"REC_LAST_UPDATE_TST" : "REC_SOURCE_LAST_UPDATE_TST"}
        , "field_format_adapter":
            {
            "rules" : 
                [
                    {
                        "allowed_data_types" : ["STRING", "VARCHAR"], "allowed_characterisations" : ["YEAR_IN_YYYY_FORMAT", "INTEGER_VALUE"]
                        , "target_data_type": "INTEGER", "length_rule": "10", "precision_rule": "{precision}"
                    }
                    , {
                        "allowed_data_types" : ["STRING"], "allowed_characterisations" : []
                        , "target_data_type": "STRING", "length_rule": "{length}", "precision_rule": "{precision}"
                    }
                    , {
                        "allowed_data_types" : ["TIMESTAMP"], "allowed_characterisations" : []
                        , "target_data_type": "TIMESTAMP_NTZ", "length_rule": "29", "precision_rule": "9"
                    }
                ]
                , "default_keep_source_format" : False
            }
        , "field_data_types_to_exclude" : ['IMAGE']
        , "field_characterisations_to_exclude" : ['FREE_TEXT']
        , "exclude_fields_without_characterisations" : True
    }
    
    FLD_DICT_1 = { 
        "name" : "id", "desc" : "ID of the product", "position" : 1, "data_type" : "NUMERIC", "length" : 10, "precision" : 0
        , "default_value": "-1", "characterisations" : [{"name" : "TEC_ID"}, {"name" : "MANDATORY"}, {"name" : "UNIQUE"}, {"name" : "UID"}]
    }
    FLD_DICT_2 = { 
        "name" : "code", "desc" : "Code of the product", "position" : 2, "data_type" : "STRING", "length" : 30, "precision" : 0
        , "default_value": "'#'", "characterisations" : [{"name" : "FCT_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]
    }
    FLD_DICT_3 = { 
        "name" : "modifiedAt", "desc" : "Last Modified At (Timestamp)", "position" : 3, "data_type" : "TIMESTAMP", "length" : 29, "precision" : 9
        , "default_value": None, "characterisations" : [{"name" : "REC_LAST_UPDATE_TST"}]
    }
    FLD_DICT_4 = { 
        "name" : "desc", "desc" : "Description of the product", "position" : 3, "data_type" : "STRING", "length" : 1000, "precision" : 0
        , "default_value": None, "characterisations" : [{"name" : "FREE_TEXT"}]
    }
    FLD_DICT_5 = { 
        "name" : "img", "desc" : "Image of the product", "position" : 3, "data_type" : "IMAGE", "length" : 1000000, "precision" : 0
        , "default_value": None, "characterisations" : [{"name" : "IMAGE"}]
    }
    FLD_DICT_6 = { 
        "name" : "desc2", "desc" : "Description of the product", "position" : 3, "data_type" : "STRING", "length" : 1000, "precision" : 0
        , "default_value": None, "characterisations" : []
    }

    def test_create_field_for_adapter_keeping_source_format(self):
        log_event_default(StdTestEvent("Field Adapter - Create Field For Adapter / Keeping Source Format - Start"))
        field_adapter : FieldAdapter = FieldAdapter.from_dict(self.FLD_ADAPTER_DICT_KEEP_SOURCE_FORMAT)
        self.assertIsNotNone(field_adapter)
        
        # Test of creation from field 1
        new_field = field_adapter.create_field(original_field=Field.from_dict(self.FLD_DICT_1))
        self.assertIsNotNone(new_field)
        self.assertEqual("id", new_field.name)
        self.assertEqual("ID of the product", new_field.desc)
        self.assertEqual(0, new_field.position)
        self.assertEqual("NUMERIC", new_field.data_type)
        self.assertEqual(10, new_field.length)
        self.assertEqual(0, new_field.precision)
        self.assertEqual("-1", new_field.default_value)
        self.assertEqual(4, len(new_field.characterisations))
        self.assertEqual(['TEC_ID', 'MANDATORY', 'UNIQUE', 'UID'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        # Test of creation from field 2
        new_field = field_adapter.create_field(original_field=Field.from_dict(self.FLD_DICT_2))
        self.assertIsNotNone(new_field)
        self.assertEqual("code", new_field.name)
        self.assertEqual("Code of the product", new_field.desc)
        self.assertEqual(0, new_field.position)
        self.assertEqual("STRING", new_field.data_type)
        self.assertEqual(30, new_field.length)
        self.assertEqual(0, new_field.precision)
        self.assertEqual("'#'", new_field.default_value)
        self.assertEqual(3, len(new_field.characterisations))
        self.assertEqual(['FCT_ID', 'UNIQUE', 'UID'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        # Test of creation from field 3
        new_field = field_adapter.create_field(original_field=Field.from_dict(self.FLD_DICT_3), override_params={'field_name' : 'DT_IS_UPDATED_AT'})
        self.assertIsNotNone(new_field)
        self.assertEqual("modifiedAt", new_field.name)
        self.assertEqual("Last Modified At (Timestamp)", new_field.desc)
        self.assertEqual(0, new_field.position)
        self.assertEqual("TIMESTAMP_NTZ", new_field.data_type)
        self.assertEqual(29, new_field.length)
        self.assertEqual(9, new_field.precision)
        self.assertIsNone(new_field.default_value)
        self.assertEqual(1, len(new_field.characterisations))
        self.assertEqual(['REC_LAST_UPDATE_TST'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        log_event_default(StdTestEvent("Field Adapter - Create Field For Adapter / Keeping Source Format - Succeeded"))
    
    def test_create_field_for_adapter_with_default_format(self):
        log_event_default(StdTestEvent("Field Adapter - Create Field For Adapter / With Default Format - Start"))
        field_adapter : FieldAdapter = FieldAdapter.from_dict(self.FLD_ADAPTER_DICT_DEFAULT_FORMAT_AND_STAGING_CONFIG)
        self.assertIsNotNone(field_adapter)
        
        # Test of creation from field 1
        new_field = field_adapter.create_field(original_field=Field.from_dict(self.FLD_DICT_1))
        self.assertIsNotNone(new_field)
        self.assertEqual("id", new_field.name)
        self.assertEqual("ID of the product", new_field.desc)
        self.assertEqual(0, new_field.position)
        self.assertEqual("STRING", new_field.data_type)
        self.assertEqual(256, new_field.length)
        self.assertEqual(0, new_field.precision)
        self.assertEqual("-1", new_field.default_value)
        self.assertEqual(2, len(new_field.characterisations))
        self.assertEqual(['UNIQUE', 'UID'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        # Test of creation from field 2
        new_field = field_adapter.create_field(original_field=Field.from_dict(self.FLD_DICT_2))
        self.assertIsNotNone(new_field)
        self.assertEqual("code", new_field.name)
        self.assertEqual("Code of the product", new_field.desc)
        self.assertEqual(0, new_field.position)
        self.assertEqual("STRING", new_field.data_type)
        self.assertEqual(30, new_field.length)
        self.assertEqual(0, new_field.precision)
        self.assertEqual("'#'", new_field.default_value)
        self.assertEqual(3, len(new_field.characterisations))
        self.assertEqual(['FCT_ID', 'UNIQUE', 'UID'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        # Test of creation from field 3
        new_field = field_adapter.create_field(original_field=Field.from_dict(self.FLD_DICT_3))
        self.assertIsNotNone(new_field)
        self.assertEqual("modifiedAt", new_field.name)
        self.assertEqual("Last Modified At (Timestamp)", new_field.desc)
        self.assertEqual(0, new_field.position)
        self.assertEqual("TIMESTAMP_NTZ", new_field.data_type)
        self.assertEqual(29, new_field.length)
        self.assertEqual(9, new_field.precision)
        self.assertIsNone(new_field.default_value)
        self.assertEqual(1, len(new_field.characterisations))
        self.assertEqual(['REC_LAST_UPDATE_TST'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        log_event_default(StdTestEvent("Field Adapter - Create Field For Adapter / With Default Format - Succeeded"))

    def test_create_field_for_adapter_for_std_curated_layer(self):
        log_event_default(StdTestEvent("Field Adapter - Create Field For Adapter / For Std Curated Layer - Start"))
        field_adapter : FieldAdapter = FieldAdapter.from_dict(self.FLD_ADAPTER_DICT_DEFAULT_CURATED_FROM_SRC)
        self.assertIsNotNone(field_adapter)
        
        # Test of creation from field 1
        new_field = field_adapter.create_field(original_field=Field.from_dict(self.FLD_DICT_1))
        self.assertIsNotNone(new_field)
        self.assertEqual("id", new_field.name)
        self.assertEqual("ID of the product", new_field.desc)
        self.assertEqual(0, new_field.position)
        self.assertEqual("STRING", new_field.data_type)
        self.assertEqual(256, new_field.length)
        self.assertEqual(0, new_field.precision)
        self.assertEqual("-1", new_field.default_value)
        self.assertEqual(4, len(new_field.characterisations))
        self.assertEqual(['TEC_ID', 'MANDATORY', 'UNIQUE', 'UID'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        # Test of creation from field 2
        new_field = field_adapter.create_field(original_field=Field.from_dict(self.FLD_DICT_2))
        self.assertIsNotNone(new_field)
        self.assertEqual("code", new_field.name)
        self.assertEqual("Code of the product", new_field.desc)
        self.assertEqual(0, new_field.position)
        self.assertEqual("STRING", new_field.data_type)
        self.assertEqual(30, new_field.length)
        self.assertEqual(0, new_field.precision)
        self.assertEqual("'#'", new_field.default_value)
        self.assertEqual(3, len(new_field.characterisations))
        self.assertEqual(['FCT_ID', 'UNIQUE', 'UID'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        # Test of creation from field 3
        new_field = field_adapter.create_field(original_field=Field.from_dict(self.FLD_DICT_3), override_params={'field_name' : 'DT_IS_UPDATED_AT'})
        self.assertIsNotNone(new_field)
        self.assertEqual("DT_IS_UPDATED_AT", new_field.name)
        self.assertEqual("Last Modified At (Timestamp)", new_field.desc)
        self.assertEqual(0, new_field.position)
        self.assertEqual("TIMESTAMP_NTZ", new_field.data_type)
        self.assertEqual(29, new_field.length)
        self.assertEqual(9, new_field.precision)
        self.assertIsNone(new_field.default_value)
        self.assertEqual(1, len(new_field.characterisations))
        self.assertEqual(['REC_SOURCE_LAST_UPDATE_TST'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        log_event_default(StdTestEvent("Field Adapter - Create Field For Adapter / For Std Curated Layer - Succeeded"))
    
    def test_should_field_be_adapted(self):
        log_event_default(StdTestEvent("Field Adapter - Should Field Be Adapted - Start"))
        field_adapter : FieldAdapter = FieldAdapter.from_dict(self.FLD_ADAPTER_DICT_DEFAULT_CURATED_FROM_SRC)
        self.assertIsNotNone(field_adapter)
        
        # Test of creation from field 1
        self.assertTrue(field_adapter.should_field_be_adapted(Field.from_dict(self.FLD_DICT_1)))
        self.assertTrue(field_adapter.should_field_be_adapted(Field.from_dict(self.FLD_DICT_2)))
        self.assertTrue(field_adapter.should_field_be_adapted(Field.from_dict(self.FLD_DICT_3)))
        self.assertFalse(field_adapter.should_field_be_adapted(Field.from_dict(self.FLD_DICT_4)))
        self.assertFalse(field_adapter.should_field_be_adapted(Field.from_dict(self.FLD_DICT_5)))
        self.assertFalse(field_adapter.should_field_be_adapted(Field.from_dict(self.FLD_DICT_6)))

        log_event_default(StdTestEvent("Field Adapter - Should Field Be Adapted - Succeeded"))
   
if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
