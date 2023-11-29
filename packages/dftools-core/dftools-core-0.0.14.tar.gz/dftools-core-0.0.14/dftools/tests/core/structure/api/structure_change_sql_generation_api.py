import unittest
import os
from jinja2 import Template

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.core.structure.core import Structure, Namespace
from dftools.core.structure.compare import StructureComparator
from dftools.core.structure.api.structure_change_sql_generation_api import StructureChangeSQLGenerationApi


class StructureChangeSQLGenerationApiTest(unittest.TestCase):
    maxDiff = 2000  # Set to 1000 due to the check of SQLs

    DFT_NAMESPACE = Namespace('Snowflake', 'DF', 'DTL')

    DFT_STRUCTURE_ORIG1_DICT = {
        "name": "df_product"
        , "desc": None
        , "type": "BASE TABLE"
        , "row_count": 320
        , "options": {"func_domain": "MD_PRODUCT"}
        , "content_type": []
        , "fields": [
            {"name": "id", "desc": "ID of the product", "position": 1, "data_type": "NUMERIC", "length": 10,
             "precision": 0
                , "default_value": "-1",
             "characterisations": [{"name": "TEC_ID"}, {"name": "MANDATORY"}, {"name": "UNIQUE"}, {"name": "UID"}]}
            , {"name": "code", "desc": "Code of the product", "position": 2, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FCT_ID"}, {"name": "UNIQUE"}]}
            , {"name": "type", "desc": "Type of the product", "position": 3, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FREE_TEXT"}]}
            , {"name": "last_update_tst", "desc": "Last Update Timestamp", "position": 4, "data_type": "TIMESTAMP_NTZ"
                , "length": 29, "precision": 9
                , "default_value": None, "characterisations": [{"name": "REC_LAST_UPDATE_TST"}]}
        ]
    }
    DFT_STRUCTURE_ORIG1 = Structure.from_dict(DFT_STRUCTURE_ORIG1_DICT)

    DFT_STRUCTURE_ORIG2_DICT = {
        "name": "df_product"
        , "desc": "MD - Product Table"
        , "type": "BASE TABLE"
        , "row_count": 320
        , "options": {"func_domain": "MD_PRODUCT"}
        , "content_type": []
        , "fields": [
            {"name": "id", "desc": "ID of the product", "position": 1, "data_type": "NUMERIC", "length": 10,
             "precision": 0
                , "default_value": "-1",
             "characterisations": [{"name": "TEC_ID"}, {"name": "MANDATORY"}, {"name": "UNIQUE"}, {"name": "UID"}]}
            , {"name": "code", "desc": "Code of the product", "position": 2, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FCT_ID"}, {"name": "UNIQUE"}]}
            , {"name": "type", "desc": "Type of the product", "position": 3, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FREE_TEXT"}]}
            , {"name": "type2", "desc": "Type 2 of the product", "position": 4, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FREE_TEXT"}]}
            , {"name": "last_update_tst", "desc": "Last Update Timestamp", "position": 5, "data_type": "TIMESTAMP_NTZ"
                , "length": 29, "precision": 9
                , "default_value": None, "characterisations": [{"name": "REC_LAST_UPDATE_TST"}]}
        ]
    }
    DFT_STRUCTURE_ORIG2 = Structure.from_dict(DFT_STRUCTURE_ORIG2_DICT)

    DFT_STRUCTURE_ORIG3_DICT = {
        "name": "df_product"
        , "desc": "[DF] MD - Product Table"
        , "type": "BASE TABLE"
        , "row_count": 320
        , "options": {"func_domain": "MD_PRODUCT"}
        , "content_type": []
        , "fields": [
            {"name": "id", "desc": "ID of the product", "position": 1, "data_type": "NUMERIC", "length": 10,
             "precision": 0
                , "default_value": "-1",
             "characterisations": [{"name": "TEC_ID"}, {"name": "MANDATORY"}, {"name": "UNIQUE"}, {"name": "UID"}]}
            , {"name": "code", "desc": "Code of the product", "position": 2, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FCT_ID"}, {"name": "UNIQUE"}]}
            , {"name": "type", "desc": "Type of the product", "position": 3, "data_type": "STRING", "length": 30,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FREE_TEXT"}]}
            , {"name": "type2", "desc": "Type 2 of the product", "position": 4, "data_type": "STRING", "length": 50,
               "precision": 0
                , "default_value": "'#'", "characterisations": [{"name": "FREE_TEXT"}]}
            , {"name": "last_update_tst", "desc": "[Technical] Last Update Timestamp", "position": 5
                , "data_type": "TIMESTAMP_NTZ", "length": 29, "precision": 9
                , "default_value": None, "characterisations": [{"name": "REC_LAST_UPDATE_TST"}]}
        ]
    }
    DFT_STRUCTURE_ORIG3 = Structure.from_dict(DFT_STRUCTURE_ORIG3_DICT)

    DFT_DROP_STRUCTURE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates'
                                                      , 'Default_Drop_Table_SQL.sql')
    DFT_CREATE_STRUCTURE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates'
                                                      , 'Default_Create_Table_SQL.sql')
    DFT_ALTER_STRUCTURE_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates'
                                                      , 'Default_Alter_Table_SQL.sql')

    def _get_table_change_sql_generation_api(self):
        with open(self.DFT_DROP_STRUCTURE_TEMPLATE_PATH, 'r') as file:
            template_file = file.read()
        drop_structure_template = Template(template_file)
        with open(self.DFT_CREATE_STRUCTURE_TEMPLATE_PATH, 'r') as file:
            template_file = file.read()
        create_structure_template = Template(template_file)
        with open(self.DFT_ALTER_STRUCTURE_TEMPLATE_PATH, 'r') as file:
            template_file = file.read()
        alter_structure_template = Template(template_file)
        return StructureChangeSQLGenerationApi(allowed_structure_types=['BASE TABLE']
            , drop_structure_sql_template=drop_structure_template
            , create_structure_sql_template=create_structure_template
            , alter_structure_sql_template=alter_structure_template)

    SQL_CREATE_EXPECTED_OUTPUT_STATEMENT = """CREATE OR REPLACE TABLE df_product (
        id NUMERIC(10) NOT NULL DEFAULT -1 COMMENT 'ID of the product'
        ,  code STRING(30) NULL DEFAULT '#' COMMENT 'Code of the product'
        ,  type STRING(30) NULL DEFAULT '#' COMMENT 'Type of the product'
        ,  last_update_tst TIMESTAMP_NTZ(9) NULL COMMENT 'Last Update Timestamp'
        , CONSTRAINT PK_df_product primary key (id)
);"""

    SQL_ALTER_EXPECTED_OUTPUT_STATEMENT_NEW_FIELD = """CREATE OR REPLACE TABLE df_product_BKP AS SELECT * FROM df_product;

CREATE OR REPLACE TABLE df_product (
        id NUMERIC(10) NOT NULL DEFAULT -1 COMMENT 'ID of the product'
        ,  code STRING(30) NULL DEFAULT '#' COMMENT 'Code of the product'
        ,  type STRING(30) NULL DEFAULT '#' COMMENT 'Type of the product'
        ,  type2 STRING(30) NULL DEFAULT '#' COMMENT 'Type 2 of the product'
        ,  last_update_tst TIMESTAMP_NTZ(9) NULL COMMENT 'Last Update Timestamp'
        , CONSTRAINT PK_df_product primary key (id)
) COMMENT = 'MD - Product Table' ;

INSERT INTO df_product
SELECT
    id
    , code
    , type
    , '#' AS type2
    , last_update_tst
FROM df_product_BKP
;

DROP TABLE df_product_BKP;
"""

    SQL_ALTER_EXPECTED_OUTPUT_STATEMENT_ALTER_ONLY = \
"""ALTER TABLE df_product COMMENT SET COMMENT = '[DF] MD - Product Table';
ALTER TABLE df_product ALTER COLUMN type2 SET DATA TYPE STRING(50);
ALTER TABLE df_product ALTER COLUMN last_update_tst COMMENT '[Technical] Last Update Timestamp';
"""
    def test_create_sql_for_drop_statement(self):
        log_event_default(StdTestEvent("Structure Change SQL Generation API - Test Drop Statement Generation - Start"))

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(self.DFT_STRUCTURE_ORIG1, None)

        structure_change_sql_gen_api = self._get_table_change_sql_generation_api()
        sql_statement = structure_change_sql_gen_api.create_sql(str_comparison)

        self.assertIsNotNone(sql_statement)
        self.assertEqual("DROP TABLE IF EXISTS df_product;", sql_statement)

        log_event_default(
            StdTestEvent("Structure Change SQL Generation API - Test Drop Statement Generation - Succeeded"))

    def test_create_sql_for_create_statement(self):
        log_event_default(StdTestEvent("Structure Change SQL Generation API - Test Create Statement Generation - Start"))

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(None, self.DFT_STRUCTURE_ORIG1)

        structure_change_sql_gen_api = self._get_table_change_sql_generation_api()
        sql_statement = structure_change_sql_gen_api.create_sql(str_comparison)

        self.assertIsNotNone(sql_statement)
        self.assertEqual(self.SQL_CREATE_EXPECTED_OUTPUT_STATEMENT, sql_statement)

        log_event_default(
            StdTestEvent("Structure Change SQL Generation API - Test Create Statement Generation - Succeeded"))

    def test_create_sql_for_alter_statement_new_field(self):
        log_event_default(StdTestEvent("Structure Change SQL Generation API - Test Alter Statement Generation (New "
                                       "Field) - Start"))

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(self.DFT_STRUCTURE_ORIG1, self.DFT_STRUCTURE_ORIG2)

        structure_change_sql_gen_api = self._get_table_change_sql_generation_api()
        sql_statement = structure_change_sql_gen_api.create_sql(str_comparison)

        self.assertIsNotNone(sql_statement)
        self.assertEqual(self.SQL_ALTER_EXPECTED_OUTPUT_STATEMENT_NEW_FIELD, sql_statement)

        log_event_default(
            StdTestEvent("Structure Change SQL Generation API - Test Alter Statement Generation (New Field) - Succeeded"))

    def test_create_sql_for_alter_statement_only_alter(self):
        log_event_default(StdTestEvent("Structure Change SQL Generation API - Test Alter Statement Generation (Only "
                                       "Alter) - Start"))

        str_comparator = StructureComparator()
        str_comparison = str_comparator.compare(self.DFT_STRUCTURE_ORIG2, self.DFT_STRUCTURE_ORIG3)

        structure_change_sql_gen_api = self._get_table_change_sql_generation_api()
        sql_statement = structure_change_sql_gen_api.create_sql(str_comparison)

        self.assertIsNotNone(sql_statement)
        self.assertEqual(self.SQL_ALTER_EXPECTED_OUTPUT_STATEMENT_ALTER_ONLY, sql_statement)

        log_event_default(StdTestEvent("Structure Change SQL Generation API - Test Alter Statement Generation (Only "
                                       "Alter) - Succeeded"))


if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
