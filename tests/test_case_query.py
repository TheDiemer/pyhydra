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
    def test_case_query(self):
        # status=Waiting%20on%20Red%20Hat%2CWaiting%20on%20Customer&fields=caseNumber,status,subject,createdDate,bugzillaNumber
        r = self.hydra.query_cases(status=["Waiting on Red Hat" ,"Waiting on Customer"],
                fields=['caseNumber','status','subject','createdDate','bugzillaNumber'],
                accounts=['551325'])
        print(json.dumps(r,sort_keys=True, indent=INDENT))
    

if __name__ == '__main__':
    unittest.main()
