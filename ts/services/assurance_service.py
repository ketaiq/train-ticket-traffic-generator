"""
This module includes all API calls provided by ts-assurance-service.
"""

import requests
import random
from json import JSONDecodeError
from ts import TIMEOUT_MAX
from locust.exception import RescheduleTask
from ts.log_syntax.locust_response import (
    log_wrong_response_error,
    log_timeout_error,
    log_response_info,
    log_http_error,
)
from enum import Enum

import ts.util as utl
tt_host = utl.tt_host

class AssuranceType(Enum):
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-preserve-service/src/main/java/preserve/entity/AssuranceType.java
    """

    NONE = "0"
    TRAFFIC_ACCIDENT = "1"


def get_assurance_types(client, bearer: str, user_id: str) -> list:
    operation = "search assurance types"
    with client.get(
        url="/api/v1/assuranceservice/assurances/types",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if not response.ok:
            data = f"user_id: {user_id}"
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
                key = "msg"
                if response.json()["msg"] != "Find All Assurance":
                    log_wrong_response_error(
                        user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(user_id, operation, response.failure)
                else:
                    key = "data"
                    assurance_types = response.json()["data"]
                    log_response_info(user_id, operation, assurance_types)
                    return assurance_types
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()


def get_assurance_types_request(request_id: str, bearer: str):
    operation = "get assurance types"
    r = requests.get(
        url=tt_host + "/api/v1/assuranceservice/assurances/types",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Find All Assurance":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            assurance_types = r.json()["data"]
            return assurance_types
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def pick_random_assurance_type(all_assurance_types: list) -> str:
    return str(random.choice(all_assurance_types)["index"])
