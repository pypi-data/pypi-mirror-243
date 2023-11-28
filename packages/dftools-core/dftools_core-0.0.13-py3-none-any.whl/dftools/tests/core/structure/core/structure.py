import unittest

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel

from dftools.core.structure.core.field import Field
from dftools.core.structure.core.structure import Structure
from dftools.exceptions import FieldRemovalException, MissingMandatoryArgumentException, FieldAdditionException

class StructureTest(unittest.TestCase):
    DFT_STRUCTURE_DICT = {
            "name" : "df_product"
            , "desc" : "Product Table"
            , "type" : "BASE TABLE"
            , "row_count" : 320
            , "options" : {"func_domain" : "PRODUCT"}
            , "content_type" : []
            , "characterisations" : ["Master Data"]
            , "fields" : [
                { "name" : "id", "desc" : "ID of the product", "position" : 1, "data_type" : "NUMERIC", "length" : 10, "precision" : 0
                    , "default_value": "-1", "characterisations" : [{"name" : "TEC_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]}
                , { "name" : "code", "desc" : "Code of the product", "position" : 2, "data_type" : "STRING", "length" : 30, "precision" : 0
                    , "default_value": "'#'", "characterisations" : [{"name" : "FCT_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]}
            ]
    }

    def test_from_dict(self):
        log_event_default(StdTestEvent("Structure - From Dict - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)

        self.assertEqual("df_product", structure.name)
        self.assertEqual("Product Table", structure.desc)
        self.assertEqual("BASE TABLE", structure.type)

        self.assertEqual(2, len(structure.fields))
        self.assertIsNone(structure.sourcing_info)
        
        log_event_default(StdTestEvent("Structure - From Dict - Succeeded"))
    
    def test_add_field_success_fixed_position(self):
        log_event_default(StdTestEvent("Structure - Add Field Success Fixed Position - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)
        self.assertEqual(2, len(structure.fields))
        new_field : Field = Field.from_dict(
            { "name" : "desc", "desc" : "Description of the product", "position" : 3, "data_type" : "STRING", "length" : 100, "precision" : 0
                    , "default_value": "null", "characterisations" : [{"name" : "FREE_TEXT"}]}
        )
        structure.add_field(new_field=new_field)
        self.assertEqual(3, len(structure.fields))
        field = structure.get_field("desc")
        self.assertEqual("desc", field.name)
        self.assertEqual(True, field.has_characterisation("FREE_TEXT"))
        self.assertEqual(3, field.position)
        log_event_default(StdTestEvent("Structure - Add Field Success Fixed Position - Succeeded"))
    
    def test_add_field_success_unknown_position(self):
        log_event_default(StdTestEvent("Structure - Add Field Success Unknown Position - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)
        self.assertEqual(2, len(structure.fields))
        new_field : Field = Field.from_dict(
            { "name" : "desc", "desc" : "Description of the product", "data_type" : "STRING", "length" : 100, "precision" : 0
                    , "default_value": "null", "characterisations" : [{"name" : "FREE_TEXT"}]}
        )
        structure.add_field(new_field=new_field)
        self.assertEqual(3, len(structure.fields))
        field = structure.get_field("desc")
        self.assertEqual("desc", field.name)
        self.assertEqual(True, field.has_characterisation("FREE_TEXT"))
        self.assertEqual(3, field.position)
        log_event_default(StdTestEvent("Structure - Add Field Success Unknown Position - Succeeded"))
    
    def test_add_field_success_unknown_position_relative_to_field(self):
        log_event_default(StdTestEvent("Structure - Add Field Success Unknown Position Relative To Field - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)
        self.assertEqual(2, len(structure.fields))
        
        # Test of previous field name on method add_field
        new_field : Field = Field.from_dict(
            { "name" : "desc", "desc" : "Description of the product", "data_type" : "STRING", "length" : 100, "precision" : 0
                    , "default_value": "null", "characterisations" : [{"name" : "FREE_TEXT"}]}
        )
        structure.add_field(new_field=new_field, previous_field_name="id")
        self.assertEqual(3, len(structure.fields))
        field = structure.get_field("desc")
        self.assertEqual("desc", field.name)
        self.assertEqual(2, field.position)
        field = structure.get_field("code")
        self.assertEqual("code", field.name)
        self.assertEqual(3, field.position)

        # Test of next field name on method add_field
        new_field : Field = Field.from_dict(
            { "name" : "desc2", "desc" : "2nd Description of the product", "data_type" : "STRING", "length" : 100, "precision" : 0
                    , "default_value": "null", "characterisations" : [{"name" : "FREE_TEXT"}]}
        )
        structure.add_field(new_field=new_field, next_field_name="code")
        self.assertEqual(4, len(structure.fields))
        field = structure.get_field("desc2")
        self.assertEqual("desc2", field.name)
        self.assertEqual(3, field.position)
        field = structure.get_field("code")
        self.assertEqual("code", field.name)
        self.assertEqual(4, field.position)

        log_event_default(StdTestEvent("Structure - Add Field Success Unknown Position Relative To Field - Succeeded"))
    
    def test_add_field_missing_mandatory_argument(self):
        log_event_default(StdTestEvent("Structure - Add Field Missing Mandatory Argument - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)
        self.assertEqual(2, len(structure.fields))
        new_field = None
        try :
            structure.add_field(new_field=new_field)
            self.fail('Addition of the field should have failed as None field should not be allowed to be added')
        except MissingMandatoryArgumentException as e:
            # Check that the message of the exception is the correct message
            self.assertEqual("Missing mandatory argument 'New Field' on call of method Add Field on Structure", e.message)
        except Exception as e:
            self.fail('Addition of field should have been thrown a MissingMandatoryArgumentException exception but exception thrown was of type : ' + type(e).__name__)

        log_event_default(StdTestEvent("Structure - Add Field Missing Mandatory Argument - Succeeded"))
    
    def test_add_field_missing_previous_field(self):
        log_event_default(StdTestEvent("Structure - Add Field Missing Previous Field - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)
        self.assertEqual(2, len(structure.fields))
        new_field : Field = Field.from_dict(
            { "name" : "desc", "desc" : "Description of the product", "data_type" : "STRING", "length" : 100, "precision" : 0
                    , "default_value": "null", "characterisations" : [{"name" : "FREE_TEXT"}]}
        )

        with self.assertRaises(FieldAdditionException):
            structure.add_field(new_field=new_field, previous_field_name="unknown")

        log_event_default(StdTestEvent("Structure - Add Field Missing Previous Field - Succeeded"))
    
    def test_add_field_missing_next_field(self):
        log_event_default(StdTestEvent("Structure - Add Field Missing Next Field - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)
        self.assertEqual(2, len(structure.fields))
        new_field : Field = Field.from_dict(
            { "name" : "desc", "desc" : "Description of the product", "data_type" : "STRING", "length" : 100, "precision" : 0
                    , "default_value": "null", "characterisations" : [{"name" : "FREE_TEXT"}]}
        )

        with self.assertRaises(FieldAdditionException):
            structure.add_field(new_field=new_field, next_field_name="unknown")

        log_event_default(StdTestEvent("Structure - Add Field Missing Next Field - Succeeded"))
    
    def test_add_field_wrong_position(self):
        log_event_default(StdTestEvent("Structure - Add Field Wrong Position - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)
        self.assertEqual(2, len(structure.fields))
        new_field : Field = Field.from_dict(
            { "name" : "desc", "desc" : "Description of the product", "data_type" : "STRING", "length" : 100, "precision" : 0
                    , "position" : 4, "default_value": "null", "characterisations" : [{"name" : "FREE_TEXT"}]}
        )
        with self.assertRaises(FieldAdditionException):
            structure.add_field(new_field=new_field, force_position=False, prevent_position_check=False)

        log_event_default(StdTestEvent("Structure - Add Field Wrong Position - Succeeded"))
    
    def test_remove_field(self):
        log_event_default(StdTestEvent("Structure - Remove Field - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)
        self.assertEqual(2, len(structure.fields))
        field = structure.get_field("id")
        self.assertIsNotNone(field) # Field with name id should be available 

        new_field : Field = Field.from_dict(
            { "name" : "desc", "desc" : "Description of the product", "data_type" : "STRING", "length" : 100, "precision" : 0
                    , "default_value": "null", "characterisations" : [{"name" : "FREE_TEXT"}]}
        )
        structure.add_field(new_field=new_field)
        self.assertEqual(3, len(structure.fields))
        
        structure.remove_field(name = "id")
        self.assertEqual(2, len(structure.fields)) # Number of fields should be 2
        field = structure.get_field("id")
        self.assertIsNone(field) # Field with name id should no longer be available
        field = structure.get_field("code")
        self.assertEqual("code", field.name)
        self.assertEqual(1, field.position)
        field = structure.get_field("desc")
        self.assertEqual("desc", field.name)
        self.assertEqual(2, field.position)

        log_event_default(StdTestEvent("Structure - Remove Field - Succeeded"))
    
    def test_remove_field_exception(self):
        log_event_default(StdTestEvent("Structure - Remove Field with Exception - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)
        self.assertEqual(2, len(structure.fields))
        
        with self.assertRaises(FieldRemovalException):
            structure.remove_field(name = "id_wrong")

        log_event_default(StdTestEvent("Structure - Remove Field with Exception - Succeeded"))
    
    def test_get_fields_with_characterisations(self):
        log_event_default(StdTestEvent("Structure - Get Fields With Characterisations - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)

        field_list = structure.get_fields_with_characterisations('TEC_ID')
        self.assertIsNotNone(field_list)
        self.assertEqual(1, len(field_list))
        self.assertEqual("id", field_list[0].name)

        log_event_default(StdTestEvent("Structure - Get Fields With Characterisations - Succeeded"))

    def test_get_fields_wo_characterisations(self):
        log_event_default(StdTestEvent("Structure - Get Fields With Characterisations - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)

        field_list = structure.get_fields_wo_characterisations('TEC_ID')
        self.assertIsNotNone(field_list)
        self.assertEqual(1, len(field_list))
        self.assertEqual("code", field_list[0].name)

        log_event_default(StdTestEvent("Structure - Get Fields With Characterisations - Succeeded"))

    def test_structures_characterisation_methods(self):
        log_event_default(StdTestEvent("Structure - Structure Characterisations methods - Start"))
        structure : Structure = Structure.from_dict(self.DFT_STRUCTURE_DICT)
        self.assertIsNotNone(structure)

        self.assertEqual(1, len(structure.characterisations))
        self.assertTrue(structure.has_characterisation("Master Data"))
        self.assertFalse(structure.has_characterisation("MasterData"))
        
        log_event_default(StdTestEvent("Structure - Structure Characterisations methods - Succeeded"))

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
