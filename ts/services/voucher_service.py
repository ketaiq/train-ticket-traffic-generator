"""
This module includes all API calls provided by ts-voucher-service.
"""

import logging
from locust.clients import HttpSession
from ts import TIMEOUT_MAX

def get_one_voucher(client: HttpSession, bearer: str, order_id: str):
    with client.post(
        url="/getVoucher",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={"orderId": order_id, "type": 1},
        name="get voucher",
    ) as response:
        if response.json()["order_id"] != order_id:
            response.failure(
                f"user tries to get one voucher by order id {order_id} but gets wrong response"
            )
            logging.error(
                f"user tries to get one voucher by order id {order_id} but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            response.failure(
                f"user tries to get one voucher by order id {order_id} but request takes too long!"
            )
            logging.warning(
                f"user tries to get one voucher by order id {order_id} but request takes too long!"
            )
        else:
            price = response.json()["price"]
            logging.info(f"user gets one voucher worth {price} by order id {order_id}")
