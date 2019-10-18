import unittest
import configparser
import json
import os

from hydra import hydra

DEBUG = os.getenv("DEBUG_TESTING", False)
INDENT = os.getenv("DEBUG_INDENT_NUMBER", 4)


class TestCasesQuery(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read('tests/test_config.cfg')

        self.hydra = hydra.hydra_api(username=config.get('hydra', 'username'),
                password=config.get('hydra', 'password'))


    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_case_create(self):
        r = self.hydra.create_case(account_number='540155', severity="4 (Low)", subject="pyhydra test case",
            description="Test Case Please Delete", 
            product="OpenShift Container Platform", version="3.11")
        print(json.dumps(r,sort_keys=True, indent=INDENT))


if __name__ == '__main__':
    unittest.main()
