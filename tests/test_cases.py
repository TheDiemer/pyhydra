import unittest
import configparser
import json
import os

from hydra import hydra

DEBUG = os.getenv("DEBUG_TESTING", False)
CASE_NUMBER = os.getenv("DEBUG_CASE_NUMBER", '02481396')
INDENT = os.getenv("DEBUG_INDENT_NUMBER", 4)


class TestCases(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read('tests/test_config.cfg')

        self.hydra = hydra.hydra_api(username=config.get('hydra', 'username'),
                password=config.get('hydra', 'password'))


    def test_case_account_number(self):
        # Case Number and Account Number are 'string's. 
        # Case Number: 02481396 Account Number: 6119113
        r = self.hydra.get_case_details(CASE_NUMBER)
        self.assertEqual(r['accountNumber'], '6119113')


    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_case_details(self):
        r = self.hydra.get_case_details(CASE_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
    

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_case_bugs(self):
        r = self.hydra.get_case_bugs(CASE_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))


    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_case_jiras(self):
        r = self.hydra.get_case_jiras(CASE_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
    

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_case_trackers(self):
        r = self.hydra.get_case_trackers(CASE_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
    

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_case_resources(self):
        r = self.hydra.get_case_resources(CASE_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
    

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_case_counts(self):
        r = self.hydra.get_case_counts(CASE_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
    

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_case_contacts(self):
        r = self.hydra.get_case_contacts(CASE_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
    

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_case_associates(self):
        r = self.hydra.get_case_associates(CASE_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
    

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_case_attachments(self):
        r = self.hydra.get_case_attachments(CASE_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))


if __name__ == '__main__':
    unittest.main()
