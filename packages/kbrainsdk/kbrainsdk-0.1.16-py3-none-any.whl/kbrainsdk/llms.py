from kbrainsdk.validation.llms import validate_openai_llms

class LLMs():
    def __init__(self, api, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.api = api
    
    def openai_chat(self, messages, model_name, model_type, deployment_id, **kwargs):
        payload = {
            "messages": messages,
            "model_name": model_name,
            "model_type": model_type,
            "deployment_id": deployment_id,
            **kwargs
        }
        validate_openai_llms(payload, 'chat')
        url = f"{self.base_url}/llms/openai/chat/v1"
        response = self.api.call_endpoint(url, payload, "post")
        return response

    def openai_completion(self, prompt, model_name, model_type, deployment_id, **kwargs):
        payload = {
            "prompt": prompt,
            "model_name": model_name,
            "model_type": model_type,
            "deployment_id": deployment_id,
            **kwargs
        }
        validate_openai_llms(payload, 'completion')
        url = f"{self.base_url}/llms/openai/completion/v1"
        response = self.api.call_endpoint(url, payload, "post")
        return response