import uuid
class SalesRequest:
    def __init__(self, client, description):
        self.client = client
        self.description = description
        self.admin_bearer = None
        self.user_id = None
        self.request_id = str(uuid.uuid4())