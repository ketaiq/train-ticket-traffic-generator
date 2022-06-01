"""
This module includes all API calls provided by ts-travel-plan-service.
"""

import logging
from locust.clients import HttpSession


def get_cheapest_travel_plans(
    client: HttpSession, startingPlace: str, endPlace: str, departure_time: str
):
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
        name="get cheapest travel plans",
    ) as response:
        if response.json()["msg"] != "Success":
            response.failure(
                f"user tries to get cheapest travel plans on {departure_time} but gets wrong response"
            )
            logging.error(
                f"user tries to get cheapest travel plans on {departure_time} but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user tries to get cheapest travel plans on {departure_time} but request takes too long!"
            )
            logging.warning(
                f"user tries to get cheapest travel plans on {departure_time} but request takes too long!"
            )
        else:
            plans = response.json()["data"]
            logging.info(f"user gets cheapest travel plans {plans} on {departure_time}")


def get_quickest_travel_plans(
    client: HttpSession, starting_place: str, end_place: str, departure_time: str
):
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
        name="get quickest travel plans",
    ) as response:
        if response.json()["msg"] != "Success":
            response.failure(
                f"user tries to get quickest travel plans on {departure_time} but gets wrong response"
            )
            logging.error(
                f"user tries to get quickest travel plans on {departure_time} but gets wrong response {response.json()}"
            )
        elif response.elapsed.total_seconds() > 10:
            response.failure(
                f"user tries to get quickest travel plans on {departure_time} but request takes too long!"
            )
            logging.warning(
                f"user tries to get quickest travel plans on {departure_time} but request takes too long!"
            )
        else:
            plans = response.json()["data"]
            logging.info(f"user gets quickest travel plans {plans} on {departure_time}")


def get_min_station_travel_plans(
    client: HttpSession, starting_place: str, end_place: str, departure_time: str
):
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
        name="get minimum stations travel plans",
    ) as response:
        if response.json()["msg"] != "Success":
            log = f"user tries to get minimum stations travel plans on {departure_time} but gets wrong response"
            response.failure(log)
            logging.error(f"{log} {response.json()}")
        elif response.elapsed.total_seconds() > 10:
            log = f"user tries to get minimum stations travel plans on {departure_time} but request takes too long!"
            response.failure(log)
            logging.warning(log)
        else:
            plans = response.json()["data"]
            logging.info(
                f"user gets minimum stations travel plans {plans} on {departure_time}"
            )
