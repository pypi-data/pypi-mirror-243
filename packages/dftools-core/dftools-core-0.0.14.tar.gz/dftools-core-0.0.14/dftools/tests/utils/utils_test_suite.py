import unittest

from dftools.events import LoggerManager, EventLevel
from dftools.tests.utils.dict_decoder import DictDecoderTest
from dftools.tests.utils.json_loadable_simple import DfJsonLoadableSimpleTest
from dftools.tests.utils.json_loadable_complex import DfJsonLoadableComplexTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(DictDecoderTest('test_check_valid_dict_valid'))
    suite.addTest(DictDecoderTest('test_check_valid_dict_error_non_authorized'))
    suite.addTest(DictDecoderTest('test_check_valid_dict_error_mandatory_missing'))
    suite.addTest(DfJsonLoadableSimpleTest('test_get_dict_decoder_info'))
    suite.addTest(DfJsonLoadableSimpleTest('test_from_dict'))
    suite.addTest(DfJsonLoadableComplexTest('test_from_dict'))
    return suite

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
