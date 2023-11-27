class APIBase():
    def __init__(self, kbrainapi, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.apiobject = kbrainapi