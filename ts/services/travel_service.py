"""
This module includes all API calls provided by ts-travel-service.
"""

import logging
from locust.clients import HttpSession


def search_ticket(
    client: HttpSession,
    departure_date: str,
    from_station: str,
    to_station: str,
    request_id: str,
):
    """
    Send a POST request of seaching tickets to the ts-travel-service to get left trip tickets.
    """
    head = {"Accept": "application/json", "Content-Type": "application/json"}
    json = {
        "startingPlace": from_station,
        "endPlace": to_station,
        "departureTime": departure_date,
    }
    with client.post(
        url="/api/v1/travelservice/trips/left",
        headers=head,
        json=json,
        catch_response=True,
        name="search ticket",
    ) as response:
        if response.json()["msg"] != "Success":
            response.failure("Got wrong response")
            logging.error("Got wrong response: {response.json()}!")
        elif response.elapsed.total_seconds() > 10:
            response.failure("Request took too long")
            logging.warning("Request took too long!")
    logging.info(
        f"user {request_id} searches train tickets from {from_station} to {to_station} on {departure_date} by running POST /api/v1/travelservice/trips/left"
    )
