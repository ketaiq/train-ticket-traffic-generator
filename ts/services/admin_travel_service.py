"""
This module includes all API calls provided by ts-admin-travel-service.
"""

import requests
import time
import random
from json import JSONDecodeError

ADMIN_TRAVEL_SERVICE_URL = (
    "http://130.211.196.121:8080/api/v1/admintravelservice/admintravel"
)
ORIGINAL_TRAVELS = [
    {
        "trip": {
            "tripId": {"type": "G", "number": "1234"},
            "trainTypeId": "GaoTieOne",
            "routeId": "92708982-77af-4318-be25-57ccb0ff69ad",
            "startingStationId": "shanghai",
            "stationsId": "suzhou",
            "terminalStationId": "taiyuan",
            "startingTime": 1367629200000,
            "endTime": 1367653912000,
        },
        "trainType": {
            "id": "GaoTieOne",
            "economyClass": 2147483647,
            "confortClass": 2147483647,
            "averageSpeed": 250,
        },
        "route": {
            "id": "92708982-77af-4318-be25-57ccb0ff69ad",
            "stations": ["nanjing", "zhenjiang", "wuxi", "suzhou", "shanghai"],
            "distances": [0, 100, 150, 200, 250],
            "startStationId": "nanjing",
            "terminalStationId": "shanghai",
        },
    },
    {
        "trip": {
            "tripId": {"type": "G", "number": "1235"},
            "trainTypeId": "GaoTieOne",
            "routeId": "aefcef3f-3f42-46e8-afd7-6cb2a928bd3d",
            "startingStationId": "shanghai",
            "stationsId": "suzhou",
            "terminalStationId": "taiyuan",
            "startingTime": 1367640000000,
            "endTime": 1367661112000,
        },
        "trainType": {
            "id": "GaoTieOne",
            "economyClass": 2147483647,
            "confortClass": 2147483647,
            "averageSpeed": 250,
        },
        "route": {
            "id": "aefcef3f-3f42-46e8-afd7-6cb2a928bd3d",
            "stations": ["nanjing", "shanghai"],
            "distances": [0, 250],
            "startStationId": "nanjing",
            "terminalStationId": "shanghai",
        },
    },
    {
        "trip": {
            "tripId": {"type": "G", "number": "1236"},
            "trainTypeId": "GaoTieOne",
            "routeId": "a3f256c1-0e43-4f7d-9c21-121bf258101f",
            "startingStationId": "shanghai",
            "stationsId": "suzhou",
            "terminalStationId": "taiyuan",
            "startingTime": 1367647200000,
            "endTime": 1367671912000,
        },
        "trainType": {
            "id": "GaoTieOne",
            "economyClass": 2147483647,
            "confortClass": 2147483647,
            "averageSpeed": 250,
        },
        "route": {
            "id": "a3f256c1-0e43-4f7d-9c21-121bf258101f",
            "stations": ["nanjing", "suzhou", "shanghai"],
            "distances": [0, 200, 250],
            "startStationId": "nanjing",
            "terminalStationId": "shanghai",
        },
    },
    {
        "trip": {
            "tripId": {"type": "G", "number": "1237"},
            "trainTypeId": "GaoTieTwo",
            "routeId": "084837bb-53c8-4438-87c8-0321a4d09917",
            "startingStationId": "shanghai",
            "stationsId": "suzhou",
            "terminalStationId": "taiyuan",
            "startingTime": 1367625600000,
            "endTime": 1367659312000,
        },
        "trainType": {
            "id": "GaoTieTwo",
            "economyClass": 2147483647,
            "confortClass": 2147483647,
            "averageSpeed": 200,
        },
        "route": {
            "id": "084837bb-53c8-4438-87c8-0321a4d09917",
            "stations": ["suzhou", "shanghai"],
            "distances": [0, 50],
            "startStationId": "suzhou",
            "terminalStationId": "shanghai",
        },
    },
    {
        "trip": {
            "tripId": {"type": "D", "number": "1345"},
            "trainTypeId": "DongCheOne",
            "routeId": "f3d4d4ef-693b-4456-8eed-59c0d717dd08",
            "startingStationId": "shanghai",
            "stationsId": "suzhou",
            "terminalStationId": "taiyuan",
            "startingTime": 1367622000000,
            "endTime": 1367668792000,
        },
        "trainType": {
            "id": "DongCheOne",
            "economyClass": 2147483647,
            "confortClass": 2147483647,
            "averageSpeed": 180,
        },
        "route": {
            "id": "f3d4d4ef-693b-4456-8eed-59c0d717dd08",
            "stations": ["shanghai", "suzhou"],
            "distances": [0, 50],
            "startStationId": "shanghai",
            "terminalStationId": "suzhou",
        },
    },
    {
        "trip": {
            "tripId": {"type": "Z", "number": "1234"},
            "trainTypeId": "ZhiDa",
            "routeId": "0b23bd3e-876a-4af3-b920-c50a90c90b04",
            "startingStationId": "shanghai",
            "stationsId": "nanjing",
            "terminalStationId": "beijing",
            "startingTime": 1367632312000,
            "endTime": 1367653912000,
        },
        "trainType": {
            "id": "ZhiDa",
            "economyClass": 2147483647,
            "confortClass": 2147483647,
            "averageSpeed": 120,
        },
        "route": {
            "id": "0b23bd3e-876a-4af3-b920-c50a90c90b04",
            "stations": ["shanghai", "nanjing", "shijiazhuang", "taiyuan"],
            "distances": [0, 350, 1000, 1300],
            "startStationId": "shanghai",
            "terminalStationId": "taiyuan",
        },
    },
    {
        "trip": {
            "tripId": {"type": "Z", "number": "1235"},
            "trainTypeId": "ZhiDa",
            "routeId": "9fc9c261-3263-4bfa-82f8-bb44e06b2f52",
            "startingStationId": "shanghai",
            "stationsId": "nanjing",
            "terminalStationId": "beijing",
            "startingTime": 1367638312000,
            "endTime": 1367661112000,
        },
        "trainType": {
            "id": "ZhiDa",
            "economyClass": 2147483647,
            "confortClass": 2147483647,
            "averageSpeed": 120,
        },
        "route": {
            "id": "9fc9c261-3263-4bfa-82f8-bb44e06b2f52",
            "stations": ["nanjing", "xuzhou", "jinan", "beijing"],
            "distances": [0, 500, 700, 1200],
            "startStationId": "nanjing",
            "terminalStationId": "beijing",
        },
    },
    {
        "trip": {
            "tripId": {"type": "Z", "number": "1236"},
            "trainTypeId": "ZhiDa",
            "routeId": "d693a2c5-ef87-4a3c-bef8-600b43f62c68",
            "startingStationId": "shanghai",
            "stationsId": "nanjing",
            "terminalStationId": "beijing",
            "startingTime": 1367622352000,
            "endTime": 1367643112000,
        },
        "trainType": {
            "id": "ZhiDa",
            "economyClass": 2147483647,
            "confortClass": 2147483647,
            "averageSpeed": 120,
        },
        "route": {
            "id": "d693a2c5-ef87-4a3c-bef8-600b43f62c68",
            "stations": ["taiyuan", "shijiazhuang", "nanjing", "shanghai"],
            "distances": [0, 300, 950, 1300],
            "startStationId": "taiyuan",
            "terminalStationId": "shanghai",
        },
    },
    {
        "trip": {
            "tripId": {"type": "T", "number": "1235"},
            "trainTypeId": "TeKuai",
            "routeId": "20eb7122-3a11-423f-b10a-be0dc5bce7db",
            "startingStationId": "shanghai",
            "stationsId": "nanjing",
            "terminalStationId": "beijing",
            "startingTime": 1367627512000,
            "endTime": 1367659312000,
        },
        "trainType": {
            "id": "TeKuai",
            "economyClass": 2147483647,
            "confortClass": 2147483647,
            "averageSpeed": 120,
        },
        "route": {
            "id": "20eb7122-3a11-423f-b10a-be0dc5bce7db",
            "stations": ["shanghai", "taiyuan"],
            "distances": [0, 1300],
            "startStationId": "shanghai",
            "terminalStationId": "taiyuan",
        },
    },
    {
        "trip": {
            "tripId": {"type": "K", "number": "1345"},
            "trainTypeId": "KuaiSu",
            "routeId": "1367db1f-461e-4ab7-87ad-2bcc05fd9cb7",
            "startingStationId": "shanghai",
            "stationsId": "nanjing",
            "terminalStationId": "beijing",
            "startingTime": 1367625112000,
            "endTime": 1367668792000,
        },
        "trainType": {
            "id": "KuaiSu",
            "economyClass": 2147483647,
            "confortClass": 2147483647,
            "averageSpeed": 90,
        },
        "route": {
            "id": "1367db1f-461e-4ab7-87ad-2bcc05fd9cb7",
            "stations": ["shanghaihongqiao", "jiaxingnan", "hangzhou"],
            "distances": [0, 150, 300],
            "startStationId": "shanghaihongqiao",
            "terminalStationId": "hangzhou",
        },
    },
]


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
        time_offset = random.randint(0, 6 * 60 * 60)
        time_op = random.randint(0, 1)
        if time_op == 0:
            self.start_time = int((time.time() + time_offset) * 1000)
        else:
            self.start_time = int((time.time() - time_offset) * 1000)
        self.end_time = self.start_time + int(
            random.randint(3 * 60 * 60, 8 * 60 * 60) * 1000
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


def restore_original_travels(
    admin_bearer: str,
    request_id: str,
):
    travels = get_all_travels_request(admin_bearer, request_id)
    for travel in travels:
        if travel not in ORIGINAL_TRAVELS:
            id = travel["trip"]["tripId"]
            if id["type"]:
                id = id["type"] + id["number"]
            else:
                id = "G" + id["number"]
            deleted_id = delete_one_travel_request(admin_bearer, request_id, id)
            if deleted_id == id:
                print(f"Delete travel {deleted_id}")


def add_travels(request_id: str, admin_bearer: str, all_travels: list):
    restore_original_travels(admin_bearer, request_id)
    for travel in all_travels:
        add_one_travel_request(admin_bearer, request_id, travel)
        print(f"Add travel {travel.__dict__}")
