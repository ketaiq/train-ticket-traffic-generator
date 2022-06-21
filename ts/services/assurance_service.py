"""
This module includes all API calls provided by ts-assurance-service.
"""

import requests
from json import JSONDecodeError
from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_wrong_response_warning,
    log_timeout_warning,
    log_response_info,
)
from enum import Enum


class AssuranceType(Enum):
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-preserve-service/src/main/java/preserve/entity/AssuranceType.java
    """

    NONE = "0"
    TRAFFIC_ACCIDENT = "1"


def get_assurance_types(client, bearer: str, user_id: str):
    operation = "get assurance types"
    with client.get(
        url="/api/v1/assuranceservice/assurances/types",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": bearer,
        },
        name=operation,
    ) as response:
        if response.json()["msg"] != "Find All Assurance":
            log_wrong_response_warning(user_id, operation, response)
        elif response.elapsed.total_seconds() > TIMEOUT_MAX:
            log_timeout_warning(user_id, operation, response)
        else:
            assurance_types = response.json()["data"]
            log_response_info(user_id, operation, assurance_types)


def get_assurance_types_request(request_id: str, bearer: str):
    operation = "get assurance types"
    r = requests.get(
        url="http://130.211.196.121:8080/api/v1/assuranceservice/assurances/types",
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


if __name__ == "__main__":
    from auth_service import login_user_request
    import uuid

    request_id = str(uuid.uuid4())
    bearer, user_id = login_user_request(
        username="fdse_microservice", password="111111", request_id=request_id
    )

    print(get_assurance_types_request(request_id, bearer))
