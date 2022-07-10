from json import JSONDecodeError
from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)


def change_booking(
    client,
    bearer: str,
    user_id: str,
    date: str,
    old_trip_id: str,
    order_id: str,
    seat_type: int,
    trip_id: str,
) -> dict:
    operation = "change booking"
    with client.post(
        url="/api/v1/rebookservice/rebook",
        headers={
            "Authorization": bearer,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "date": date,
            "oldTripId": old_trip_id,
            "orderId": order_id,
            "seatType": seat_type,
            "tripId": trip_id,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if not response.ok:
            response.raise_for_status()
        else:
            try:
                key = "msg"
                if response.json()["msg"] == "Success!":
                    key = "data"
                    new_order = response.json()["data"]
                    log_response_info(user_id, operation, new_order)
                    return new_order
                elif response.json()["msg"] == "Please pay the different money!":
                    new_order = pay_difference(
                        client,
                        bearer,
                        user_id,
                        date,
                        old_trip_id,
                        order_id,
                        seat_type,
                        trip_id,
                    )
                    log_response_info(user_id, operation, new_order)
                    return new_order
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_warning(user_id, operation, response.failure)
                else:
                    log_wrong_response_warning(
                        user_id, operation, response.failure, response.json()
                    )
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")


def pay_difference(
    client,
    bearer: str,
    user_id: str,
    date: str,
    old_trip_id: str,
    order_id: str,
    seat_type: str,
    trip_id: str,
) -> dict:
    operation = "pay difference for changing booking"
    with client.post(
        url="/api/v1/rebookservice/rebook/difference",
        headers={
            "Authorization": bearer,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "date": date,
            "oldTripId": old_trip_id,
            "orderId": order_id,
            "seatType": seat_type,
            "tripId": trip_id,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if not response.ok:
            response.raise_for_status()
        else:
            try:
                key = "msg"
                if "success" in response.json()["msg"].lower():
                    key = "data"
                    new_order = response.json()["data"]
                    log_response_info(user_id, operation, new_order)
                    return new_order
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_warning(user_id, operation, response.failure)
                else:
                    log_wrong_response_warning(
                        user_id, operation, response.failure, response.json()
                    )
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
