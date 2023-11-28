import unittest

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel

from dftools.core.structure.core import Structure
from dftools.core.structure.template.structure_template import StructureTemplate

class StructureTemplateTest(unittest.TestCase):
    DFT_FLD_ADAPTER_DICT = {
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
            ]
    }

    DFT_DATALAKE_TEMPLATE_DICT = {
            "name" : "DF_Datalake"
            , "name_rule" : "'RAW_' + original_structure.options['func_domain'].upper() + '_' + original_structure.name"
            , "desc_rule": "'DataLake ' + original_structure.options['func_domain'].upper() + ' - ' + original_structure.desc"
            , "type_rule": "'BASE TABLE'"
            , "mandatory_parameters" : ["original_structure"]
            , "field_adapter" : DFT_FLD_ADAPTER_DICT
            , "field_templates" : [
                {
                    "name" : "STD_LAST_UPDATE_TST_FIELD"
                    , "relative_position" : "END"
                    , "override_existing_field_on_characterisation" :"REC_LAST_UPDATE_TST"
                    , "field": {
                        "name" : "DT_IS_UPDATED_AT", "desc" : "Technical - The entry was last updated at (date and time)"
                        , "position" : 0, "data_type" : "TIMESTAMP_NTZ", "length" : 29, "precision" : 9
                        , "default_value" : None, "characterisations" : [{"name" : "REC_LAST_UPDATE_TST"}]
                    }
                }
            ]
    }

    def test_create_structure(self):
        log_event_default(StdTestEvent("Structure Template - Create Structure - Start"))
        str_template : StructureTemplate = StructureTemplate.from_dict(self.DFT_DATALAKE_TEMPLATE_DICT)
        self.assertIsNotNone(str_template)
        new_structure = str_template.create_structure(original_structure=Structure.from_dict(self.DFT_STRUCTURE_DICT))
        self.assertIsNotNone(new_structure)
        self.assertEqual("RAW_PRODUCT_df_product", new_structure.name)
        self.assertEqual("DataLake PRODUCT - Product Table", new_structure.desc)
        self.assertEqual("BASE TABLE", new_structure.type)
        self.assertEqual(3, len(new_structure.fields))
        
        # Test 1st field : id
        new_field = new_structure.get_field("id")
        self.assertIsNotNone(new_field)
        self.assertEqual("id", new_field.name)
        self.assertEqual("ID of the product", new_field.desc)
        self.assertEqual(1, new_field.position)
        self.assertEqual("STRING", new_field.data_type)
        self.assertEqual(256, new_field.length)
        self.assertEqual(0, new_field.precision)
        self.assertEqual("-1", new_field.default_value)
        self.assertEqual(4, len(new_field.characterisations))
        self.assertEqual(['TEC_ID', 'MANDATORY', 'UNIQUE', 'UID'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        # Test 2nd field : code
        new_field = new_structure.get_field("code")
        self.assertIsNotNone(new_field)
        self.assertEqual("code", new_field.name)
        self.assertEqual("Code of the product", new_field.desc)
        self.assertEqual(2, new_field.position)
        self.assertEqual("STRING", new_field.data_type)
        self.assertEqual(30, new_field.length)
        self.assertEqual(0, new_field.precision)
        self.assertEqual("'#'", new_field.default_value)
        self.assertEqual(3, len(new_field.characterisations))
        self.assertEqual(['FCT_ID', 'UNIQUE', 'UID'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        # Test 2nd field : code
        new_field = new_structure.get_field("DT_IS_UPDATED_AT")
        self.assertIsNotNone(new_field)
        self.assertEqual("DT_IS_UPDATED_AT", new_field.name)
        self.assertEqual("Technical - The entry was last updated at (date and time)", new_field.desc)
        self.assertEqual(3, new_field.position)
        self.assertEqual("TIMESTAMP_NTZ", new_field.data_type)
        self.assertEqual(29, new_field.length)
        self.assertEqual(9, new_field.precision)
        self.assertIsNone(new_field.default_value)
        self.assertEqual(1, len(new_field.characterisations))
        self.assertEqual(['REC_LAST_UPDATE_TST'], new_field.get_characterisation_names())
        self.assertIsNone(new_field.sourcing_info)

        log_event_default(StdTestEvent("Structure Template - Create Structure - Succeeded"))
   
if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
