import os

from dftools.service.core.df_obj_service import DFObjProviderService
from dftools.tests.configurations import TEST_MODEL_ROOT_DIR

DF_OBJ_PROVIDER = DFObjProviderService(system_folder=os.path.join(TEST_MODEL_ROOT_DIR, 'sample_1'), user_folder=None)
DF_OBJ_PROVIDER.load_objects_from_files()