"""
This module includes all API calls provided by ts-voucher-service.
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
        catch_response=True,
    ) as response:
        if not response.ok:
            data = f"order_id: {order_id}"
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
                key = "msg"
                if response.json()["order_id"] == order_id:
                    voucher = response.json()
                    log_response_info(user_id, operation, voucher)
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(user_id, operation, response.failure)
                else:
                    log_wrong_response_error(
                        user_id, operation, response.failure, response.json()
                    )
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()
