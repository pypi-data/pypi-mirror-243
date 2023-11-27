
from kbrainsdk.validation.common import get_payload


def validate_create_account(req):
    body = get_payload(req)
    account_name = body.get('account_name')
    account_email = body.get('account_email')
    notes = body.get('notes')

    if not all([account_name, account_email]):
        raise ValueError("Missing or empty parameter in request body. Requires: account_name, account_email")

    return account_name, account_email, notes


def validate_create_api_key(req):
    body = get_payload(req)
    account_id = body.get('account_id')
    scopes = body.get('scopes')

    if not all([account_id, scopes]):
        raise ValueError("Missing or empty parameter in request body. Requires: account_id, scopes")

    return account_id, scopes