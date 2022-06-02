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
    with client.post(
        url="/api/v1/travelservice/trips/left",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={
            "startingPlace": from_station,
            "endPlace": to_station,
            "departureTime": departure_date,
        },
        catch_response=True,
        name="search ticket",
    ) as response:
        msg = response.json()["msg"]
        if msg != "Success":
            log = f"request {request_id} tries to search train tickets from {from_station} to {to_station} on {departure_date} but got wrong response"
            logging.warning(f"{log}: {msg}")
            response.failure(f"{log}: {msg}")
        elif response.elapsed.total_seconds() > 10:
            log = f"request {request_id} tries to search train tickets from {from_station} to {to_station} on {departure_date} but request took too long"
            response.failure(log)
            logging.warning(log)
        else:
            logging.info(
                f"request {request_id} searches train tickets from {from_station} to {to_station} on {departure_date} by running POST /api/v1/travelservice/trips/left"
            )
