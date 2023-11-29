import unittest
from typing import Dict

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.service.core import ObjReadHelper, ObjectStandardProviderService
from dftools.service.core.df_obj_service import DfObjects
from dftools.core.structure import Structure, StructureTemplate
from dftools.tests.func_tests.obj_provider import SAMPLE_1_MODEL_SYSTEM_FILE_PATH, SAMPLE_1_MODEL_USER_FILE_PATH

class StructureTemplateFuncTest(unittest.TestCase):
    ORIG_STRUCTURE_DICT = {
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

    RAW_STRUCTURE_DICT = {
            "name" : "RAW_PRODUCT_df_product"
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
                , { "name" : "DS_INTEGRATED_FILENAME", "desc" : "Technical - Source - Integrated file name", "position" : 3
                    , "data_type" : "TEXT", "length" : 1000, "precision" : 0
                    , "default_value": "-1", "characterisations" : [{"name" : "SOURCE_FILE_TECHNICAL_NAME"}]}
                , { "name" : "DT_IS_INSERTED_AT", "desc" : "Technical - The entry was created at (date and time)", "position" : 4
                    , "data_type" : "TIMESTAMP_NTZ", "length" : 29, "precision" : 9
                    , "default_value": None, "characterisations" : [{"name" : "REC_INSERT_TST"}]}
                , { "name" : "DT_IS_UPDATED_AT", "desc" : "Technical - The entry was last updated at (date and time)", "position" : 4
                    , "data_type" : "TIMESTAMP_NTZ", "length" : 29, "precision" : 9
                    , "default_value": None, "characterisations" : [{"name" : "REC_LAST_UPDATE_TST"}]}
            ]
    }

    def test_template_From_Source_FF_STG(self):
        log_event_default(StdTestEvent("Structure Template / Func Test - Template From Source FF Staging - Start"))
        specific_read_helper : Dict[str, ObjReadHelper] = {
            DfObjects.STRUCTURE_TEMPLATE : 
                ObjReadHelper(DfObjects.STRUCTURE_TEMPLATE, True, DfObjects.STRUCTURE_TEMPLATE, "From_Source_FF_STG.json", StructureTemplate)
        }
        provider = ObjectStandardProviderService(system_folder=SAMPLE_1_MODEL_SYSTEM_FILE_PATH, user_folder=SAMPLE_1_MODEL_USER_FILE_PATH
            , object_read_helper_dict=specific_read_helper)
        provider.load_objects_from_files()
        self.assertEqual(['structure_template'], provider.get_available_object_types())
        self.assertEqual(1, len(provider.get_object_keys(object_type=DfObjects.STRUCTURE_TEMPLATE)))
        str_template : StructureTemplate = provider.get_object(DfObjects.STRUCTURE_TEMPLATE, "From_Source_FF_STG")
        self.assertIsNotNone(provider.get_object(DfObjects.STRUCTURE_TEMPLATE, "From_Source_FF_STG"))

        new_structure = str_template.create_structure(original_structure=Structure.from_dict(self.ORIG_STRUCTURE_DICT))
        self.assertEqual(3, len(new_structure.fields))
        self.assertEqual(0, len(new_structure.get_field_names_with_characterisation('TEC_ID')))
        self.assertEqual(1, len(new_structure.get_field_names_with_characterisation('FCT_ID')))
        self.assertEqual(1, len(new_structure.get_field_names_with_characterisations(['TEC_ID', 'FCT_ID'])))
        self.assertEqual(2, len(new_structure.get_field_names_with_characterisations(['UNIQUE', 'WRONG_CHAR'])))
        log_event_default(StdTestEvent("Structure Template / Func Test - Template From Source FF Staging - Succeeded"))

    def test_template_From_Source_FF_DTL_RAW(self):
        log_event_default(StdTestEvent("Structure Template / Func Test - Template From Source FF Raw - Start"))
        specific_read_helper : Dict[str, ObjReadHelper] = {
            DfObjects.STRUCTURE_TEMPLATE : 
                ObjReadHelper(DfObjects.STRUCTURE_TEMPLATE, True, DfObjects.STRUCTURE_TEMPLATE, "From_Source_FF_DTL_RAW.json", StructureTemplate)
        }
        provider = ObjectStandardProviderService(system_folder=SAMPLE_1_MODEL_SYSTEM_FILE_PATH, user_folder=SAMPLE_1_MODEL_USER_FILE_PATH
            , object_read_helper_dict=specific_read_helper)
        provider.load_objects_from_files()
        self.assertEqual(['structure_template'], provider.get_available_object_types())
        self.assertEqual(1, len(provider.get_object_keys(object_type=DfObjects.STRUCTURE_TEMPLATE)))
        str_template : StructureTemplate = provider.get_object(DfObjects.STRUCTURE_TEMPLATE, "From_Source_FF_DTL_RAW")
        self.assertIsNotNone(provider.get_object(DfObjects.STRUCTURE_TEMPLATE, "From_Source_FF_DTL_RAW"))

        new_structure = str_template.create_structure(original_structure=Structure.from_dict(self.ORIG_STRUCTURE_DICT))
        self.assertEqual(12, len(new_structure.fields))
        self.assertEqual(1, len(new_structure.get_field_names_with_characterisation('TEC_ID')))
        self.assertEqual(1, len(new_structure.get_field_names_with_characterisation('FCT_ID')))
        self.assertEqual(2, len(new_structure.get_field_names_with_characterisations(['TEC_ID', 'FCT_ID'])))
        self.assertEqual(2, len(new_structure.get_field_names_with_characterisations(['UNIQUE', 'WRONG_CHAR'])))
        self.assertEqual(1, len(new_structure.get_fields_with_characterisations(['REC_SOURCE_LAST_UPDATE_USER_NAME'])))
        field = new_structure.get_fields_with_characterisations(['REC_LAST_UPDATE_TST'])[0]
        self.assertEqual('DT_IS_UPDATED_AT', field.name)
        self.assertEqual(6, field.position)
        field = new_structure.get_fields_with_characterisations(['REC_SOURCE_LAST_UPDATE_USER_NAME'])[0]
        self.assertEqual('DT_IS_SRC_UPDATED_BY', field.name)
        self.assertEqual(12, field.position)
        log_event_default(StdTestEvent("Structure Template / Func Test - Template From Source FF Raw - Succeeded"))  
    
    def test_template_From_Source_FF_DTL_RAW_With_Snapshot(self):
        log_event_default(StdTestEvent("Structure Template / Func Test - Template From Source FF Raw With Snapshot - Start"))
        specific_read_helper : Dict[str, ObjReadHelper] = {
            DfObjects.STRUCTURE_TEMPLATE : 
                ObjReadHelper(DfObjects.STRUCTURE_TEMPLATE, True, DfObjects.STRUCTURE_TEMPLATE, "From_Source_FF_DTL_RAW_WITH_SNAPSHOT.json", StructureTemplate)
        }
        provider = ObjectStandardProviderService(system_folder=SAMPLE_1_MODEL_SYSTEM_FILE_PATH, user_folder=SAMPLE_1_MODEL_USER_FILE_PATH
            , object_read_helper_dict=specific_read_helper)
        provider.load_objects_from_files()
        self.assertEqual(['structure_template'], provider.get_available_object_types())
        self.assertEqual(1, len(provider.get_object_keys(object_type=DfObjects.STRUCTURE_TEMPLATE)))
        str_template : StructureTemplate = provider.get_object(DfObjects.STRUCTURE_TEMPLATE, "From_Source_FF_DTL_RAW_WITH_SNAPSHOT")
        self.assertIsNotNone(provider.get_object(DfObjects.STRUCTURE_TEMPLATE, "From_Source_FF_DTL_RAW_WITH_SNAPSHOT"))

        new_structure = str_template.create_structure(original_structure=Structure.from_dict(self.ORIG_STRUCTURE_DICT))
        self.assertEqual(13, len(new_structure.fields))
        self.assertEqual(2, len(new_structure.get_field_names_with_characterisation('TEC_ID')))
        self.assertEqual(2, len(new_structure.get_field_names_with_characterisation('FCT_ID')))
        self.assertEqual(2, len(new_structure.get_field_names_with_characterisation('MANDATORY')))
        self.assertEqual(3, len(new_structure.get_field_names_with_characterisations(['TEC_ID', 'FCT_ID'])))
        self.assertEqual(2, len(new_structure.get_field_names_with_characterisations(['UNIQUE', 'WRONG_CHAR'])))
        self.assertEqual(1, len(new_structure.get_fields_with_characterisations(['REC_SOURCE_LAST_UPDATE_USER_NAME'])))
        field = new_structure.get_fields_with_characterisations(['SNAPSHOT_DATE'])[0]
        self.assertEqual('DA_SNAPSHOT', field.name)
        self.assertEqual(1, field.position)
        field = new_structure.get_fields_with_characterisations(['REC_LAST_UPDATE_TST'])[0]
        self.assertEqual('DT_IS_UPDATED_AT', field.name)
        self.assertEqual(7, field.position)
        field = new_structure.get_fields_with_characterisations(['REC_SOURCE_LAST_UPDATE_USER_NAME'])[0]
        self.assertEqual('DT_IS_SRC_UPDATED_BY', field.name)
        self.assertEqual(13, field.position)
        log_event_default(StdTestEvent("Structure Template / Func Test - Template From Source FF Raw With Snapshot - Succeeded"))  

    def test_template_DTL_Curated_From_Raw(self):
        log_event_default(StdTestEvent("Structure Template / Func Test - Template From Source FF Raw With Snapshot - Start"))
        specific_read_helper : Dict[str, ObjReadHelper] = {
            DfObjects.STRUCTURE_TEMPLATE : 
                ObjReadHelper(DfObjects.STRUCTURE_TEMPLATE, True, DfObjects.STRUCTURE_TEMPLATE, "DTL_CURATED_FROM_RAW.json", StructureTemplate)
        }
        provider = ObjectStandardProviderService(system_folder=SAMPLE_1_MODEL_SYSTEM_FILE_PATH, user_folder=SAMPLE_1_MODEL_USER_FILE_PATH
            , object_read_helper_dict=specific_read_helper)
        provider.load_objects_from_files()
        self.assertEqual(['structure_template'], provider.get_available_object_types())
        self.assertEqual(1, len(provider.get_object_keys(object_type=DfObjects.STRUCTURE_TEMPLATE)))
        str_template : StructureTemplate = provider.get_object(DfObjects.STRUCTURE_TEMPLATE, "DTL_CURATED_FROM_RAW")
        self.assertIsNotNone(provider.get_object(DfObjects.STRUCTURE_TEMPLATE, "DTL_CURATED_FROM_RAW"))

        new_structure = str_template.create_structure(original_structure=Structure.from_dict(self.RAW_STRUCTURE_DICT))
        self.assertEqual(14, len(new_structure.fields))
        self.assertEqual(1, len(new_structure.get_field_names_with_characterisation('TEC_ID')))
        self.assertEqual(1, len(new_structure.get_field_names_with_characterisation('FCT_ID')))
        self.assertEqual(1, len(new_structure.get_field_names_with_characterisation('MANDATORY')))
        self.assertEqual(2, len(new_structure.get_field_names_with_characterisations(['TEC_ID', 'FCT_ID'])))
        self.assertEqual(2, len(new_structure.get_field_names_with_characterisations(['UNIQUE', 'WRONG_CHAR'])))
        self.assertEqual(1, len(new_structure.get_fields_with_characterisations(['REC_SOURCE_LAST_UPDATE_USER_NAME'])))
        field = new_structure.get_fields_with_characterisations(['REC_LAST_UPDATE_TST'])[0]
        self.assertEqual('DT_IS_UPDATED_AT', field.name)
        self.assertEqual(6, field.position)
        field = new_structure.get_fields_with_characterisations(['REC_SOURCE_LAST_UPDATE_USER_NAME'])[0]
        self.assertEqual('DT_IS_SRC_UPDATED_BY', field.name)
        self.assertEqual(14, field.position)
        log_event_default(StdTestEvent("Structure Template / Func Test - Template From Source FF Raw With Snapshot - Succeeded"))  

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
