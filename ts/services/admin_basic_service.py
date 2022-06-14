import requests
from json import JSONDecodeError

ADMIN_PRICE_SERVICE_URL = (
    "http://34.98.120.134/api/v1/adminbasicservice/adminbasic/prices"
)

ORIGINAL_PRICES = [
    {
        "id": "6d20b8cb-039c-474c-ae25-b6177ea41152",
        "trainType": "GaoTieOne",
        "routeId": "92708982-77af-4318-be25-57ccb0ff69ad",
        "basicPriceRate": 0.38,
        "firstClassPriceRate": 1.0,
    },
    {
        "id": "c5679b7e-4a54-4f52-9939-1ae86ba16fa7",
        "trainType": "GaoTieOne",
        "routeId": "aefcef3f-3f42-46e8-afd7-6cb2a928bd3d",
        "basicPriceRate": 0.5,
        "firstClassPriceRate": 1.0,
    },
    {
        "id": "719287d6-d3e7-4b54-9a92-71d039748b22",
        "trainType": "GaoTieOne",
        "routeId": "a3f256c1-0e43-4f7d-9c21-121bf258101f",
        "basicPriceRate": 0.7,
        "firstClassPriceRate": 1.0,
    },
    {
        "id": "7de18cf8-bb17-4bb2-aeb4-85d8176d3a93",
        "trainType": "GaoTieTwo",
        "routeId": "084837bb-53c8-4438-87c8-0321a4d09917",
        "basicPriceRate": 0.6,
        "firstClassPriceRate": 1.0,
    },
    {
        "id": "d5c4523a-827c-468c-95be-e9024a40572e",
        "trainType": "DongCheOne",
        "routeId": "f3d4d4ef-693b-4456-8eed-59c0d717dd08",
        "basicPriceRate": 0.45,
        "firstClassPriceRate": 1.0,
    },
    {
        "id": "b90a6ad7-ffad-4624-9655-48e9e185fa6c",
        "trainType": "ZhiDa",
        "routeId": "0b23bd3e-876a-4af3-b920-c50a90c90b04",
        "basicPriceRate": 0.35,
        "firstClassPriceRate": 1.0,
    },
    {
        "id": "8fb01829-393f-4af4-9e96-f72866f94d14",
        "trainType": "ZhiDa",
        "routeId": "9fc9c261-3263-4bfa-82f8-bb44e06b2f52",
        "basicPriceRate": 0.35,
        "firstClassPriceRate": 1.0,
    },
    {
        "id": "8b059dc5-01a2-4f8f-8f94-6c886b38bb34",
        "trainType": "ZhiDa",
        "routeId": "d693a2c5-ef87-4a3c-bef8-600b43f62c68",
        "basicPriceRate": 0.32,
        "firstClassPriceRate": 1.0,
    },
    {
        "id": "dd0e572e-7443-420c-8280-7d8215636069",
        "trainType": "TeKuai",
        "routeId": "20eb7122-3a11-423f-b10a-be0dc5bce7db",
        "basicPriceRate": 0.3,
        "firstClassPriceRate": 1.0,
    },
    {
        "id": "0eb474c9-f8be-4119-8681-eb538a404a6a",
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


def restore_original_prices(admin_bearer: str, request_id: str):
    prices = get_all_prices_request(admin_bearer, request_id)
    for price in prices:
        if price not in ORIGINAL_PRICES:
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
    for travel in all_travels:
        new_price = add_one_price_request(
            admin_bearer,
            request_id,
            Price(None, 1, 2, travel.route_id, travel.train_type_id),
        )
        print(f"Add price {new_price}")
