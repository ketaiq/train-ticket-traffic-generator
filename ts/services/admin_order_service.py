from json import JSONDecodeError
import time

from locust.exception import RescheduleTask
from requests.exceptions import ConnectionError

from ts import TIMEOUT_MAX
from ts.log_syntax.locust_response import (
    log_wrong_response_error,
    log_timeout_error,
    log_response_info,
    log_http_error,
)


class Order:
    def __init__(
        self,
        boughtDate,
        travelDate,
        travelTime,
        accountId,
        contactsName,
        documentType,
        contactsDocumentNumber,
        trainNumber,
        coachNumber,
        seatClass,
        seatNumber,
        from_station,
        to_station,
        status,
        price,
    ):
        self.id = None
        self.boughtDate = boughtDate
        self.travelDate = travelDate
        self.travelTime = travelTime
        self.accountId = accountId
        self.contactsName = contactsName
        self.documentType = documentType
        self.contactsDocumentNumber = contactsDocumentNumber
        self.trainNumber = trainNumber
        self.coachNumber = coachNumber
        self.seatClass = seatClass
        self.seatNumber = seatNumber
        self.from_station = from_station
        self.to_station = to_station
        self.status = status
        self.price = price


def admin_add_order(
    client, admin_bearer: str, admin_user_id: str, order: Order, description
):
    operation = description
    boughtDate = int(float(time.time()) * 1000)

    with client.post(
        url="/api/v1/adminorderservice/adminorder",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": order.id,
            "boughtDate": boughtDate,
            "travelDate": order.travelDate,
            "travelTime": order.travelTime,
            "accountId": order.accountId,
            "contactsName": order.contactsName,
            "documentType": order.documentType,
            "contactsDocumentNumber": order.contactsDocumentNumber,
            "trainNumber": order.trainNumber.lstrip("G"),
            "coachNumber": order.coachNumber,
            "seatClass": order.seatClass,
            "seatNumber": order.seatNumber,
            "from": order.from_station,
            "to": order.to_station,
            "status": order.status,
            "price": order.price,
        },
        name=operation,
        catch_response=True,
    ) as response:
        try:
            if not response.ok:
                data = str(order.__dict__)
                log_http_error(
                    admin_user_id,
                    operation,
                    response,
                    data,
                )
            else:
                key = "msg"
                if response.json()["msg"] != "Success":
                    log_wrong_response_error(
                        admin_user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(admin_user_id, operation, response.failure)
                else:
                    key = "data"
                    data = response.json()["data"]
                    log_response_info(admin_user_id, operation, data)
                    return data
        except ConnectionError:
            raise RescheduleTask()
        except JSONDecodeError:
            response.failure(f"Response could not be decoded as JSON")
            raise RescheduleTask()
        except KeyError:
            response.failure(f"Response did not contain expected key '{key}'")
            raise RescheduleTask()


def admin_update_order(
    client, admin_bearer: str, user_id: str, order: Order, description
):
    operation = description

    with client.put(
        url="/api/v1/adminorderservice/adminorder",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        json={
            "id": order.id,
            "boughtDate": order.boughtDate,
            "travelDate": order.travelDate,
            "travelTime": order.travelTime,
            "accountId": order.accountId,
            "contactsName": order.contactsName,
            "documentType": order.documentType,
            "contactsDocumentNumber": order.contactsDocumentNumber,
            "trainNumber": order.trainNumber.lstrip("G"),
            "coachNumber": order.coachNumber,
            "seatClass": order.seatClass,
            "seatNumber": order.seatNumber,
            "from": order.from_station,
            "to": order.to_station,
            "status": order.status,
            "price": order.price,
        },
        name=operation,
        catch_response=True,
    ) as response:
        try:
            if not response.ok:
                data = str(order.__dict__)
                log_http_error(
                    user_id,
                    operation,
                    response,
                    data,
                )
            else:
                key = "msg"
                if response.json()["msg"] != "Success":
                    log_wrong_response_error(
                        user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(user_id, operation, response.failure)
                else:
                    key = "data"
                    data = response.json()["data"]
                    log_response_info(user_id, operation, data)
        except ConnectionError:
            raise RescheduleTask()
        except JSONDecodeError:
            response.failure(f"Response could not be decoded as JSON")
            raise RescheduleTask()
        except KeyError:
            response.failure(f"Response did not contain expected key '{key}'")
            raise RescheduleTask()


def admin_get_all_orders(client, admin_bearer: str):
    operation = "admin get all orders"
    with client.get(
        url="/api/v1/adminorderservice/adminorder",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        name=operation,
        catch_response=True,
    ) as response:
        try:
            if response.ok:
                return response.json()["data"]
            else:
                log_http_error("admin", operation, response, "Nothing")
        except ConnectionError:
            raise RescheduleTask()
        except JSONDecodeError:
            response.failure(f"Response could not be decoded as JSON")
            raise RescheduleTask()
        except KeyError:
            response.failure(f"Response did not contain expected key '{key}'")
            raise RescheduleTask()


def admin_delete_one_order(
    client, admin_bearer: str, user_id: str, order_id: str, trip_id: str
):
    operation = "admin delete order"
    with client.delete(
        url="/api/v1/adminorderservice/adminorder/" + order_id + "/" + trip_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        name=operation,
        catch_response=True,
    ) as response:
        try:
            if not response.ok:
                data = f"order_id: {order_id}, trip_id: {trip_id}"
                log_http_error(
                    user_id,
                    operation,
                    response,
                    data,
                )
            else:
                key = "msg"
                if response.json()["msg"] != "Success":
                    log_wrong_response_error(
                        user_id, operation, response.failure, response.json()
                    )
                elif response.elapsed.total_seconds() > TIMEOUT_MAX:
                    log_timeout_error(user_id, operation, response.failure)
                else:
                    key = "data"
                    data = response.json()["data"]
                    log_response_info(user_id, operation, data)
        except ConnectionError:
            raise RescheduleTask()
        except JSONDecodeError:
            response.failure(f"Response could not be decoded as JSON")
            raise RescheduleTask()
        except KeyError:
            response.failure(f"Response did not contain expected key '{key}'")
            raise RescheduleTask()


def gen_random_order(user_id) -> Order:
    boughtDate = "1"
    travelDate = "2"
    travelTime = "3"
    coachNumber = "4"
    seat_type = "5"
    seat_price = "6"
    seat_number = "7"
    contact_name = "John"
    contact_document_type = "1"
    contact_document_number = "1234"

    return Order(
        boughtDate,
        travelDate,
        travelTime,
        user_id,
        contact_name,
        contact_document_type,
        contact_document_number,
        "8",
        coachNumber,
        seat_type,
        seat_number,
        "s1",
        "s2",
        0,
        seat_price,
    )
