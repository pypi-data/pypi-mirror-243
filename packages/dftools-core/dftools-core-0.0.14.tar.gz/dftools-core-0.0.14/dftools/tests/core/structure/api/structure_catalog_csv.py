import unittest
import os

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.core import StructureCatalog, Structure, Namespace
from dftools.core.structure.api.structure_catalog_csv import StructureCatalogCsv


class StructureCatalogCsvTest(unittest.TestCase):
    maxDiff = 1000 # Set to 1000 due to the check of the content of the csv file generated

    DFT_STRUCTURE_DICT = {
            "name" : "df_product"
            , "desc" : "Product Table"
            , "type" : "BASE TABLE"
            , "row_count" : 320
            , "options" : {"func_domain" : "PRODUCT"}
            , "content_type" : []
            , "characterisations" : ["Master Data", "Complete Data"]
            , "fields" : [
                { "name" : "id", "desc" : "ID of the product", "position" : 1, "data_type" : "NUMERIC", "length" : 10, "precision" : 0
                    , "default_value": "-1", "characterisations" : [{"name" : "TEC_ID"}, {"name" : "MANDATORY"}, {"name" : "UNIQUE"}, {"name" : "UID"}]}
                , { "name" : "code", "desc" : "Code of the product", "position" : 2, "data_type" : "STRING", "length" : 30, "precision" : 0
                    , "default_value": "'#'", "characterisations" : [{"name" : "FCT_ID"}, {"name" : "UNIQUE"}, {"name" : "UID"}]}
            ]
    }
    DFT_NAMESPACE = Namespace('Snowflake', 'DF', 'DTL')

    DFT_STRUCTURE_CSV_CONTENT = "DataBank;Catalog;Namespace;Structure Name;Structure Type;Row Type;Position;Field Name;Description;Characterisations;DataType/Options;Length;Precision;Default Value\n" \
            + "Snowflake;DF;DTL;df_product;BASE TABLE;Data Structure;;;Product Table;Master Data,Complete Data;func_domain=PRODUCT;320;;;;;;;;\n" \
            + "Snowflake;DF;DTL;df_product;BASE TABLE;Field Structure;1;id;ID of the product;TEC_ID,MANDATORY,UNIQUE,UID;NUMERIC;10;0;-1;;;;;;\n" \
            + "Snowflake;DF;DTL;df_product;BASE TABLE;Field Structure;2;code;Code of the product;FCT_ID,UNIQUE,UID;STRING;30;0;'#';;;;;;\n"

    def test_write_csv(self):
        log_event_default(StdTestEvent("Structure Catalog - Test Write CSV - Start"))
        str_catalog = StructureCatalog()
        str_catalog.add_namespace(self.DFT_NAMESPACE)
        str_catalog.add_structure(self.DFT_NAMESPACE, Structure.from_dict(self.DFT_STRUCTURE_DICT))

        file_path = 'structure_catalog_test_write.csv'
        abs_file_path = os.path.abspath(file_path)
        if os.path.exists(abs_file_path):
            if os.path.isfile(abs_file_path):
                os.remove(abs_file_path)
            else : 
                raise ValueError('Cannot remove object located at : ' + abs_file_path)
            
        self.assertFalse(os.path.exists(abs_file_path))

        StructureCatalogCsv.to_csv(file_path=abs_file_path, obj=str_catalog)

        self.assertTrue(os.path.exists(abs_file_path))
        with open(abs_file_path, "r") as file :
            file_data = file.read()
            self.assertEqual(self.DFT_STRUCTURE_CSV_CONTENT, file_data)

        log_event_default(StdTestEvent("Structure Catalog - Test Write CSV - Succeeded"))

    def test_read_csv(self):
        log_event_default(StdTestEvent("Structure Catalog - Test Read CSV - Start"))
        input_csv_str = "DataBank;Catalog;Namespace;Structure Name;Structure Type;Row Type;Position;Field Name;Description;Characterisations;DataType/Options;Length;Precision;Default Value\n" \
            + "Snowflake;DF;DTL;df_product;BASE TABLE;Data Structure;;;Product Table;Master Data,Complete Data;func_domain=product,layer=CDS;320;;;;;;;;\n" \
            + "Snowflake;DF;DTL;df_product;BASE TABLE;Field Structure;1;id;ID of the product;TEC_ID,MANDATORY,UNIQUE,UID;NUMERIC;10;0;-1;;;;;;\n" \
            + "Snowflake;DF;DTL;df_product;BASE TABLE;Field Structure;2;code;Code of the product;FCT_ID,UNIQUE,UID;STRING;30;0;'#';;;;;;"
        
        file_path = 'structure_catalog_test_read.csv'
        abs_file_path = os.path.abspath(file_path)
        with open(abs_file_path, "w") as file :
            file.write(input_csv_str)

        str_catalog = StructureCatalogCsv.read_csv(file_path=abs_file_path)
        
        self.assertIsNotNone(str_catalog)
        structures = str_catalog.get_structures(self.DFT_NAMESPACE)
        self.assertEqual(1, len(structures))
        self.assertTrue("df_product" in structures.keys())
        structure = structures['df_product']
        self.assertEqual(['id', 'code'], structure.get_field_names())
        self.assertEqual(['Master Data', 'Complete Data'], structure.get_characterisations())
        self.assertEqual(2, len(structure.get_option_keys()))
        self.assertEqual({'func_domain': 'product', "layer" : "CDS"}, structure.get_options())
        
        log_event_default(StdTestEvent("Structure Catalog - Test Read CSV - Succeeded"))


if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
