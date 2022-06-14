from re import L


from ts.services.admin_basic_service import (
    get_all_prices_request,
    add_one_price_request,
    Price,
    delete_one_price_request,
    restore_original_prices,
    ORIGINAL_PRICES,
)


def test_all(admin_bearer: str, request_id: str, assertIsInstance, assertEqual):
    _test_get_all_prices_request(admin_bearer, request_id, assertIsInstance)
    _test_add_one_price_request(admin_bearer, request_id, assertEqual)
    _test_delete_one_price_request(admin_bearer, request_id, assertEqual)
    _test_restore_original_prices(admin_bearer, request_id, assertEqual)


def _test_get_all_prices_request(admin_bearer: str, request_id: str, assertIsInstance):
    prices = get_all_prices_request(admin_bearer, request_id)
    assertIsInstance(prices, list)


def _test_add_one_price_request(admin_bearer: str, request_id: str, assertEqual):
    added_price = add_one_price_request(
        admin_bearer,
        request_id,
        Price(None, 1, 2, "0b23bd3e-876a-4af3-b920-c50a90c90b04", "G-TEST"),
    )
    assertEqual(added_price["basicPriceRate"], 1)
    assertEqual(added_price["firstClassPriceRate"], 2)
    assertEqual(added_price["routeId"], "0b23bd3e-876a-4af3-b920-c50a90c90b04")
    assertEqual(added_price["trainType"], "G-TEST")


def _test_delete_one_price_request(admin_bearer: str, request_id: str, assertEqual):
    prices = get_all_prices_request(admin_bearer, request_id)
    deleted_price = delete_one_price_request(
        admin_bearer,
        request_id,
        Price(
            prices[-1]["id"],
            prices[-1]["basicPriceRate"],
            prices[-1]["firstClassPriceRate"],
            prices[-1]["routeId"],
            prices[-1]["trainType"],
        ),
    )
    assertEqual(deleted_price["basicPriceRate"], 1)
    assertEqual(deleted_price["firstClassPriceRate"], 2)
    assertEqual(deleted_price["routeId"], "0b23bd3e-876a-4af3-b920-c50a90c90b04")
    assertEqual(deleted_price["trainType"], "G-TEST")


def _test_restore_original_prices(admin_bearer: str, request_id: str, assertEqual):
    restore_original_prices(admin_bearer, request_id)
    prices = get_all_prices_request(admin_bearer, request_id)
    assertEqual(prices, ORIGINAL_PRICES)
