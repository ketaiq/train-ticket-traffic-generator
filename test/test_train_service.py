from ts.services.train_service import (
    get_all_trains_request,
    add_one_train_request,
    gen_random_train,
    delete_one_train_request,
)


def test_all(admin_bearer: str, request_id: str, assertIsInstance, assertEqual):
    _test_get_all_trains_request(admin_bearer, request_id, assertIsInstance)
    _test_add_one_train_request(admin_bearer, request_id, assertEqual)
    _test_delete_one_train_request(admin_bearer, request_id, assertEqual)


def _test_get_all_trains_request(admin_bearer: str, request_id: str, assertIsInstance):
    trains = get_all_trains_request(admin_bearer, request_id)
    assertIsInstance(trains, list)
    print(trains)


def _test_add_one_train_request(admin_bearer: str, request_id: str, assertEqual):
    new_train = gen_random_train("TestTrain")
    r = add_one_train_request(admin_bearer, request_id, new_train)
    assertEqual(r, None)


def _test_delete_one_train_request(admin_bearer: str, request_id: str, assertEqual):
    r = delete_one_train_request(admin_bearer, request_id, "TestTrain")
    assertEqual(r, True)
