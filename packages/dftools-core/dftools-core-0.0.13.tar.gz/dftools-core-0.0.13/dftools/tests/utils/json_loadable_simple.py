import unittest
from dataclasses import dataclass

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.utils.dict_decoder import DictDecoderInfo
from dftools.utils.json_loadable import DfJsonLoadable

@dataclass()
class DummyClass(DfJsonLoadable):
    
    id: int
    name: str
    desc: str

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["id"], ["id", "name", "desc"], {})
    
    @classmethod
    def _default_instance(cls):
        return cls(id=1, name='', desc='')

class DfJsonLoadableSimpleTest(unittest.TestCase):
    def test_get_dict_decoder_info(self):
        log_event_default(StdTestEvent("Json Loadable / Simple - Get Dict Decoder Info - Start"))
        dict_decoder_info = DummyClass._get_dict_decoder_info()
        self.assertEqual(DictDecoderInfo, type(dict_decoder_info))
        log_event_default(StdTestEvent("Json Loadable / Simple - Get Dict Decoder Info - Succeeded"))

    def test_from_dict(self):
        log_event_default(StdTestEvent("Json Loadable / Simple - From Dict - Start"))
        input_dict = {"id": 1, "name": 'test1', "desc" : "desc1"}
        dummy_class_inst = DummyClass.from_dict(input_dict)
        self.assertIsInstance(dummy_class_inst, DummyClass)
        self.assertEqual(dummy_class_inst.id, 1)
        self.assertEqual(dummy_class_inst.name, "test1")
        self.assertEqual(dummy_class_inst.id, 1)
        log_event_default(StdTestEvent("Json Loadable / Simple - From Dict - Succeeded"))

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
