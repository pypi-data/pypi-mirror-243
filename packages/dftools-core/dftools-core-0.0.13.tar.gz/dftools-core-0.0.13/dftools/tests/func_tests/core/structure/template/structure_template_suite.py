import unittest

from dftools.events import LoggerManager, EventLevel

from dftools.tests.func_tests.core.structure.template.structure_template import StructureTemplateFuncTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(StructureTemplateFuncTest('test_template_From_Source_FF_STG'))
    suite.addTest(StructureTemplateFuncTest('test_template_From_Source_FF_DTL_RAW'))
    suite.addTest(StructureTemplateFuncTest('test_template_From_Source_FF_DTL_RAW_With_Snapshot'))
    suite.addTest(StructureTemplateFuncTest('test_template_DTL_Curated_From_Raw'))
    return suite

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
