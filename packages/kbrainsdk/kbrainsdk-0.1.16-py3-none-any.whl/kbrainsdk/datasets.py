from kbrainsdk.validation.datasets import validate_list_datasets

class Datasets():
    def __init__(self, api, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.api = api

    def list_datasets(self, email, token, client_id, oauth_secret, tenant_id):
        
        payload = {
            "email": email,
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_list_datasets(payload)

        url = f"{self.base_url}/datasets/list/v1"
        response = self.api.call_endpoint(url, payload, "post")
        return response
