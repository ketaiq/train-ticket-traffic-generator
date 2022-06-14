import pandas as pd
import re
from ts.services.station_service import gen_random_station, add_stations
from ts.services.admin_route_service import (
    Route,
    gen_random_route,
    add_routes,
)
import uuid
from ts.services.auth_service import login_user_request


def extract_stations_from_series(row: pd.Series) -> pd.Series:
    if row["Stations len"] < 3:
        row["Stations"] = [
            trim_station_tag(row["START OPK"]),
            trim_station_tag(row["END OPK"]),
        ]
    return row


def init_dataframe() -> pd.DataFrame:
    df = pd.read_csv("resources/linie.csv", sep=";", usecols=[0, 1, 2, 3, 4, 5])
    df["Stations"] = df["Line.1"].str.split(" - ")
    df["Stations len"] = df["Stations"].apply(lambda x: len(x))
    df = df.apply(extract_stations_from_series, axis=1)
    return df


def trim_station_tag(station) -> str:
    return re.sub(r"(\s\(.*\))|(\s\[.*\])", "", station)


def extract_stations(df: pd.DataFrame) -> list:
    all_stations = set(
        [
            station
            for route_stations in df["Stations"].tolist()
            for station in route_stations
        ]
    )
    return [gen_random_station(name=station) for station in all_stations]


def extract_routes_from_series(row: pd.Series) -> Route:
    return gen_random_route(
        id=row["Line"],
        stations=row["Stations"],
        km_start=row["KM START"],
        km_end=row["KM END"],
    )


def extract_routes(df: pd.DataFrame) -> list:
    routes_df = df.apply(extract_routes_from_series, axis=1)
    return routes_df.values.tolist()


def main():
    """Create stations and routes according to SBB's route network"""
    df = init_dataframe()
    all_stations = extract_stations(df)
    all_routes = extract_routes(df)
    request_id = str(uuid.uuid4())
    admin_bearer, admin_user_id = login_user_request(
        username="admin", password="222222", request_id=request_id
    )
    add_stations(admin_bearer, admin_user_id, all_stations)
    add_routes(request_id, admin_bearer, admin_user_id, all_routes)


if __name__ == "__main__":
    # main()
    print()
