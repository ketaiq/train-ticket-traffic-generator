import logging


def log_wrong_response_warning(
    id: str, operation: str, response_failure, data, name: str = "user"
):
    response_failure(f"tries to {operation} but gets wrong response")
    logging.warning(f"{name} {id} tries to {operation} but gets wrong response {data}")


def log_http_error(
    id: str, operation: str, response_failure, status_code, data, name: str = "user"
):
    response_failure(f"tries to {operation} but gets http error {status_code}")
    logging.error(
        f"{name} {id} tries to {operation} but gets http error {status_code} when {data}"
    )


def log_timeout_warning(id: str, operation: str, response_failure, name: str = "user"):
    response_failure(f"tries to {operation} but request takes too long!")
    logging.warning(f"{name} {id} tries to {operation} but request takes too long!")


def log_response_info(id: str, operation: str, data, name: str = "user"):
    logging.info(f"{name} {id} {operation}: {data}")
