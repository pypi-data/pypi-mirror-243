import re
import requests
from kbrainsdk.validation.ingest import validate_ingest_onedrive, validate_ingest_sharepoint, validate_ingest_status
class Ingest():
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def ingest_onedrive(self, email, token, client_id, oauth_secret, tenant_id, environment):

        payload = {
            "email": email,
            "token": token,
            "environment": environment,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_ingest_onedrive(payload)

        url = f"{self.base_url}/ingest/onedrive/v1"
        response = self.call_endpoint(url, payload, "post")
        return response

    def ingest_sharepoint(self, host, site, token, client_id, oauth_secret, tenant_id, environment):

        payload = {
            "host": host,
            "site": site,
            "token": token,
            "environment": environment,
            "client_id": client_id,
            "oauth_secret": oauth_secret,
            "tenant_id": tenant_id
        }

        validate_ingest_sharepoint(payload)

        url = f"{self.base_url}/ingest/sharepoint/v1"
        response = self.call_endpoint(url, payload, "post")
        return response

    def get_status(self, datasource):

        payload = {
            "datasource": datasource 
        }

        validate_ingest_status(payload)

        url = f"{self.base_url}/ingest/status/v1"
        response = self.call_endpoint(url, payload, "post")
        return response

    def convert_email_to_datasource(email):
        return f"drive-{email.lower().replace('@', '-at-').replace('.', '-')}"