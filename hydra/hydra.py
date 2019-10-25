#!/bin/python

import requests
from concurrent.futures import ThreadPoolExecutor

class hydra_api:


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


    # TODO: Consider refactoring this (next 3 methods) back to __call_api,
    #        __call_api should take in the 'method' to run (and execute that).
    def __get_api(self, endpoint, parameters=None):
        authentication=(self.username, self.password)

        r = requests.get("{}/{}".format(self.base_api_uri, endpoint),
                params=parameters, auth=authentication,
                verify=self.ca_certificate_path)
        if r.status_code == 204:
            return []
        if r.status_code != 200:
            raise Exception('''looking up infomation from: {}\n
                    Error Code: {}'''.format(endpoint, r.status_code))

        return r.json()


    def __put_api(self, endpoint, parameters=None, payload=None):
        authentication=(self.username, self.password)

        r = requests.put("{}/{}".format(self.base_api_uri, endpoint),
                params=parameters, auth=authentication, json=payload,
                verify=self.ca_certificate_path)
        if r.status_code != 200:
            raise Exception('''Putting information to '{}' failed.\n
                    Error Code: {}'''.format(endpoint, r.status_code))


    def __post_api(self, endpoint, parameters=None, payload=None):
        authentication=(self.username, self.password)

        r = requests.post("{}/{}".format(self.base_api_uri, endpoint),
                params=parameters, auth=authentication, json=payload,
                verify=self.ca_certificate_path)
        if r.status_code != 200:
            print(r.text)
            raise Exception('''Posting information to '{}' failed.\n
                    Error Code: {}'''.format(endpoint, r.status_code))

        return r.json()


    def __del_api(self, endpoint, parameters=None, payload=None):
        authentication=(self.username, self.password)

        r = requests.delete("{}/{}".format(self.base_api_uri, endpoint),
                params=parameters, auth=authentication, json=payload,
                verify=self.ca_certificate_path)
        if r.status_code != 200:
            print(r.text)
            raise Exception('''Deleting information from '{}' failed.\n
                    Error Code: {}'''.format(endpoint, r.status_code))
        try:
            response = r.json()
        except:
            response = r.text
        if response == '': response = 'Deleting information from "{}" succeeded.'.format(endpoint)
        return response


    ### Account Functions
    def get_account_details(self, account_number):
        return self.__get_api('accounts/{}'.format(account_number))


    def get_account_contacts(self, account_number):
        return self.__get_api('accounts/{}/contacts'.format(account_number))


    def get_account_associates(self, account_number):
        return self.__get_api('accounts/{}/associates'.format(account_number))


    def get_account_entitlements(self, account_number):
        product = 'your_api_is_broken'
        endpoint = "entitlements/account/{}/?product={}&showAll=true".format(
                account_number, product)

        ## The data returned from entitlements is too much (filtered return)
        return [
                {'name': e['name'], 'startDate': e['startDate'],
                'endDate': e['endDate'], 'sku': e['externalProductCode'],
                'quantity': e['quantity'], 'supportLevel': e['supportLevel']}
                for e in self.__get_api(endpoint)
                ]


    def get_account_notes(self, account_number):
        ## The data returned from notes is too much (filtered return)
        return [
                {'type': n['type'], 'subject': n['subject'],
                    'active': n['isRetired'], 'note': n['body'], 'id': n['id']}
                for n in self.__get_api(
                    'accounts/{}/notes'.format(account_number))
                ]


    def post_account_notes(self, account_number, body="", intendedReviewDate=None, needsReview=False, retired=False, subject="", noteType="Key Notes"):
        content = {'note':{}}
        content['note'].update({'body': body})
        if intendedReviewDate: content['note'].update({'intendedReviewDate':intendedReviewDate})
        content['note'].update({'needsReview':needsReview})
        content['note'].update({'retired':retired})
        content['note'].update({'type':noteType})
        content['note'].update({'subject':subject})

        return self.__post_api('accounts/{}/notes'.format(account_number), payload=content)


    def del_account_notes(self, account_number, noteID):
        content = {'note':{'id':noteID}}
        return self.__del_api('accounts/{}/notes'.format(account_number), payload=content)

    ### Case Functions
    def get_case_details(self, case_number):
        return self.__get_api('cases/{}'.format(case_number))


    def get_account_number(self, case_number):
        case = self.get_case_details(case_number)
        return case['accountNumber']


    def get_case_bugs(self, case_number):
        ## The data returned from bugs is too much (filtered return)
        return [
                {'key': b['bugzillaNumber'], 'url': b['bugzillaLink']}
                for b in self.__get_api('cases/{}/bugs'.format(case_number))
                ]


    def get_case_jiras(self, case_number):
        ## The data returned from jiras is too much (filtered return)
        return [
                {'key': j['resourceKey'], 'url': j['resourceURL']}
                for j in self.__get_api('cases/{}/jiras'.format(case_number))
                ]


    def get_case_trackers(self, case_number):
        ## The data returned from trackers is too much (filtered return)
        return [
                {'key': t['resourceKey'], 'url': t['resourceURL'],
                    'system': t['system'], 'instance': t['systemInstance']}
                for t in self.__get_api('cases/{}/jiras'.format(case_number))
                ]


    def get_case_resources(self, case_number):
        ## The data returned from resources is too much (filtered return)
        return [
            {'key': r['resourceId'], 'url': r['resourceViewURI'],
                'title': r['title'], 'type': r['resourceType'],
                'exact': r['isExact']}
            for r in self.__get_api('cases/{}/resources'.format(case_number))
            ]


    def get_case_counts(self, case_number):
        return self.__get_api('cases/{}/count'.format(case_number))


    def get_case_contacts(self, case_number):
        return self.__get_api('cases/{}/contacts'.format(case_number))


    def get_case_associates(self, case_number):
        data = []

        ## The data returned from users is too much (filtered return)
        def get_case_user_details(associate):
            user = self.__get_api('users/{}'.format(associate['OwnerId']))
            a_data.append(
                {'role': associate['role'], 'name': user['fullName'],
                    'title': user['fullTitle'], 'irc_nick': user['ircNick'],
                    'ooo': user['outOfOffice'], 'phone': user['phone'],
                    'email': user['email'], 'region': user['superRegion']}
                )

        associates = self.__get_api('cases/{}/associates'.format(case_number))
        self.thread_pool.map(get_case_user_details, associates, chunksize=1)

        return data


    def get_case_attachments(self, case_number):
        # This is a non documented api
        return self.__get_api('cases/{}/attachments'.format(case_number))


    def create_case(self, account_number=None, severity=None, subject=None,
            description=None, product=None, version=None, sbrGroup=None):

        body = {}

        if account_number: body.update({'accountNumber': account_number})
        if severity: body.update({'severity': severity})
        if subject: body.update({'subject': subject})
        if description: body.update({'description': description})
        if product: body.update({'product': product})
        if version: body.update({'version': version})
        if sbrGroup: body.update({'sbrGroup': sbrGroup})

        return self.__post_api('cases/', payload=body)


    def put_case_comment(self, case_number, comment="",
            doNotChangeSBT=False, isPublic=True):
        return self.__put_api('/cases/comments',
                payload={"caseNumber":case_number, "commentBody":comment,
                    "doNotChangeSBT": doNotChangeSBT, "isPublic": isPublic})


    def query_cases(self, status=[], fields=[], accounts=[], cases=[],
           sbrGroups=[], needsNewOwner=None, severity=[], serviceLevel=[],
           fts=None, ownerSsousername=[]):
       query_params = {}

       if status: query_params.update({'status': ", ".join(status)})
       if fields: query_params.update({'fields': ", ".join(fields)})
       if accounts: query_params.update({'accounts': ", ".join(accounts)})
       if cases: query_params.update({'cases': ", ".join(cases)})
       if sbrGroups: query_params.update({'sbrGroups': ", ".join(sbrGroups)})
       if needsNewOwner: query_params.update({'needsNewOwner': needsNewOwner})
       if severity: query_params.update({'severity': ", ".join(severity)})
       if serviceLevel:
           query_params.update({'serviceLevel': ", ".join(serviceLevel)})
       if fts: query_params.update({'fts': fts})
       if ownerSsousername:
           query_params.update({'ownerSsousername': ", ".join(ownerSsousername)})

       return self.__get_api('cases/', parameters=query_params)
