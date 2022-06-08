import logging


def log_wrong_response_warning(user_id: str, operation: str, response):
    log = f"user {user_id} tries to {operation} but gets wrong response"
    response.failure(log)
    logging.warning(f"{log} {response.json()}")


def log_timeout_warning(user_id: str, operation: str, response):
    log = f"user {user_id} tries to {operation} but request takes too long!"
    response.failure(log)
    logging.warning(log)


def log_response_info(user_id: str, operation: str, response):
    logging.info(f"user {user_id} {operation}: {response}")
