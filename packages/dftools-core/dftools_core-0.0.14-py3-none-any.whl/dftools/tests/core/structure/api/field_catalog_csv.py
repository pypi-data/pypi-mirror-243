import unittest
import os

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.core import FieldCatalog, Field, Namespace
from dftools.core.structure.api.field_catalog_csv import FieldCatalogCsv

class FieldCatalogCsvTest(unittest.TestCase):
    maxDiff = 1000 # Set to 1000 due to the check of the content of the csv file generated
    
    DFT_FIELD_DICT = {
        "name" : "DT_IS_INSERTED_AT", "desc" : "Technical - The entry was created at (date and time)"
        , "position" : 0, "data_type" : "TIMESTAMP_NTZ", "length" : 29, "precision" : 9
        , "characterisations" : [{"name" : "REC_INSERT_TST"}]
        , "default_value" : None
    }

    DFT_NAMESPACE = Namespace('Snowflake', 'DF', 'DTL')

    DFT_FIELD_CSV_CONTENT = "Row Type;DataBank;Catalog;Namespace;Name;Description;Position;Characterisations;DataType;Length;Precision;Default Value\n" \
            + "Field;Snowflake;DF;DTL;DT_IS_INSERTED_AT;Technical - The entry was created at (date and time);0;REC_INSERT_TST;TIMESTAMP_NTZ;29;9;\n"

    def test_write_csv(self):
        log_event_default(StdTestEvent("Field Catalog - Test Write CSV - Start"))
        field_catalog = FieldCatalog()
        field_catalog.add_namespace(self.DFT_NAMESPACE)
        field_catalog.add_field(self.DFT_NAMESPACE, Field.from_dict(self.DFT_FIELD_DICT))

        file_path = 'field_catalog_test_write.csv'
        abs_file_path = os.path.abspath(file_path)
        if os.path.exists(abs_file_path):
            if os.path.isfile(abs_file_path):
                os.remove(abs_file_path)
            else : 
                raise ValueError('Cannot remove object located at : ' + abs_file_path)
            
        self.assertFalse(os.path.exists(abs_file_path))

        FieldCatalogCsv.to_csv(file_path=abs_file_path, obj=field_catalog)

        self.assertTrue(os.path.exists(abs_file_path))
        with open(abs_file_path, "r") as file :
            file_data = file.read()
            self.assertEqual(self.DFT_FIELD_CSV_CONTENT, file_data)

        log_event_default(StdTestEvent("Field Catalog - Test Write CSV - Succeeded"))
    
    def test_read_csv(self):
        log_event_default(StdTestEvent("Field Catalog - Test Read CSV - Start"))
        input_csv_str = "Row Type;DataBank;Catalog;Namespace;Name;Description;Position;Characterisations;DataType;Length;Precision;Default Value\n" \
            + "Field;Snowflake;DF;DTL;DT_IS_INSERTED_AT;Technical - The entry was created at (date and time);0;REC_INSERT_TST;TIMESTAMP_NTZ;29;9;\n" \
            + "Field;Snowflake;DF;DTL;DT_IS_UPDATED_AT;The entry was last updated at (date and time);0;REC_LAST_UPDATE_TST;TIMESTAMP_NTZ;29;9;\n" \
            + "Field;Snowflake;DF;DTL;DS_IS_UPDATED_BY;Technical - The entry was last updated by (user or process);0;REC_LAST_UPDATE_USER_NAME;TEXT;100;0;\n" \
            + "Field;Snowflake;DF;DTL;DT_IS_SRC_EXTRACTED_AT;Technical - Source - The data was extracted from source at (date and time);0;REC_SOURCE_EXTRACTION_TST;TIMESTAMP_NTZ;29;9;\n"

        file_path = 'field_catalog_test_read.csv'
        abs_file_path = os.path.abspath(file_path)
        with open(abs_file_path, "w") as file :
            file.write(input_csv_str)

        field_catalog = FieldCatalogCsv.read_csv(file_path=abs_file_path)
        
        self.assertIsNotNone(field_catalog)
        fields = field_catalog.get_fields(self.DFT_NAMESPACE)
        self.assertEqual(4, len(fields))
        self.assertTrue('DT_IS_SRC_EXTRACTED_AT' in list(fields.keys()))
        field = fields['DT_IS_SRC_EXTRACTED_AT']
        self.assertIsNotNone(field)
        self.assertEqual('Technical - Source - The data was extracted from source at (date and time)', field.desc)
        self.assertEqual(0, field.position)
        self.assertEqual(1, len(field.characterisations))
        self.assertTrue(field.has_characterisation('REC_SOURCE_EXTRACTION_TST'))
        self.assertFalse(field.has_characterisation('REC_SOURCE_EXTRACTION_TST_WRONG'))
        self.assertEqual('TIMESTAMP_NTZ', field.data_type)
        self.assertEqual(29, field.length)
        self.assertEqual(9, field.precision)
        
        log_event_default(StdTestEvent("Field Catalog - Test Read CSV - Succeeded"))
    
if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
