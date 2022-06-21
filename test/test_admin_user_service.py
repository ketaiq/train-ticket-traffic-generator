from ts.services.admin_user_service import get_all_users_request


def test_all(request_id: str, admin_bearer: str, assertIsInstance, assertEqual):
    _test_get_all_users_request(admin_bearer, request_id)


def _test_get_all_users_request(admin_bearer: str, request_id: str, assertIsInstance):
    users = get_all_users_request(admin_bearer, request_id)
    assertIsInstance(users, list)
