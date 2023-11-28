import unittest

from dftools.events import LoggerManager, EventLevel
from dftools.tests.core.structure.adapter.field_format_adapter import FieldFormatAdaptRuleTest, FieldFormatAdapterTest
from dftools.tests.core.structure.adapter.field_adapter import FieldAdapterTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(FieldFormatAdaptRuleTest('test_adapter_rule_simple'))
    suite.addTest(FieldFormatAdaptRuleTest('test_adapter_rule_complex'))
    suite.addTest(FieldFormatAdapterTest('test_get_adapted_field_format'))
    suite.addTest(FieldAdapterTest('test_create_field_for_adapter_keeping_source_format'))
    suite.addTest(FieldAdapterTest('test_create_field_for_adapter_with_default_format'))
    suite.addTest(FieldAdapterTest('test_create_field_for_adapter_for_std_curated_layer'))
    suite.addTest(FieldAdapterTest('test_should_field_be_adapted'))
    return suite

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
