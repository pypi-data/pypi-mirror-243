from kbrainsdk.validation.common import get_payload, validate_email

def validate_list_datasets(req):
    body = get_payload(req)
    email = body.get('email')
    token = body.get('token')
    client_id = body.get('client_id')
    oauth_secret = body.get('oauth_secret')
    tenant_id = body.get('tenant_id')

 # Validate parameters
    if not all([email, token, client_id, oauth_secret, tenant_id]):
        raise ValueError("Missing or empty parameter in request body")

    if not validate_email(email):
        raise ValueError("Invalid email address")
    
    return email, token, client_id, oauth_secret, tenant_id
