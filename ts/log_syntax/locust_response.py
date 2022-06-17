import logging


def log_wrong_response_warning(id: str, operation: str, response, name: str = "user"):
    log = f"{name} {id} tries to {operation} but gets wrong response"
    response.failure(log)
    logging.warning(f"{log} {response.json()}")


def log_timeout_warning(id: str, operation: str, response, name: str = "user"):
    log = f"{name} {id} tries to {operation} but request takes too long!"
    response.failure(log)
    logging.warning(log)


def log_response_info(id: str, operation: str, response, name: str = "user"):
    logging.info(f"{name} {id} {operation}: {response}")
