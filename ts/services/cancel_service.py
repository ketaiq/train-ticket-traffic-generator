"""
This module includes all API calls provided by ts-cancel-service.
"""

import logging
from locust.clients import HttpSession


def cancel_one_order(
    client: HttpSession, bearer: str, order_id: str, user_id: str, description: str
):
    with client.get(
        url="/api/v1/cancelservice/cancel/" + order_id + "/" + user_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name=description,
    ) as response:
        if response.json()["msg"] != "Success.":
            response.failure(
                f"user {user_id} tries to cancel the order {order_id} but gets wrong response"
            )
            logging.error(
                f"user {user_id} tries to cancel the order {order_id} but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user {user_id} tries to cancel the order {order_id} but request takes too long!"
            )
            logging.warning(
                f"user {user_id} tries to cancel the order {order_id} but request takes too long!"
            )
        else:
            logging.info(f"user {user_id} cancels the order {order_id}")
