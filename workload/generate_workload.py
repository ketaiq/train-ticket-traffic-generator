import os
import random
import csv
from collections import defaultdict
from matplotlib import pyplot as plt
import sys


file_name_wl_pattern_weekdays = "wl_pattern_weekdays.csv"
file_name_wl_pattern_weekends = "wl_pattern_weekends.csv"


def get_wl_pattern(wl_pattern_file_name):
    workload = defaultdict(list)
    with open(os.path.join("workload", wl_pattern_file_name)) as fil:
        csv_reader = csv.DictReader(fil, delimiter=",")
        for row in csv_reader:
            for key, value in row.items():
                workload[key].append(value)

    users_list = [int(xx) for xx in list(workload.items())[0][1]]
    return users_list


def create_week(weekdays_pattern, weekends_pattern, start_day):
    days = [[] for ii in range(7)]

    for day_idx in range(len(days)):
        if day_idx < 5:
            workload_pattern = weekdays_pattern
        else:
            workload_pattern = weekends_pattern

        for user_number in workload_pattern:
            number_of_users_period = random.randint(user_number - 1, user_number + 2)

            if number_of_users_period < 0:
                number_of_users_period = 0

            days[day_idx].append(number_of_users_period)

    return days[-(7 - start_day) :] + days[:start_day]


def create_week_workload_by_day(weekdays_pattern, weekends_pattern, num_weeks: int):
    """Create week workload separated by days according to the designed pattern."""
    for week in range(num_weeks):
        for day in range(7):
            if day < 5:
                workload_pattern = weekdays_pattern
            else:
                workload_pattern = weekends_pattern
            day_workload = []

            for user_number in workload_pattern:
                number_of_users_period = random.randint(
                    user_number - 1, user_number + 2
                )
                if number_of_users_period <= 0:
                    number_of_users_period = 1
                day_workload.append(number_of_users_period)

            global_day_index = 7 * week + day + 1
            write_wl_to_csv(day_workload, f"workload_day_{global_day_index}.csv")


def create_week_workload_by_overlapped_hours(
    weekdays_pattern,
    weekends_pattern,
    num_weeks: int,
    num_hours_workload: int,
    num_overlapped_hours: int,
):
    """
    Create week workload separated by hours according to the designed pattern.
    For example, 12-hour workload with 1 overlapped hour means 1h (begin) + 12h (workload) + 1h (end) = 14h in total.

    Parameters
    ----------
    num_hours_workload: int
        number of meaningful hours in a workload
    num_overlapped_hours: int
        number of overlapped hours before and after the workload period

    """
    workloads = []
    for _ in range(num_weeks):
        for day in range(7):
            if day < 5:
                workload_pattern = weekdays_pattern
            else:
                workload_pattern = weekends_pattern
            day_workload = []

            for user_number in workload_pattern:
                number_of_users_period = random.randint(
                    user_number - 1, user_number + 2
                )
                if number_of_users_period <= 0:
                    number_of_users_period = 1
                day_workload.append(number_of_users_period)

            workloads.extend(day_workload)
    for i in range(
        0, len(workloads) - num_hours_workload * 4 + 1, num_hours_workload * 4
    ):
        hours_workload = workloads[i : i + num_hours_workload * 4]
        begin_workload = gen_overlapped_workload(
            num_overlapped_hours, hours_workload[0], True
        )
        end_workload = gen_overlapped_workload(
            num_overlapped_hours, hours_workload[-1], False
        )
        hours_workload = begin_workload + hours_workload + end_workload
        write_wl_to_csv(
            hours_workload,
            f"workload/workload_{num_hours_workload}hours_{i//48}.csv",
        )


def gen_overlapped_workload(num_overlapped_hours: int, value: int, increasing: bool):
    num_overlapped_workload = num_overlapped_hours * 4
    workload = []
    if increasing:
        for i in range(num_overlapped_workload):
            num_users = value // (2**i)
            if num_users < 1:
                num_users = 1
            workload.append(num_users)
        workload.reverse()
    else:
        workload = [value] * num_overlapped_workload
    return workload


def make_flat(wl_week):
    wl_flat = []
    for wl_day in wl_week:
        for wl_period in wl_day:
            wl_flat.append(wl_period)

    return wl_flat


def write_wl_to_csv(wl_list, file_name_wl):
    with open(file_name_wl, "w") as fil:
        writer = csv.writer(fil)
        writer.writerow(["Users", "SpawnRate"])
        for xx in wl_list:
            writer.writerow([xx, 1])


if __name__ == "__main__":
    file_name_wl_two_weeks = "workload-2-weeks.csv"
    start_day = 0  # weekdays from 0 to 6

    wl_pattern_weekdays = get_wl_pattern(file_name_wl_pattern_weekdays)
    wl_pattern_weekends = get_wl_pattern(file_name_wl_pattern_weekends)

    # wl_week_1 = create_week(wl_pattern_weekdays, wl_pattern_weekends, start_day)
    # wl_week_2 = create_week(wl_pattern_weekdays, wl_pattern_weekends, start_day)
    # wl_two_weeks = make_flat(wl_week_1) + make_flat(wl_week_2)

    # create_week_workload_by_day(wl_pattern_weekdays, wl_pattern_weekends, 2)
    create_week_workload_by_overlapped_hours(
        wl_pattern_weekdays, wl_pattern_weekends, 2, 12, 1
    )

    # plt.plot(wl_two_weeks)
    # plt.ylabel("")
    # plt.show()

    # write_wl_to_csv(wl_two_weeks, file_name_wl_two_weeks)
