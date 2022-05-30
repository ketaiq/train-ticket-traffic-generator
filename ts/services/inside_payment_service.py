"""
This module includes all API calls provided by ts-inside-payment-service.
"""

import logging
from locust.clients import HttpSession


def pay_one_order(client: HttpSession, order_id: str, bearer: str):
    client.post(
        url="/api/v1/inside_pay_service/inside_payment",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={"orderId": order_id, "tripId": "D1345"},
        name="pay for an order",
    )

    logging.info(f"user pays the order {order_id}")
