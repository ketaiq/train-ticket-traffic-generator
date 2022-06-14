import requests
import logging
import time
import random
from json import JSONDecodeError

ADMIN_TRAVEL_SERVICE_URL = "http://34.98.120.134/api/v1/admintravelservice/admintravel"


class Travel:
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-admin-travel-service/src/main/java/admintravel/entity/TravelInfo.java
    """

    def __init__(
        self,
        trip_id: str,
        train_type_id: str,
        route_id: str,
    ):
        self.trip_id = "G-" + trip_id
        self.train_type_id = train_type_id
        self.route_id = route_id
        self.start_time = int(time.time() * 1000)
        self.end_time = int(
            (time.time() + random.randint(2 * 60 * 60, 12 * 60 * 60)) * 1000
        )


def get_all_travels_request(admin_bearer: str, request_id: str) -> list:
    operation = "get all travels"
    r = requests.get(
        url=ADMIN_TRAVEL_SERVICE_URL,
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


def add_one_travel_request(admin_bearer: str, request_id: str, travel: Travel) -> str:
    operation = "add one travel"
    r = requests.post(
        url=ADMIN_TRAVEL_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "tripId": travel.trip_id,
            "trainTypeId": travel.train_type_id,
            "routeId": travel.route_id,
            "startingTime": travel.start_time,
            "endTime": travel.end_time,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "[Admin add new travel]":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            new_travel = r.json()["data"]
            print(f"request {request_id} {operation}")
            return new_travel
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def delete_one_travel_request(admin_bearer: str, request_id: str, trip_id: str) -> str:
    operation = "delete one travel"
    r = requests.delete(
        url=ADMIN_TRAVEL_SERVICE_URL + "/" + trip_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != f"Delete trip:{trip_id}.":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            deleted_travel = r.json()["data"]
            print(f"request {request_id} {operation} {deleted_travel}")
            return deleted_travel
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def add_travels(request_id: str, admin_bearer: str, all_travels: list):
    for travel in all_travels:
        add_one_travel_request(admin_bearer, request_id, travel)
        print(f"Add travel {travel.__dict__}")
