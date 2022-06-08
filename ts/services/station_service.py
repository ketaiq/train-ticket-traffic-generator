"""
This module includes all API calls provided by ts-station-service.
"""

import logging
import requests
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)
from json import JSONDecodeError


def get_all_stations(client, admin_bearer: str, admin_user_id: str):
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


def get_all_stations_request(admin_user_id: str, admin_bearer: str) -> list:
    operation = "get food menu"
    r = requests.get(
        url="http://35.238.101.76:8080/api/v1/stationservice/stations",
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
            "id": new_station_name.lower(),
            "name": new_station_name,
            "stayTime": stay_time,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Create success":
            log_wrong_response_warning(admin_user_id, operation, response)
        elif response.elapsed.total_seconds() > 10:
            log_timeout_warning(admin_user_id, operation, response)
        else:
            new_station = response.json()["data"]
            log_response_info(admin_user_id, operation, new_station)


def add_one_new_station_request(
    admin_bearer: str,
    admin_user_id: str,
    new_station_name: str,
    stay_time: int,
) -> dict:
    operation = "add a new station"
    r = requests.post(
        url="http://35.238.101.76:8080/api/v1/stationservice/stations",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": new_station_name.lower(),
            "name": new_station_name,
            "stayTime": stay_time,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Create success":
            print(
                f"user {admin_user_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            new_station = r.json()["data"]
            return new_station
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
        url="http://35.238.101.76:8080/api/v1/stationservice/stations",
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
        url="http://35.238.101.76:8080/api/v1/stationservice/stations",
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
