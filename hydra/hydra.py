#!/bin/python

import requests
from concurrent.futures import ThreadPoolExecutor

class hydra_api:
    """."""
    def __init__(self, api="https://access.redhat.com/hydra/rest/", 
            ca_path="/etc/pki/tls/certs/ca-bundle.crt", username=None,
            password=None):
        if username is None or password is None:
            raise Exception("Username or Password were not supplied.")

        self.base_api_uri = api
        self.username = username
        self.password = password

        self.ca_certificate_path = ca_path
        if ca_path == False: # Used to Disable SSL warning (from each api call)
            requests.packages.urllib3.disable_warnings()

        self.thread_pool = ThreadPoolExecutor(4)

    def __del__(self):
        self.thread_pool.shutdown(wait=True)


    def __call_api(self, endpoint):
        authentication=(self.username, self.password)

        r = requests.get("{}/{}".format(self.base_api_uri, endpoint), 
                auth=authentication, verify=self.ca_certificate_path)
        if r.status_code == 204:
            return []
        if r.status_code != 200:
            raise Exception('''looking up infomation from: {}\n
                    Error Code: {}'''.format(endpoint, r.status_code))

        return r.json()

    ### Account Functions
    def get_account_details(self, account_number):
        return self.__call_api('accounts/{}'.format(account_number))

    def get_account_contacts(self, account_number):
        return self.__call_api('accounts/{}/contacts'.format(account_number))


    def get_account_associates(self, account_number):
        return self.__call_api('accounts/{}/associates'.format(account_number))

    
    def get_account_entitlements(self, account_number):
        product = 'your_api_is_broken'
        endpoint = "entitlements/account/{}/?product={}&showAll=true".format(
                account_number, product)

        ## The data returned from entitlements is too much (filtered return)
        return [
                {'name': e['name'], 'startDate': e['startDate'],
                'endDate': e['endDate'], 'sku': e['externalProductCode'],
                'quantity': e['quantity'], 'supportLevel': e['supportLevel']} 
                for e in self.__call_api(endpoint)
                ]


    def get_account_notes(self, account_number):
        ## The data returned from notes is too much (filtered return)
        return [
                {'type': n['type'], 'subject': n['subject'],
                    'active': n['isRetired'], 'note': n['body']}
                for n in self.__call_api(
                    'accounts/{}/notes'.format(account_number))
                ]


    ### Case Functions
    def get_case_details(self, case_number):
        return self.__call_api('cases/{}'.format(case_number))


    def get_account_number(self, case_number):
        case = self.get_case(case_number)
        return case['accountNumber']


    def get_case_bugs(self, case_number):
        ## The data returned from bugs is too much (filtered return)
        return [
                {'key': b['bugzillaNumber'], 'url': b['bugzillaLink']} 
                for b in self.__call_api('cases/{}/bugs'.format(case_number))
                ]


    def get_case_jiras(self, case_number):
        ## The data returned from jiras is too much (filtered return)
        return [
                {'key': j['resourceKey'], 'url': j['resourceURL']} 
                for j in self.__call_api('cases/{}/jiras'.format(case_number))
                ]


    def get_case_trackers(self, case_number):
        ## The data returned from trackers is too much (filtered return)
        return [
                {'key': t['resourceKey'], 'url': t['resourceURL'], 
                    'system': t['system'], 'instance': t['systemInstance']} 
                for t in self.__call_api('cases/{}/jiras'.format(case_number))
                ]


    def get_case_resources(self, case_number):
        ## The data returned from resources is too much (filtered return)
        return [
            {'key': r['resourceId'], 'url': r['resourceViewURI'], 
                'title': r['title'], 'type': r['resourceType'], 
                'exact': r['isExact']} 
            for r in self.__call_api('cases/{}/resources'.format(case_number))
            ]


    def get_case_counts(self, case_number):
        return self.__call_api('cases/{}/count'.format(case_number))


    def get_case_contacts(self, case_number):
        return self.__call_api('cases/{}/contacts'.format(case_number))
    

    def get_case_associates(self, case_number):
        data = []

        ## The data returned from users is too much (filtered return)
        def get_case_user_details(associate):
            user = self.__call_api('users/{}'.format(associate['OwnerId']))
            a_data.append(
                {'role': associate['role'], 'name': user['fullName'], 
                    'title': user['fullTitle'], 'irc_nick': user['ircNick'], 
                    'ooo': user['outOfOffice'], 'phone': user['phone'], 
                    'email': user['email'], 'region': user['superRegion']}
                )

        associates = self.__call_api('cases/{}/associates'.format(case_number))
        self.thread_pool.map(get_case_user_details, associates, chunksize=1)

        return data

    
    def get_case_attachments(self, case_number):
        # This is a non documented api
        return self.__call_api('cases/{}/attachments'.format(case_number))

