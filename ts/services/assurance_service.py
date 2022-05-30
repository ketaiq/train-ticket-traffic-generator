"""
This module includes all API calls provided by ts-assurance-service.
"""

import logging
from locust.clients import HttpSession


def get_assurance_types(client: HttpSession, bearer: str):
    # get assurance types
    client.get(
        url="/api/v1/assuranceservice/assurances/types",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name="get assurance types",
    )

    logging.info(f"get assurance types")
