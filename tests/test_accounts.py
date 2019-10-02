import unittest
import configparser
import json
import os

from hydra import hydra

DEBUG = os.getenv("DEBUG_TESTING", False)
ACCOUNT_NUMBER = os.getenv("DEBUG_ACCOUNT_NUMBER", 551325)
INDENT = os.getenv("DEBUG_INDENT_NUMBER", 4)


class TestAccounts(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read('tests/test_config.cfg')

        self.hydra = hydra.hydra_api(username=config.get('hydra', 'username'),
                password=config.get('hydra', 'password'))


    def test_account_name(self):
        # Account Number: 551325 Name: 'EMIRATES NBD BANK (P.J.S.C)'
        r = self.hydra.get_account_details(ACCOUNT_NUMBER)
        self.assertEqual(r['name'], "EMIRATES NBD BANK (P.J.S.C)")
   
    
    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_account_details(self):
        # Account Number: 551325 Name: 'EMIRATES NBD BANK (P.J.S.C)'
        r = self.hydra.get_account_details(ACCOUNT_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
    

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_account_contacts(self):
        # Account Number: 551325 Name: 'EMIRATES NBD BANK (P.J.S.C)'
        r = self.hydra.get_account_contacts(ACCOUNT_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
   

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_account_associates(self):
        # Account Number: 551325 Name: 'EMIRATES NBD BANK (P.J.S.C)'
        r = self.hydra.get_account_associates(ACCOUNT_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
   

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_account_entitlements(self):
        # Account Number: 551325 Name: 'EMIRATES NBD BANK (P.J.S.C)'
        r = self.hydra.get_account_entitlements(ACCOUNT_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))
    

    @unittest.skipUnless(DEBUG, "skipping manuall debugging test")
    def test_account_notes(self):
        # Account Number: 551325 Name: 'EMIRATES NBD BANK (P.J.S.C)'
        r = self.hydra.get_account_notes(ACCOUNT_NUMBER)
        print(json.dumps(r,sort_keys=True, indent=INDENT))


if __name__ == '__main__':
    unittest.main()
