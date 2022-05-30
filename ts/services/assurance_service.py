"""
This module includes all API calls provided by ts-assurance-service.
"""

import logging
from locust.clients import HttpSession


def get_assurance_types(client: HttpSession, bearer: str, user_id: str):
    # get assurance types
    with client.get(
        url="/api/v1/assuranceservice/assurances/types",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name="get assurance types",
    ) as response:
        if response.json()["msg"] != "Find All Assurance":
            response.failure(
                f"user {user_id} tries to get assurance types but gets wrong response"
            )
            logging.error(
                f"user {user_id} tries to get assurance types but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user {user_id} tries to get assurance types but request takes too long!"
            )
            logging.warning(
                f"user {user_id} tries to get assurance types but request takes too long!"
            )
        else:
            assurance_types = response.json()["data"]
            logging.info(f"user {user_id} gets assurance types {assurance_types}")
