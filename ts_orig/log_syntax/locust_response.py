import logging


def log_wrong_response_warning(
    id: str, operation: str, response_failure, data, name: str = "user"
):
    log = f"{name} {id} tries to {operation} but gets wrong response"
    response_failure(log)
    logging.warning(f"{log} {data}")


def log_timeout_warning(id: str, operation: str, response_failure, name: str = "user"):
    log = f"{name} {id} tries to {operation} but request takes too long!"
    response_failure(log)
    logging.warning(log)


def log_response_info(id: str, operation: str, data, name: str = "user"):
    logging.info(f"{name} {id} {operation}: {data}")
