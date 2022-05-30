"""
This module includes all API calls provided by ts-food-service.
"""

import logging
from locust.clients import HttpSession


def get_food_menu(client: HttpSession, bearer: str, user_id: str):
    # get food
    with client.get(
        url="/api/v1/foodservice/foods/2022-02-11/Shang%20Hai/Su%20Zhou/D1345",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name="get all food",
    ) as response:
        if response.json()["msg"] != "Get All Food Success":
            response.failure(
                f"user {user_id} tries to get food menu but gets wrong response"
            )
            logging.error(
                f"user {user_id} tries to get food menu but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user {user_id} tries to get food menu but request takes too long!"
            )
            logging.warning(
                f"user {user_id} tries to get food menu but request takes too long!"
            )
        else:
            data = response.json()["data"]
            food_list = data["trainFoodList"]
            food_store_map = data["foodStoreListMap"]
            logging.info(
                f"user {user_id} get food menu {food_list} and {food_store_map}"
            )
