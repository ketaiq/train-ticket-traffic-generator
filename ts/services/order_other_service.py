from json import JSONDecodeError
import logging
from ts import TIMEOUT_MAX
from locust.exception import RescheduleTask
from ts.log_syntax.locust_response import (
    log_http_error,
    log_timeout_error,
    log_response_info,
)

def refresh_user_other_orders(client, user_id: str, bearer: str) -> list:
    operation = "refresh user other orders"
    with client.post(
        url="/api/v1/orderOtherService/orderOther/refresh",
        name=operation,
        catch_response=True,
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
        if not response.ok:
            data = f"user_id: {user_id}"
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
                res_json = response.json()
                msg = res_json["msg"]
                status = res_json["status"]
                orders = res_json["data"]
                if status == "1":
                    log_response_info(user_id, operation, orders)
                    return orders
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(user_id, operation, response.failure)
                else:
                    logging.warning(
                        f"User {user_id} tries to {operation} but gets {msg}."
                    )
            except JSONDecodeError:
                logging.error(f"Response {response.text} could not be decoded as JSON!")
                raise RescheduleTask()
