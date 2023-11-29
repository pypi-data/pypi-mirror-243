import unittest
import logging

from dftools.events.base import EventLevel, BaseEvent, StandardInfoEvent

class DfDummyLogger(logging.Logger):
    def __init__(self, name: str, level = 0) -> None:
        super().__init__(name, level)
    
    def log_event(self, event : BaseEvent):
        if event.level_tag() == EventLevel.INFO:
            self.info(msg=event.message())
    
    def log_event_args(self, event : BaseEvent, *args):
        self._log()
        if event.level_tag() == EventLevel.INFO:
            self.info(msg=event.message())

class BaseEventTest(unittest.TestCase):
    def test_log_of_standard_info_event(self):
        logging.setLoggerClass(DfDummyLogger)
        logging.basicConfig(level=logging.INFO, format = '[%(asctime)s] [%(levelname)s] - %(message)s')
        logger = logging.getLogger('BaseEventTest')
        event = StandardInfoEvent(toto="toto_desc")
        #logger.info(msg = event.message())
        logger.log_event(event)

if __name__ == '__main__':
    unittest.main()
