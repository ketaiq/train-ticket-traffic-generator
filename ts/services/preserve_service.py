"""
This module includes all API calls provided by ts-preserve-service.
"""

from locust.clients import HttpSession
from enum import Enum
from ts.services.food_service import Food
from ts.services.consign_service import Consign
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)


class SeatType(Enum):
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-preserve-service/src/main/java/preserve/entity/SeatClass.java
    """

    FIRST_CLASS = "2"
    SECOND_CLASS = "3"


def reserve_one_ticket(
    client: HttpSession,
    bearer: str,
    user_id: str,
    contact_id: str,
    seat_type: str,
    date: str,
    from_station: str,
    to_station: str,
    assurance: str,
    food: Food,
    consign: Consign,
):
    operation = "reserve a ticket"
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
        catch_response=True,
        name="reserve a ticket",
    ) as response:
        if response.json()["msg"] != "Success.":
            log_wrong_response_warning(user_id, operation, response)
        elif response.elapsed.total_seconds() > 10:
            log_timeout_warning(user_id, operation, response)
        else:
            log_response_info(user_id, operation, response.json()["data"])
