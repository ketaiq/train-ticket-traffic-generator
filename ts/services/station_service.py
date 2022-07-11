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
from ts import TIMEOUT_MAX

STATION_SERVICE_URL = "http://34.160.158.68/api/v1/stationservice/stations"

ORIGINAL_STATIONS = [
    {"id": "shanghai", "name": "Shang Hai", "stayTime": 10},
    {"id": "shanghaihongqiao", "name": "Shang Hai Hong Qiao", "stayTime": 10},
    {"id": "taiyuan", "name": "Tai Yuan", "stayTime": 5},
    {"id": "beijing", "name": "Bei Jing", "stayTime": 10},
    {"id": "nanjing", "name": "Nan Jing", "stayTime": 8},
    {"id": "shijiazhuang", "name": "Shi Jia Zhuang", "stayTime": 8},
    {"id": "xuzhou", "name": "Xu Zhou", "stayTime": 7},
    {"id": "jinan", "name": "Ji Nan", "stayTime": 5},
    {"id": "hangzhou", "name": "Hang Zhou", "stayTime": 9},
    {"id": "jiaxingnan", "name": "Jia Xing Nan", "stayTime": 2},
    {"id": "zhenjiang", "name": "Zhen Jiang", "stayTime": 2},
    {"id": "wuxi", "name": "Wu Xi", "stayTime": 3},
    {"id": "suzhou", "name": "Su Zhou", "stayTime": 3},
]
european_stations = []


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
        name=operation,
        catch_response=True,
    ) as response:
        if response.json()["msg"] != "Find all content":
            log_wrong_response_warning(
                admin_user_id, operation, response.failure, response.json()
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(admin_user_id, operation, response.failure)
        else:
            stations = response.json()["data"]
            log_response_info(admin_user_id, operation, stations)
            return stations


def get_all_stations_request(admin_user_id: str, admin_bearer: str) -> list:
    operation = "get all stations"
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
    operation = "add one station"
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
        catch_response=True,
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
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(admin_user_id, operation, response.failure)
        else:
            log_wrong_response_warning(
                admin_user_id, operation, response.failure, response.json()
            )


def add_one_station_request(
    admin_bearer: str,
    admin_user_id: str,
    new_station_id: str,
    new_station_name: str,
    stay_time: int,
) -> dict:
    operation = "add one station"
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
            return add_one_station_request(
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
    operation = "update one station"
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
        catch_response=True,
    ) as response:
        if response.json()["msg"] != "Update success":
            log_wrong_response_warning(
                admin_user_id, operation, response.failure, response.json()
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(admin_user_id, operation, response.failure)
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
    operation = "update one station"
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
    operation = "delete one station"
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
        catch_response=True,
    ) as response:
        if not response.ok:
            response.raise_for_status()
        else:
            try:
                key = "msg"
                if response.json()["msg"] != "Delete success":
                    log_wrong_response_warning(
                        admin_user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_warning(admin_user_id, operation, response.failure)
                else:
                    key = "data"
                    deleted_station = response.json()["data"]
                    log_response_info(admin_user_id, operation, deleted_station)
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")


def delete_one_station_request(
    admin_bearer: str,
    admin_user_id: str,
    station_id: str,
    station_name: str,
) -> dict:
    operation = "delete one station"
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


def restore_original_stations(admin_user_id: str, admin_bearer: str):
    stations = get_all_stations_request(admin_user_id, admin_bearer)
    for station in stations:
        if station not in ORIGINAL_STATIONS:
            deleted_station = delete_one_station_request(
                admin_bearer, admin_user_id, station["id"], station["name"]
            )
            print(f"Delete station {deleted_station}")


def _gen_random_station() -> Station:
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


def _gen_random_station_by_name(
    name: str, minimum_stay_time: int, maximum_stay_time: int
) -> Station:
    return Station(
        name.lower(), name, random.randint(minimum_stay_time, maximum_stay_time)
    )


def gen_random_station(
    name: str = "", minimum_stay_time: int = 1, maximum_stay_time: int = 20
) -> Station:
    if name == "":
        return _gen_random_station()
    else:
        return _gen_random_station_by_name(name, minimum_stay_time, maximum_stay_time)


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


def pick_random_station(all_stations: list, original_stations: list) -> Station:
    picked_station = random.choice(all_stations)
    while picked_station in original_stations:
        picked_station = random.choice(all_stations)
    return Station(
        picked_station["id"], picked_station["name"], picked_station["stayTime"]
    )


def add_stations(admin_bearer: str, admin_user_id: str, all_stations: list):
    restore_original_stations(admin_user_id, admin_bearer)
    for station in all_stations:
        new_station = add_one_station_request(
            admin_bearer, admin_user_id, station.id, station.name, station.stay_time
        )
        print(f"Add station {new_station}")


def init_european_stations(admin_user_id: str, admin_bearer: str):
    all_stations = get_all_stations_request(admin_user_id, admin_bearer)
    for station in ORIGINAL_STATIONS:
        all_stations.remove(station)
    european_stations.extend(all_stations)
    print("num of european_stations: ", len(european_stations))
