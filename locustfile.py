from locust import HttpUser, task, between, constant, events
from locust import LoadTestShape
from datetime import datetime, timedelta, date
from random import randint, gauss, randrange
import random
import json
import uuid
import numpy as np
import sys
import time
import os
import csv
from collections import defaultdict
import logging
from requests.adapters import HTTPAdapter
import locust.stats

from ts.requests.irregular_budget import IrregularBudgetRequest
from ts.requests.irregular_normal import IrregularNormalRequest
from ts.requests.irregular_comfort import IrregularComfortRequest
from ts.requests.regular import RegularRequest
from ts.requests.cancel_without_refund import CancelWithoutRefundRequest
from ts.requests.cancel_with_refund import CancelWithRefundRequest
from ts.requests.sales import SalesRequest

locust.stats.CONSOLE_STATS_INTERVAL_SEC = 30
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 10
locust.stats.PERCENTILES_TO_REPORT = [0.25, 0.50, 0.75, 0.80, 0.90, 0.95, 0.98, 0.99, 0.999, 0.9999, 1.0]
VERBOSE_LOGGING = 0

period_duration = 120
peak_1 = 13
peak_2 = 53

weights_non_peak_hours = [random.randint(11, 13), random.randint(9, 11), random.randint(1, 3), random.randint(23, 25), random.randint(0, 2), random.randint(0, 2), random.randint(45, 47), random.randint(1, 3), random.randint(1, 3)]
weights_peak_hours = [random.randint(5, 7), random.randint(4, 5), random.randint(0, 2), random.randint(35, 36), random.randint(0, 2), random.randint(0, 2), random.randint(45, 47), random.randint(1, 3), random.randint(1, 3)]

peak_hours_1 = [int(x) for x in range(period_duration * (peak_1 - 3), period_duration * (peak_1 + 2))]
peak_hours_2 = [int(x) for x in range(period_duration * (peak_2 - 3), period_duration * (peak_2 + 2))]


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    from ts.services.admin_route_service import init_european_routes
    from ts.services.station_service import init_european_stations
    from ts.services.auth_service import login_user_request

    print("Fetch shared data, including routes, stations")
    request_id = str(uuid.uuid4())
    admin_bearer, admin_user_id = login_user_request(
        username="admin", password="222222", request_id=request_id
    )
    init_european_routes(admin_bearer, request_id)
    init_european_stations(admin_user_id, admin_bearer)


class Passenger(HttpUser):
    wait_time = between(1, 5)
    weights_global = [1, 1, 1, 1, 1, 1, 1, 1, 1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
        self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

        self.irregular_budget_request = IrregularBudgetRequest(
            self.client, "Irregular Budget"
        )
        self.irregular_normal_request = IrregularNormalRequest(
            self.client, "Irregular Normal"
        )
        self.irregular_comfort_request = IrregularComfortRequest(
            self.client, "Irregular Comfort"
        )
        self.regular_request = RegularRequest(self.client, "Regular")
        self.cancel_without_refund_request = CancelWithoutRefundRequest(
            self.client, "Cancel Without Refund"
        )
        self.cancel_with_refund_request = CancelWithRefundRequest(
            self.client, "Cancel With Refund"
        )

    @task(weights_global[0])
    def irregular_budget(self):
        self.irregular_budget_request.perform_actions()

    @task(weights_global[1])
    def irregular_normal(self):
        self.irregular_normal_request.perform_actions()

    @task(weights_global[2])
    def irregular_comfort(self):
        self.irregular_comfort_request.perform_actions()

    @task(weights_global[3])
    def regular(self):
        self.regular_request.perform_actions()

    @task(weights_global[4])
    def cancel_without_refund(self):
        self.cancel_without_refund_request.perform_actions()

    @task(weights_global[5])
    def cancel_with_refund(self):
        self.cancel_with_refund_request.perform_actions()


class Sales(HttpUser):
    wait_time = between(6, 10)
    weights_global = [1, 1, 1, 1, 1, 1, 1, 1, 1]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
        self.client.mount("http://", HTTPAdapter(pool_maxsize=50))
        self.sales_request = SalesRequest(self.client)

    @task(weights_global[6])
    def sales_create_order(self):
        self.sales_request.perform_create_order_actions()

    @task(weights_global[7])
    def sales_update_order(self):
        self.sales_request.perform_update_order_actions()

    @task(weights_global[8])
    def sales_delete_order(self):
        self.sales_request.perform_delete_order_actions()


class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.
    Keyword arguments:
        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage
        stop_at_end -- Can be set to stop once all stages have run.
    """

    stages = []

    def __init__(self, timeIntervals=period_duration):
        """
        This function needs an external csv file, with header where the 2 and 4th columns are respectively
        the rate of users and the rate at which these are spawned.
        Keyword arguments:
            totalUsersNumber -- Number of users to be used for the rates.
            timeIntervals -- how long between each stage needs to pass (i.e., 60seconds).
        """

        workload = defaultdict(list)
        with open("workload.csv") as f:
            csv_reader = csv.DictReader(f, delimiter=",")
            for row in csv_reader:
                for key, value in row.items():
                    workload[key].append(value)

        usersNumber = list(workload.items())[0][1]
        spawnRate = list(workload.items())[1][1]

        usersList = [int(x) for x in usersNumber]
        spawnRateList = [int(x) for x in spawnRate]
        durationList = np.cumsum([timeIntervals] * len(usersList))

        stagesDict = {"duration": list(durationList), 'users': usersList, 'spawn_rate':spawnRateList}

        self.stages = [dict(zip(stagesDict,t)) for t in zip(*stagesDict.values())]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:

                if (round(run_time) in peak_hours_1) or (round(run_time) in peak_hours_2):
                    hour_type = "Peak"
                    weights_list = weights_peak_hours
                else:
                    hour_type = "Non-Peak"
                    weights_list = weights_non_peak_hours

                print(round(run_time), hour_type, stage["users"], stage["duration"])
                Passenger.weights_global = weights_list
                Sales.weights_global = weights_list

                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None

