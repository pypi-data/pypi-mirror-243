class Admin():

    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def create_account(self, req):
        url = f"{self.base_url}/account/v1"
        response = requests.post(url, json=req, headers=self.headers)
        return response.json()

    def create_keys(self, req):
        url = f"{self.base_url}/keys/v1"
        response = requests.post(url, json=req, headers=self.headers)
        return response.json()