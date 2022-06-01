"""
This module includes all calls of simply getting specific pages.
"""

import logging
from locust.clients import HttpSession


def visit_home(client: HttpSession, request_id: str):
    client.get("/index.html", name="visit home page")
    logging.info(f"user request {request_id} visits the home page")


def visit_client_login(client: HttpSession, request_id: str):
    client.get("/client_login.html", name="visit client login page")
    logging.info(f"user request {request_id} visits the client ticket book page")


def visit_client_ticket_book(client: HttpSession, bearer: str, user_id: str):
    client.get(
        url="/client_ticket_book.html?tripId=D1345&from=Shang%20Hai&to=Su%20Zhou&seatType=2&seat_price=50.0&date=2022-02-11",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name="visit client ticket book page",
    )
    logging.info(f"user {user_id} visits the client ticket book page")
