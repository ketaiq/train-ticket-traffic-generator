import requests
import uuid
from json import JSONDecodeError
from pymongo import MongoClient
import random
from ts.util import gen_random_phone_number

FOOD_MAP_SERVICE_URL = "http://35.222.140.129:18855/api/v1/foodmapservice"

ORIGINAL_TRAINFOODS = [
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.TrainFood",
        "tripId": "G1234",
        "foodList": [
            {"foodName": "Pork Chop with rice", "price": 9.5},
            {"foodName": "Egg Soup", "price": 3.2},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.TrainFood",
        "tripId": "G1235",
        "foodList": [
            {"foodName": "Beef with rice", "price": 9.5},
            {"foodName": "Soup", "price": 3.7},
            {"foodName": "Pork pickled mustard green noodles", "price": 10.0},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.TrainFood",
        "tripId": "G1236",
        "foodList": [
            {"foodName": "Seafood noodles", "price": 9.5},
            {"foodName": "Glutinous rice", "price": 0.9},
            {"foodName": "Dumplings", "price": 5.5},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.TrainFood",
        "tripId": "G1237",
        "foodList": [
            {"foodName": "Spring rolls", "price": 1.5},
            {"foodName": "Vegetable soup", "price": 0.8},
            {"foodName": "Rice and vegetable roll", "price": 1.0},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.TrainFood",
        "tripId": "D1345",
        "foodList": [
            {"foodName": "Spicy hot noodles", "price": 5.0},
            {"foodName": "Soup", "price": 3.7},
            {"foodName": "Oily bean curd", "price": 2.0},
        ],
    },
]
ORIGINAL_STORES = [
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": "shanghai",
        "storeName": "KFC",
        "telephone": "01-234567",
        "businessTime": "10:00-20:00",
        "deliveryFee": 20.0,
        "foodList": [
            {"foodName": "Hamburger", "price": 5.0},
            {"foodName": "Cola", "price": 2.0},
            {"foodName": "Chicken", "price": 10.5},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": "shanghai",
        "storeName": "Good Taste",
        "telephone": "6228480012",
        "businessTime": "08:00-21:00",
        "deliveryFee": 10.0,
        "foodList": [
            {"foodName": "Rice", "price": 1.2},
            {"foodName": "Chicken Soup", "price": 2.5},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": "nanjing",
        "storeName": "Burger King",
        "telephone": "88348215681",
        "businessTime": "08:00-23:00",
        "deliveryFee": 15.0,
        "foodList": [
            {"foodName": "Big Burger", "price": 1.2},
            {"foodName": "Bone Soup", "price": 2.5},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": "nanjing",
        "storeName": "Pizza Hut",
        "telephone": "2382614",
        "businessTime": "08:00-23:00",
        "deliveryFee": 15.0,
        "foodList": [
            {"foodName": "Big Burger", "price": 1.2},
            {"foodName": "Bone Soup", "price": 2.5},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": "nanjing",
        "storeName": "McDonald's",
        "telephone": "2836485",
        "businessTime": "08:00-23:00",
        "deliveryFee": 15.0,
        "foodList": [
            {"foodName": "Big Mac", "price": 2.2},
            {"foodName": "McChicken", "price": 1.5},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": "suzhou",
        "storeName": "Roman Holiday",
        "telephone": "3769464",
        "businessTime": "09:00-23:00",
        "deliveryFee": 15.0,
        "foodList": [
            {"foodName": "Big Burger", "price": 1.2},
            {"foodName": "Bone Soup", "price": 2.5},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": "beijing",
        "storeName": "Perfect",
        "telephone": "975335664",
        "businessTime": "08:00-23:00",
        "deliveryFee": 15.0,
        "foodList": [
            {"foodName": "French Fries", "price": 1.2},
            {"foodName": "Vegetable Seafood Soup", "price": 2.5},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": "beijing",
        "storeName": "Delicious",
        "telephone": "237452946",
        "businessTime": "08:00-21:00",
        "deliveryFee": 15.0,
        "foodList": [
            {"foodName": "Hot Chocolate", "price": 1.2},
            {"foodName": "Pineapple Pie", "price": 2.5},
        ],
    },
    {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": "taiyuan",
        "storeName": "GOODWILL",
        "telephone": "23753855",
        "businessTime": "08:00-21:00",
        "deliveryFee": 15.0,
        "foodList": [
            {"foodName": "Karubi Beef", "price": 1.2},
            {"foodName": " Low Fat Yogurt Blackberry", "price": 2.5},
        ],
    },
]


def get_all_food_stores_request(
    request_id: str,
) -> list:
    operation = "get food stores"
    r = requests.get(
        url=FOOD_MAP_SERVICE_URL + "/" + "foodstores",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Success":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            food_stores = r.json()["data"]
            return food_stores
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def get_train_food_in_one_trip_request(request_id: str, trip_id: str) -> list:
    operation = "get train food in one trip"
    r = requests.get(
        url=FOOD_MAP_SERVICE_URL + "/" + "trainfoods" + "/" + trip_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Success":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            train_food = r.json()["data"]
            return train_food
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def print_all_food_from_mongo():
    client = MongoClient("mongodb://35.232.87.32:27017/")
    db = client["ts"]
    trainfoods = db["trainfoods"]
    stores = db["stores"]
    print("trainfoods")
    for train_food in trainfoods.find():
        print(train_food)
    print("stores")
    for store in stores.find():
        print(store)


def _gen_random_food_list(food_choices) -> list:
    food_names = random.sample(food_choices, k=random.randint(1, len(food_choices)))
    return [
        {"foodName": name, "price": round(random.uniform(5, 20), 1)}
        for name in food_names
    ]


def _gen_random_train_food_record(food_choices, travel) -> dict:
    return {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.TrainFood",
        "tripId": travel.trip_id,
        "foodList": _gen_random_food_list(food_choices),
    }


def _gen_random_store_record(food_choices, store_choices, station) -> dict:
    business_start_time_choices = ["06:00", "07:00", "08:00", "09:00", "10:00"]
    business_end_time_choices = ["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
    business_time = (
        random.choice(business_start_time_choices)
        + "-"
        + random.choice(business_end_time_choices)
    )
    return {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": station.id,
        "storeName": random.choice(store_choices),
        "telephone": gen_random_phone_number(),
        "businessTime": business_time,
        "deliveryFee": round(random.uniform(5, 15), 1),
        "foodList": _gen_random_food_list(food_choices),
    }


def add_food(all_travels, all_stations):
    client = MongoClient("mongodb://35.232.87.32:27017/")
    db = client["ts"]
    trainfoods = db["trainfoods"]
    trainfoods.delete_many({})
    stores = db["stores"]
    stores.delete_many({})
    print("Food is clear")
    for train_food in trainfoods.find():
        print(train_food)
    for store in stores.find():
        print(store)
    food_choices = [
        "Pork Chop with rice",
        "Egg Soup",
        "Beef with rice",
        "Soup",
        "Pork pickled mustard green noodles",
        "Seafood noodles",
        "Glutinous rice",
        "Dumplings",
        "Spring rolls",
        "Vegetable soup",
        "Rice and vegetable roll",
        "Spicy hot noodles",
        "Soup",
        "Oily bean curd",
        "Hamburger",
        "Cola",
        "Chicken",
        "Rice",
        "Chicken Soup",
        "Big Burger",
        "Bone Soup",
        "Big Burger",
        "Bone Soup",
        "Big Mac",
        "McChicken",
        "Big Burger",
        "Bone Soup",
        "French Fries",
        "Vegetable Seafood Soup",
        "Hot Chocolate",
        "Pineapple Pie",
        "Karubi Beef",
        "Low Fat Yogurt Blackberry",
    ]
    store_choices = [
        "KFC",
        "Good Taste",
        "Burger King",
        "Pizza Hut",
        "McDonald's",
        "Roman Holiday",
        "Perfect",
        "Delicious",
        "16 Handles",
        "Tequila Mockingbird",
        "Of Rice & Men",
        "Planet of the Crepes",
        "The Codfather",
        "The Breakfast Club",
        "Custard's Last Stand",
        "Happy Grillmore",
        "Café Jack",
        "Life of Pie",
        "Filled of Dreams",
        "Lord of the Wings",
        "Eat Pray Love",
        "Frying Nemo",
        "Grillenium Falcon",
        "Pita Pan",
        "Earth, Wind and Flour",
        "Wok This Way",
        "Gochew Grill",
    ]
    all_train_food_records = [
        _gen_random_train_food_record(food_choices, travel) for travel in all_travels
    ]
    all_store_records = [
        _gen_random_store_record(food_choices, store_choices, station)
        for station in all_stations
    ]
    trainfoods.insert_many(ORIGINAL_TRAINFOODS)
    trainfoods.insert_many(all_train_food_records)
    stores.insert_many(ORIGINAL_STORES)
    stores.insert_many(all_store_records)

    for train_food in trainfoods.find():
        print(train_food)
    for store in stores.find():
        print(store)
