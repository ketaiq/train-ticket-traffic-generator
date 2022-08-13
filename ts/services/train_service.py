import requests
from json import JSONDecodeError
from ts import HOST_URL

TRAIN_SERVICE_URL = f"http://{HOST_URL}/api/v1/adminbasicservice/adminbasic/trains"
ORIGINAL_TRAINS = [
    {
        "id": "GaoTieOne",
        "economyClass": 2147483647,
        "confortClass": 2147483647,
        "averageSpeed": 250,
    },
    {
        "id": "GaoTieTwo",
        "economyClass": 2147483647,
        "confortClass": 2147483647,
        "averageSpeed": 200,
    },
    {
        "id": "DongCheOne",
        "economyClass": 2147483647,
        "confortClass": 2147483647,
        "averageSpeed": 180,
    },
    {
        "id": "ZhiDa",
        "economyClass": 2147483647,
        "confortClass": 2147483647,
        "averageSpeed": 120,
    },
    {
        "id": "TeKuai",
        "economyClass": 2147483647,
        "confortClass": 2147483647,
        "averageSpeed": 120,
    },
    {
        "id": "KuaiSu",
        "economyClass": 2147483647,
        "confortClass": 2147483647,
        "averageSpeed": 90,
    },
]


class Train:
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-train-service/src/main/java/train/entity/TrainType.java
    """

    def __init__(
        self, id: str, economy_class: int, comfort_class: int, average_speed: int
    ):
        self.id = id
        self.economy_class = economy_class
        self.comfort_class = comfort_class
        self.average_speed = average_speed


def get_all_trains_request(admin_bearer: str, request_id: str) -> list:
    operation = "get all trains"
    r = requests.get(
        url=TRAIN_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if "success" not in msg.lower():
            print(f"request {request_id} tries to {operation} but gets wrong response")
        else:
            key = "data"
            return r.json()["data"]
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def add_one_train_request(admin_bearer: str, request_id: str, train: Train) -> str:
    operation = "add one train"
    r = requests.post(
        url=TRAIN_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": train.id,
            "economyClass": train.economy_class,
            "confortClass": train.comfort_class,
            "averageSpeed": train.average_speed,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if "success" not in msg.lower():
            print(f"request {request_id} tries to {operation} but gets wrong response")
        else:
            key = "data"
            return r.json()["data"]
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def delete_one_train_request(admin_bearer: str, request_id: str, id: str) -> str:
    operation = "delete one train"
    r = requests.delete(
        url=TRAIN_SERVICE_URL + "/" + id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if "success" not in msg.lower():
            print(f"request {request_id} tries to {operation} but gets wrong response")
        else:
            key = "data"
            return r.json()["data"]
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def gen_random_train(id: str) -> Train:
    return Train(id, 2147483647, 2147483647, 250)


def restore_original_trains(
    admin_bearer: str,
    request_id: str,
):
    trains = get_all_trains_request(admin_bearer, request_id)
    for train in trains:
        if train not in ORIGINAL_TRAINS:
            result = delete_one_train_request(admin_bearer, request_id, train["id"])
            if result:
                print(f"Delete train {train}")


def add_trains(request_id: str, admin_bearer: str, all_trains: list):
    restore_original_trains(admin_bearer, request_id)
    for train in all_trains:
        add_one_train_request(admin_bearer, request_id, train)
        print(f"Add train {train.__dict__}")
