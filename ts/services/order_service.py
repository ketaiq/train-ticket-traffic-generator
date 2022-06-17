"""
This module includes all API calls provided by ts-order-service.
"""

import logging
from locust.clients import HttpSession
from ts import TIMEOUT_MAX


def get_orders_by_login_id(client: HttpSession, user_id: str, bearer: str) -> str:
    order_id = ""
    with client.post(
        url="/api/v1/orderservice/order/refresh",
        name="get an order",
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
            response.failure(
                f"user {user_id} tries to get orders by login id {user_id} but gets wrong response"
            )
            logging.error(
                f"user {user_id} tries to get orders by login id {user_id} but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            response.failure(
                f"user {user_id} tries to get orders by login id {user_id} but request takes too long!"
            )
            logging.warning(
                f"user {user_id} tries to get orders by login id {user_id} but request takes too long!"
            )
        else:
            data = response.json()["data"]
            if data is not None:
                if len(data) > 0:
                    order_id = data[0]["id"]
                    logging.info(
                        f"user {user_id} gets orders by login id {user_id}, its order id is {order_id}"
                    )
                else:
                    logging.info(
                        f"user {user_id} tries to get orders by login id {user_id}, but there is no this order"
                    )
            else:
                logging.error(
                    f"user {user_id} fails to get orders by login id {user_id} because there is no response data"
                )
    return order_id
