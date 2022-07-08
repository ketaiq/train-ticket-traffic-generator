"""
This module includes all API calls provided by ts-cancel-service.
"""

import logging
from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)


def cancel_one_order(client, bearer: str, order_id: str, user_id: str):
    operation = "cancel order"
    with client.get(
        url="/api/v1/cancelservice/cancel/" + order_id + "/" + user_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Success.":
            log_wrong_response_warning(
                user_id, operation, response.failure, response.json()
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response.failure)
        else:
            log_response_info(user_id, operation, response.json())


def get_refund_amount(client, bearer: str, order_id: str, user_id: str):
    operation = "get refund from cancelling order"
    with client.get(
        url="/api/v1/cancelservice/cancel/refound/" + order_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name=operation,
    ) as response:
        if "Success" not in response.json()["msg"]:
            log_wrong_response_warning(
                user_id, operation, response.failure, response.json()
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response.failure)
        else:
            refund = response.json()["data"]
            log_response_info(user_id, operation, refund)
