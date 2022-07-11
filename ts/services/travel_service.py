"""
This module includes all API calls provided by ts-travel-service.
"""

from json import JSONDecodeError
from ts.log_syntax.locust_response import (
    log_wrong_response_error,
    log_timeout_error,
    log_response_info,
    log_http_error,
)
from ts import TIMEOUT_MAX
from locust.exception import RescheduleTask
import random


def search_ticket(
    client,
    departure_date: str,
    from_station: str,
    to_station: str,
    request_id: str,
) -> list:
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
        if not response.ok:
            data = f"from_station: {from_station}, to_station: {to_station}, departure_date: {departure_date}"
            log_http_error(
                request_id,
                operation,
                response,
                data,
                name="request",
            )
        else:
            try:
                key = "msg"
                msg = response.json()["msg"]
                operation += f" from {from_station} to {to_station} on {departure_date}"
                if msg != "Success":
                    log_wrong_response_error(
                        request_id,
                        operation,
                        response.failure,
                        response.json(),
                        name="request",
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(
                        request_id, operation, response.failure, name="request"
                    )
                else:
                    key = "data"
                    data = response.json()["data"]
                    res = ""
                    if data and len(data) > 0:
                        res = f"{len(data)} trips"
                    else:
                        res = "No tickets"
                    log_response_info(request_id, operation, res, name="request")
                    return data
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()


def pick_random_travel(trips: list) -> dict:
    return random.choice(trips)
