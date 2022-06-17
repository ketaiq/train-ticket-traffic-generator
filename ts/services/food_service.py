"""
This module includes all API calls provided by ts-food-service.
"""

import logging
from enum import IntEnum
import requests
from json import JSONDecodeError
import random
import urllib.parse
from ts import TIMEOUT_MAX

FOOD_SERVICE_URL = "http://34.98.120.134/api/v1/foodservice/foods"


class FoodType(IntEnum):
    NONE = 0
    TRAIN_FOOD = 1
    STATION_FOOD_STORES = 2


class Food:
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-preserve-service/src/main/java/preserve/entity/FoodOrder.java
    """

    def __init__(self, name: str, type: int, station: str, store: str, price: float):
        self.name = name
        self.type = type
        if type == FoodType.STATION_FOOD_STORES:
            self.station = station
            self.store = store
        else:
            self.station = ""
            self.store = ""

        self.price = price


def get_food_menu(client, bearer: str, user_id: str) -> dict:
    food_menu = dict()
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
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            response.failure(
                f"user {user_id} tries to get food menu but request takes too long!"
            )
            logging.warning(
                f"user {user_id} tries to get food menu but request takes too long!"
            )
        else:
            food_menu = response.json()["data"]
            logging.info(f"user {user_id} get food menu {food_menu}")

    return food_menu


def get_all_train_and_store_food_request(
    request_id: str,
    bearer: str,
    date: str,
    from_station: str,
    to_station: str,
    trip_id: str,
) -> dict:
    operation = "get food menu"
    r = requests.get(
        url=FOOD_SERVICE_URL
        + "/"
        + urllib.parse.quote(date)
        + "/"
        + urllib.parse.quote(from_station)
        + "/"
        + urllib.parse.quote(to_station)
        + "/"
        + urllib.parse.quote(trip_id),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Get All Food Success":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            food = r.json()["data"]
            return food
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def pick_random_food(food_menu: dict) -> Food:
    food_type = random.randint(FoodType.NONE.value, FoodType.STATION_FOOD_STORES.value)
    if food_type == FoodType.TRAIN_FOOD:
        train_food = food_menu["trainFoodList"][0]
        chosen_food_index = random.randint(0, len(train_food["foodList"]) - 1)
        chosen_food = train_food["foodList"][chosen_food_index]
        return Food(
            chosen_food["foodName"],
            food_type,
            "",
            "",
            chosen_food["price"],
        )
    elif food_type == FoodType.STATION_FOOD_STORES:
        station_food = food_menu["foodStoreListMap"]
        station = random.randint(0, 1)
        if station == 0:
            station_food = station_food["shanghai"]
        else:
            station_food = station_food["suzhou"]
        station_food_index = random.randint(0, len(station_food) - 1)
        station_food = station_food[station_food_index]
        chosen_food_index = random.randint(0, len(station_food["foodList"]) - 1)
        chosen_food = station_food["foodList"][chosen_food_index]
        return Food(
            chosen_food["foodName"],
            food_type,
            station_food["stationId"],
            station_food["storeName"],
            chosen_food["price"],
        )
    else:
        return Food(
            "",
            food_type,
            "",
            "",
            0,
        )
