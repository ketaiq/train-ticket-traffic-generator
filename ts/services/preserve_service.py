"""
This module includes all API calls provided by ts-preserve-service.
"""
from enum import Enum
from ts.services.food_service import Food
from ts.services.consign_service import Consign
from ts.log_syntax.locust_response import (
    log_http_error,
    log_wrong_response_error,
    log_timeout_error,
    log_response_info,
)
import requests
from json import JSONDecodeError
from ts import TIMEOUT_MAX
from locust.exception import RescheduleTask
import random

from ts.config import tt_host

PRESERVE_SERVICE_URL = tt_host + "/api/v1/preserveservice/preserve"


class SeatType(Enum):
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-preserve-service/src/main/java/preserve/entity/SeatClass.java
    """

    FIRST_CLASS = "2"
    SECOND_CLASS = "3"


def reserve_one_ticket(
    client,
    bearer: str,
    user_id: str,
    contact_id: str,
    trip_id: str,
    seat_type: str,
    date: str,
    from_station: str,
    to_station: str,
    assurance: str,
    food: Food,
    consign: Consign,
):
    operation = "reserve ticket"

    with client.post(
        url="/api/v1/preserveservice/preserve",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={
            "accountId": user_id,
            "contactsId": contact_id,
            # "tripId" : trip_id,
            "tripId": "D1345",
            "seatType": seat_type,
            "date": date,
            "from": from_station,
            "to": to_station,
            "assurance": assurance,
            # food
            "foodType": food.type,
            "foodName": food.name,
            "foodPrice": food.price,
            "stationName": food.station,
            "storeName": food.store,
            # consign
            "handleDate": date,
            "isWithin": False,
            "consigneeName": consign.name,
            "consigneePhone": consign.phone,
            "consigneeWeight": consign.weight,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if not response.ok:
            data = {
                "accountId": user_id,
                "contactsId": contact_id,
                # "tripId" : trip_id,
                "tripId": "D1345",
                "seatType": seat_type,
                "date": date,
                "from": from_station,
                "to": to_station,
                "assurance": assurance,
                # food
                "foodType": food.type,
                "foodName": food.name,
                "foodPrice": food.price,
                "stationName": food.station,
                "storeName": food.store,
                # consign
                "handleDate": date,
                "isWithin": False,
                "consigneeName": consign.name,
                "consigneePhone": consign.phone,
                "consigneeWeight": consign.weight,
            }
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
                key = "msg"
                if response.json()["msg"] != "Success.":
                    log_wrong_response_error(
                        user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(user_id, operation, response.failure)
                else:
                    key = "data"
                    log_response_info(user_id, operation, response.json()["data"])
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()


def reserve_one_ticket_request(
    request_id: str,
    bearer: str,
    user_id: str,
    contact_id: str,
    trip_id: str,
    seat_type: str,
    date: str,
    from_station: str,
    to_station: str,
    assurance: str,
    food: Food,
    consign: Consign,
) -> str:
    operation = "reserve a ticket"

    r = requests.post(
        url=PRESERVE_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={
            "accountId": user_id,
            "contactsId": contact_id,
            "tripId": trip_id,
            "seatType": seat_type,
            "date": date,
            "from": from_station,
            "to": to_station,
            "assurance": assurance,
            # food
            "foodType": food.type,
            "foodName": food.name,
            "foodPrice": food.price,
            "stationName": food.station,
            "storeName": food.store,
            # consign
            "handleDate": date,
            "isWithin": False,
            "consigneeName": consign.name,
            "consigneePhone": consign.phone,
            "consigneeWeight": consign.weight,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Success.":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            data = r.json()["data"]
            print(f"request {request_id} {operation} {data}")
            return data
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def pick_random_seat_type() -> str:
    return random.choice(list(SeatType)).value
