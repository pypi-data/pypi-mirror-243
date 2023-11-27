import os
import requests
import base64
from kbrainsdk.admin import Admin
from kbrainsdk.llms import LLMs
from kbrainsdk.datasets import Datasets

VALID_MODEL_NAMES = ["gpt-3.5-turbo", "gpt-4", "gpt-3.5-instruct"]

class KBRaiNAPI:
    def __init__(self, base_url=None, account_id=None, api_key=None):
        self.base_url = base_url or os.getenv('KBRAIN_BASE_URL')
        account_id = account_id or os.getenv('KBRAIN_ACCOUNT_ID')
        api_key = api_key or os.getenv('KBRAIN_API_KEY')
        auth_string = f"{account_id}:{api_key}"
        auth_bytes = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        self.headers = {'Authorization': f'Basic {auth_bytes}'}
        self.admin = Admin(self, self.base_url, self.headers)
        self.llms = LLMs(self, self.base_url, self.headers)
        self.datasets = Datasets(self, self.base_url, self.headers)
    
    def healthy(self):
        url = f"{self.base_url}/health/v1"
        response = self.call_endpoint(url, {}, "get")
        return response

    
    def call_endpoint(self, endpoint, payload, method):
        response = requests(url=endpoint, json=payload, headers=self.headers, method=method)
        if response.status_code >= 200 and response.status_code <= 300:
            return response.json()
        
        message = response.json().get('message')
        raise Exception(message)