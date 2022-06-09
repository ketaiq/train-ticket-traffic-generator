"""
This module includes all API calls provided by ts-station-service.
"""

import requests
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)
from json import JSONDecodeError
import random
import string

STATION_SERVICE_URL = "http://35.238.101.76:8080/api/v1/stationservice/stations"


class Station:
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-station-service/src/main/java/fdse/microservice/entity/Station.java
    """

    def __init__(self, id: str, name: str, stay_time: int):
        self.id = id
        self.name = name
        self.stay_time = stay_time


def get_all_stations(client, admin_bearer: str, admin_user_id: str) -> list:
    operation = "get all stations"
    with client.get(
        url="/api/v1/stationservice/stations",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        name="get all stations",
    ) as response:
        if response.json()["msg"] != "Find all content":
            log_wrong_response_warning(admin_user_id, operation, response)
        elif response.elapsed.total_seconds() > 10:
            log_timeout_warning(admin_user_id, operation, response)
        else:
            stations = response.json()["data"]
            log_response_info(admin_user_id, operation, stations)
            return stations


def get_all_stations_request(admin_user_id: str, admin_bearer: str) -> list:
    operation = "get food menu"
    r = requests.get(
        url=STATION_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Find all content":
            print(
                f"user {admin_user_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            stations = r.json()["data"]
            return stations
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def add_one_new_station(
    client,
    admin_bearer: str,
    admin_user_id: str,
    new_station_id: str,
    new_station_name: str,
    stay_time: int,
):
    operation = "add a new station"
    with client.post(
        url="/api/v1/stationservice/stations",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": new_station_id,
            "name": new_station_name,
            "stayTime": stay_time,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] == "Create success":
            new_station = response.json()["data"]
            log_response_info(admin_user_id, operation, new_station)
        elif response.json()["msg"] == "Already exists":
            id_separated_by_space = new_station_id.split()
            if len(id_separated_by_space) > 1:
                new_count = str(int(id_separated_by_space[1]) + 1)
                new_station_id = id_separated_by_space[0] + " " + new_count
                new_station_name = (
                    id_separated_by_space[0].capitalize() + " " + new_count
                )
            else:
                new_station_id = id_separated_by_space[0] + " 1"
                new_station_name = id_separated_by_space[0].capitalize() + " 1"
            add_one_new_station(
                client,
                admin_bearer,
                admin_user_id,
                new_station_id,
                new_station_name,
                stay_time,
            )
        elif response.elapsed.total_seconds() > 10:
            log_timeout_warning(admin_user_id, operation, response)
        else:
            log_wrong_response_warning(admin_user_id, operation, response)


def add_one_new_station_request(
    admin_bearer: str,
    admin_user_id: str,
    new_station_id: str,
    new_station_name: str,
    stay_time: int,
) -> dict:
    operation = "add a new station"
    r = requests.post(
        url=STATION_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": new_station_id,
            "name": new_station_name,
            "stayTime": stay_time,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg == "Create success":
            key = "data"
            new_station = r.json()["data"]
            return new_station
        elif msg == "Already exists":
            id_separated_by_space = new_station_id.split()
            if len(id_separated_by_space) > 1:
                new_count = str(int(id_separated_by_space[1]) + 1)
                new_station_id = id_separated_by_space[0] + " " + new_count
                new_station_name = (
                    id_separated_by_space[0].capitalize() + " " + new_count
                )
            else:
                new_station_id = id_separated_by_space[0] + " 1"
                new_station_name = id_separated_by_space[0].capitalize() + " 1"
            return add_one_new_station_request(
                admin_bearer,
                admin_user_id,
                new_station_id,
                new_station_name,
                stay_time,
            )
        else:
            print(
                f"user {admin_user_id} tries to {operation} but gets wrong response {msg}"
            )
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def update_one_station(
    client,
    admin_bearer: str,
    admin_user_id: str,
    station_id: str,
    new_station_name: str,
    new_station_stay_time: int,
):
    operation = "update a station"
    with client.put(
        url="/api/v1/stationservice/stations",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": station_id,
            "name": new_station_name,
            "stayTime": new_station_stay_time,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Update success":
            log_wrong_response_warning(admin_user_id, operation, response)
        elif response.elapsed.total_seconds() > 10:
            log_timeout_warning(admin_user_id, operation, response)
        else:
            updated_station = response.json()["data"]
            log_response_info(admin_user_id, operation, updated_station)


def update_one_station_request(
    admin_bearer: str,
    admin_user_id: str,
    station_id: str,
    new_station_name: str,
    new_station_stay_time: int,
) -> dict:
    operation = "update a station"
    r = requests.put(
        url=STATION_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": station_id,
            "name": new_station_name,
            "stayTime": new_station_stay_time,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Update success":
            print(
                f"user {admin_user_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            updated_station = r.json()["data"]
            return updated_station
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def delete_one_station(
    client,
    admin_bearer: str,
    admin_user_id: str,
    station_id: str,
    station_name: str,
):
    operation = "delete a station"
    with client.delete(
        url="/api/v1/stationservice/stations",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": station_id,
            "name": station_name,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Delete success":
            log_wrong_response_warning(admin_user_id, operation, response)
        elif response.elapsed.total_seconds() > 10:
            log_timeout_warning(admin_user_id, operation, response)
        else:
            deleted_station = response.json()["data"]
            log_response_info(admin_user_id, operation, deleted_station)


def delete_one_station_request(
    admin_bearer: str,
    admin_user_id: str,
    station_id: str,
    station_name: str,
) -> dict:
    operation = "update a station"
    r = requests.delete(
        url=STATION_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": station_id,
            "name": station_name,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Delete success":
            print(
                f"user {admin_user_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            deleted_station = r.json()["data"]
            return deleted_station
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def gen_random_station() -> Station:
    name_1_len = random.randint(3, 8)
    name_1 = "".join(
        random.choice(string.ascii_lowercase) for _ in range(name_1_len)
    ).capitalize()
    name_2 = ""
    name_3 = ""
    if random.randint(0, 1) == 1:
        name_2_len = random.randint(3, 8)
        name_2 = "".join(
            random.choice(string.ascii_lowercase) for _ in range(name_2_len)
        ).capitalize()
        if random.randint(0, 1) == 1:
            name_3_len = random.randint(3, 8)
            name_3 = "".join(
                random.choice(string.ascii_lowercase) for _ in range(name_3_len)
            ).capitalize()

    name = ""
    if name_2 != "" and name_3 == "":
        name = f"{name_1} {name_2}"
    elif name_2 != "" and name_3 != "":
        name = f"{name_1} {name_2} {name_3}"
    else:
        name = name_1

    return Station(name.lower(), name, random.randint(1, 20))


def gen_updated_station(station: Station) -> Station:
    original_name = station.name
    name_suffix_len = random.randint(3, 8)
    name_suffix = "".join(
        random.choice(string.ascii_lowercase) for _ in range(name_suffix_len)
    ).capitalize()
    name = ""
    name_separated_by_space = original_name.split()
    if len(name_separated_by_space) <= 2:
        name = original_name + " " + name_suffix
    else:
        name = (
            name_separated_by_space[0]
            + " "
            + name_separated_by_space[1]
            + " "
            + name_suffix
        )

    return Station(station.id, name, random.randint(1, 20))


def pick_random_station(
    client, admin_bearer: str, admin_user_id: str, original_stations: list
) -> Station:
    stations = get_all_stations(client, admin_bearer, admin_user_id)
    picked_station = random.choice(stations)
    while picked_station in original_stations:
        picked_station = random.choice(stations)
    return Station(
        picked_station["id"], picked_station["name"], picked_station["stayTime"]
    )
