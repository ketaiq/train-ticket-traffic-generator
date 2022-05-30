"""
This module includes all API calls provided by ts-consign-service.
"""

import logging
from locust.clients import HttpSession


def add_one_consign_by_order_id(
    client: HttpSession, bearer: str, user_id: str, order_id: str
):
    with client.post(
        url="/api/v1/consignservice/consigns",
        name="add a consign",
        json={
            "accountId": user_id,
            "handleDate": "2022-05-20",
            "from": "Shang Hai",
            "to": "Su Zhou",
            "orderId": order_id,
            "consignee": order_id,
            "phone": "123",
            "weight": "1",
            "id": "",
            "isWithin": "false",
        },
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
    ) as response:
        if "You have consigned successfully!" not in response.json()["msg"]:
            response.failure(
                f"user {user_id} tries to consign a ticket but gets wrong response"
            )
            logging.error(
                f"user {user_id} tries to consign a ticket but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user {user_id} tries to consign a ticket but request takes too long!"
            )
            logging.warning(
                f"user {user_id} tries to consign a ticket but request takes too long!"
            )
        else:
            logging.info(f"user {user_id} consigns a ticket")


def get_one_consign_by_order_id(client: HttpSession, bearer: str, order_id: str):
    with client.get(
        url="/api/v1/consignservice/consigns/order/" + order_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name="get a consign",
    ) as response:
        if response.json()["msg"] != "Find consign by order id success":
            response.failure(
                f"user tries to get a consigned ticket by order id {order_id} but gets wrong response"
            )
            logging.error(
                f"user tries to get a consigned ticket by order id {order_id} but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user tries to get a consigned ticket by order id {order_id} but request takes too long!"
            )
            logging.warning(
                f"user tries to get a consigned ticket by order id {order_id} but request takes too long!"
            )
        else:
            price = response.json()["data"]["price"]
            logging.info(
                f"user gets a consigned ticket worth {price} by order id {order_id}"
            )


def update_one_consign_by_order_id(
    client: HttpSession, bearer: str, user_id: str, order_id: str
):
    with client.put(
        url="/api/v1/consignservice/consigns",
        name="update a consign",
        json={
            "accountId": user_id,
            "handleDate": "2022-05-20",
            "from": "Shang Hai",
            "to": "Su Zhou",
            "orderId": order_id,
            "consignee": order_id,
            "phone": "123",
            "weight": "1",
            "id": "",
            "isWithin": "false",
        },
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
    ) as response:
        if "You have consigned successfully!" not in response.json()["msg"]:
            response.failure(
                f"user {user_id} tries to update a consigned ticket by order id {order_id} but gets wrong response"
            )
            logging.error(
                f"user {user_id} tries to update a consigned ticket by order id {order_id} but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user {user_id} tries to update a consigned ticket by order id {order_id} but request takes too long!"
            )
            logging.warning(
                f"user {user_id} tries to update a consigned ticket by order id {order_id} but request takes too long!"
            )
        else:
            logging.info(
                f"user {user_id} update a consigned ticket by order id {order_id}"
            )
