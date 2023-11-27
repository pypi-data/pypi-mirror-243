from kbrainsdk.validation.ingest import validate_ingest_onedrive, validate_ingest_sharepoint, validate_ingest_status
from kbrainsdk.apibase import APIBase

class Ingest(APIBase):

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

        path = f"/ingest/onedrive/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
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

        path = f"/ingest/sharepoint/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def get_status(self, datasource):

        payload = {
            "datasource": datasource 
        }

        validate_ingest_status(payload)

        path = f"/ingest/status/v1"
        response = self.apiobject.call_endpoint(path, payload, "post")
        return response

    def convert_email_to_datasource(self, email):
        return f"drive-{email.lower().replace('@', '-at-').replace('.', '-')}"