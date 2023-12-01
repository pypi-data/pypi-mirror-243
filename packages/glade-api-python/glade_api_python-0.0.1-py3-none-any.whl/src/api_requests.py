import requests
from .helpers import Helpers

class APIRequests:
    def __init__(self, merchantId, merchantKey, baseUrl):
        self.merchantId = merchantId
        self.merchantKey = merchantKey
        self.baseUrl = baseUrl
        self.headers = {
            "mid": self.merchantId,
            "key": self.merchantKey,
            "accept": "application/json",
            "content_type": "application/json",
        }

    def makeApiCall(self, method, endpoint, payload):
        if self.merchantId == None or not isinstance(self.merchantId, str):
            return Helpers.handleCustomResponse(400, "error", "Please set your merchant ID")
        
        if self.merchantKey == None  or not isinstance(self.merchantKey, str):
            return Helpers.handleCustomResponse(400, "error", "Please set your merchant key")
        
        url = f"{self.baseUrl}{endpoint}"

        try:
            if method == "post":
                response = self.post(url, payload)
            elif method == "put":
                response = self.put(url, payload)
            elif method == "patch":
                response = self.patch(url, payload)
            elif method == "delete":
                response = self.delete(url)
            else:
                response = self.get(url)
        except Exception as e:
            return Helpers.exceptionsHandler(e)
        except:
            return Helpers.apiFailureResponse()

        if response.status_code in [200, 201]:
            return response.json()
        else:
            return Helpers.handleFailureResponse(response)

    def get(self, url):
        return requests.get(url, headers=self.headers)

    def post(self, url, payload):
        return requests.post(url, json=payload, headers=self.headers)

    def put(self, url, payload):
        return requests.put(url, json=payload, headers=self.headers)

    def patch(self, url, payload):
        return requests.patch(url, json=payload, headers=self.headers)

    def delete(self, url):
        return requests.delete(url, headers=self.headers)
