from kbrainsdk.apibase import APIBase

class Admin(APIBase):

    def create_account(self, req):
        path = "/account/v1"
        response = self.apiobject.call_endpoint(path, req, "post")
        return response


    def create_keys(self, req):
        path = "/keys/v1"
        response = self.apiobject.call_endpoint(path, req, "post")
        return response
