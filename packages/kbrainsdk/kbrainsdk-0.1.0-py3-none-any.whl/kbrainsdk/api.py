import os
import requests
import base64

VALID_MODEL_NAMES = ["gpt-3.5-turbo", "gpt-4", "gpt-3.5-instruct"]

class KBRaiNAPI:
    def __init__(self, base_url, account_id=None, api_key=None):
        self.base_url = base_url or os.getenv('KBRAIN_BASE_URL')
        account_id = account_id or os.getenv('KBRAIN_ACCOUNT_ID')
        api_key = api_key or os.getenv('KBRAIN_API_KEY')
        auth_string = f"{account_id}:{api_key}"
        auth_bytes = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        self.headers = {'Authorization': f'Basic {auth_bytes}'}

    def create_account(self, req):
        url = f"{self.base_url}/account/v1"
        response = requests.post(url, json=req, headers=self.headers)
        return response.json()

    def create_keys(self, req):
        url = f"{self.base_url}/keys/v1"
        response = requests.post(url, json=req, headers=self.headers)
        return response.json()

    def openai_chat(self, req):
        if not isinstance(req, dict):
            raise ValueError("Payload must be a dictionary")
        if 'messages' not in req or not isinstance(req['messages'], list):
            raise ValueError("Payload must contain a 'messages' key with a list value")
        for message in req['messages']:
            if not isinstance(message, dict) or 'role' not in message or 'content' not in message:
                raise ValueError("Each message must be a dictionary with 'role' and 'content' keys")
            if not isinstance(message['role'], str) or not isinstance(message['content'], str):
                raise ValueError("'role' and 'content' must be strings")
        if 'model_name' not in req or not isinstance(req['model_name'], str):
            raise ValueError("Payload must contain a 'model_name' key with a string value")
        if req['model_name'] not in VALID_MODEL_NAMES:
            raise ValueError(f"Model name must be one of {VALID_MODEL_NAMES}")
        if 'model_type' not in req or not isinstance(req['model_type'], str):
            raise ValueError("Payload must contain a 'model_type' key with a string value")
        url = f"{self.base_url}/llms/openai/chat/v1"
        response = requests.post(url, json=req, headers=self.headers)
        return response.json()

    def openai_completion(self, req):
        url = f"{self.base_url}/llms/openai/completion/v1"
        if not isinstance(req, dict):
                raise ValueError("Payload must be a dictionary")
        if 'prompt' not in req or not isinstance(req['prompt'], str):
            raise ValueError("Payload must contain a 'prompt' key with a string value")
        if 'model_name' not in req or not isinstance(req['model_name'], str):
            raise ValueError("Payload must contain a 'model_name' key with a string value")
        if req['model_name'] not in VALID_MODEL_NAMES:
            raise ValueError(f"Model name must be one of {VALID_MODEL_NAMES}")
        if 'model_type' not in req or not isinstance(req['model_type'], str):
            raise ValueError("Payload must contain a 'model_type' key with a string value")
        if 'message' in req
        response = requests.post(url, json=req, headers=self.headers)
        return response.json()
    
    def kbrain_healthy(self):
        url = f"{self.base_url}/health/v1"
        response = requests.get(url, headers=self.headers)
        return response.json()