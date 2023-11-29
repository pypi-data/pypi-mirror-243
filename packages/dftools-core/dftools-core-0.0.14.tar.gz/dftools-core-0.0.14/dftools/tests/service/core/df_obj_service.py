import unittest
import os

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.service.core.df_obj_service import DFObjProviderService
from dftools.tests.configurations import TEST_MODEL_ROOT_DIR


class DFObjProviderServiceTest(unittest.TestCase):

    def test_load_objects_from_files(self):
        log_event_default(StdTestEvent("DF Obj Provider Service - Load Objects From Files - Start"))
        provider = DFObjProviderService(system_folder=os.path.join(TEST_MODEL_ROOT_DIR, 'sample_1'), user_folder=None)
        provider.load_objects_from_files()
        self.assertEqual(['structure_template', 'data_flow_def_template'], provider.get_available_object_types())
        self.assertEqual(1, len(provider.get_data_flow_def_templates()))
        self.assertEqual(4, len(provider.get_structure_templates()))
        log_event_default(StdTestEvent("DF Obj Provider Service - Load Objects From Files - Succeeded"))
    
if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
