"""
This module includes all API calls provided by ts-travel-plan-service.
"""

from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
    log_http_error,
)
import random
from json import JSONDecodeError

from random import randint
from time import sleep


def get_cheapest_travel_plans(
    client,
    request_id: str,
    startingPlace: str,
    endPlace: str,
    departure_time: str,
) -> list:
    operation = "search cheapest travel plans"
    with client.post(
        url="/api/v1/travelplanservice/travelPlan/cheapest",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "startingPlace": startingPlace,
            "endPlace": endPlace,
            "departureTime": departure_time,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if response.ok:
            try:
                key = "msg"
                if response.json()["msg"] != "Success":
                    log_wrong_response_warning(
                        request_id,
                        operation,
                        response.failure,
                        response.json(),
                        name="request",
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_warning(
                        request_id, operation, response.failure, name="request"
                    )
                else:
                    key = "data"
                    plans = response.json()["data"]
                    log_response_info(request_id, operation, plans, name="request")
                    return plans
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
        else:
            data = f"searching from {startingPlace} to {endPlace} on {departure_time}"
            log_http_error(
                request_id,
                operation,
                response.failure,
                response.status_code,
                data,
                name="request",
            )


def get_quickest_travel_plans(
    client,
    request_id: str,
    starting_place: str,
    end_place: str,
    departure_time: str,
) -> list:
    operation = "search quickest travel plans"
    with client.post(
        url="/api/v1/travelplanservice/travelPlan/quickest",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "startingPlace": starting_place,
            "endPlace": end_place,
            "departureTime": departure_time,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if response.ok:
            try:
                key = "msg"
                if response.json()["msg"] != "Success":
                    log_wrong_response_warning(
                        request_id,
                        operation,
                        response.failure,
                        response.json(),
                        name="request",
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_warning(
                        request_id, operation, response.failure, name="request"
                    )
                else:
                    key = "data"
                    plans = response.json()["data"]
                    log_response_info(request_id, operation, plans, name="request")
                    return plans
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
        else:
            data = f"searching from {starting_place} to {end_place} on {departure_time}"
            log_http_error(
                request_id,
                operation,
                response.failure,
                response.status_code,
                data,
                name="request",
            )


def get_min_station_travel_plans(
    client,
    request_id: str,
    starting_place: str,
    end_place: str,
    departure_time: str,
) -> list:
    operation = "search minimum stations travel plans"
    with client.post(
        url="/api/v1/travelplanservice/travelPlan/minStation",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "startingPlace": starting_place,
            "endPlace": end_place,
            "departureTime": departure_time,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if not response.ok:
            data = f"searching from {starting_place} to {end_place} on {departure_time}"
            log_http_error(
                request_id,
                operation,
                response.failure,
                response.status_code,
                data,
                name="request",
            )
        else:
            try:
                key = "msg"
                if response.json()["msg"] != "Success":
                    log_wrong_response_warning(
                        request_id,
                        operation,
                        response.failure,
                        response.json(),
                        name="request",
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_warning(
                        request_id, operation, response.failure, name="request"
                    )
                else:
                    key = "data"
                    plans = response.json()["data"]
                    log_response_info(request_id, operation, plans, name="request")
                    return plans
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")


def pick_random_strategy_and_search(
    client,
    request_id: str,
    from_station: str,
    to_station: str,
    departure_date: str,
) -> list:
    strategy = random.randint(0, 2)
    if strategy == 0:
        return get_cheapest_travel_plans(
            client, request_id, from_station, to_station, departure_date
        )
    elif strategy == 1:
        return get_quickest_travel_plans(
            client, request_id, from_station, to_station, departure_date
        )
    else:
        return get_min_station_travel_plans(
            client, request_id, from_station, to_station, departure_date
        )
