"""
This module includes all API calls provided by ts-voucher-service.
"""

from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)


def get_one_voucher(client, bearer: str, user_id: str, order_id: str):
    operation = "print voucher"
    with client.post(
        url="/getVoucher",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={"orderId": order_id, "type": 1},
        name=operation,
    ) as response:
        if response.json()["order_id"] == order_id:
            voucher = response.json()
            log_response_info(user_id, operation, voucher)
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response.failure)
        else:
            log_wrong_response_warning(
                user_id, operation, response.failure, response.json()
            )