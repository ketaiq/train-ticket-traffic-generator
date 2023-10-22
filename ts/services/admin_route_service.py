"""
This module includes all API calls provided by ts-admin-route-service.
"""
from __future__ import annotations

import logging
import sys
import requests
from json import JSONDecodeError
from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_response_info,
    log_timeout_error,
    log_wrong_response_error,
)
from ts.services.station_service import ORIGINAL_STATIONS
from ts.errors import UndesirableResultError
import random
import uuid
import math

from ts.config import tt_host

ADMIN_ROUTE_SERVICE_URL = tt_host + "/api/v1/adminrouteservice/adminroute"

ORIGINAL_ROUTES = [
    {
        "stations": ["shanghai", "nanjing", "shijiazhuang", "taiyuan"],
        "distances": [0, 350, 1000, 1300],
        "startStationId": "shanghai",
        "terminalStationId": "taiyuan",
    },
    {
        "stations": ["nanjing", "xuzhou", "jinan", "beijing"],
        "distances": [0, 500, 700, 1200],
        "startStationId": "nanjing",
        "terminalStationId": "beijing",
    },
    {
        "stations": ["taiyuan", "shijiazhuang", "nanjing", "shanghai"],
        "distances": [0, 300, 950, 1300],
        "startStationId": "taiyuan",
        "terminalStationId": "shanghai",
    },
    {
        "stations": ["shanghai", "taiyuan"],
        "distances": [0, 1300],
        "startStationId": "shanghai",
        "terminalStationId": "taiyuan",
    },
    {
        "stations": ["shanghaihongqiao", "jiaxingnan", "hangzhou"],
        "distances": [0, 150, 300],
        "startStationId": "shanghaihongqiao",
        "terminalStationId": "hangzhou",
    },
    {
        "stations": ["nanjing", "zhenjiang", "wuxi", "suzhou", "shanghai"],
        "distances": [0, 100, 150, 200, 250],
        "startStationId": "nanjing",
        "terminalStationId": "shanghai",
    },
    {
        "stations": ["nanjing", "shanghai"],
        "distances": [0, 250],
        "startStationId": "nanjing",
        "terminalStationId": "shanghai",
    },
    {
        "stations": ["nanjing", "suzhou", "shanghai"],
        "distances": [0, 200, 250],
        "startStationId": "nanjing",
        "terminalStationId": "shanghai",
    },
    {
        "stations": ["suzhou", "shanghai"],
        "distances": [0, 50],
        "startStationId": "suzhou",
        "terminalStationId": "shanghai",
    },
    {
        "stations": ["shanghai", "suzhou"],
        "distances": [0, 50],
        "startStationId": "shanghai",
        "terminalStationId": "suzhou",
    },
]
european_routes = []


