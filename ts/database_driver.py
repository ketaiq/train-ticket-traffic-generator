from pymongo import MongoClient
from urllib.parse import quote_plus


class DatabaseDriver:
    def __init__(self, host: str, username: str, password: str):
        uri = "mongodb://%s:%s@%s" % (quote_plus(username), quote_plus(password), host)
        self.client = MongoClient(uri)
        self.db = self.client["trainticket"]
        self.users = self.db["users"]
        self.sample_user_index = 0

    def sample_user(self) -> dict:
        sampled_user = self.users.find().sort("_id")[self.sample_user_index]
        self.sample_user_index += 1
        if self.sample_user_index >= self.users.count_documents({}):
            self.sample_user_index = 0
        return sampled_user


db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
