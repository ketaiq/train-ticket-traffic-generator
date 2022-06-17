from ts.services.food_service import (
    get_all_train_and_store_food_request,
    pick_random_food,
)


def test_all(bearer: str, request_id: str, assertIsInstance, assertEqual):
    _test_get_all_train_and_store_food_request(request_id, bearer, assertIsInstance)
    _test_pick_random_food(request_id, bearer)


def _test_get_all_train_and_store_food_request(
    request_id: str, bearer: str, assertIsInstance
):
    all_food = get_all_train_and_store_food_request(
        request_id, bearer, "2022-06-15", "Shang Hai", "Su Zhou", "D1345"
    )
    assertIsInstance(all_food, dict)


def _test_pick_random_food(request_id: str, bearer: str):
    food_menu = get_all_train_and_store_food_request(request_id, bearer)
    print(pick_random_food(food_menu).__dict__)
