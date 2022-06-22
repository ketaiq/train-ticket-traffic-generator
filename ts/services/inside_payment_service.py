"""
This module includes all API calls provided by ts-inside-payment-service.
"""

from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)


def pay_one_order(client, bearer: str, user_id: str, order_id: str, trip_id: str):
    operation = "pay order"
    with client.post(
        url="/api/v1/inside_pay_service/inside_payment",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={"orderId": order_id, "tripId": trip_id},
        name=operation,
    ) as response:
        if response.json()["msg"] != "Payment Success Pay Success":
            log_wrong_response_warning(user_id, operation, response)
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response)
        else:
            data = response.json()["data"]
            log_response_info(user_id, operation, data)
