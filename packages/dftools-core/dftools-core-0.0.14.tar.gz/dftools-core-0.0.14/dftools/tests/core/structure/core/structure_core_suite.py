import unittest

from dftools.events import LoggerManager, EventLevel

from dftools.tests.core.structure.core.field import FieldTest
from dftools.tests.core.structure.core.field_deep_copy import FieldDeepCopyTest
from dftools.tests.core.structure.core.structure_catalog import StructureCatalogTest
from dftools.tests.core.structure.core.structure import StructureTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(FieldTest('test_from_dict'))
    suite.addTest(FieldTest('test_deep_copy'))
    suite.addTest(FieldTest('test_characterisation_methods'))
    suite.addTest(FieldDeepCopyTest('test_deep_copy'))
    suite.addTest(StructureCatalogTest('test_namespace_methods'))
    suite.addTest(StructureCatalogTest('test_add_structure'))
    suite.addTest(StructureCatalogTest('test_get_number_of_structures_methods'))
    suite.addTest(StructureTest('test_from_dict'))
    suite.addTest(StructureTest('test_add_field_success_fixed_position'))
    suite.addTest(StructureTest('test_add_field_success_unknown_position'))
    suite.addTest(StructureTest('test_add_field_success_unknown_position_relative_to_field'))
    suite.addTest(StructureTest('test_add_field_missing_mandatory_argument'))
    suite.addTest(StructureTest('test_add_field_missing_previous_field'))
    suite.addTest(StructureTest('test_add_field_missing_next_field'))
    suite.addTest(StructureTest('test_add_field_wrong_position'))
    suite.addTest(StructureTest('test_remove_field'))
    suite.addTest(StructureTest('test_remove_field_exception'))
    suite.addTest(StructureTest('test_get_fields_with_characterisations'))
    suite.addTest(StructureTest('test_get_fields_wo_characterisations'))
    return suite

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
