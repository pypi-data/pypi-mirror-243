import unittest

from dftools.events import LoggerManager, EventLevel

from dftools.tests.func_tests.core.structure.template.structure_template_suite import suite as structure_template_suite

def suite() : 
    suite = unittest.TestSuite()
    suite.addTests([test for test in structure_template_suite()])
    return suite

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
