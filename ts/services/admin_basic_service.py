"""
This module includes all API calls provided by ts-admin-basic-service.
"""
from __future__ import annotations

import requests
from json import JSONDecodeError
import random
from ts.services.contacts_service import Contact
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)
from ts import TIMEOUT_MAX

ADMIN_PRICE_SERVICE_URL = (
    "http://34.160.158.68/api/v1/adminbasicservice/adminbasic/prices"
)

ORIGINAL_PRICES = [
    {
        "trainType": "GaoTieOne",
        "routeId": "92708982-77af-4318-be25-57ccb0ff69ad",
        "basicPriceRate": 0.38,
        "firstClassPriceRate": 1.0,
    },
    {
        "trainType": "GaoTieOne",
        "routeId": "aefcef3f-3f42-46e8-afd7-6cb2a928bd3d",
        "basicPriceRate": 0.5,
        "firstClassPriceRate": 1.0,
    },
    {
        "trainType": "GaoTieOne",
        "routeId": "a3f256c1-0e43-4f7d-9c21-121bf258101f",
        "basicPriceRate": 0.7,
        "firstClassPriceRate": 1.0,
    },
    {
        "trainType": "GaoTieTwo",
        "routeId": "084837bb-53c8-4438-87c8-0321a4d09917",
        "basicPriceRate": 0.6,
        "firstClassPriceRate": 1.0,
    },
    {
        "trainType": "DongCheOne",
        "routeId": "f3d4d4ef-693b-4456-8eed-59c0d717dd08",
        "basicPriceRate": 0.45,
        "firstClassPriceRate": 1.0,
    },
    {
        "trainType": "ZhiDa",
        "routeId": "0b23bd3e-876a-4af3-b920-c50a90c90b04",
        "basicPriceRate": 0.35,
        "firstClassPriceRate": 1.0,
    },
    {
        "trainType": "ZhiDa",
        "routeId": "9fc9c261-3263-4bfa-82f8-bb44e06b2f52",
        "basicPriceRate": 0.35,
        "firstClassPriceRate": 1.0,
    },
    {
        "trainType": "ZhiDa",
        "routeId": "d693a2c5-ef87-4a3c-bef8-600b43f62c68",
        "basicPriceRate": 0.32,
        "firstClassPriceRate": 1.0,
    },
    {
        "trainType": "TeKuai",
        "routeId": "20eb7122-3a11-423f-b10a-be0dc5bce7db",
        "basicPriceRate": 0.3,
        "firstClassPriceRate": 1.0,
    },
    {
        "trainType": "KuaiSu",
        "routeId": "1367db1f-461e-4ab7-87ad-2bcc05fd9cb7",
        "basicPriceRate": 0.2,
        "firstClassPriceRate": 1.0,
    },
]


class Price:
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-admin-basic-info-service/src/main/java/adminbasic/entity/PriceInfo.java
    """

    def __init__(
        self,
        id: str | None,
        basic_price_rate: float,
        first_class_price_rate: float,
        route_id: str,
        train_type: str,
    ):
        self.id = id
        self.basic_price_rate = basic_price_rate
        self.first_class_price_rate = first_class_price_rate
        self.route_id = route_id
        self.train_type = train_type


def get_all_prices_request(admin_bearer: str, request_id: str) -> list:
    operation = "get all prices"
    r = requests.get(
        url=ADMIN_PRICE_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Success":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            prices = r.json()["data"]
            print(f"request {request_id} {operation} {prices}")
            return prices
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def add_one_price_request(admin_bearer: str, request_id: str, price: Price) -> dict:
    operation = "add one price"
    r = requests.post(
        url=ADMIN_PRICE_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "basicPriceRate": price.basic_price_rate,
            "firstClassPriceRate": price.first_class_price_rate,
            "routeId": price.route_id,
            "trainType": price.train_type,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Create success":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            added_price = r.json()["data"]
            print(f"request {request_id} {operation} {added_price}")
            return added_price
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def delete_one_price_request(admin_bearer: str, request_id: str, price: Price) -> dict:
    operation = "delete one price"
    r = requests.delete(
        url=ADMIN_PRICE_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": price.id,
            "basicPriceRate": price.basic_price_rate,
            "firstClassPriceRate": price.first_class_price_rate,
            "routeId": price.route_id,
            "trainType": price.train_type,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Delete success":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            deleted_price = r.json()["data"]
            print(f"request {request_id} {operation} {deleted_price}")
            return deleted_price
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def admin_add_one_contact(client, admin_bearer: str, user_id: str, contact: Contact):
    operation = "admin add contact"
    with client.post(
        url="/api/v1/adminbasicservice/adminbasic/contacts",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "name": contact.name,
            "accountId": contact.user_id,
            "documentType": contact.document_type,
            "documentNumber": contact.document_number,
            "phoneNumber": contact.phone_number,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Create Success":
            log_wrong_response_warning(
                user_id, operation, response.failure, response.json()
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response.failure)
        else:
            data = response.json()["data"]
            log_response_info(user_id, operation, data)


def restore_original_prices(admin_bearer: str, request_id: str):
    prices = get_all_prices_request(admin_bearer, request_id)
    for price in prices:
        price_without_id = {
            "trainType": price["trainType"],
            "routeId": price["routeId"],
            "basicPriceRate": price["basicPriceRate"],
            "firstClassPriceRate": price["firstClassPriceRate"],
        }
        if price_without_id not in ORIGINAL_PRICES:
            deleted_price = delete_one_price_request(
                admin_bearer,
                request_id,
                Price(
                    price["id"],
                    price["basicPriceRate"],
                    price["firstClassPriceRate"],
                    price["routeId"],
                    price["trainType"],
                ),
            )
            print(f"Delete price {deleted_price}")


def add_prices(request_id: str, admin_bearer: str, all_travels: list):
    restore_original_prices(admin_bearer, request_id)
    for travel in all_travels:
        new_price = add_one_price_request(
            admin_bearer,
            request_id,
            Price(
                None,
                round(random.uniform(0.3, 1), 2),
                round(random.uniform(1, 3), 2),
                travel.route_id,
                travel.train_type_id,
            ),
        )
        print(f"Add price {new_price}")
