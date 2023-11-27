from kbrainsdk.apibase import APIBase

class Admin(APIBase):

    def create_account(self, req):
        url = f"{self.base_url}/account/v1"
        response = self.apiobject.call_endpoint(url, req, "post")
        return response


    def create_keys(self, req):
        url = f"{self.base_url}/keys/v1"
        response = self.apiobject.call_endpoint(url, req, "post")
        return response
