"""
This module includes all API calls provided by ts-travel-service.
"""

from locust.clients import HttpSession
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)


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
    operation = "search tickets"
    with client.post(
        url="/api/v1/travelservice/trips/left",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={
            "startingPlace": from_station,
            "endPlace": to_station,
            "departureTime": departure_date,
        },
        catch_response=True,
        name=operation,
    ) as response:
        msg = response.json()["msg"]
        operation += f" from {from_station} to {to_station} on {departure_date}"
        if msg != "Success":
            log_wrong_response_warning(request_id, operation, response, name="request")
        elif response.elapsed.total_seconds() > 10:
            log_timeout_warning(request_id, operation, response, name="request")
        else:
            data = response.json()["data"]
            res = ""
            if data and len(data) > 0:
                res = data[0]
            else:
                res = "No tickets"
            log_response_info(request_id, operation, res, name="request")
