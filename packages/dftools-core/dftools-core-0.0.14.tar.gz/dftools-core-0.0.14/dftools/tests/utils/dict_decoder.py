import unittest

from dftools.events import LoggerManager, log_event_default, StandardTestEvent as StdTestEvent, EventLevel
from dftools.utils.dict_decoder import DictDecoder
from dftools.exceptions import DfJSONValidationException

class DictDecoderTest(unittest.TestCase):
    def test_check_valid_dict_valid(self):
        log_event_default(StdTestEvent("Dict Decoder - Check Valid Dict / Valid - Start"))
        dict_decoder = DictDecoder("Dummy", ["id"], ["id", "name", "desc"], {})
        input_dict = {"id": 1, "name": 'test1', "desc" : "desc1"}
        valid_dict_check = dict_decoder._check_valid_dict(input_dict)
        self.assertTrue(valid_dict_check)
        log_event_default(StdTestEvent("Dict Decoder - Check Valid Dict / Valid - Succeeded"))
    
    def test_check_valid_dict_error_non_authorized(self):
        log_event_default(StdTestEvent("Dict Decoder - Check Valid Dict / Error Non Authorized - Start"))
        dict_decoder = DictDecoder("Dummy", ["id"], ["id", "name", "desc"], {})
        input_dict = {"id": 1, "name": 'test1', "desc_2" : "desc1"}
        
        with self.assertRaises(DfJSONValidationException):
            dict_decoder._check_valid_dict(input_dict)
        
        log_event_default(StdTestEvent("Dict Decoder - Check Valid Dict / Error Non Authorized - Succeeded"))
    
    def test_check_valid_dict_error_mandatory_missing(self):
        log_event_default(StdTestEvent("Dict Decoder - Check Valid Dict / Error Mandatory Missing - Start"))
        dict_decoder = DictDecoder("Dummy", ["id"], ["id", "name", "desc"], {})
        input_dict = {"name": 'test1', "desc" : "desc1"}
        with self.assertRaises(DfJSONValidationException):
            dict_decoder._check_valid_dict(input_dict)
    
        log_event_default(StdTestEvent("Dict Decoder - Check Valid Dict / Error Mandatory Missing - Succeeded"))

if __name__ == '__main__':
    LoggerManager(level=EventLevel.TEST)
    unittest.main()
