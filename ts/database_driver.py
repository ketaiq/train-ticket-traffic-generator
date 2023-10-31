from pymongo import MongoClient
from urllib.parse import quote_plus


class DatabaseDriver:
    def __init__(self, host: str, username: str, password: str):
        uri = "mongodb://%s:%s@%s" % (quote_plus(username), quote_plus(password), host)
        self.client = MongoClient(uri)
        self.db = self.client["trainticket"]
        self.users = self.db["users"]
        self.contacts = self.db["contacts"]


db_driver = DatabaseDriver("localhost:27017", "root", "rootpass")
