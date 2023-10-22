import csv
import logging
import random
from time import sleep
import locust.stats
import numpy as np
from locust import HttpUser, task, events, LoadTestShape
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ts.requests.passenger_actions import PassengerActions
from ts.services.admin_route_service import init_all_routes
from ts.services.auth_service import login_user_request
from ts.services.station_service import init_all_stations
from ts.services.auth_service import login_user
from ts.role import Role

from ts.config import (
    wl_file_name,
    weekday_peak_hours,
    weekend_peak_hours,
    wl_day,
    wl_interval_mins,
    wl_start_hour,
    wl_num_start_interval,
)
from ts.util import calculate_peak_seconds

# configure locust statistics
locust.stats.CONSOLE_STATS_INTERVAL_SEC = 30
locust.stats.CSV_STATS_INTERVAL_SEC = 60  # default is 1 second
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = (
    60  # Determines how often the data is flushed to disk, default is 10 seconds
)
locust.stats.PERCENTILES_TO_REPORT = [
    0.25,
    0.50,
    0.75,
    0.80,
    0.90,
    0.95,
    0.98,
    0.99,
    0.999,
    0.9999,
    1.0,
]

number_of_points_in_period = wl_interval_mins * 60  # seconds
peak_points = calculate_peak_seconds(
    wl_start_hour,
    wl_num_start_interval,
    number_of_points_in_period,
    weekday_peak_hours,
    weekend_peak_hours,
    wl_day,
)


def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter("%(asctime)s %(message)s")

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


logger_tasks = setup_logger("logger_1", "tasks.log")
logger_actions = setup_logger("logger_actions", "actions.log")


# @events.init.add_listener
# def on_locust_init(environment, **kwargs):
#     print("Wait for fetching shared data, including routes, stations")
#     print("Log in as admin")
#     request_id = str(uuid.uuid4())
#     admin_bearer, admin_user_id = login_user_request(
#         username="admin", password="222222", request_id=request_id
#     )
#     print("Start initialisation")
#     init_all_routes(admin_bearer, request_id)
#     init_all_stations(admin_user_id, admin_bearer)


class Passenger_Role(HttpUser):
    peak_hour = None
    current_time = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        adapter = HTTPAdapter(
            pool_connections=100,
            pool_maxsize=100,
            max_retries=Retry(total=10, backoff_factor=2),
        )
        self.client.mount("https://", adapter)
        self.client.mount("http://", adapter)

    @task
    def perform_task(self):
        if self.peak_hour:
            min_wait_seconds = 5
            max_wait_seconds = 10
            role_weights = (
                random.randint(5, 7),
                random.randint(4, 6),
                random.randint(0, 2),
                random.randint(35, 37),
                random.randint(0, 2),
                random.randint(0, 2),
                random.randint(45, 47),
                random.randint(3, 5),
                random.randint(3, 5),
            )
        else:
            min_wait_seconds = 10
            max_wait_seconds = 15
            role_weights = (
                random.randint(11, 13),
                random.randint(9, 11),
                random.randint(1, 3),
                random.randint(23, 25),
                random.randint(0, 2),
                random.randint(0, 2),
                random.randint(45, 47),
                random.randint(3, 5),
                random.randint(3, 5),
            )

        role_to_perform = int(random.choices(list(Role), weights=role_weights)[0])
        description = role_to_perform.name
        request = PassengerActions(
            self.client,
            description,
        )

        if role_to_perform == Role.Irregular_Budget:
            request.perform_actions(logger_tasks, 1, 1, 5, 10, False, False, False)

        elif role_to_perform == Role.Irregular_Normal:
            request.perform_actions(logger_tasks, 5, 10, 1, 1, True, False, False)

        elif role_to_perform == Role.Irregular_Comfort:
            request.perform_actions(logger_tasks, 1, 1, 5, 10, True, True, True)

        elif role_to_perform == Role.Regular:
            request.perform_actions(logger_tasks, 1, 1, 1, 1, True, True, False)

        elif role_to_perform == Role.Cancel_No_Refund:
            request.perform_actions(logger_tasks, 1, 1, 1, 1, False, False, False)

        elif role_to_perform == Role.Cancel_With_Refund:
            request.perform_actions(logger_tasks, 1, 1, 1, 1, False, False, False)

        elif role_to_perform == Role.Sales_Add_Order:
            request.perform_actions_sales()

        elif role_to_perform == Role.Sales_Add_Update_Order:
            request.perform_actions_sales()
        elif role_to_perform == Role.Sales_Delete_Order:
            request.perform_actions_sales()

        sleep(random.randint(min_wait_seconds, max_wait_seconds))


class StagesShape(LoadTestShape):
    stages = []

    def __init__(self, timeIntervals=number_of_points_in_period):
        workload = []
        with open(wl_file_name, newline="") as fil:
            reader = csv.reader(fil)
            next(reader)

            for row in reader:
                workload.append(int(row[0]))

        spawnRate = [1 for x in workload]
        durationList = np.cumsum([timeIntervals] * len(workload))

        stagesDict = {
            "duration": list(durationList),
            "users": workload,
            "spawn_rate": spawnRate,
        }

        self.stages = [dict(zip(stagesDict, t)) for t in zip(*stagesDict.values())]

    def tick(self):
        run_time = self.get_run_time()
        current_time = round(run_time)

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])

                if current_time in peak_points:
                    Passenger_Role.peak_hour = True
                else:
                    Passenger_Role.peak_hour = False

                Passenger_Role.current_time = current_time
                return tick_data
        return None
