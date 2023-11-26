import requests

class LLMs():
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
    
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
        if 'model_type' not in req or not isinstance(req['model_type'], str):
            raise ValueError("Payload must contain a 'model_type' key with a string value")
        url = f"{self.base_url}/llms/openai/chat/v1"
        response = requests.post(url, json=req, headers=self.headers)
        return response.json()

    def openai_completion(self, req):
        if not isinstance(req, dict):
                raise ValueError("Payload must be a dictionary")
        if 'prompt' not in req or not isinstance(req['prompt'], str):
            raise ValueError("Payload must contain a 'prompt' key with a string value")
        if 'model_name' not in req or not isinstance(req['model_name'], str):
            raise ValueError("Payload must contain a 'model_name' key with a string value")
        if 'model_type' not in req or not isinstance(req['model_type'], str):
            raise ValueError("Payload must contain a 'model_type' key with a string value")
        if 'messages' in req:
            raise ValueError("Completion endpoint uses 'prompt' instead of messages")
        url = f"{self.base_url}/llms/openai/completion/v1"
        response = requests.post(url, json=req, headers=self.headers)
        return response.json()