import unittest
from dataclasses import dataclass

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.utils.dict_decoder import DictDecoderInfo
from dftools.utils.json_loadable import DfJsonLoadable

@dataclass
class DummyClass(DfJsonLoadable):
    
    id: int
    name: str
    desc: str

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["id"], ["id", "name", "desc"], {})

@dataclass
class DummyComplexClass(DfJsonLoadable):
    
    key: DummyClass
    name: str
    desc: str

    def _get_dict_decoder_info() -> DictDecoderInfo:
        return DictDecoderInfo(["key"], ["key", "name", "desc"], {"key" : DummyClass})

class DfJsonLoadableComplexTest(unittest.TestCase):
    def test_from_dict(self):
        log_event_default(StdTestEvent("Json Loadable / Complex - From Dict - Start"))
        input_dict = {"key": {"id": 1, "name": 'test1', "desc" : "desc1"}, "name": 'complex_name1', "desc" : "complex_desc1"}
        dummy_class_inst : DummyComplexClass = DummyComplexClass.from_dict(input_dict)
        self.assertIsNotNone(dummy_class_inst.key)
        self.assertEqual(dummy_class_inst.key.id, 1)
        self.assertEqual(dummy_class_inst.key.name, "test1")
        self.assertEqual(dummy_class_inst.key.desc, "desc1")
        self.assertEqual(dummy_class_inst.name, "complex_name1")
        self.assertEqual(dummy_class_inst.desc, "complex_desc1")
        log_event_default(StdTestEvent("Json Loadable / Complex - From Dict - Succeeded"))

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
