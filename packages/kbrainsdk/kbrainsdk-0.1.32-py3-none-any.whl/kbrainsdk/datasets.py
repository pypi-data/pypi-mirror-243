from kbrainsdk.validation.datasets import validate_list_datasets
from kbrainsdk.apibase import APIBase

class Datasets(APIBase):

    def list_datasets(self, email, token, client_id, oauth_secret, tenant_id):
        
        payload = {
            "email": email,
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_list_datasets(payload)

        path = f"/datasets/list/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
