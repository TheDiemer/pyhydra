import unittest
import configparser
import json
import os

from hydra import hydra

DEBUG = os.getenv("DEBUG_TESTING", False)
CASE_NUMBER = os.getenv("DEBUG_CASE_NUMBER", '02486049')
INDENT = os.getenv("DEBUG_INDENT_NUMBER", 4)

class TestComments(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read('tests/test_config.cfg')

        self.hydra = hydra.hydra_api(username=config.get('hydra', 'username'),
                password=config.get('hydra', 'password'))


    def test_comment_put(self):
        # Case number: 02486049, 
        r = self.hydra.put_case_comment(CASE_NUMBER)


if __name__ == '__main__':
    unittest.main()
