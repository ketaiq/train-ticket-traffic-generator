"""
This module includes all API calls provided by ts-food-service.
"""

import logging
from locust.clients import HttpSession


def get_all_food(client: HttpSession, bearer: str):
    # get food
    client.get(
        url="/api/v1/foodservice/foods/2022-02-11/Shang%20Hai/Su%20Zhou/D1345",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name="get all food",
    )

    logging.info(f"user gets all food")
