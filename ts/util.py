import random
from datetime import datetime
import uuid
import string
import time


def gen_random_phone_number() -> str:
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 999)).zfill(3)
    last = str(random.randint(1, 9999)).zfill(4)
    return "{}-{}-{}".format(first, second, last)


def gen_random_date(
    after: int = random.randint(24 * 60 * 60, 100 * 24 * 60 * 60)
) -> str:
    # getting the timestamp
    timestamp = datetime.timestamp(datetime.now())
    new_time = datetime.fromtimestamp(after + timestamp)
    return new_time.strftime("%Y-%m-%d")


def gen_random_time() -> int:
    return int(
        time.time() + random.randint(24 * 60 * 60, 100 * 24 * 60 * 60)
    ) * 1000 + random.randint(0, 999)


def gen_random_document_number() -> str:
    return str(uuid.uuid4())[:8].upper()


def now_time() -> int:
    return int(time.time() * 1000)


def convert_date_to_time(date: str) -> int:
    return int(
        time.mktime(datetime.strptime(date, "%Y-%m-%d").timetuple())
        + random.randint(0, 99)
    ) * 1000 + random.randint(0, 999)


def gen_random_name() -> str:
    first_name_len = random.randint(3, 8)
    first_name = "".join(
        random.choice(string.ascii_lowercase) for _ in range(first_name_len)
    ).capitalize()
    last_name_len = random.randint(3, 8)
    last_name = "".join(
        random.choice(string.ascii_lowercase) for _ in range(last_name_len)
    ).capitalize()
    return f"{first_name} {last_name}"


def gen_random_email() -> str:
    local_part = "".join(
        random.choice(string.ascii_lowercase + string.digits)
        for _ in range(random.randint(3, 20))
    )
    domain = "".join(
        random.choice(string.ascii_lowercase + string.digits)
        for _ in range(random.randint(3, 10))
    )
    return f"{local_part}@{domain}.com"


def gen_random_gender() -> str:
    return random.randint(1, 3)


def gen_random_document_type() -> str:
    return random.randint(1, 3)


def calculate_peak_seconds(
    wl_start_hour,
    wl_num_start_interval,
    number_of_points_in_period,
    weekday_peak_hours,
    weekend_peak_hours,
    wl_day,
) -> list:
    start_offset = wl_num_start_interval * number_of_points_in_period
    if wl_day < 0 or wl_day > 6:
        print(f"Workload day {wl_day} is illegal!")
        return
    peak_seconds = []
    if wl_day < 5:
        for peak_hour in weekday_peak_hours:
            if peak_hour > wl_start_hour:
                peak_seconds += calculate_peak_range(start_offset, wl_start_hour, peak_hour)
    else:
        for peak_hour in weekend_peak_hours:
            if peak_hour > wl_start_hour:
                peak_seconds += calculate_peak_range(start_offset, wl_start_hour, peak_hour)
    return peak_seconds


def calculate_peak_range(start_offset, wl_start_hour, peak_hour):
    begin_peak_point = start_offset + (peak_hour - 2 - wl_start_hour) * 60 * 60
    end_peak_point = start_offset + (peak_hour + 3 - wl_start_hour) * 60 * 60
    return list(range(begin_peak_point, end_peak_point))


if __name__ == "__main__":
    # print(gen_random_document_number())
    # print(gen_random_name())
    # print(gen_random_email())
    # print(gen_random_time())
    # print(convert_date_to_time(gen_random_date()))
    print(uuid.uuid4())
