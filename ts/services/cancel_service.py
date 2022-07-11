"""
This module includes all API calls provided by ts-cancel-service.
"""

from json import JSONDecodeError
import logging
from ts import TIMEOUT_MAX
from locust.exception import RescheduleTask
from ts.log_syntax.locust_response import (
    log_wrong_response_error,
    log_timeout_error,
    log_response_info,
    log_http_error,
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
        catch_response=True,
    ) as response:
        if not response.ok:
            data = f"order_id: {order_id}, user_id: {user_id}"
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
                key = "msg"
                if response.json()["msg"] != "Success.":
                    log_wrong_response_error(
                        user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(user_id, operation, response.failure)
                else:
                    log_response_info(user_id, operation, response.json())
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()


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
        catch_response=True,
    ) as response:
        if not response.ok:
            data = f"order_id: {order_id}, user_id: {user_id}"
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
                key = "msg"
                if "Success" not in response.json()["msg"]:
                    log_wrong_response_error(
                        user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(user_id, operation, response.failure)
                else:
                    key = "data"
                    refund = response.json()["data"]
                    log_response_info(user_id, operation, refund)
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()
