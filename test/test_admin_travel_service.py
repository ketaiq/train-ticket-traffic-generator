from ts.services.admin_travel_service import (
    get_all_travels_request,
    add_one_travel_request,
    Travel,
    delete_one_travel_request,
)


def test_all(admin_bearer: str, request_id: str, assertIsInstance, assertEqual):
    _test_get_all_travels_request(admin_bearer, request_id, assertIsInstance)
    _test_add_one_travel_request(admin_bearer, request_id, assertEqual)
    _test_delete_one_travel_request(admin_bearer, request_id, assertEqual)


def _test_get_all_travels_request(admin_bearer: str, request_id: str, assertIsInstance):
    travels = get_all_travels_request(admin_bearer, request_id)
    assertIsInstance(travels, list)
    print(travels)


def _test_add_one_travel_request(admin_bearer: str, request_id: str, assertEqual):
    new_travel = Travel("TEST00", "GaoTieOne", "92708982-77af-4318-be25-57ccb0ff69ad")
    r = add_one_travel_request(admin_bearer, request_id, new_travel)
    assertEqual(r, None)


def _test_delete_one_travel_request(admin_bearer: str, request_id: str, assertEqual):
    id = delete_one_travel_request(admin_bearer, request_id, "G-TEST00")
    assertEqual(id, "G-TEST00")
