from ts.services.station_service import (
    ORIGINAL_STATIONS,
    get_all_stations_request,
    add_one_station_request,
    update_one_station_request,
    delete_one_station_request,
    gen_random_station,
    restore_original_stations,
)


def test_all(admin_bearer, admin_user_id, assertIsInstance, assertEqual):
    _test_get_all_stations_request(admin_bearer, admin_user_id, assertIsInstance)
    _test_add_one_new_station_request(admin_bearer, admin_user_id, assertIsInstance)
    _test_update_one_station_request(admin_bearer, admin_user_id, assertIsInstance)
    _test_delete_one_station_request(admin_bearer, admin_user_id, assertIsInstance)
    _test_gen_random_station()
    # _test_restore_original_stations(admin_bearer, admin_user_id, assertEqual)


def _test_get_all_stations_request(
    admin_bearer: str, admin_user_id: str, assertIsInstance
):
    print("Test get_all_stations_request")
    stations = get_all_stations_request(admin_user_id, admin_bearer)
    print(stations)
    assertIsInstance(stations, list)


def _test_add_one_new_station_request(
    admin_bearer: str, admin_user_id: str, assertIsInstance
):
    print("Test add_one_new_station_request")
    added_station = add_one_station_request(
        admin_bearer, admin_user_id, "lugano", "Lugano", 5
    )
    print(added_station)
    assertIsInstance(added_station, dict)


def _test_update_one_station_request(
    admin_bearer: str, admin_user_id: str, assertIsInstance
):
    print("Test update_one_station_request")
    updated_station = update_one_station_request(
        admin_bearer, admin_user_id, "lugano", "New Lugano", 10
    )
    print(updated_station)
    assertIsInstance(updated_station, dict)


def _test_delete_one_station_request(
    admin_bearer: str, admin_user_id: str, assertIsInstance
):
    print("Test delete_one_station_request")
    deleted_station = delete_one_station_request(
        admin_bearer, admin_user_id, "lugano", "New Lugano"
    )
    print(deleted_station)
    assertIsInstance(deleted_station, dict)


def _test_gen_random_station():
    print("Test gen_random_station")
    print(gen_random_station().__dict__)


# def _test_restore_original_stations(admin_bearer: str, admin_user_id: str, assertEqual):
#     print("Test restore_original_stations")
#     restore_original_stations(admin_user_id, admin_bearer)
#     stations = get_all_stations_request(admin_user_id, admin_bearer)
#     assertEqual(stations, ORIGINAL_STATIONS)
