import random
from datetime import datetime
import uuid
import string

def gen_random_phone_number() -> str:
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 999)).zfill(3)
    last = str(random.randint(1, 9999)).zfill(4)
    return "{}-{}-{}".format(first, second, last)


def gen_random_date(after: int = random.randint(90000, 50000000)) -> str:
    # getting the timestamp
    timestamp = datetime.timestamp(datetime.now())
    return datetime.fromtimestamp(after + timestamp).strftime("%Y-%m-%d")


def gen_random_document_number() -> str:
    return str(uuid.uuid4())[:8].upper()

def gen_random_name() -> str:
    first_name_len = random.randint(3, 8)
    first_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(first_name_len)).capitalize()
    last_name_len = random.randint(3, 8)
    last_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(last_name_len)).capitalize()
    return f"{first_name} {last_name}"


if __name__ == "__main__":
    print(gen_random_document_number())
    print(gen_random_name())
