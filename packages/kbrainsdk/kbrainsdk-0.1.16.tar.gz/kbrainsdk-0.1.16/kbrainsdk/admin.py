class Admin():

    def __init__(self, api, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.api = api

    def create_account(self, req):
        url = f"{self.base_url}/account/v1"
        response = self.api.call_endpoint(url, req, "post")
        return response


    def create_keys(self, req):
        url = f"{self.base_url}/keys/v1"
        response = self.api.call_endpoint(url, req, "post")
        return response
