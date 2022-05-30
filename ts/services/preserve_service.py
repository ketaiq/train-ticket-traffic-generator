"""
This module includes all API calls provided by ts-preserve-service.
"""

import logging
from locust.clients import HttpSession


def reserve_one_ticket(
    client: HttpSession, account_id: str, contacts_id: str, bearer: str
):
    with client.post(
        url="/api/v1/preserveservice/preserve",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        json={
            "accountId": account_id,
            "contactsId": contacts_id,
            "tripId": "D1345",
            "seatType": "2",
            "date": "2022-12-20",  # must be later than now
            "from": "Shang Hai",
            "to": "Su Zhou",
            "assurance": "0",
            "foodType": 1,
            "foodName": "Bone Soup",
            "foodPrice": 2.5,
            "stationName": "",
            "storeName": "",
        },
        catch_response=True,
        name="reserve a ticket",
    ) as response:
        if response.json()["msg"] != "Success.":
            response.failure(
                f"user {account_id} tries to reserve a ticket but gets wrong response"
            )
            logging.error(
                f"user {account_id} tries to reserve a ticket but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user {account_id} tries to reserve a ticket but request takes too long!"
            )
            logging.warning(
                f"user {account_id} tries to reserve a ticket but request takes too long!"
            )
        else:
            logging.info(f"user {account_id} reserves a ticket")
