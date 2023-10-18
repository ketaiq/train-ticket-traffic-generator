"""
This module includes all API calls provided by ts-food-service.
"""
from __future__ import annotations

from enum import IntEnum
import requests
from json import JSONDecodeError
import random
import urllib.parse
from ts import TIMEOUT_MAX
from locust.exception import RescheduleTask
from ts.log_syntax.locust_response import (
    log_http_error,
    log_wrong_response_error,
    log_timeout_error,
    log_response_info,
)

from ts.config import tt_host

FOOD_SERVICE_URL = tt_host + "/api/v1/foodservice/foods"


class FoodType(IntEnum):
    NONE = 0
    TRAIN_FOOD = 1
    STATION_FOOD_STORES = 2


class Food:
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-preserve-service/src/main/java/preserve/entity/FoodOrder.java
    """

    def __init__(
        self,
        name: str = "",
        type: int = 0,
        station: str = "",
        store: str = "",
        price: float = 0,
    ):
        self.name = name
        self.type = type
        if type == FoodType.STATION_FOOD_STORES:
            self.station = station
            self.store = store
        else:
            self.station = ""
            self.store = ""
        self.price = price


def search_food_on_trip(
    client,
    bearer: str,
    user_id: str,
    date: str,
    from_station: str,
    to_station: str,
    trip_id: str,
) -> dict | None:
    operation = "search food on trip"
    with client.get(
        url="/api/v1/foodservice/foods/"
        + urllib.parse.quote(date)
        + "/"
        + urllib.parse.quote(from_station)
        + "/"
        + urllib.parse.quote(to_station)
        + "/"
        + urllib.parse.quote("D1345"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if not response.ok:
            data = f"date: {date}, from_station: {from_station}, to_station: {to_station}, trip_id: {trip_id}"
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
                key = "msg"
                if response.json()["msg"] == "Get All Food Failed":
                    return None
                if response.json()["msg"] != "Get All Food Success":
                    log_wrong_response_error(
                        user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(user_id, operation, response.failure)
                else:
                    key = "data"
                    all_food = response.json()["data"]
                    log_response_info(user_id, operation, all_food)
                    return all_food
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()


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
    food_type = random.randint(
        FoodType.TRAIN_FOOD.value, FoodType.STATION_FOOD_STORES.value
    )
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
    else:
        all_station_food = food_menu["foodStoreListMap"]
        station_food = all_station_food[random.choice(list(all_station_food.keys()))]
        store_index = random.randint(0, len(station_food) - 1)
        store_food = station_food[store_index]
        chosen_food_index = random.randint(0, len(store_food["foodList"]) - 1)
        chosen_food = store_food["foodList"][chosen_food_index]
        return Food(
            chosen_food["foodName"],
            food_type,
            store_food["stationId"],
            store_food["storeName"],
            chosen_food["price"],
        )
