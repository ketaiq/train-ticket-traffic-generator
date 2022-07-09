import pandas as pd
import json
import math
import uuid
from ts.services.station_service import gen_random_station, add_stations
from ts.services.admin_route_service import (
    gen_random_route,
    Route,
    add_routes,
    get_reverse_route,
)
from ts.services.auth_service import login_user_request
from ts.services.train_service import gen_random_train, add_trains
from ts.services.admin_travel_service import Travel, add_travels
from ts.services.admin_basic_service import add_prices
from ts.services.food_map_service import add_food
from unidecode import unidecode
import re


def init_dataframe() -> pd.DataFrame:
    df = pd.read_csv(
        "resources/direktverbindungen.csv", sep=";", usecols=[2, 3, 14, 15, 16]
    )
    df["vias"] = (
        df["vias"]
        .str.split(";")
        .apply(lambda cell: [json.loads(station) for station in cell])
    )
    df["stations"] = df["vias"].apply(
        lambda cell: [
            re.sub("[^\w\s]+", "", unidecode(station["station_name"]))
            for station in cell
        ]
    )
    df["distances"] = df["vias"].apply(extract_distances)
    routes_series = df.apply(extract_routes_from_series, axis=1)
    reversed_routes_series = routes_series.apply(get_reverse_route)
    df = df.assign(routes=routes_series, reversed_routes=reversed_routes_series)
    df["tripname"] = [
        "RailjetXpress",
        "InterCity",
        "EuroCity311",
        "EuroCity151",
        "Nightjet402",
        "Nightjet40470",
        "ICE102",
        "EuroCity",
        "ICE74",
        "ICE70",
        "ICE104",
        "EuroCity163",
        "Nightjet465",
        "RailjetXpress",
        "EuroCity",
        "TGV",
        "EuroNight40465",
        "EuroCity151",
        "EuroCity",
        "TGV",
        "TGV",
        "EuroNight40467",
        "TGV",
        "EuroCity327",
        "RailjetXpress",
        "EuroCity52",
        "EuroCity",
        "Nightjet467",
        "EuroCity",
        "EuroCity",
        "EuroCity",
        "EuroCity307",
        "ICE",
        "EuroNight50467",
        "EuroCity",
        "Nightjet470",
    ]
    return df.drop(columns=["vias"])


def calculate_distance(coordinate_1, coordinate_2) -> int:
    return int(
        math.sqrt(
            (coordinate_1[0] - coordinate_2[0]) ** 2
            + (coordinate_1[1] - coordinate_2[1]) ** 2
        )
        / 1000
    )


def extract_distances(vias: list) -> list:
    distances = [0]
    for i in range(len(vias) - 1):
        distance = calculate_distance(
            vias[i]["coordinates"], vias[i + 1]["coordinates"]
        )
        distances.append(distances[-1] + distance)
    return distances


def extract_stations(df: pd.DataFrame) -> list:
    all_stations = set(
        [
            station
            for route_stations in df["stations"].tolist()
            for station in route_stations
        ]
    )
    return [gen_random_station(station, 10, 20) for station in all_stations]


def extract_routes_from_series(row: pd.Series) -> Route:
    return gen_random_route(
        id=str(uuid.uuid4()),
        stations=[station.lower() for station in row["stations"]],
        distances=row["distances"],
    )


def extract_routes(df: pd.DataFrame) -> list:
    return df["routes"].values.tolist() + df["reversed_routes"].values.tolist()


def extract_trains(df: pd.DataFrame) -> list:
    trains = df["name"].apply(lambda x: "G-" + x.split()[0]).unique()
    return [gen_random_train(train) for train in trains]


def extract_travels_from_series(row: pd.Series) -> list:
    return [
        Travel(
            str(row["id"]) + row["tripname"],
            "G-" + row["name"].split()[0],
            row["routes"].id,
        ),
        Travel(
            str(row["id"]) + "R" + row["tripname"],
            "G-" + row["name"].split()[0],
            row["reversed_routes"].id,
        ),
    ]


def extract_travels(df: pd.DataFrame) -> list:
    travels_df = df.apply(extract_travels_from_series, axis=1)
    return [travel for row in travels_df.values.tolist() for travel in row]


def main():
    """Create stations and routes according to Direct Trains in Europe"""
    df = init_dataframe()
    all_stations = extract_stations(df)  # 203
    all_routes = extract_routes(df)  # 72
    all_trains = extract_trains(df)  # 7
    all_travels = extract_travels(df)  # 72
    request_id = str(uuid.uuid4())
    admin_bearer, admin_user_id = login_user_request(
        username="admin", password="222222", request_id=request_id
    )
    add_stations(admin_bearer, admin_user_id, all_stations)
    add_routes(request_id, admin_bearer, admin_user_id, all_routes)
    add_trains(request_id, admin_bearer, all_trains)
    add_prices(request_id, admin_bearer, all_travels)
    add_travels(request_id, admin_bearer, all_travels)
    add_food(all_travels, all_stations)


if __name__ == "__main__":
    main()
