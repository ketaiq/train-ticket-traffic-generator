"""
This module includes all API calls provided by ts-inside-payment-service.
"""

from json import JSONDecodeError
from ts import TIMEOUT_MAX
from locust.exception import RescheduleTask
from ts.log_syntax.locust_response import (
    log_http_error,
    log_wrong_response_error,
    log_timeout_error,
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
        catch_response=True,
    ) as response:
        if not response.ok:
            data = f"order_id: {order_id}, trip_id: {trip_id}"
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
                key = "msg"
                if response.json()["msg"] != "Payment Success Pay Success":
                    log_wrong_response_error(
                        user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(user_id, operation, response.failure)
                else:
                    key = "data"
                    data = response.json()["data"]
                    log_response_info(user_id, operation, data)
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()
