import requests
from kbrainsdk.validation.llms import validate_openai_llms

class LLMs():
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
    
    def openai_chat(self, messages, model_name, model_type, **kwargs):
        payload = {
            "messages": messages,
            "model_name": model_name,
            "model_type": model_type,
            **kwargs
        }
        validate_openai_llms(payload)
        url = f"{self.base_url}/llms/openai/chat/v1"
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    def openai_completion(self, prompt, model_name, model_type, **kwargs):
        payload = {
            "prompt": prompt,
            "model_name": model_name,
            "model_type": model_type,
            **kwargs
        }
        url = f"{self.base_url}/llms/openai/completion/v1"
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()