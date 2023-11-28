import unittest

from dftools.events import LoggerManager, EventLevel
from dftools.tests.core.structure.api.structure_catalog_csv import StructureCatalogCsvTest
from dftools.tests.core.structure.api.field_catalog_csv import FieldCatalogCsvTest
from dftools.tests.core.structure.api.structure_change_sql_generation_api import StructureChangeSQLGenerationApiTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(StructureCatalogCsvTest('test_write_csv'))
    suite.addTest(StructureCatalogCsvTest('test_read_csv'))
    suite.addTest(FieldCatalogCsvTest('test_write_csv'))
    suite.addTest(FieldCatalogCsvTest('test_read_csv'))
    suite.addTest(StructureChangeSQLGenerationApiTest('test_create_sql_for_drop_statement'))
    suite.addTest(StructureChangeSQLGenerationApiTest('test_create_sql_for_create_statement'))
    suite.addTest(StructureChangeSQLGenerationApiTest('test_create_sql_for_alter_statement_new_field'))
    suite.addTest(StructureChangeSQLGenerationApiTest('test_create_sql_for_alter_statement_only_alter'))
    return suite


if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
