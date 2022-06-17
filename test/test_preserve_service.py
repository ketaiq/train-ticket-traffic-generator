from ts.services.preserve_service import reserve_one_ticket_request
from ts.services.food_service import Food
from ts.services.consign_service import Consign


def test_all(request_id: str, bearer: str, user_id: str, assertIsInstance, assertEqual):
    _test_reserve_one_ticket_request(request_id, bearer, user_id, assertEqual)


def _test_reserve_one_ticket_request(
    request_id: str, bearer: str, user_id: str, assertEqual
):
    result = reserve_one_ticket_request(
        request_id,
        bearer,
        user_id,
        "3fcb512a-339d-4cf2-ad62-744558353adb",
        "G-37EuroCity151",
        "2",
        "2022-10-17",
        "Lugano",
        "Monza",
        "0",
        Food(
            "",
            0,
            "",
            "",
            0,
        ),
        Consign("", "", 0),
    )
    assertEqual(result, "Success")
