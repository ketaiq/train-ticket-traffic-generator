"""
This module includes all API calls provided by ts-station-service.
"""

import logging
from locust.clients import HttpSession
import requests


def get_all_stations(client: HttpSession, admin_bearer: str, request_id: str):
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
            log = f"request {request_id} tries to get all train stations but gets wrong response"
            response.failure(log)
            logging.error(f"{log} {response.json()}")
        elif response.elapsed.total_seconds() > 10:
            log = f"request {request_id} tries to get all train stations but request takes too long!"
            response.failure(log)
            logging.warning(log)
        else:
            stations = response.json()["data"]
            logging.info(f"request {request_id} gets all train stations {stations}")


def add_one_new_station(
    client: HttpSession,
    admin_bearer: str,
    request_id: str,
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
            log = f"request {request_id} tries to {operation} but gets wrong response"
            logging.error(f"log {response.json()}")
            response.failure(log)
        elif response.elapsed.total_seconds() > 10:
            log = (
                f"request {request_id} tries to {operation} but request takes too long!"
            )
            logging.warning(log)
            response.failure(log)
        else:
            new_station = response.json()["data"]
            logging.info(f"request {request_id} {operation} {new_station}")


def update_one_station(
    client: HttpSession,
    admin_bearer: str,
    request_id: str,
    new_station_name: str,
    stay_time: int,
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
            "id": new_station_name.lower(),
            "name": new_station_name,
            "stayTime": stay_time,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Update success":
            log = f"request {request_id} tries to {operation} but gets wrong response"
            logging.error(f"log {response.json()}")
            response.failure(log)
        elif response.elapsed.total_seconds() > 10:
            log = (
                f"request {request_id} tries to {operation} but request takes too long!"
            )
            logging.warning(log)
            response.failure(log)
        else:
            station = response.json()["data"]
            logging.info(f"request {request_id} {operation} {station}")


def delete_one_station(
    client: HttpSession,
    admin_bearer: str,
    request_id: str,
    new_station_name: str,
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
            "id": new_station_name.lower(),
            "name": new_station_name,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Delete success":
            log = f"request {request_id} tries to {operation} but gets wrong response"
            logging.error(f"log {response.json()}")
            response.failure(log)
        elif response.elapsed.total_seconds() > 10:
            log = (
                f"request {request_id} tries to {operation} but request takes too long!"
            )
            logging.warning(log)
            response.failure(log)
        else:
            station = response.json()["data"]
            logging.info(f"request {request_id} {operation} {station}")
