"""
This module includes all API calls provided by ts-execute-service.
"""
from json import JSONDecodeError
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
        catch_response=True,
    ) as response:
        if not response.ok():
            response.raise_for_status()
        else:
            try:
                key = "msg"
                if response.json()["msg"] != "Success":
                    log_wrong_response_warning(
                        user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_warning(user_id, operation, response.failure)
                else:
                    key = "data"
                    data = response.json()["data"]
                    log_response_info(user_id, operation, data)
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")


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
        catch_response=True,
    ) as response:
        if not response.ok():
            response.raise_for_status()
        else:
            try:
                key = "msg"
                if response.json()["msg"] != "Success.":
                    log_wrong_response_warning(
                        user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_warning(user_id, operation, response.failure)
                else:
                    key = "data"
                    data = response.json()["data"]
                    log_response_info(user_id, operation, data)
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
