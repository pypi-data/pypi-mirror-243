import unittest

from dftools.events import LoggerManager, EventLevel

from dftools.tests.core.structure.check.std_structure_checks import StructureCheckRuleTest
from dftools.tests.core.structure.check.structure_checker import StructureCheckerTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(StructureCheckRuleTest('test_structure_check_rule_comment_filled'))
    suite.addTest(StructureCheckRuleTest('test_structure_check_rule_field_present'))
    suite.addTest(StructureCheckerTest('test_structure_checker_all_valid'))
    suite.addTest(StructureCheckerTest('test_structure_checker_missing_fields'))
    suite.addTest(StructureCheckerTest('test_to_csv_all_valid'))
    return suite

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
