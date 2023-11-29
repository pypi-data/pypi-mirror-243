import unittest

from dftools.events import LoggerManager, EventLevel

from dftools.tests.core.structure.template.structure_template import StructureTemplateTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(StructureTemplateTest('test_create_structure'))
    return suite

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
