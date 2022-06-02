"""
This module includes all API calls provided by ts-admin-route-service.
"""

import logging
import requests
from json import JSONDecodeError

url = "http://35.238.101.76:8080/api/v1/adminrouteservice/adminroute"


def get_routes(admin_bearer: str, request_id: str) -> list:
    operation = "get all routes"
    r = requests.get(
        url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        if r.json()["msg"] != "Success":
            logging.warning(
                f"request {request_id} tries to {operation} but gets wrong response"
            )
        else:
            key = "data"
            return r.json()["data"]
    except JSONDecodeError:
        logging.error("Response could not be decoded as JSON")
    except KeyError:
        logging.error(f"Response did not contain expected key '{key}'")


def add_one_route(
    admin_bearer: str,
    request_id: str,
    user_id: str,
    route_id: str,
    stations: list,
    distances: list,
):
    operation = "add one route"
    r = requests.post(
        url,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "loginId": user_id,
            "id": route_id,
            "stationList": ",".join(stations),
            "distanceList": ",".join([str(i) for i in distances]),
            "startStation": stations[0],
            "endStation": stations[-1],
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if "success" not in msg.lower():
            logging.warning(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            new_route = r.json()["data"]
            logging.info(f"request {request_id} {operation} {new_route}")
    except JSONDecodeError:
        logging.error("Response could not be decoded as JSON")
    except KeyError:
        logging.error(f"Response did not contain expected key '{key}'")


def delete_one_route(admin_bearer: str, request_id: str, route_id: str):
    operation = f"delete one route {route_id}"
    r = requests.delete(
        f"{url}/{route_id}",
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
            logging.warning(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            logging.info(f"request {request_id} {operation}")
    except JSONDecodeError:
        logging.error("Response could not be decoded as JSON")
    except KeyError:
        logging.error(f"Response did not contain expected key '{key}'")


if __name__ == "__main__":
    from auth_service import login_user_request
    import uuid

    request_id = str(uuid.uuid4())
    admin_bearer, user_id = login_user_request(
        username="admin", password="222222", request_id=request_id
    )

    print(get_routes(admin_bearer, request_id))
    route_id = str(uuid.uuid4())
    add_one_route(
        admin_bearer,
        request_id,
        user_id,
        route_id,
        ["Schaffhausen", "Singen", "Konstanz"],
        [0, 100, 200],
    )
    delete_one_route(admin_bearer, request_id, route_id)
