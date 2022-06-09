import uuid
from ts.services.station_service import (
    gen_random_station,
    add_one_new_station,
    update_one_station,
    gen_updated_station,
    pick_random_station,
    delete_one_station,
)
from ts.services.auth_service import login_user


class RailTrafficControllerRequest:
    """
    - Login
    - Travel
        - Add
        - Update
        - Delete
    - Route
        - Add
        - Update
        - Delete
    - Station
        - Add
        - Update
        - Delete
    - Train
        - Add
        - Update
        - Delete
    """

    def __init__(self, client):
        self.client = client
        self.bearer, self.user_id = login_user(
            self.client,
            username="admin",
            password="222222",
            description="login admin user",
        )
        self.request_id = str(uuid.uuid4())
        self.original_stations = [
            {"id": "shanghai", "name": "Shang Hai", "stayTime": 10},
            {"id": "shanghaihongqiao", "name": "Shang Hai Hong Qiao", "stayTime": 10},
            {"id": "taiyuan", "name": "Tai Yuan", "stayTime": 5},
            {"id": "beijing", "name": "Bei Jing", "stayTime": 10},
            {"id": "nanjing", "name": "Nan Jing", "stayTime": 8},
            {"id": "shijiazhuang", "name": "Shi Jia Zhuang", "stayTime": 8},
            {"id": "xuzhou", "name": "Xu Zhou", "stayTime": 7},
            {"id": "jinan", "name": "Ji Nan", "stayTime": 5},
            {"id": "hangzhou", "name": "Hang Zhou", "stayTime": 9},
            {"id": "jiaxingnan", "name": "Jia Xing Nan", "stayTime": 2},
            {"id": "zhenjiang", "name": "Zhen Jiang", "stayTime": 2},
            {"id": "wuxi", "name": "Wu Xi", "stayTime": 3},
            {"id": "suzhou", "name": "Su Zhou", "stayTime": 3},
        ]

    def add_one_new_station(self):
        new_station = gen_random_station()
        add_one_new_station(
            self.client,
            self.bearer,
            self.user_id,
            new_station.id,
            new_station.name,
            new_station.stay_time,
        )

    def update_one_station(self):
        picked_station = pick_random_station(
            self.client, self.bearer, self.user_id, self.original_stations
        )
        updated_station = gen_updated_station(picked_station)
        update_one_station(
            self.client,
            self.bearer,
            self.user_id,
            updated_station.id,
            updated_station.name,
            updated_station.stay_time,
        )

    def delete_one_station(self):
        picked_station = pick_random_station(
            self.client, self.bearer, self.user_id, self.original_stations
        )
        delete_one_station(
            self.client,
            self.bearer,
            self.user_id,
            picked_station.id,
            picked_station.name,
        )
