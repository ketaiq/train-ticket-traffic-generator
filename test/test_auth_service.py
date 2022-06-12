import uuid
from ts.services.auth_service import login_user_request


def test_all(assertIsInstance):
    _test_login_user_request(assertIsInstance)


def _test_login_user_request(assertIsInstance):
    print("Test login_user_request")
    request_id = str(uuid.uuid4())
    admin_bearer, user_id = login_user_request(
        username="admin", password="222222", request_id=request_id
    )
    print(admin_bearer)
    print(user_id)
    assertIsInstance(admin_bearer, str)
    assertIsInstance(user_id, str)
