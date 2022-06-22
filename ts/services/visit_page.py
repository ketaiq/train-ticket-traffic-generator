"""
This module includes all calls of simply getting specific pages.
"""

import logging
import requests
from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)
import urllib.parse


def visit_home(client, request_id: str):
    client.get("/index.html", name="visit home page")
    logging.info(f"user request {request_id} visits the home page")


def visit_client_login(client, request_id: str):
    client.get("/client_login.html", name="visit login page")
    logging.info(f"user request {request_id} visits the client ticket book page")


def visit_ticket_book(
    client,
    bearer: str,
    user_id: str,
    trip_id: str,
    from_station: str,
    to_station: str,
    seat_type: str,
    seat_price: str,
    date: str,
):
    operation = "visit ticket book page"
    with client.get(
        url="/client_ticket_book.html",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        params={
            "tripId": urllib.parse.quote(trip_id),
            "from": urllib.parse.quote(from_station),
            "to": urllib.parse.quote(to_station),
            "seatType": urllib.parse.quote(seat_type),
            "seat_price": urllib.parse.quote(seat_price),
            "date": urllib.parse.quote(date),
        },
        name=operation,
    ) as response:
        if response.status_code != 200:
            log_wrong_response_warning(user_id, operation, response)
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response)
        else:
            log_response_info(user_id, operation, response.url)


def visit_ticket_book_request(
    bearer: str,
    request_id: str,
    trip_id: str,
    from_station: str,
    to_station: str,
    seat_type: str,
    seat_price: str,
    date: str,
):
    operation = "visit ticket book page"
    r = requests.get(
        url="http://130.211.196.121:8080/client_ticket_book.html",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        params={
            "tripId": trip_id,
            "from": from_station,
            "to": to_station,
            "seatType": seat_type,
            "seat_price": seat_price,
            "date": date,
        },
    )
    if r.status_code != 200:
        print(f"request {request_id} failed to {operation}")
