import unittest

from dftools.events import LoggerManager, EventLevel
from dftools.tests.service.core.df_obj_service import DFObjProviderServiceTest

def suite():
    suite = unittest.TestSuite()
    suite.addTest(DFObjProviderServiceTest('test_load_objects_from_files'))
    return suite

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
