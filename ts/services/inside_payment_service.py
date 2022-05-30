"""
This module includes all API calls provided by ts-inside-payment-service.
"""

import logging
from locust.clients import HttpSession


def pay_one_order(client: HttpSession, order_id: str, bearer: str, user_id: str):
    with client.post(
        url="/api/v1/inside_pay_service/inside_payment",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={"orderId": order_id, "tripId": "D1345"},
        name="pay for an order",
    ) as response:
        if response.json()["msg"] != "Payment Success Pay Success":
            response.failure(
                f"user {user_id} tries to pay the order {order_id} but gets wrong response"
            )
            logging.error(
                f"user {user_id} tries to pay the order {order_id} but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user {user_id} tries to pay the order {order_id} but request takes too long!"
            )
            logging.warning(
                f"user {user_id} tries to pay the order {order_id} but request takes too long!"
            )
        else:
            logging.info(f"user {user_id} pays the order {order_id}")
