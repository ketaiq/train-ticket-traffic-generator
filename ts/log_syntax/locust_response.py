import logging
from locust.exception import RescheduleTask


def log_wrong_response_error(
    id: str, operation: str, response_failure, data, name: str = "user"
):
    response_failure(f"tries to {operation} but gets wrong response")
    logging.error(f"{name} {id} tries to {operation} but gets wrong response {data}")
    raise RescheduleTask()


def log_http_error(id: str, operation: str, response, data, name: str = "user"):
    compact_desc = f"tries to {operation} but gets HTTP error {response.status_code}"
    response.failure(compact_desc)
    logging.error(f"{name} {id} {compact_desc} with data {data}")
    raise RescheduleTask()


def log_timeout_error(id: str, operation: str, response_failure, name: str = "user"):
    response_failure(f"tries to {operation} but request takes too long!")
    logging.error(f"{name} {id} tries to {operation} but request takes too long!")
    raise RescheduleTask()


def log_response_info(id: str, operation: str, data, name: str = "user"):
    logging.info(f"{name} {id} {operation}: {data}")
