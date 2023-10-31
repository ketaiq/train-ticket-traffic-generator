"""
This module includes all API calls provided by ts-inside-payment-service.
"""
import logging
import requests
from json import JSONDecodeError
from ts import TIMEOUT_MAX
from locust.exception import RescheduleTask
from ts.log_syntax.locust_response import (
    log_http_error,
    log_wrong_response_error,
    log_timeout_error,
    log_response_info,
)

from ts.config import tt_host


def pay_one_order(client, bearer: str, user_id: str, order_id: str, trip_id: str):
    operation = "pay order"
    with client.post(
        url="/api/v1/inside_pay_service/inside_payment",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={"orderId": order_id, "tripId": "D1345"},
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


def delete_payment_by_order_id_request(admin_bearer: str, order_id: str):
    response = requests.delete(
        url=f"{tt_host}/api/v1/inside_pay_service/inside_payment/order/{order_id}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        print(response.json()["msg"])
    except JSONDecodeError:
        print("Response could not be decoded as JSON")


def delete_payment_by_order_id(client, admin_bearer: str, order_id: str):
    operation = "admin delete payment"
    with client.delete(
        url=f"/api/v1/inside_pay_service/inside_payment/order/{order_id}",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        name=operation,
        catch_response=True,
    ) as response:
        try:
            if response.ok:
                res_json = response.json()
                msg = res_json["msg"]
                logging.info(msg)
            else:
                log_http_error(
                    "admin",
                    operation,
                    response,
                    f"order ID {order_id}",
                )
        except JSONDecodeError:
            response.failure(f"Response could not be decoded as JSON!")
            raise RescheduleTask()
        except KeyError:
            response.failure(f"Response did not contain expected key!")
            raise RescheduleTask()
