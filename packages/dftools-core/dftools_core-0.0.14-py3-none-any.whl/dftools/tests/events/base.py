from logging import _Level
import unittest
import logging

from dftools.events.base import StandardInfoEvent

class BaseEventTest(unittest.TestCase):
    def test_log_of_standard_info_event(self):
        logging.basicConfig(level=logging.INFO, format = '[%(asctime)s] [%(levelname)s] - %(message)s')
        logger = logging.getLogger('BaseEventTest')
        event = StandardInfoEvent(toto="toto_desc")
        logger.info(msg = event.message())
        

if __name__ == '__main__':
    unittest.main()
