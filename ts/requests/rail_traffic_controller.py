import uuid
from ts.services.station_service import (
    gen_random_station,
    add_one_new_station,
    update_one_station,
    gen_updated_station,
    pick_random_station,
    delete_one_station,
    ORIGINAL_STATIONS,
)
from ts.services.auth_service import login_user
from ts.services.admin_route_service import (
    ORIGINAL_ROUTES,
    gen_random_route,
    get_all_stations,
    add_one_route,
    get_all_routes,
    get_reverse_route,
    pick_random_route,
    gen_updated_route,
    update_one_route,
    delete_one_route,
)


class RailTrafficControllerRequest:
    """
    - Login
    - Travel
        - Add
        - Update
        - Delete
    - Route
        - Add
        - Update
        - Delete
    - Station
        - Add
        - Update
        - Delete
    - Train
        - Add
        - Update
        - Delete
    """

    def __init__(self, client):
        self.client = client
        self.admin_bearer, self.admin_user_id = login_user(
            self.client,
            username="admin",
            password="222222",
            description="login admin user",
        )
        self.request_id = str(uuid.uuid4())
        self.original_stations = ORIGINAL_STATIONS
        self.original_routes = ORIGINAL_ROUTES

    def add_one_station(self):
        new_station = gen_random_station()
        add_one_new_station(
            self.client,
            self.admin_bearer,
            self.admin_user_id,
            new_station.id,
            new_station.name,
            new_station.stay_time,
        )

    def update_one_station(self):
        all_stations = get_all_stations(
            self.client, self.admin_bearer, self.admin_user_id
        )
        picked_station = pick_random_station(all_stations, self.original_stations)
        updated_station = gen_updated_station(picked_station)
        update_one_station(
            self.client,
            self.admin_bearer,
            self.admin_user_id,
            updated_station.id,
            updated_station.name,
            updated_station.stay_time,
        )

    def delete_one_station(self):
        all_stations = get_all_stations(
            self.client, self.admin_bearer, self.admin_user_id
        )
        picked_station = pick_random_station(all_stations, self.original_stations)
        delete_one_station(
            self.client,
            self.admin_bearer,
            self.admin_user_id,
            picked_station.id,
            picked_station.name,
        )

    def add_one_route(self):
        all_stations = get_all_stations(
            self.client, self.admin_bearer, self.admin_user_id
        )
        all_stations = [station["name"] for station in all_stations]
        new_route = gen_random_route(all_stations)
        new_route_reversed = get_reverse_route(new_route)
        add_one_route(
            self.client,
            self.admin_bearer,
            self.admin_user_id,
            new_route.stations,
            new_route.distances,
        )
        add_one_route(
            self.client,
            self.admin_bearer,
            self.admin_user_id,
            new_route_reversed.stations,
            new_route_reversed.distances,
        )

    def update_one_route(self):
        all_stations = get_all_stations(
            self.client, self.admin_bearer, self.admin_user_id
        )
        all_stations = [station["name"] for station in all_stations]
        all_routes = get_all_routes(self.client, self.admin_bearer, self.admin_user_id)
        picked_route = pick_random_route(all_routes, self.original_routes)
        updated_route = gen_updated_route(picked_route, all_stations)
        update_one_route(
            self.client,
            self.admin_bearer,
            self.admin_user_id,
            updated_route.id,
            updated_route.stations,
            updated_route.distances,
        )

    def delete_one_route(self):
        all_routes = get_all_routes(self.client, self.admin_bearer, self.admin_user_id)
        picked_route = pick_random_route(all_routes, self.original_routes)
        delete_one_route(
            self.client, self.admin_bearer, self.admin_user_id, picked_route.id
        )
