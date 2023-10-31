from ts.services.auth_service import login_user_request
from ts.services.inside_payment_service import delete_payment_by_order_id_request


def test_delete_payment_by_order_id_request():
    admin_bearer, admin_user_id = login_user_request(
        username="admin", password="222222", request_id=0
    )
    order_id = "63e4352e-8eff-4ca7-893b-47a33476f628"
    delete_payment_by_order_id_request(admin_bearer, order_id)


test_delete_payment_by_order_id_request()
