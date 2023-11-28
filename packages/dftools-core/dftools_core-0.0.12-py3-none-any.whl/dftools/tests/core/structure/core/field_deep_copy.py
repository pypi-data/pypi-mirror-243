import unittest

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.core.field import Field

class FieldDeepCopyTest(unittest.TestCase):
   
    def test_deep_copy(self):
        log_event_default(StdTestEvent("Field - Deep Copy - Start"))
        input_dict = {
            "name" : "Field1", "desc" : "toto", "default_value": "dft_val", "characterisations" : [{"name" : "TEC_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]
            , "sourcing_info" : {
                "master_source_structure_ref" : {"databank_name" : "ERP_1", "catalog" : "dbo", "namespace" : "public", "structure_name" : "Master_Source_1"}
                , "master_source_structure_field_name" : "Field1"
                , "source_structure_ref" : {"databank_name" : "DataLake", "catalog" : "DF", "namespace" : "DTL", "structure_name" : "Source_1"}
                , "source_structure_field_name" : "Field1"
                , "field_update_strategies" : []
            }
        }
        field : Field = Field.from_dict(input_dict)
        field_copy : Field = Field.deep_copy(field)
        self.assertIsNotNone(field_copy)
        self.assertEqual("Field1", field_copy.name)
        self.assertEqual("toto", field_copy.desc)
        self.assertEqual(0, field_copy.position)
        self.assertEqual('', field_copy.data_type)
        self.assertEqual(3, len(field_copy.characterisations))
        self.assertIsNotNone(field_copy.sourcing_info)
        self.assertIsNotNone(field_copy.sourcing_info.master_source_structure_ref)
        self.assertEqual("Master_Source_1", field.sourcing_info.master_source_structure_ref.structure_name)
        self.assertEqual("Master_Source_1", field_copy.sourcing_info.master_source_structure_ref.structure_name)
        field_copy.sourcing_info.master_source_structure_ref.structure_name = "Master_Source_2"
        self.assertEqual("Master_Source_1", field.sourcing_info.master_source_structure_ref.structure_name)
        self.assertEqual("Master_Source_2", field_copy.sourcing_info.master_source_structure_ref.structure_name)
        log_event_default(StdTestEvent("Field - Deep Copy - Succeeded"))

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
