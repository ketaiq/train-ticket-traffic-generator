from ts.services.food_map_service import (
    get_all_food_stores_request,
    get_train_food_in_one_trip_request,
)


def test_all(request_id: str, assertIsInstance, assertEqual):
    _test_get_all_food_stores_request(request_id, assertIsInstance)
    _test_get_train_food_in_one_trip(request_id, assertIsInstance)


def _test_get_all_food_stores_request(request_id: str, assertIsInstance):
    food_stores = get_all_food_stores_request(request_id)
    print(food_stores)
    assertIsInstance(food_stores, list)


def _test_get_train_food_in_one_trip(request_id: str, assertIsInstance):
    train_food = get_train_food_in_one_trip_request(request_id, "G-TEST")
    assertIsInstance(train_food, list)

