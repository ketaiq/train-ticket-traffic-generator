from ts.services.visit_page import visit_ticket_book_request


def test_all(request_id: str,bearer: str,  assertIsInstance, assertEqual):
    _test_visit_ticket_book_request(bearer, request_id)


def _test_visit_ticket_book_request(bearer: str, request_id: str):
    visit_ticket_book_request(
        bearer,
        request_id,
        "D1345",
        "Shang%20Hai",
        "Su%20Zhou",
        "2",
        "50.0",
        "2022-10-11",
    )
