"""
This module includes all API calls provided by ts-admin-user-service.
"""

import logging
from locust.clients import HttpSession


def add_one_user(
    client: HttpSession,
    admin_bearer: str,
    document_num: str,
    username: str,
    password: str,
):
    client.post(
        url="/api/v1/adminuserservice/users",
        headers={
            "Authorization": admin_bearer,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "documentNum": document_num,
            "documentType": 0,
            "email": "string",
            "gender": 0,
            "password": username,
            "userName": password,
        },
        name="create user",
    )
    logging.info(f"admin adds a new user {username}")
