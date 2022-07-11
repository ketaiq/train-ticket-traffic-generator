"""
This module includes all API calls provided by ts-admin-order-service.
"""
from json import JSONDecodeError
from ts.log_syntax.locust_response import (
    log_wrong_response_error,
    log_timeout_error,
    log_response_info,
    log_http_error,
)
from ts import TIMEOUT_MAX
from locust.exception import RescheduleTask
from ts.services.preserve_service import SeatType, pick_random_seat_type
from ts.util import now_time, convert_date_to_time
import random


class Order:
    """
    According to https://github.com/FudanSELab/train-ticket/blob/master/ts-admin-order-service/src/main/java/adminorder/entity/Order.java
    """

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


def admin_add_one_order(client, admin_bearer: str, user_id: str, order: Order):
    operation = "admin add order"
    with client.post(
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
        if not response.ok:
            data = str(order.__dict__)
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
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
                    return data
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()


def admin_update_one_order(client, admin_bearer: str, user_id: str, order: Order):
    operation = "admin update order"
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
        if not response.ok:
            data = str(order.__dict__)
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
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
        url="/api/v1/adminorderservice/adminorder/"
        + order_id
        + "/"
        + trip_id.lstrip("G"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": admin_bearer,
        },
        name=operation,
        catch_response=True,
    ) as response:
        if not response.ok:
            data = f"order_id: {order_id}, trip_id: {trip_id}"
            log_http_error(
                user_id,
                operation,
                response,
                data,
            )
        else:
            try:
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
            except JSONDecodeError:
                response.failure(f"Response could not be decoded as JSON")
                raise RescheduleTask()
            except KeyError:
                response.failure(f"Response did not contain expected key '{key}'")
                raise RescheduleTask()


def gen_random_order(trip, departure_date, user_id, contact) -> Order:
    boughtDate = str(now_time())
    travelDate = str(convert_date_to_time(departure_date))
    travelTime = str(trip["startingTime"])
    coachNumber = random.randint(1, 10)
    seat_type = pick_random_seat_type()
    seat_price = "0"
    if seat_type == SeatType.FIRST_CLASS.value:
        seat_price = trip["priceForFirstClassSeat"]
    else:
        seat_price = trip["priceForSecondClassSeat"]
    seat_number = random.randint(1, 10000)
    return Order(
        boughtDate,
        travelDate,
        travelTime,
        user_id,
        contact.name,
        contact.document_type,
        contact.document_number,
        trip["tripId"],
        coachNumber,
        seat_type,
        seat_number,
        trip["fromStationName"].lower(),
        trip["toStationName"].lower(),
        0,
        seat_price,
    )
