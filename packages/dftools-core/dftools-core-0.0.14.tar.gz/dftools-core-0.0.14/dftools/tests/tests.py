import unittest

from dftools.events import LoggerManager, EventLevel

from dftools.tests.core.structure.core.structure_core_suite import suite as structure_core_suite
from dftools.tests.core.structure.adapter.structure_adapter_suite import suite as structure_adapter_suite
from dftools.tests.core.structure.check.structure_check_suite import suite as structure_check_suite
from dftools.tests.core.structure.compare.compare_suite import suite as structure_compare_suite
from dftools.tests.core.structure.api.structure_api_suite import suite as structure_api_suite
from dftools.tests.core.structure.template.structure_template_suite import suite as structure_template_suite

from dftools.tests.service.core.service_core_suite import suite as service_core_suite

from dftools.tests.utils.utils_test_suite import suite as utils_test_suite


def suite():
    suite = unittest.TestSuite()
    suite.addTests([test for test in structure_core_suite()])
    suite.addTests([test for test in structure_adapter_suite()])
    suite.addTests([test for test in structure_check_suite()])
    suite.addTests([test for test in structure_compare_suite()])
    suite.addTests([test for test in structure_api_suite()])
    suite.addTests([test for test in structure_template_suite()])
    suite.addTests([test for test in service_core_suite()])
    suite.addTests([test for test in utils_test_suite()])
    return suite


if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    runner = unittest.TextTestRunner()
    runner.run(suite())
