"""
This module includes all API calls provided by ts-order-service.
"""

from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)


def get_orders_by_login_id(client, user_id: str, bearer: str) -> list:
    operation = "search orders"
    with client.post(
        url="/api/v1/orderservice/order/refresh",
        name=operation,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={
            "loginId": user_id,
            "enableStateQuery": "false",
            "enableTravelDateQuery": "false",
            "enableBoughtDateQuery": "false",
            "travelDateStart": "null",
            "travelDateEnd": "null",
            "boughtDateStart": "null",
            "boughtDateEnd": "null",
        },
    ) as response:
        if response.json()["msg"] != "Query Orders For Refresh Success":
            log_wrong_response_warning(user_id, operation, response)
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response)
        else:
            orders = response.json()["data"]
            log_response_info(user_id, operation, orders)
            return orders