import csv
import logging
import random
import uuid
from datetime import datetime

import locust.stats
import numpy as np
from locust import HttpUser, task, events, LoadTestShape
from requests.adapters import HTTPAdapter

from ts.requests.passenger_actions import PassengerActions
from ts.services.admin_route_service import init_all_routes
from ts.services.auth_service import login_user_request
from ts.services.station_service import init_all_stations

import ts.util as utl
tt_host = utl.tt_host
wl_file_name = utl.wl_file_name

locust.stats.CONSOLE_STATS_INTERVAL_SEC = 30
locust.stats.CSV_STATS_INTERVAL_SEC = 60 # default is 1 second
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 60 # Determines how often the data is flushed to disk, default is 10 seconds
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
VERBOSE_LOGGING = 0


number_of_days = 14
number_of_periods_per_day = 96
number_of_points_in_period = 900
peak_period_1 = 13
peak_period_2 = 53

peak_points_1 = []
peak_points_2 = []

for day_number in range(number_of_days):
    periods_shift = number_of_periods_per_day * day_number

    for x in range(number_of_points_in_period * (periods_shift + peak_period_1 - 3), number_of_points_in_period * (periods_shift + peak_period_1 + 2)):
        peak_points_1.append(x)

    for x in range(number_of_points_in_period * (periods_shift + peak_period_2 - 3), number_of_points_in_period * (periods_shift + peak_period_2 + 2)):
        peak_points_2.append(x)


def setup_logger(name, log_file, level=logging.INFO):

    formatter = logging.Formatter('%(asctime)s %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


logger_tasks = setup_logger('logger_1', 'tasks.log')
logger_actions = setup_logger('logger_actions', 'actions.log')

now = datetime.now()
current_dateTime = now.strftime("%Y-%m-%d %H:%M:%S")
logger_assignments = setup_logger('logger_assignments', 'assignments-{date_time}.log'.format(date_time=current_dateTime))


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    print("Wait for fetching shared data, including routes, stations")
    print("Log in as admin")
    request_id = str(uuid.uuid4())
    admin_bearer, admin_user_id = login_user_request(username="admin", password="222222", request_id=request_id)
    print("Start initialisation")
    init_all_routes(admin_bearer, request_id)
    init_all_stations(admin_user_id, admin_bearer)


class Passenger_Role(HttpUser):
    peak_hour = None
    current_time = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
        self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

    @task
    def perform_task(self):

        role_list = [ii for ii in range(8)]

        if self.peak_hour:
            role_weights = (
                random.randint(5, 7),
                random.randint(4, 6),
                random.randint(0, 2),
                random.randint(35, 37),
                random.randint(0, 2),
                random.randint(0, 2),
                random.randint(45, 47),
                random.randint(3, 5)
            )
        else:
            role_weights = (
                random.randint(11, 13),
                random.randint(9, 11),
                random.randint(1, 3),
                random.randint(23, 25),
                random.randint(0, 2),
                random.randint(0, 2),
                random.randint(45, 47),
                random.randint(3, 5)
            )

        # role_weights = (0, 0, 0, 0, 100, 100, 0, 0)

        role_to_perform = int(random.choices(role_list, weights=role_weights)[0])

        assignment_id = "a-{ID}".format(ID=uuid.uuid4())
        logger_assignments.info(assignment_id + " start")

        if role_to_perform == 0:
            request = PassengerActions(self.client, "Irregular_Budget")
            request.perform_actions(logger_tasks, 1, 1, 5, 10, False, False, False)

        if role_to_perform == 1:
            request = PassengerActions(self.client, "Irregular_Normal")
            request.perform_actions(logger_tasks, 5, 10, 1, 1, True, False, False)

        if role_to_perform == 2:
            request = PassengerActions(self.client, "Irregular_Comfort")
            request.perform_actions(logger_tasks, 1, 1, 5, 10, True, True, True)

        if role_to_perform == 3:
            request = PassengerActions(self.client, "Regular")
            request.perform_actions(logger_tasks, 1, 1, 1, 1, True, True, False)

        if role_to_perform == 4:
            request = PassengerActions(self.client, "Cancel_No_Refund")
            request.perform_actions(logger_tasks, 1, 1, 1, 1, False, False, False)

        if role_to_perform == 5:
            request = PassengerActions(self.client, "Cancel_With_Refund")
            request.perform_actions(logger_tasks, 1, 1, 1, 1, False, False, False)

        if role_to_perform == 6:
            request = PassengerActions(self.client, "sales_add_order")
            request.perform_actions_sales()

        if role_to_perform == 7:
            request = PassengerActions(self.client, "sales_update_order")
            request.perform_actions_sales()

        logger_assignments.info(assignment_id + " end")


class StagesShape(LoadTestShape):
    stages = []

    def __init__(self, timeIntervals=number_of_points_in_period):

        workload = []
        with open(wl_file_name, newline='') as fil:
            reader = csv.reader(fil)
            next(reader)

            periods_to_skip = 0
            for ii in range(periods_to_skip):
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

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])

                if (round(run_time) in peak_points_1) or (round(run_time) in peak_points_2):
                    Passenger_Role.peak_hour = True
                else:
                    Passenger_Role.peak_hour = False

                current_time = round(run_time)
                Passenger_Role.current_time = current_time

                return tick_data

        return None
