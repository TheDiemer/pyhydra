#!/bin/python

import requests, warnings, functools, deprecation
from concurrent.futures import ThreadPoolExecutor, as_completed


class hydra_api:
    def __init__(
        self,
        api="https://access.redhat.com/hydra/rest/",
        ca_path="/etc/pki/tls/certs/ca-bundle.crt",
        username=None,
        password=None,
    ):
        if username is None or password is None:
            raise Exception("Username or Password were not supplied.")

        self.base_api_uri = api
        self.username = username
        self.password = password

        self.ca_certificate_path = ca_path
        if ca_path == False:  # Used to Disable SSL warning (from each api call)
            requests.packages.urllib3.disable_warnings()

        self.thread_pool = ThreadPoolExecutor(4)
        self.thread_pool = ThreadPoolExecutor(4)

    def __del__(self):
        self.thread_pool.shutdown(wait=True)

    def __pretty_print_REQ(self, req):
        print(
            "{}\n{}\n{}\n\n{}".format(
                "-----------BEGIN REQUEST-----------",
                req.method + " " + req.url,
                "\n".join("{}: {}".format(k, v) for k, v in req.headers.items()),
                req.body,
            )
        )

    # TODO: Consider refactoring this (next 3 methods) back to __call_api,
    #        __call_api should take in the 'method' to run (and execute that).
    def __get_api(self, endpoint, parameters=None, headers=None):
        authentication = (self.username, self.password)

        ## NOTE: This is how you debug a http request.
        # bare = requests.Request('GET', "{}/{}".format(self.base_api_uri, endpoint),
        #         params=parameters, headers=headers, auth=authentication)
        # prepared = bare.prepare()
        # self.__pretty_print_REQ(prepared)
        # s = requests.Session()
        # s.verify = self.ca_certificate_path
        # r = s.send(prepared)

        # NOTE: Comment this out; if you use the block above.
        try:
            r = requests.get(
                "{}/{}".format(self.base_api_uri, endpoint),
                params=parameters,
                headers=headers,
                auth=authentication,
                verify=self.ca_certificate_path,
            )
            if r.status_code == 204:
                return []
            if r.status_code != 200:
                raise Exception(
                    """looking up infomation from: {}\n
                        Error Code: {}""".format(
                        endpoint, r.status_code
                    )
                )
            try:
                return r.json()
            except:
                raise Exception(
                    """looking up information from: {}\n
                    Error returning json""".format(
                        endpoint
                    )
                )
        except Exception:
            raise Exception(
                """looking up information from: {}\n
                Error during request call""".format(
                    endpoint
                )
            )

        return r.json()

    def __put_api(self, endpoint, parameters=None, payload=None):
        authentication = (self.username, self.password)

        r = requests.put(
            "{}/{}".format(self.base_api_uri, endpoint),
            params=parameters,
            auth=authentication,
            json=payload,
            verify=self.ca_certificate_path,
        )
        if r.status_code != 200:
            raise Exception(
                """Putting information to '{}' failed.\n
                    Error Code: {}""".format(
                    endpoint, r.status_code
                )
            )

    def __post_api(self, endpoint, parameters=None, payload=None):
        authentication = (self.username, self.password)

        r = requests.post(
            "{}/{}".format(self.base_api_uri, endpoint),
            params=parameters,
            auth=authentication,
            json=payload,
            verify=self.ca_certificate_path,
        )
        if r.status_code != 200:
            print(r.text)
            raise Exception(
                """Posting information to '{}' failed.\n
                    Error Code: {}""".format(
                    endpoint, r.status_code
                )
            )

        return r.json()

    def __del_api(self, endpoint, parameters=None, payload=None):
        authentication = (self.username, self.password)

        r = requests.delete(
            "{}/{}".format(self.base_api_uri, endpoint),
            params=parameters,
            auth=authentication,
            json=payload,
            verify=self.ca_certificate_path,
        )
        if r.status_code != 200:
            print(r.text)
            raise Exception(
                """Deleting information from '{}' failed.\n
                    Error Code: {}""".format(
                    endpoint, r.status_code
                )
            )
        try:
            response = r.json()
        except:
            response = r.text
        if response == "":
            response = 'Deleting information from "{}" succeeded.'.format(endpoint)
        return response

    ### Account Functions
    def get_account_details(self, account_number):
        return self.__get_api("accounts/{}".format(account_number))

    def get_account_contacts(self, account_number):
        return self.__get_api("accounts/{}/contacts".format(account_number))

    def get_account_associates(self, account_number):
        return self.__get_api("accounts/{}/associates".format(account_number))

    def get_account_entitlements(self, account_number):
        product = "your_api_is_broken"
        endpoint = "entitlements/account/{}/?product={}&showAll=true".format(
            account_number, product
        )

        ## The data returned from entitlements is too much (filtered return)
        return [
            {
                "name": e.get("name", "Unknown"),
                "startDate": e.get("startDate", None),
                "endDate": e.get("endDate", None),
                "sku": e.get("externalProductCode", None),
                "quantity": e.get("quantity", None),
                "supportLevel": e.get("supportLevel", None),
            }
            for e in self.__get_api(endpoint)
        ]

    def get_account_notes(self, account_number):
        ## The data returned from notes is too much (filtered return)
        return [
            {
                "type": n["type"],
                "subject": n["subject"],
                "active": n["isRetired"],
                "note": n["body"],
                "id": n["id"],
            }
            for n in self.__get_api("accounts/{}/notes".format(account_number))
        ]

    def post_account_notes(
        self,
        account_number,
        body="",
        intendedReviewDate=None,
        needsReview=False,
        retired=False,
        subject="",
        noteType="Key Notes",
    ):
        content = {"note": {}}
        content["note"].update({"body": body})
        if intendedReviewDate:
            content["note"].update({"intendedReviewDate": intendedReviewDate})
        content["note"].update({"needsReview": needsReview})
        content["note"].update({"retired": retired})
        content["note"].update({"type": noteType})
        content["note"].update({"subject": subject})

        return self.__post_api(
            "accounts/{}/notes".format(account_number), payload=content
        )

    def del_account_notes(self, account_number, noteID):
        content = {"note": {"id": noteID}}
        return self.__del_api(
            "accounts/{}/notes".format(account_number), payload=content
        )

    ### Case Functions
    def get_case_details(self, case_number):
        return self.__get_api("cases/{}".format(case_number))

    def get_account_number(self, case_number):
        case = self.get_case_details(case_number)
        return case["accountNumber"]

    def get_case_bugs(self, case_number):
        ## The data returned from bugs is too much (filtered return)
        return [
            {"key": b["bugzillaNumber"], "url": b["bugzillaLink"]}
            for b in self.__get_api("cases/{}/bugs".format(case_number))
        ]

    def get_case_jiras(self, case_number):
        ## The data returned from jiras is too much (filtered return)
        return [{"key": j.get("resourceKey", ""), "url": j.get("resourceURL", "")}
                    for j in self.__get_api("cases/{}/jiras".format(case_number))]

    def get_case_jira_count(self, case_number):
        return self.__get_api("cases/{}/count/jiras".format(case_number))

    def get_case_trackers(self, case_number):
        ## The data returned from trackers is too much (filtered return)
        return [
            {
                "key": t["resourceKey"],
                "url": t["resourceURL"],
                "system": t["system"],
                "instance": t["systemInstance"],
            }
            for t in self.__get_api("cases/{}/externaltrackers".format(case_number))
        ]

    def get_case_resources(self, case_number):
        ## The data returned from resources is too much (filtered return)
        return [
            {
                "key": r["resourceId"],
                "url": r["resourceViewURI"],
                "title": r["title"],
                "type": r["resourceType"],
                "exact": r["isExact"],
            }
            for r in self.__get_api("cases/{}/resources".format(case_number))
        ]

    def get_case_counts(self, case_number):
        return self.__get_api("cases/{}/count".format(case_number))

    def get_case_contacts(self, case_number):
        return self.__get_api("cases/{}/contacts".format(case_number))

    def get_case_comments(self, case_number):
        comment_data = []
        comments = self.__get_api("cases/{}/comments".format(case_number))
        for comment in comments:
            commenter_type = comment.get("createdByType", "None")

            if commenter_type == "Bug":  # TODO: Enhance this
                ### Skipping Comments from bugs and jira's (this seems to work)
                continue
            if "createdByContact" in comment:
                comment_data.append(
                    {
                        "create_date": comment.get("lastModifiedDateCustom"),
                        "commenter": comment.get("createdByContact").get(
                            "fullNameCustom"
                        ),
                        "commenter_region": comment.get("createdByContact").get(
                            "timezone"
                        ),
                        "commenter_email": comment.get("createdByContact").get("email"),
                        "comment_body": comment.get("commentBody"),
                        "isPublic": comment.get("isPublic"),
                        "isDraft": comment.get("isDraft"),
                        "isBreached": comment.get("inBreach"),
                    }
                )
            elif "createdByUser" in comment:
                comment_data.append(
                    {
                        "create_date": comment.get("lastModifiedDateCustom"),
                        "commenter": comment.get("createdByUser").get("name"),
                        "commenter_region": comment.get("createdByUser").get("region"),
                        "commenter_email": comment.get("createdByUser").get("email"),
                        "comment_body": comment.get("commentBody"),
                        "isPublic": comment.get("isPublic"),
                        "isDraft": comment.get("isDraft"),
                        "isBreached": comment.get("inBreach"),
                    }
                )
            else:
                pass  ## If this happens exiting this way is bad)
                # TODO: Fix this and thow an error!

        return comment_data

    def get_case_associates(self, case_number):

        # The data returned from users is too much (filtered return)
        def get_case_user_details(associate):
            user = self.__get_api("users/{}".format(associate["OwnerId"]))
            return {
                "role": associate.get("role"),
                "name": user.get("fullName"),
                "title": user.get("fullTitle"),
                "irc_nick": user.get("ircNick"),
                "ooo": user.get("outOfOffice"),
                "phone": user.get("phone"),
                "email": user.get("email"),
                "region": user.get("superRegion")
            }

        associates = self.__get_api("cases/{}/associates".format(case_number))

        data = []
        with ThreadPoolExecutor() as thread_executor:
            futures = [thread_executor.submit(get_case_user_details, a) for a in associates]

            for future in as_completed(futures):
                data.append(future.result())

        return data

    def get_case_attachments(self, case_number):
        # This is a non documented api
        return self.__get_api("cases/{}/attachments".format(case_number))

    def get_product_versions(self, product=None):
        return self.__get_api(
            "products/{}/versions".format("%20".join(product.split()))
        )

    def get_case_history(self, case_number, parameters={}):
        """Returns case history items.

        Note that each history item will not have the same field names, because each conveys a different
        history entry. For example, setting a new owner and closing a case are different events and will have
        correspondingly different fields.

        parameters may contain the following fields
            - fields: Case history fields.
            - limit: Max number of records to fetch.
            - orderBy: Field to order results by.
            - orderDirection: Defaults to ascending (asc), set to 'desc' for descending.
            - offsetValue: Last value from a prior result set by which to offset the current query
                            MUST SET orderBy TO A FIELD WITH UNIQUE VALUES TO GUARANTEE ALL RESULTS ARE RETURNED
            - offsetType: Type of offsetValue parameter. Defaults to string, set to 'double' for double values,
                            'int' for integer values, 'datetime' for dateTime values.
        """
        # Sanitize the input by only allowing valid field names and excluding fields where the value is None
        valid_parameter_names = ['fields', 'limit', 'orderBy', 'orderDirection', 'offsetValue', 'offsetType']
        params = {key: parameters[key] for key in valid_parameter_names if parameters.get(key, None)}
        return self.__get_api(f'cases/{case_number}/history', parameters=params)

    def get_case_remote_sessions(self, case_number, parameters={}):
        """Returns case Bomgar remote sessions.

        parameters may contain the following fields
            - fields: The remote session fields to include in the output.
            - limit: Max number of records to fetch.
        """
        # Sanitize the input by only allowing valid field names and excluding fields where the value is None
        valid_parameter_names = ['fields', 'limit']
        params = {key: parameters[key] for key in valid_parameter_names if parameters.get(key, None)}
        return self.__get_api(f'cases/{case_number}/remotesessions', parameters=params)

    def create_case(
        self,
        account_number=None,
        severity=None,
        subject=None,
        description=None,
        product=None,
        version=None,
        sbrGroup=None,
        caseLanguage=None,
        contact=None,
        clusterID=None,
    ):

        body = {}

        if account_number:
            body.update({"accountNumber": account_number})
        if severity:
            body.update({"severity": severity})
        if subject:
            body.update({"subject": subject})
        if description:
            body.update({"description": description})
        if product:
            body.update({"product": product})
        if version:
            body.update({"version": version})
        if sbrGroup:
            body.update({"sbrGroup": sbrGroup})
        if caseLanguage:
            body.update({"caseLanguage": caseLanguage})
        if contact:
            body.update({"contactSSOName": contact})
        if clusterID:
            body.update({"openshiftClusterID": clusterID})

        return self.__post_api("cases/", payload=body)

    def put_case_comment(
        self,
        case_number,
        comment="",
        doNotChangeSBT=False,
        isPublic=True,
        newStatus="",
        newInternalStatus="",
        nno=" ",
        newResolution="",
        newResolutionDescription="",
    ):
        payload = {
            "caseComment": {},
            "additionalData": {},
        }
        payload["caseComment"].update({"caseNumber": case_number})
        if comment:
            payload["caseComment"].update({"commentBody": comment})
        if doNotChangeSBT:
            payload["caseComment"].update({"doNotChangeSBT": doNotChangeSBT})
        if isPublic:
            payload["caseComment"].update({"isPublic": isPublic})
        if newStatus:
            payload["additionalData"].update({"newStatus": newStatus})
        if newInternalStatus:
            payload["additionalData"].update({"newInternalStatus": newInternalStatus})
        if nno:
            payload["additionalData"].update({"needsNewOwner": nno})
        # Both of these fields are for setting the Resolution status and a brief description of how it was resolved. To be used when setting the newStatus and newInternalStatus to "Closed"
        if newResolution:
            payload["additionalData"].update({"newResolution": newResolution})
        if newResolutionDescription:
            payload["additionalData"].update(
                {"newResolutionDescription": newResolutionDescription}
            )
        return self.__put_api("cases/v2/comments", payload=payload)

    def put_tag(self, case_number, tags=[]):
        return self.__put_api(
            "cases/{}/tags".format(case_number), payload={"tags": tags}
        )

    def put_owner(self, case_number, user=""):
        return self.__put_api("cases/{}/owner".format(case_number), payload=user)

    @deprecation.deprecated(
        deprecated_in="0.1",
        removed_in="1.0",
        details="Use the search_cases function instead",
    )
    def query_cases(
        self,
        status=[],
        fields=[],
        accounts=[],
        cases=[],
        sbrGroups=[],
        needsNewOwner=None,
        severity=[],
        serviceLevel=[],
        fts=None,
        ownerSsousername=[],
        tags=[],
    ):
        query_params = {}

        if status:
            query_params.update({"status": ", ".join(status)})
        if fields:
            query_params.update({"fields": ", ".join(fields)})
        if accounts:
            query_params.update({"accounts": ", ".join(accounts)})
        if cases:
            query_params.update({"case_number": ", ".join(cases)})
        if sbrGroups:
            query_params.update({"sbrGroups": ", ".join(sbrGroups)})
        if needsNewOwner:
            query_params.update({"needsNewOwner": needsNewOwner})
        if severity:
            query_params.update({"severity": ", ".join(severity)})
        if serviceLevel:
            query_params.update({"serviceLevel": ", ".join(serviceLevel)})
        if fts:
            query_params.update({"fts": fts})
        if ownerSsousername:
            query_params.update({"ownerSsousername": ", ".join(ownerSsousername)})
        if tags:
            query_params.update({"tags": ", ".join(tags)})

        return self.__get_api("cases/", parameters=query_params)

    def search_cases(self, **kwargs):

        query_params = {}
        fq_vals = []
        # Looping back over the incoming kwargs
        for k, v in kwargs.items():
            ## Fields add a much needed filter as the query will return a LOT of information without some!
            if k.lower() == "fl":
                query_params.update({"fl": ",".join(v)})
            elif k.lower() == "start":
                query_params.update({"start": v})
            elif k.lower() == "rows":
                query_params.update({"rows": v})
            else:
                # Modifying the way the value is handed to the dictionary if handed a list or not
                if isinstance(v, list):
                    v = [f'"{x}"' for x in v]
                    fq_vals.append("{0}:({1})".format(k, " OR ".join(v)))
                else:
                    fq_vals.append("{0}:{1}".format(k, v))
        query_params.update({"q": '*:*'})
        query_params.update({"fq": fq_vals})

        return self.__get_api(
            "search/cases/",
            parameters=query_params,
            headers={"Content-Type": "application/json"},
        )


    def search_kcs(self, **kwargs):

        query_params = {}
        fq_vals = []
        # Looping back over the incoming kwargs
        for k, v in kwargs.items():
            ## Fields add a much needed filter as the query will return a LOT of information without some!
            if k.lower() == "fl":
                query_params.update({"fl": ",".join(v)})
            elif k.lower() == "start":
                query_params.update({"start": v})
            elif k.lower() == "rows":
                query_params.update({"rows": v})
            elif k.lower() == "q":
                query_params.update({"q": v})
            else:
                # Modifying the way the value is handed to the dictionary if handed a list or not
                if isinstance(v, list):
                    v = [f'"{x}"' for x in v]
                    fq_vals.append("{0}:({1})".format(k, " OR ".join(v)))
                else:
                    fq_vals.append("{0}:{1}".format(k, v))
        query_params.update({"fq": fq_vals})

        return self.__get_api(
            "search/kcs/",
            parameters=query_params,
            headers={"Content-Type": "application/json"},
        )
