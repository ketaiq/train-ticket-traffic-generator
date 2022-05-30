"""
This module includes all API calls provided by ts-auth-service.
"""

import logging
from locust.clients import HttpSession
from typing import Tuple


def login_user(
    client: HttpSession, username: str, password: str, description: str
) -> Tuple[str, str]:
    admin_bearer = ""
    user_id = ""

    with client.post(
        url="/api/v1/users/login",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={"username": username, "password": password},
        name=description,
    ) as response:
        if response.json()["msg"] != "login success":
            response.failure(f"user {username} tries to log in but gets wrong response")
            logging.error(
                f"user {username} tries to log in but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user {username} tries to log in but request takes too long!"
            )
            logging.warning(
                f"user {username} tries to log in but request takes too long!"
            )
        else:
            data = response.json()["data"]
            if data is not None:
                admin_bearer = "Bearer " + data["token"]
                user_id = data["userId"]
                logging.info(f"user {username} logs in")
            else:
                logging.error(
                    f"user {username} fails to log in because there is no response data"
                )

    return admin_bearer, user_id
