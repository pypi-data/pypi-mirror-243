from kbrainsdk.validation.llms import validate_openai_llms
from kbrainsdk.apibase import APIBase

class LLMs(APIBase):
    
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
        response = self.apiobject.call_endpoint(url, payload, "post")
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
        response = self.apiobject.call_endpoint(url, payload, "post")
        return response