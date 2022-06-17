import uuid
from ts.services.station_service import ORIGINAL_STATIONS
from ts.services.admin_route_service import (
    get_all_routes_request,
    restore_original_routes,
    ORIGINAL_ROUTES,
    add_or_update_one_route_request,
    gen_random_route,
    delete_one_route_request,
    gen_updated_route,
    Route,
)


def test_all(
    admin_bearer: str,
    admin_user_id: str,
    request_id: str,
    assertIsInstance,
    assertEqual,
):
    _test_get_routes(admin_bearer, request_id, assertIsInstance)
    _test_add_one_route(admin_bearer, request_id, admin_user_id, assertEqual)
    _test_update_one_route(
        admin_bearer,
        request_id,
        admin_user_id,
        assertIsInstance,
        assertEqual,
    )
    _test_delete_one_route(admin_bearer, request_id, assertEqual)
    _test_gen_random_route(assertIsInstance, assertEqual)
    _test_gen_updated_route(assertIsInstance, assertEqual)
    # _test_restore_original_routes(admin_bearer, request_id, assertEqual)


def _test_get_routes(admin_bearer: str, request_id: str, assertIsInstance):
    print("Test get_routes")
    routes = get_all_routes_request(admin_bearer, request_id)
    print(routes)
    assertIsInstance(routes, list)


def _test_add_one_route(
    admin_bearer: str, request_id: str, admin_user_id: str, assertEqual
):
    print("Test add_one_route")
    new_route = {
        "id": "e18c9ae5-610b-4cda-a990-65081e64ec8d",
        "stations": ["wu xi", "ji nan", "nan jing"],
        "distances": [0, 395, 638],
        "startStationId": "wu xi",
        "terminalStationId": "nan jing",
    }
    added_route = add_or_update_one_route_request(
        admin_bearer,
        request_id,
        admin_user_id,
        new_route["id"],
        new_route["stations"],
        new_route["distances"],
    )
    print(added_route)
    assertEqual(new_route, added_route)


def _test_update_one_route(
    admin_bearer: str,
    request_id: str,
    admin_user_id: str,
    assertIsInstance,
    assertEqual,
):
    print("Test update_one_route")
    new_route = {
        "id": "e18c9ae5-610b-4cda-a990-65081e64ec8d",
        "stations": ["schaffhausen", "singen", "konstanz"],
        "distances": [0, 100, 200],
        "startStationId": "schaffhausen",
        "terminalStationId": "konstanz",
    }
    updated_route = add_or_update_one_route_request(
        admin_bearer,
        request_id,
        admin_user_id,
        new_route["id"],
        new_route["stations"],
        new_route["distances"],
    )
    print(updated_route)
    assertIsInstance(updated_route, dict)
    assertEqual(new_route, updated_route)


def _test_delete_one_route(admin_bearer: str, request_id: str, assertEqual):
    print("Test delete_one_route")
    deleted_route_id = delete_one_route_request(
        admin_bearer, request_id, "e18c9ae5-610b-4cda-a990-65081e64ec8d"
    )
    print(deleted_route_id)
    assertEqual(deleted_route_id, "e18c9ae5-610b-4cda-a990-65081e64ec8d")


def _test_gen_random_route(assertIsInstance, assertEqual):
    print("Test gen_random_route")
    route = gen_random_route()
    print(route.__dict__)
    assertIsInstance(route, Route)
    assertEqual(len(route.stations), len(route.distances))


def _test_gen_updated_route(assertIsInstance, assertEqual):
    print("Test gen_updated_route")
    original_route = Route(
        str(uuid.uuid4()),
        ["schaffhausen", "singen", "konstanz"],
        [0, 100, 200],
    )
    original_stations = ORIGINAL_STATIONS
    original_stations = [station["name"] for station in original_stations]
    updated_route = gen_updated_route(original_route, original_stations)
    print(updated_route.__dict__)
    assertIsInstance(updated_route, Route)
    assertEqual(len(updated_route.stations), len(updated_route.distances))


def _test_restore_original_routes(admin_bearer: str, request_id: str, assertEqual):
    print("Test restore_original_routes")
    restore_original_routes(admin_bearer, request_id)
    routes = get_all_routes_request(admin_bearer, request_id)
    assertEqual(routes, ORIGINAL_ROUTES)