class Route:
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-admin-route-service/src/main/java/adminroute/entity/Route.java
    """

    def __init__(self, id: str | None, stations: list, distances: list):
        self.id = id
        self.stations = stations
        self.distances = distances


def get_all_routes(client, admin_bearer: str, admin_user_id: str) -> list:
    operation = "get all routes"
    with client.get(
        url="/api/v1/adminrouteservice/adminroute",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if response.json()["msg"] != "Success":
            log_wrong_response_error(
                admin_user_id, operation, response.failure, response.json()
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_error(admin_user_id, operation, response.failure)
        else:
            routes = response.json()["data"]
            log_response_info(admin_user_id, operation, routes)
            return routes


def get_all_routes_request(admin_bearer: str, request_id: str) -> list:
    print("get_all_routes_request: Start")
    operation = "get all routes"
    r = requests.get(
        url=ADMIN_ROUTE_SERVICE_URL,
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
    client,
    admin_bearer: str,
    admin_user_id: str,
    stations: list,
    distances: list,
) -> dict:
    operation = "add one route"
    with client.post(
        url="/api/v1/adminrouteservice/adminroute",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "loginId": admin_user_id,
            "id": None,
            "stationList": ",".join(stations),
            "distanceList": ",".join([str(i) for i in distances]),
            "startStation": stations[0].lower(),
            "endStation": stations[-1].lower(),
        },
        name=operation,
        catch_response=True,
    ) as response:
        if response.json()["msg"] != "Save Success":
            log_wrong_response_error(
                admin_user_id, operation, response.failure, response.json()
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_error(admin_user_id, operation, response.failure)
        else:
            new_route = response.json()["data"]
            log_response_info(admin_user_id, operation, new_route)
            return new_route


def update_one_route(
    client,
    admin_bearer: str,
    admin_user_id: str,
    route_id: str,
    stations: list,
    distances: list,
) -> dict:
    operation = "update one route"
    with client.post(
        url="/api/v1/adminrouteservice/adminroute",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "loginId": admin_user_id,
            "id": route_id,
            "stationList": ",".join(stations),
            "distanceList": ",".join([str(i) for i in distances]),
            "startStation": stations[0].lower(),
            "endStation": stations[-1].lower(),
        },
        name=operation,
        catch_response=True,
    ) as response:
        if response.json()["msg"] != "Modify success":
            log_wrong_response_error(
                admin_user_id, operation, response.failure, response.json()
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_error(admin_user_id, operation, response.failure)
        else:
            new_route = response.json()["data"]
            log_response_info(admin_user_id, operation, new_route)
            return new_route


def add_or_update_one_route_request(
    admin_bearer: str,
    request_id: str,
    user_id: str,
    route_id: str,
    stations: list,
    distances: list,
) -> dict:
    operation = "add or update one route"
    r = requests.post(
        url=ADMIN_ROUTE_SERVICE_URL,
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
            "startStation": stations[0].lower(),
            "endStation": stations[-1].lower(),
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
            return new_route
    except JSONDecodeError:
        logging.error("Response could not be decoded as JSON")
    except KeyError:
        logging.error(f"Response did not contain expected key '{key}'")


def delete_one_route(
    client,
    admin_bearer: str,
    admin_user_id: str,
    route_id: str,
) -> str:
    operation = "delete one route"
    with client.delete(
        url=f"/api/v1/adminrouteservice/adminroute/{route_id}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if response.json()["msg"] != "Delete Success":
            log_wrong_response_error(
                admin_user_id, operation, response.failure, response.json()
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_error(admin_user_id, operation, response.failure)
        else:
            deleted_route_id = response.json()["data"]
            log_response_info(admin_user_id, operation, deleted_route_id)
            return deleted_route_id


def delete_one_route_request(admin_bearer: str, request_id: str, route_id: str) -> str:
    operation = f"delete one route {route_id}"
    r = requests.delete(
        url=f"{ADMIN_ROUTE_SERVICE_URL}/{route_id}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Delete Success":
            logging.warning(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            deleted_route_id = r.json()["data"]
            logging.info(f"request {request_id} {operation}")
            return deleted_route_id
    except JSONDecodeError:
        logging.error("Response could not be decoded as JSON")
    except KeyError:
        logging.error(f"Response did not contain expected key '{key}'")


def restore_original_routes(admin_bearer: str, request_id: str):
    routes = get_all_routes_request(admin_bearer, request_id)
    for route in routes:
        route_without_id = {
            "stations": route["stations"],
            "distances": route["distances"],
            "startStationId": route["startStationId"],
            "terminalStationId": route["terminalStationId"],
        }
        if route_without_id not in ORIGINAL_ROUTES:
            deleted_route_id = delete_one_route_request(
                admin_bearer, request_id, route["id"]
            )
            print(f"Delete route {deleted_route_id}")


def gen_random_route(all_stations: list) -> Route:
    route_len = random.randint(2, 30)
    while route_len > len(all_stations):
        route_len = random.randint(2, 30)
    picked_stations = random.sample(all_stations, k=route_len)
    distances = [0]
    for _ in range(1, route_len):
        distance = random.randint(1, 1000)
        distances.append(distances[-1] + distance)

    return Route(None, picked_stations, distances)


def _gen_random_route_from_original_stations() -> Route:
    route_len = random.randint(2, 30)
    while route_len > len(ORIGINAL_STATIONS):
        route_len = random.randint(2, 30)
    picked_stations = random.sample(ORIGINAL_STATIONS, k=route_len)
    distances = [0]
    for _ in range(1, route_len):
        distance = random.randint(1, 1000)
        distances.append(distances[-1] + distance)

    return Route(str(uuid.uuid4()), picked_stations, distances)


def _gen_route_from_sbb_data(
    id: str, stations: list, km_start: float, km_end: float
) -> Route:
    distances = [0]
    distance_interval = km_end - km_start
    minimum_distance = 1
    distance_avg = int(max(minimum_distance, distance_interval / (len(stations) - 1)))
    for i in range(1, len(stations)):
        distance = random.randint(minimum_distance, distance_avg)
        if i == len(stations) - 1:
            if math.ceil(distance_interval) > distances[-1]:
                distances.append(math.ceil(distance_interval))
            else:
                distances.append(distances[-1] + 1)
        else:
            distances.append(distances[-1] + distance)
    return Route(id, stations, distances)


def _gen_route_from_euro_data(id: str, stations: list, distances: list):
    return Route(id, stations, distances)


def gen_random_route(
    id: str = str(uuid.uuid4()),
    stations: list = [],
    distances: list = [],
    km_start: float = sys.float_info.max,
    km_end: float = sys.float_info.max,
) -> Route:
    if (
        stations
        and not distances
        and km_start != sys.float_info.max
        and km_end != sys.float_info.max
    ):
        return _gen_route_from_sbb_data(id, stations, km_start, km_end)
    elif (
        stations
        and distances
        and km_start == sys.float_info.max
        and km_end == sys.float_info.max
    ):
        return _gen_route_from_euro_data(id, stations, distances)
    else:
        return _gen_random_route_from_original_stations()


def gen_updated_route(route: Route, all_stations: list) -> Route:
    stations = route.stations
    distances = route.distances
    available_stations = list(set(all_stations).difference(set(stations)))
    if random.randint(0, 1) == 1 and len(stations) > 10:
        removed_len = random.randint(1, 5)
        stations = stations[: len(stations) - removed_len]
        distances = distances[: len(distances) - removed_len]
    if random.randint(0, 1) == 1 and len(available_stations) > 0:
        added_len_max = 10
        if added_len_max > len(available_stations):
            added_len_max = len(available_stations)
        added_len = random.randint(1, added_len_max)
        added_stations = random.sample(available_stations, k=added_len)
        stations += added_stations
        for _ in range(added_len):
            distance = random.randint(1, 1000)
            distances.append(distances[-1] + distance)
    return Route(route.id, stations, distances)


def get_reverse_route(route: Route) -> Route:
    stations = route.stations[::-1]
    distances = [0]
    for i in range(len(route.distances) - 1, 0, -1):
        distances.append(distances[-1] + route.distances[i] - route.distances[i - 1])
    return Route(str(uuid.uuid4()), stations, distances)


def pick_random_route(all_routes: list, original_routes: list) -> Route:
    picked_route = random.choice(all_routes)
    while picked_route in original_routes:
        picked_route = random.choice(all_routes)
    return Route(
        picked_route["id"], picked_route["stations"], picked_route["distances"]
    )


def add_routes(
    request_id: str, admin_bearer: str, admin_user_id: str, all_routes: list
):
    restore_original_routes(admin_bearer, request_id)
    for route in all_routes:
        new_route = add_or_update_one_route_request(
            admin_bearer,
            request_id,
            admin_user_id,
            route.id,
            route.stations,
            route.distances,
        )
        print(f"Add route {new_route}")


def pick_two_random_stations_in_one_route() -> tuple[str, str]:
    from ts.services.station_service import european_stations

    results = []
    if len(european_routes) > 0:
        picked_route = random.choice(european_routes)
        picked_stations = random.sample(picked_route["stations"], k=2)
        for picked_station in picked_stations:
            for station in european_stations:
                if station["id"] == picked_station:
                    results.append(station["name"])
                    break
    else:
        raise UndesirableResultError("No routes", "at least one european route")
    if len(results) == 2:
        return results[0], results[1]
    else:
        print("picked_route: ", picked_route)
        print("picked_stations: ", picked_stations)
        raise UndesirableResultError(results, ["station A", "station B"])


def init_european_routes(admin_bearer: str, request_id: str):
    all_routes = get_all_routes_request(admin_bearer, request_id)
    new_routes = []
    for route in all_routes:
        route_without_id = {
            "stations": route["stations"],
            "distances": route["distances"],
            "startStationId": route["startStationId"],
            "terminalStationId": route["terminalStationId"],
        }
        if route_without_id not in ORIGINAL_ROUTES:
            new_routes.append(route)
    european_routes.extend(new_routes)
    print("num of european_routes: ", len(european_routes))


def init_all_routes(admin_bearer: str, request_id: str):
    print("init_all_routes function start")
    all_routes = get_all_routes_request(admin_bearer, request_id)
    european_routes.extend(all_routes)
    print("num of all routes: ", len(european_routes))
