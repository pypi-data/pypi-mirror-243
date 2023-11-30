from kbrainsdk.validation.ai import validate_ai_decide
from kbrainsdk.apibase import APIBase

class AI(APIBase):

    def decide(self, query, choices, examples, **kwargs):
        
        payload = {
            "query": query,
            "choices": choices,
            "examples": examples,
            **kwargs
        }

        validate_ai_decide(payload)

        path = f"/ai/decide/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response
