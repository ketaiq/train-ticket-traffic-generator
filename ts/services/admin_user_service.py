"""
This module includes all API calls provided by ts-admin-user-service.
"""

import requests
from json import JSONDecodeError
from ts import TIMEOUT_MAX
from locust.exception import RescheduleTask
from ts.util import (
    gen_random_document_number,
    gen_random_document_type,
    gen_random_email,
    gen_random_gender,
)
from ts.log_syntax.locust_response import (
    log_wrong_response_error,
    log_timeout_error,
    log_response_info,
    log_http_error,
)

ADMIN_USER_SERVICE_URL = "http://34.160.158.68/api/v1/adminuserservice/users"


def add_one_user(
    client,
    request_id: str,
    admin_bearer: str,
    username: str,
    password: str,
) -> dict:
    operation = "create user"
    with client.post(
        url="/api/v1/adminuserservice/users",
        headers={
            "Authorization": admin_bearer,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        json={
            "documentNum": gen_random_document_number(),
            "documentType": gen_random_document_type(),
            "email": gen_random_email(),
            "gender": gen_random_gender(),
            "password": password,
            "userName": username,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if not response.ok:
            data = f"username: {username}, password: {password}"
            log_http_error(
                request_id,
                operation,
                response,
                data,
                name="request",
            )
        else:
            try:
                key = "msg"
                if response.json()["msg"] != "REGISTER USER SUCCESS":
                    log_wrong_response_error(
                        request_id,
                        operation,
                        response.failure,
                        response.json(),
                        name="request",
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(
                        request_id, operation, response.failure, name="request"
                    )
                else:
                    key = "data"
                    new_user = response.json()["data"]
                    log_response_info(request_id, operation, new_user, name="request")
                    return new_user
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()


def get_all_users_request(admin_bearer: str, request_id: str) -> list:
    operation = "get all users"
    r = requests.get(
        url=ADMIN_USER_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        if r.json()["msg"] != "Success":
            print(f"request {request_id} tries to {operation} but gets wrong response")
        else:
            key = "data"
            return r.json()["data"]
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def add_one_user_request(
    request_id: str,
    admin_bearer: str,
    username: str,
    password: str,
):
    operation = "add one user"
    r = requests.post(
        url=ADMIN_USER_SERVICE_URL,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "documentNum": gen_random_document_number(),
            "documentType": gen_random_document_type(),
            "email": gen_random_email(),
            "gender": gen_random_gender(),
            "password": password,
            "userName": username,
        },
    )
    try:
        key = "msg"
        if r.json()["msg"] != "REGISTER USER SUCCESS":
            print(f"request {request_id} tries to {operation} but gets wrong response")
        else:
            key = "data"
            return r.json()["data"]
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def delete_one_user_request(request_id: str, admin_bearer: str, id: str):
    operation = "delete one user"
    r = requests.delete(
        url=ADMIN_USER_SERVICE_URL + "/" + id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
    )
    try:
        key = "msg"
        if r.json()["msg"] != "Success":
            print(f"request {request_id} tries to {operation} but gets wrong response")
        else:
            key = "data"
            return r.json()["data"]
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")
