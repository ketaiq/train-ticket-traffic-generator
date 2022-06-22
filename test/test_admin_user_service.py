from ts.services.admin_user_service import (
    get_all_users_request,
    add_one_user_request,
    delete_one_user_request,
)


def test_all(request_id: str, admin_bearer: str, assertIsInstance, assertEqual):
    _test_get_all_users_request(admin_bearer, request_id, assertIsInstance)
    _test_add_one_user_request(admin_bearer, request_id)
    _test_delete_one_user_request(admin_bearer, request_id)


def _test_get_all_users_request(admin_bearer: str, request_id: str, assertIsInstance):
    users = get_all_users_request(admin_bearer, request_id)
    assertIsInstance(users, list)


def _test_add_one_user_request(
    admin_bearer: str,
    request_id: str,
):
    add_one_user_request(request_id, admin_bearer, "testuser", "test")


def _test_delete_one_user_request(
    admin_bearer: str,
    request_id: str,
):
    id = ""
    users = get_all_users_request(admin_bearer, request_id)
    for user in users:
        if user["userName"] == "test":
            id = user["userId"]
            break
    delete_one_user_request(request_id, admin_bearer, id)
