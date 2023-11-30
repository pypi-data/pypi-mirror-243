
from kbrainsdk.validation.common import get_payload

DECIDE_ARGUMENTS = ["query", "choices", "examples", "argument_temperature", "decision_temperature"]
DECIDE_MANDATORY_ARGUMENTS = ["query", "choices", "examples"]

def validate_ai_decide(req):
    payload = get_payload(req)
    log_payload = {key: payload[key] for key in DECIDE_ARGUMENTS if (key in payload and payload[key] is not None)}

    # Check if mandatory values are present
    missing_values = [value for value in DECIDE_MANDATORY_ARGUMENTS if value not in log_payload]
    if missing_values:
        raise ValueError("Missing or empty parameter in request body. Requires: {}".format(", ".join(missing_values)))

    if not all(isinstance(choice, dict) and 'label' in choice and 'description' in choice for choice in log_payload['choices']):
        raise ValueError("'choices' must be a list of objects with properties 'label' and 'description'")

    if not all(isinstance(example, dict) and 'query' in example and 'argument' in example and 'decision' in example for example in log_payload['examples']):
        raise ValueError("'examples' must be a list of objects with properties 'query', 'argument', and 'decision'")

    return log_payload