import unittest

from dftools.events import LoggerManager, EventLevel

from dftools.tests.core.structure.compare.structure_compare import StructureCompareTest
from dftools.tests.core.structure.compare.structure_compare_multiple import StructureCompareForMultipleTest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(StructureCompareTest('test_compare_structure_desc_changed_and_std_methods'))
    suite.addTest(StructureCompareTest('test_compare_with_field_changes'))
    suite.addTest(StructureCompareTest('test_to_csv'))
    suite.addTest(StructureCompareTest('test_get_event_status'))
    suite.addTest(StructureCompareTest('test_is_methods'))
    suite.addTest(StructureCompareTest('test_field_changes_methods'))
    suite.addTest(StructureCompareTest('test_get_event_dict'))
    suite.addTest(StructureCompareTest('test_compare_with_field_renaming'))
    suite.addTest(StructureCompareForMultipleTest('test_compare_multiple_with_renaming_of_structure'))
    return suite


if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
