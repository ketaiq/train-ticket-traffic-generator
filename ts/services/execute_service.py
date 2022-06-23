"""
This module includes all API calls provided by ts-execute-service.
"""
from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)


def collect_one_ticket(client, bearer: str, user_id: str, order_id: str):
    operation = "collect ticket"
    with client.get(
        url="/api/v1/executeservice/execute/collected/" + order_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Success":
            log_wrong_response_warning(user_id, operation, response.failure, response.json())
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response.failure)
        else:
            data = response.json()["data"]
            log_response_info(user_id, operation, data)


def enter_station(client, bearer: str, user_id: str, order_id: str):
    operation = "enter station"
    with client.get(
        url="/api/v1/executeservice/execute/execute/" + order_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Success.":
            log_wrong_response_warning(user_id, operation, response.failure, response.json())
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response.failure)
        else:
            data = response.json()["data"]
            log_response_info(user_id, operation, data)
