class Datasets():
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def list_datasets(email, token, client_id, oauth_secret, tenant_id):
        # Validation
        assert all(item is not None for item in [email, token, client_id, oauth_secret, tenant_id]), "None of the parameters can be None"
        assert all(isinstance(item, str) for item in [email, token, client_id, oauth_secret, tenant_id]), "All parameters must be strings"
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Email is not valid"

        payload = {
            "email": email,
            "token": token,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        url = f"{self.base_url}/datasets/list/v1"
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

